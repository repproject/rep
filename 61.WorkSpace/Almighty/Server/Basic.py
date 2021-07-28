from common.database.repSqlAlchemy import *
import DAO.KADM
from common.ui.comUi import *
from Server.COM import *

def merge(table):
    s.merge(table)
    s.commit()
    return True

def mergeList(tableList):
    for table in tableList:
        print(table)
        s.merge(table)
    s.commit()

dic = {}

def deleteBasic(table):
    s.delete(table)
    s.commit()
    return True

def getCode(grp):
    result = s.query(DAO.KADM.ComCdDtl).filter_by(com_cd_grp=grp).all()
    setCodeByTable(result[0])
    return result