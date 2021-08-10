from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *
from DAO.KMIG import *

def getBBLv1Regn():
    return s.query(BBLv1Regn).all()