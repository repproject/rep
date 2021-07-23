from common.database.repSqlAlchemy import *
#from DAO.KADM import *
import DAO.KADM
from common.ui.comUi import *
from Server.COM import *

def merge(table):
    try:
        s.merge(table)
        s.commit()
    except Exception as e :
        print("Basic Except : " + e)
        return False

def mergeList(tableList):
    try:
        for table in tableList:
            s.merge(table)
        s.commit()
    except Exception as e :
        print(e)

dic = {}

def getCode(grp):
    result = s.query(DAO.KADM.ComCdDtl).filter_by(com_cd_grp=grp).all()
    setCodeByTable(result[0])
    return result