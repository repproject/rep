from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *
from DAO.KMIG import *
from DAO.KRED import *
from common.Batch.Basic import *
from common.common.UserException import *
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta
import dateutil.relativedelta
import copy
import Server.ADM


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

def getLegalDongLv2(flag,job_id,act_id,func_id,exec_dtm,process_number):
    if flag == 1:
        # 3개월치 가져오도록 세팅
        date_only = date.today()
        t = date_only - dateutil.relativedelta.relativedelta(months=2)
        ym = str(t.year) + str(t.month).zfill(2)  # + str(t.day).zfill(2)
        todayym = str(date_only.year) + str(date_only.month).zfill(2)

        # rslt = s.query(LeglDong, StdYymm).filter(LeglDong.lv_cd == '2', StdYymm.std_yymm <= todayym,StdYymm.std_yymm >= ym)\
        rslt = s.query(StdYymm).filter(StdYymm.std_yymm <= todayym,StdYymm.std_yymm >= ym) \
            .order_by(StdYymm.std_yymm).all()  # 실거래가 시행이 06년 #'200601' #,LeglDong.legl_dong_cd=='4145000000'

        listFuncExecParm = []
        for r in rslt:
            tbJobFuncExecStrd = JobFuncExecStrd(job_id=job_id,act_id=act_id,func_id=func_id,exec_dtm=exec_dtm,std_parm1=r.std_yymm)
            mergeNC(tbJobFuncExecStrd)
        commit()

    elif flag == 2:
        rslt = Server.ADM.getJobFuncExecStrdFirst(job_id,act_id,func_id,exec_dtm,process_number)
        if rslt == False:
            raise CrawlingEndException
        rr = s.query(LeglDong, StdYymm).filter(LeglDong.lv_cd == '2',StdYymm.std_yymm == rslt.std_parm1).all()  # 실거래가 시행이 06년 #'200601' #,LeglDong.legl_dong_cd=='4145000000'
        rslt2 = copy.deepcopy(rr)
        for t in rslt2:
            t[0].legl_dong_cd = t[0].legl_dong_cd[:5]
        return (rslt2,rslt)

def getLegalDongLv3():
    rslt = s.query(LeglDong).filter(LeglDong.lv_cd == '3').order_by(LeglDong.legl_dong_cd).all()
    return rslt

def getLeglDongLv2LandValue(): #공시지가 도로명 주소 get
    rslt = s.query(LeglDong,ComCdDtl).filter(LeglDong.lv_cd == '2',ComCdDtl.com_cd_grp=="HG_CS").order_by(LeglDong.legl_dong_cd,ComCdDtl.prnt_seq).all() #,LeglDong.legl_dong_cd == '4145000000'
    rslt2 = copy.deepcopy(rslt)
    for t in rslt2:
        t[0].legl_dong_cd = t[0].legl_dong_cd[:5]
    return rslt2

def getNvCmpx():
    return s.query(NvCmpx).all()

def getOlvRoadNm():
    return s.query(OlvRoadNm).filter(OlvRoadNm.job_id == 'LVIN001',OlvRoadNm.exec_dtm == '20220419131229').order_by(OlvRoadNm.gov_legl_dong_cd).all()

def getNvCmpxTyp(flag,job_id,act_id,func_id,exec_dtm,process_number):
    """
    네이버 매물 갱신 기준정보를
    :param flag:
    :param job_id:
    :param act_id:
    :param func_id:
    :param exec_dtm:
    :return:
    """
    if flag == 1:
        rslt = s.query(LeglDong).order_by(LeglDong.legl_dong_cd).all()
        listFuncExecParm = []
        for r in rslt:
            tbJobFuncExecStrd = JobFuncExecStrd(job_id=job_id,act_id=act_id,func_id=func_id,exec_dtm=exec_dtm,std_parm1=r.legl_dong_cd)
            mergeNC(tbJobFuncExecStrd)
        commit()

    elif flag == 2:
        while True: #가져온 기준정보가 재수행이 필요 없다면
            rslt = getJobFuncExecStrdFirst(job_id,act_id,func_id,exec_dtm,process_number)
            if rslt == False:              #실행기준정보가 없는 경우
                raise CrawlingEndException #Batch 종료를 위한 Exception
            rr = s.query(NvCmpx,NvCmpxTyp).join(NvCmpxTyp.nvcmpx).filter(NvCmpx.legl_dong_cd == rslt.std_parm1).all()
            if len(rr) > 0: #Crawling을 수행할 기준정보가 있으면 정상적으로 Return
                rslt2 = copy.deepcopy(rr)
                rslt.req_tgt_cnt = len(rr)
                return (rslt2,rslt)
            else: #여기코딩
                rslt.std_exec_stat_cd = 'T'
                rslt.req_tgt_cnt = 0
                s.add(rslt)
                s.commit()

        #return s.query(NvCmpxTyp).order_by(NvCmpxTyp.nv_cmpx_id,NvCmpxTyp.nv_cmpx_typ_seq).filter(NvCmpxTyp.job_id == 'NVDC006',NvCmpxTyp.exec_dtm == '20220418182200', NvCmpxTyp.nv_cmpx_id >= '104535').order_by(NvCmpxTyp.nv_cmpx_id).all()

if __name__ == "__main__":
    print(getNvCmpxTyp(2,'a','b','c','2'))
    #print(len(getNvCmpxTyp()))
    #date_only = date.today()
    #t = date_only - dateutil.relativedelta.relativedelta(months=3)
    #ym = str(t.year) + str(t.month).zfill(2)# + str(t.day).zfill(2)
    #print(ym)
    #t = datetime.now()
    #t.
    #print(t)
    #str = datetime.now().strftime('%Y%m')
    #print(str)
    #rslt = getLegalDongLv2()
    #print(rslt)
    pass