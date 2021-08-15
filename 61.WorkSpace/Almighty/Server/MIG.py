from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *
from DAO.KMIG import *
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta

def getBBLv1Regn():
    return s.query(BbLv1Regn).all()

def getBBLv2Regn():
    return s.query(BbLv2Regn).all()

def getBBLv3Regn():
    return s.query(BbLv3Regn).all()

def getBBCmpxCrawl():
    now = datetime.now()
    strd = now - timedelta(days = 2)

    return s.query(BbCmpx).filter(~(s.query(BbCmpxTyp).filter(BbCmpx.bb_cmpx_id == BbCmpxTyp.bb_cmpx_id,BbCmpxTyp.chg_dtm > strd).exists())).all()

def getBBCmpxTyp(): return s.query(BbCmpxTyp).all()

# def test():
#     #BbCmpx_alias = aliased(BbCmpx)
#
#     now = datetime.now()
#     strd = now - timedelta(days = 2)
#
#     return s.query(BbCmpx) \
#         .filter(session.query(BbCmpxTyp) \
#                 .filter(BbCmpx.bb_cmpx_id != BbCmpxTyp.bb_cmpx_id) \
#                 .filter(BbCmpxTyp.chg_dtm < strd) \
#                 .exists())

if __name__ == "__main__":
    #rslt = getPasiFinder({'searchText':""})
    #rslt = getBBCmpxCrawl()
    rslt = getBBCmpxCrawl()
    print(rslt)
    pass