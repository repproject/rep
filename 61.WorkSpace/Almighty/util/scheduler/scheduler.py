import sys
#print(sys.path)


from apscheduler.schedulers.background import BackgroundScheduler
from Server.ADM import *
from common.Batch.Basic import *
from common.Batch.doJob import *
import datetime
import Server.Basic

# Cron 방식 - Cron 표현식으로 Python code 를 수행
# Date 방식 - 특정 날짜에 Python code 를 수행
# Interval 방식 - 일정 주기로 Python code 를 수행

def doSchedule():    #JOB수행
    try:
        blog = Logger(LogName='scheduler', Level="DEBUG", name="scheduler").logger
        sched = BackgroundScheduler()
        sched.start()
        listJobExec = getJobSchd()


        for jobExec in listJobExec:

            #값 -> 변수로 세팅 숫자는 Integer로 변환
            jobId = jobExec[1].job_id               #Job Id
            jobSeq = jobExec[1].job_seq             #Job Seq
            execPerdCd = jobExec[1].exec_perd_cd    #실행주기 CYCL:cycle, DAY:요일, DD:일, HH:24, MM:월
            if isNotNull(jobExec[1].exec_mm): execMM = int(jobExec[1].exec_mm)             #실행월
            else: execMM = None
            if isNotNull(jobExec[1].exec_mm): execDD = int(jobExec[1].exec_dd)             #실행일
            else: execDD = None  # 실행월
            if isNotNull(jobExec[1].exec_hh): execHH = int(jobExec[1].exec_hh)             #실행시
            else: execHH = None
            if isNotNull(jobExec[1].exec_mi): execMI = int(jobExec[1].exec_mi)             #실행분
            else: execMI = None
            execDayCd = jobExec[1].exec_day_cd      #실행요일
            if isNotNull(jobExec[1].cycl_mi): cyclMi = int(jobExec[1].cycl_mi)             #반복분
            else: cyclMi = None
            imdiExecYn = jobExec[1].imdi_exec_yn    #즉시실행여부
            jobNm = jobExec[0].job_nm               #Job명

            if execPerdCd == 'DAY' or execPerdCd == 'DD' or execPerdCd == 'HH' or execPerdCd == 'MM': #주기작업(요일,월,일,시간)의 경우
                if execPerdCd == 'DD':
                    sched.add_job(do, 'cron', month='*',day='*',hour=execHH, minute=execMI, second=1,day_of_week = '*', id=jobId+str(jobSeq), args=[jobId,jobSeq])

        blog.info("REP Scheduler Start...")

        while True:
            #즉시실행된 Job 목록을 추출한다.
            blog.debug("Find Immediate Job...")
            ss = createSession()
            ImdiExecList = getImdiJobList(ss)
            blog.debug("ImdiExecList[" + str(len(ImdiExecList)) + "]:" + str(ImdiExecList))

            if len(ImdiExecList) > 0 :
                for imdiExec in ImdiExecList:
                    message = "REP Scheduler Immediate start..." + imdiExec[0].job_id + "/" + str(imdiExec[0].job_seq) + imdiExec[1].job_nm
                    blog.info(message)
                    blog.info("Immediate execute Job : " + str(imdiExec[0]))
                    imdiExec[0].imdi_exec_yn = 'N'
                    ss.add(imdiExec[0])
                    ss.commit()
                    sendTelegramMessage(message)
                    r = sched.add_job(do, id=jobId + str(jobSeq) + 'Y', #즉시실행여부를 분류하기 위하여 변경 ,
                                  args=[imdiExec[0].job_id, int(imdiExec[0].job_seq)])
                    blog.debug("add Job result : " + str(r))
                    blog.info("REP Scheduler Immediate Add Job Complete!!!")
                #try:
                    #sched.start()
                #except : error()
            ss.close()
            time.sleep(10) #즉시실행 Batch가 2번 실행되는 이슈가 존재. 10초로 변경해서 해결했으나 궁극적인 해결은 아님 Await기능을 찾아 해결 필요

    except : error()

if __name__ == '__main__':
    doSchedule()
