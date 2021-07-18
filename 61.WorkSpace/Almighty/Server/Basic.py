from common.database.repSqlAlchemy import *
#from DAO.KADM import *
import DAO.KADM
from common.ui.comUi import *

def merge(table):
    try:
        s.merge(table)
        print(table)
        s.commit()
    except Exception as e :
        print("Basic Except : " + e)
        return False

dic = {}

def getCode(grp):
    result = s.query(DAO.KADM.ComCdDtl).filter_by(com_cd_grp=grp).all()
    return result