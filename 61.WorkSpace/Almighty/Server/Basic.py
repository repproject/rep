from common.database.repSqlAlchemy import *
import DAO.KADM
from common.ui.comUi import *
from Server.COM import *
import pymysql
import common.common.Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy import update

def merge(table):
    mergeNC(table)
    s.commit()
    return True

def mergeNC(table):
    """
        NC = Not Commit
        성능을 위하여 Commit하지 않은 함수를 의미
        table.updateChg를 통하여 수정일시, 수정자ID, 등록자ID 등의 ROW 기본컬럼을 update한다.
    :param table:
    :return:
    """
    table.updateChg()
    s.merge(table)
    return True

def insert(table):
    s.add(table)
    s.commit()
    return True

def insertNC(table):
    s.add(table)
    return True

def mergeList(tableList):
    mergeListNC(tableList)
    s.commit()

def mergeListNC(tableList):
    for table in tableList:
        mergeNC(table)

def insertList(tableList):
    for table in tableList:
        s.add(table)
    s.commit()
    return True

def insertListNC(tableList):
    for table in tableList:
        s.add(table)
    return True

dic = {}

def deleteBasic(table):
    s.delete(table)
    s.commit()
    return True

def getCode(grp):
    result = s.query(DAO.KADM.ComCdDtl).filter_by(com_cd_grp=grp).all()
    setCodeByTable(result[0])
    return result

def commit():
    s.commit()

def rollback():
    s.rollback()

if __name__ == "__main__":
    rslt = Server.COM.getJob()
    dic = common.common.Table.getDicFromListTable(rslt[0])
    del dic[0]['reg_user_id']
    del dic[0]['reg_dtm']
    dic[0]['job_nm'] = '주식가격 삽입 테스트'

