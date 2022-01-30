from Server.Basic import *
from DAO.KADM import *

def getJobSchd():
    result = s.query(JobSchd,JobSchdExec).outerjoin(JobSchdExec, and_(JobSchd.job_id == JobSchdExec.job_seq,JobSchd.job_seq == JobSchdExec.job_seq)).all()
    return result

if __name__ == '__main__':
    pass


