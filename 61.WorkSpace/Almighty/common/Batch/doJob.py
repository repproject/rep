# #import B2B_MIG_BTC
# import B2B_MIG_Stock
# import B2B_TLGR
# import B2B_JOB
# import pymysql
# import B2B_COM
# import B2B_SIML
# import B2B_COM_Data
# import sys
from multiprocessing import Pool

import DAO.KADM
import Server.ADM
from batch.Crawling.CrawlingmNV import *
import common.Batch.Crawling
from common.Batch.Basic import *
import datetime

userid = '1000000001'
def do(job_id,job_seq):
    """
    Job을 실행하는 함수이다.
    현재 크롤링 타입만 수행 가능하도록 구현되어 있다.
    다른구분값을 추가하면 됨.
    :param job_id:
    :return:
    """
    blog.info("Do Job Start : [" + job_id + "][" + str(job_seq) + "]")
    listFunc = Server.ADM.getJobFuncAct(job_id)

    jobSchdExec = Server.COM.getJobSchdExecFirst(job_id, int(job_seq))

    #JOB 실행정보 기록 'R(실행중)'
    je = writeJobExec(job_id,job_seq,'R')
    exec_dtm = je.exec_dtm

    try:
        if len(listFunc) == 0:  #Function이 등록되지 않은 경우
            logMessage = "Function is not registerd in job : " + job_id
            blog.error(logMessage)
            sendTelegramMessage(logMessage)
            return False

        blog.info("Function of Job List is...")
        blog.info(listFunc)

        #core 수 세팅
        if je.exec_parm6 != None and je.exec_parm6 != '':
            num_cores = int(je.exec_parm6)
        else:
            num_cores = 0

        blog.info("num_cores : " + str(num_cores))

        for Func in listFunc:
            function = copy.deepcopy(Func[4])
            act = copy.deepcopy(Func[2])
            job = copy.deepcopy(Func[0])

            #Function 실행 기록
            writeFuncExec(job_id,job_seq,act.act_id,function.func_id,'R')

            #기준Data사전세팅
            tbSvcPasi = Server.ADM.getSvcPasi(function.src_func_nm,function.ref1)
            execStrd = tbSvcPasi.parm_load_func_nm
            execStrd = execStrd[:-1] + "1,'" + job.job_id +"','"+ act.act_id + "','" + function.func_id + "','" + exec_dtm + "',0)"  # Crawling Object에서 수행하는 경우 2번으로 호출
            print(execStrd)
            eval(execStrd)

            try:
                if function.func_cl_cd == 'CRWL':
                    if num_cores > 1:
                        pool = Pool(num_cores)
                        listParam = []
                        for i in range(0,num_cores):
                            ll = []
                            ll.append(job)
                            ll.append(act)
                            ll.append(function)
                            ll.append(je)
                            ll.append(i)
                            listParam.append(ll)
                        pool.map(runCrawling, listParam)
                        pool.close()
                        pool.join()
                    else:
                        ll = []
                        ll.append(job)
                        ll.append(act)
                        ll.append(function)
                        ll.append(je)
                        ll.append(1)
                        runCrawling(ll)
                elif function.func_cl_cd == 'CRWC':
                    if num_cores > 1:
                        return False
                    else:
                        batchContext = simpleBatchContext(
                            "[" + job.job_id + "][" + job.job_nm + "][" + function.func_id + "][" + function.func_nm + "][" + function.func_cl_cd + "][" + exec_dtm + "]")
                        batchContext.setLogFileName(
                            "[" + job.job_id + "][" + job.job_nm + "][" + function.func_id + "][" + function.func_nm + "][" + function.func_cl_cd + "][" + je.exec_dtm + "]")
                        execStr = function.ref2 + "(function.src_func_nm, function.ref1, batchContext, je, job, act, function)"
                        CrawlObject = eval(execStr)
                        CrawlObject.run()
            except Exception as e:
                #Function 오류 종료 업데이트
                writeFuncExec(job_id, job_seq, act.act_id,function.func_id, 'E', exec_dtm, str(traceback.format_exc()))
                raise

        message = 'JOB 정상종료 : [' + job.job_id + "][" + job.job_nm + "]"
        sendTelegramMessage(message)
        blog.info(message)
        writeJobExec(job_id, job_seq, 'T', exec_dtm, message)
        writeFuncExec(job_id, job_seq, act.act_id, function.func_id, 'T', exec_dtm, str(traceback.format_exc()))
    except Exception as e:
        message = 'JOB 오류종료 : [' + job.job_id + "][" + job.job_nm + "][" + str(traceback.format_exc()) + "]"
        blog.error(message)
        sendTelegramMessage(message)
        writeJobExec(job_id,job_seq,'E',exec_dtm,str(traceback.format_exc()))
        error()

def runCrawling(list):
    job = copy.deepcopy(list[0])
    act = copy.deepcopy(list[1])
    function = copy.deepcopy(list[2])
    je = copy.deepcopy(list[3])
    process_number = copy.deepcopy(list[4])
    batchContext = simpleBatchContext("[" + job.job_id + "][" + job.job_nm + "][" + function.func_id + "][" + function.func_nm + "][" + function.func_cl_cd + "][" + je.exec_dtm + "][" + str(process_number) + "]")
    batchContext.setLogFileName("[" + job.job_id + "][" + job.job_nm + "][" + function.func_id + "][" + function.func_nm + "][" + function.func_cl_cd + "][" + je.exec_dtm + "]")
    CrawlObject = common.Batch.Crawling.Crawling(function.src_func_nm, function.ref1, batchContext, je, job, act, function,process_number)
    CrawlObject.run()

def writeJobExec(job_id,job_seq,exec_stat_cd,exec_dtm=None,message=''):
    if len(message)>2000:
        message = message[:2000]

    jobSchdExec = Server.COM.getJobSchdExecFirst(job_id, int(job_seq))
    if isNull(jobSchdExec):
        jobSchdExec = DAO.KADM.JobSchdExec(job_id = job_id,job_seq = job_seq)

    # JOB 실행정보 기록
    nowStrTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if exec_stat_cd == 'R': #JOB이 신규로 실행중
        je = JobExec(job_id=job_id
                     , exec_dtm=nowStrTime
                     , exec_stat_cd=exec_stat_cd
                     , sta_dtm=nowStrTime
                     , end_dtm='99991231235959'
                     , exec_parm1=jobSchdExec.exec_parm1
                     , exec_parm2=jobSchdExec.exec_parm2
                     , exec_parm3=jobSchdExec.exec_parm3
                     , exec_parm4=jobSchdExec.exec_parm4
                     , exec_parm5=jobSchdExec.exec_parm5
                     , exec_parm6=jobSchdExec.exec_parm6
                     , exec_parm7=jobSchdExec.exec_parm7
                     , exec_parm8=jobSchdExec.exec_parm8
                     , exec_parm9=jobSchdExec.exec_parm9
                     , exec_parm10=jobSchdExec.exec_parm10)
        merge(je)
        return je
    elif exec_stat_cd == 'E' or exec_stat_cd == 'T':
        if isNull(exec_dtm):
            message = message + "Job종료시 실행일시가 정상적으로 입력되지 않았습니다. [JOB_ID : " + job_id + "][EXEC_DTM : " + exec_dtm + "]"
            blog.error(message)
            sendTelegramMessage(message)
            raise ValueError
        Server.ADM.terminateJob(job_id,exec_dtm,exec_stat_cd,message)
        return True
    else:
        message = "Job종료시 실행상태가 정상적으로 입력되지 않았습니다. [JOB_ID : " + job_id + "][EXEC_DTM : " + exec_dtm + "]"
        blog.error(message)
        sendTelegramMessage(message)
        return False
    return False

def writeFuncExec(job_id,job_seq,act_id,func_id,exec_stat_cd,exec_dtm=None,message=''):
    #입력된 스케쥴 정보를 가져온다. 없으면 신규로 생성한다.
    jobSchdExec = Server.COM.getJobSchdExecFirst(job_id, int(job_seq))
    if isNull(jobSchdExec):
        return False

    # JOB 실행정보 기록
    nowStrTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if exec_stat_cd == 'R': #Func가 신규로 실행중
        je = JobFuncExec(job_id = job_id
                     , act_id = act_id
                     , func_id = func_id
                     , exec_dtm = nowStrTime
                     , exec_stat_cd=exec_stat_cd
                     , sta_dtm=nowStrTime
                     , end_dtm='99991231235959'
                     , exec_parm1=jobSchdExec.exec_parm1
                     , exec_parm2=jobSchdExec.exec_parm2
                     , exec_parm3=jobSchdExec.exec_parm3
                     , exec_parm4=jobSchdExec.exec_parm4
                     , exec_parm5=jobSchdExec.exec_parm5
                     , exec_parm6=jobSchdExec.exec_parm6
                     , exec_parm7=jobSchdExec.exec_parm7
                     , exec_parm8=jobSchdExec.exec_parm8
                     , exec_parm9=jobSchdExec.exec_parm9
                     , exec_parm10=jobSchdExec.exec_parm10)
        merge(je)
        return je
    elif exec_stat_cd == 'E' or exec_stat_cd == 'T':
        if isNull(exec_dtm):
            message = message + "Func 종료시 실행일시가 정상적으로 입력되지 않았습니다. [JOB_ID : " + job_id + "][ACT_ID : " + act_id + "][FUNC_ID : " + func_id + "[EXEC_DTM : " + exec_dtm + "]"
            blog.error(message)
            sendTelegramMessage(message)
            raise ValueError
        Server.ADM.terminateJobFunc(job_id,act_id,func_id,exec_dtm,exec_stat_cd,message)
        return True
    else:
        message = "Func종료시 실행상태가 정상적으로 입력되지 않았습니다. [JOB_ID : " + job_id + "][ACT_ID : " + act_id + "][FUNC_ID : " + func_id + "[EXEC_DTM : " + exec_dtm + "]"
        blog.error(message)
        sendTelegramMessage(message)
        return False
    return False

#첫 수행 문장
if __name__ == '__main__':
    #print(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    #blog.info("START JOB doJOB main...")
    #blog.info("parameter : " + *args)
    #jobSchdExec = Server.COM.getJobSchdExecFirst('NVDC002', 1)
    #print(jobSchdExec)
    do('GOIN001',1)
    #do('NVDC005', 1)
    #main()