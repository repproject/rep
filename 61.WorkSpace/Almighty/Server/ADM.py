from Server.Basic import *
from DAO.KADM import *
import time

# def getJobSchd():
#     result = s.query(JobSchd,JobSchdExec).outerjoin(JRRrobSchdExec, and_(JobSchd.job_id == JobSchdExec.job_seq,JobSchd.job_seq == JobSchdExec.job_seq)).all()
#     return result

def getJobSchd(): #사용여부가 'Y'이고 삭제여부가 'N'인 Job의 사용여부는 'Y'인 유효한 Job 실행을 가져옴
    result = s.query(Job,JobSchd).join(JobSchd.job).filter(JobSchd.use_yn=='Y',JobSchd.del_yn=='N',Job.use_yn=='Y').all()
    return result

def getJobSchdExec(job_id):
    result = s.query(JobExec).filter(JobExec.job_id == job_id)
    return result

def getChgJobSchd():
    result = s.query(Job,JobSchd).join(JobSchd.job).filter(JobSchd.use_yn=='Y',JobSchd.del_yn=='N',Job.use_yn=='Y').all()
    return result

def getJobFuncAct(job_id):
    result = s.query(Job,JobAct,Act,ActFunc,Func).join(JobAct.job).join(JobAct.act).join(ActFunc.func)\
        .filter(Job.job_id == job_id,Act.act_id == ActFunc.act_id,Job.use_yn == 'Y',JobAct.use_yn == 'Y',Act.use_yn == 'Y',ActFunc.use_yn == 'Y',Func.use_yn == 'Y')\
        .order_by(JobAct.exec_seq,ActFunc.exec_seq).all()
    return result

def getImdiJobList(session):
    """
        scheduler에서 즉시 실행할 Job 목록을 가져옴.
        외부에서 변경 후 Commit된 정보를 가져오지 못해 별도 Session을 Create 하도록 변경.
        추후 이슈에 대해선 파악 필요 refresh가 대안이 될 수 있으나 가져온 instance에 대하여 refresh 하는 용도로 보임
        시간이 없으니 일단 new Session으로 해결
    :return:
    """
    rslt = session.query(JobSchd,Job).join(JobSchd.job).filter(JobSchd.imdi_exec_yn == 'Y',JobSchd.del_yn == 'N', JobSchd.use_yn == 'Y').all()
    return rslt

def updateImdiJobN(job_id,job_seq):
    """
    즉시실행 이후 다음 실행 하지 않기 위하여 즉시실행여부를 'N'으로 세팅
    update 최초 문장으로 update 작업시 select 이후 add commit 순서로 추후 작업 필요
    :param job_id:
    :param job_seq:
    :return:
    """

    rslt = s.query(JobSchd).filter(JobSchd.job_id == job_id, JobSchd.job_seq == int(job_seq)).all()
    rslt[0].imdi_exec_yn = 'N'
    rslt[0].chg_user_id = user.getUserId()
    rslt[0].chg_dtm = datetime.datetime.now()
    s.add(rslt[0])
    s.commit()
    return True

def terminateJob(job_id,exec_dtm,exec_stat_cd,message):
    """
        job종료
    :param job_id:
    :param exec_dtm:
    :param exec_stat_cd:
    :return:
    """

    rslt = s.query(JobExec).filter(JobExec.job_id == job_id, JobExec.exec_dtm == exec_dtm).first()
    rslt.exec_stat_cd = exec_stat_cd
    rslt.end_dtm = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rslt.chg_user_id = user.getUserId()
    rslt.chg_dtm = datetime.datetime.now()
    rslt.msg_cnts = message
    s.add(rslt)
    s.commit()
    return True

def terminateJobFunc(job_id,act_id,func_id,exec_dtm,exec_stat_cd,message):
    """
        job종료
    :param job_id:
    :param exec_dtm:
    :param exec_stat_cd:
    :return:
    """
    rslt = s.query(JobFuncExec).filter(JobFuncExec.job_id == job_id, JobFuncExec.act_id == act_id, JobFuncExec.func_id == func_id, JobFuncExec.exec_dtm == exec_dtm).first()
    rslt.exec_stat_cd = exec_stat_cd
    rslt.end_dtm = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rslt.chg_user_id = user.getUserId()
    rslt.chg_dtm = datetime.datetime.now()
    rslt.msg_cnts = message
    s.add(rslt)
    s.commit()
    return True

def getTblLst(dicParam):
    return s.query(Tbl).filter(or_(Tbl.tbl_nm.like("%" + dicParam['searchText'] + "%"),Tbl.tbl_desc.like("%" + dicParam['searchText'] + "%"))).all()

def getTblColLst(tbl_nm):
    return s.query(TblCol).filter(TblCol.tbl_nm == tbl_nm).filter(TblCol.col_nm.notin_(['reg_user_id','reg_dtm','chg_dtm','chg_user_id'])).order_by(TblCol.col_seq).all()

def getRcvUserList():
    return s.query(TlgrUser).filter(TlgrUser.rcv_tgt_yn == 'Y').order_by(TlgrUser.send_cl_cd).all()

def getSvcPasi(pasi_id,svc_id):
    return s.query(SvcPasi).filter(SvcPasi.pasi_id == pasi_id,SvcPasi.svc_id == svc_id).first()

def getJobFuncExecStrdFirst(strjob_id,stract_id,strfunc_id,strexec_dtm):
    """
    :param strjob_id: job_id
    :param stract_id:  act_id
    :param strfunc_id:  func_id
    :param strexec_dtm:  exec_dtm
        실행기준정보에서 값을 하나 가져와
    :return:
    """
    rslt = s.query(JobFuncExecStrd).filter(JobFuncExecStrd.job_id == strjob_id,JobFuncExecStrd.act_id == stract_id,JobFuncExecStrd.func_id == strfunc_id,JobFuncExecStrd.exec_dtm == strexec_dtm,JobFuncExecStrd.std_exec_stat_cd=='N').with_for_update().first()
    rslt.std_exec_stat_cd = 'R'
    s.add(rslt)
    s.commit()
    if isNull(rslt):
        return False
    else:
        return rslt


if __name__ == '__main__':
    #r = updateImdiJobN('GOIN001',1)
    #print(getLeglDongLv2LandValue())
    a = getImdiJobList()
    print(getImdiJobList())
    for b in a:
        print(b)
    pass


