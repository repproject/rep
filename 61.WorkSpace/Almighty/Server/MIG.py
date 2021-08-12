from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *
from DAO.KMIG import *

def getBBLv1Regn():
    return s.query(BbLv1Regn).all()

def getBBLv2Regn():
    return s.query(BbLv2Regn).all()

def getBBLv3Regn():
    return s.query(BbLv3Regn).all()

if __name__ == "__main__":
    #rslt = getPasiFinder({'searchText':""})
    rslt = getBBLv2Regn()
    print(rslt)
    pass