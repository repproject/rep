from Server.Basic import *
from DAO.KADM import *

# def getJobSchd():
#     result = s.query(JobSchd,JobSchdExec).outerjoin(JobSchdExec, and_(JobSchd.job_id == JobSchdExec.job_seq,JobSchd.job_seq == JobSchdExec.job_seq)).all()
#     return result

def getJobSchd(): #사용여부가 'Y'이고 삭제여부가 'N'인 Job의 사용여부는 'Y'인 유효한 Job 실행을 가져옴
    result = s.query(Job,JobSchd).join(JobSchd.job).filter(JobSchd.use_yn=='Y',JobSchd.del_yn=='N',Job.use_yn=='Y').all()
    return result

if __name__ == '__main__':
    pass


