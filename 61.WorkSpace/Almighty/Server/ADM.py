from Server.Basic import *
from DAO.KADM import *

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

def getTblLst(dicParam):
    return s.query(Tbl).filter(or_(Tbl.tbl_nm.like("%" + dicParam['searchText'] + "%"),Tbl.tbl_desc.like("%" + dicParam['searchText'] + "%"))).all()

def getTblColLst(tbl_nm):
    return s.query(TblCol).filter(TblCol.tbl_nm == tbl_nm).filter(TblCol.col_nm.notin_(['reg_user_id','reg_dtm','chg_dtm','chg_user_id'])).order_by(TblCol.col_seq).all()

def getRcvUserList():
    return s.query(TlgrUser).filter(TlgrUser.rcv_tgt_yn == 'Y').order_by(TlgrUser.send_cl_cd).all()

#SELECT TLGR_USER_ID FROM kadm_tlgr_user WHERE RCV_TGT_YN = 'Y' ORDER BY SEND_CL_CD DESC

if __name__ == '__main__':
    r = getJobSchdExec()
    print(r)
    pass


