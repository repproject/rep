from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *
from DAO.KMIG import *
from DAO.KRED import *
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta
import copy


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
    t = datetime.now()
    ymd = str(t.year) + str(t.month).zfill(2) + str(t.day).zfill(2)
    rslt = s.query(LeglDong, StdYymm).filter(LeglDong.lv_cd == '2', StdYymm.std_yymm <= ymd,StdYymm.std_yymm >= '201011').order_by(
        StdYymm.std_yymm).all()  # 실거래가 시행이 06년 #'200601' #,LeglDong.legl_dong_cd=='4145000000'
    rslt2 = copy.deepcopy(rslt)
    for t in rslt2:
        t[0].legl_dong_cd = t[0].legl_dong_cd[:5]
    return rslt2

def getLegalDongLv3():
    rslt = s.query(LeglDong).filter(LeglDong.lv_cd == '3').order_by(LeglDong.legl_dong_cd).all()
    return rslt

if __name__ == "__main__":
    str = datetime.now().strftime('%Y%m')
    print(str)
    #rslt = getLegalDongLv2()
    #print(rslt)
    pass