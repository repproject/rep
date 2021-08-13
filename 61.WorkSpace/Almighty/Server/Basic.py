from common.database.repSqlAlchemy import *
import DAO.KADM
from common.ui.comUi import *
from Server.COM import *
import pymysql
import common.common.Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import PendingRollbackError

def merge(table):
    delattr(table, 'reg_user_id')
    delattr(table, 'reg_dtm')
    table.updateChg()
    s.merge(table)
    s.commit()
    return True

def insert(table):
    s.add(table)
    s.commit()
    return True

def updateSomeDic(tbl,dicTable):
    s.query(tbl).update(dicTable)
    s.commit()

def mergeList(tableList):
    for table in tableList:
        delattr(table, 'reg_user_id')
        delattr(table, 'reg_dtm')
        table.updateChg()
        s.merge(table)
    s.commit()

def insertList(tableList):
    for table in tableList:
        s.add(table)
    s.commit()
    return True

# def inup(table):
#     s.add(table)
#     s.commit()
#
# def inUpList(tableList):
#     for table in tableList:
#         try:
#             s.add(table)
#         except pymysql.IntegrityError as e:
#             table.updateChg()
#     s.commit()

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
    updateSomeDic(rslt[0].__table__,dic[0])
