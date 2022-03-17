from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *
from DAO.KMIG import *
from DAO.KRED import *
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

def getBBCmpxTypCrawl():
    now = datetime.now()
    strd = now - timedelta(days = 2)
    return s.query(BbCmpxTyp).filter(~(s.query(BbCmpxTypMonPrc).filter(BbCmpxTyp.bb_cmpx_id == BbCmpxTypMonPrc.bb_cmpx_id,
                                                                       BbCmpxTyp.bb_cmpx_typ_seq == BbCmpxTypMonPrc.bb_cmpx_typ_seq,
                                                                       BbCmpxTypMonPrc.chg_dtm > strd).exists())).all()

def getLegalDongLv2():
    rslt = s.query(LeglDong, StdYymm).filter(LeglDong.lv_cd == '2', LeglDong.legl_dong_cd == '4145000000',
                                      StdYymm.std_yymm < '2023').all()
    for t in rslt:
        t[0].legl_dong_cd = t[0].legl_dong_cd[:5]
    return rslt

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
    rslt = getLegalDongLv2()
    print(rslt)
    pass