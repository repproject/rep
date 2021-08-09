from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *

def getSite(strSiteCode=None):
    if strSiteCode == None : result = s.query(Site).all()
    else : result = s.query(Site).filter_by(site_cd=strSiteCode).all()
    return result

def getMenu():
    setCodeByTable(Menu)
    result = s.query(Menu).order_by(Menu.prnt_seq).all()
    return result

def getMenuLv(lv):
    setCodeByTable(Menu)
    stmt = select(Menu).filter_by(menu_lv=lv).order_by(Menu.prnt_seq)
    result = s.execute(stmt).all()
    return result

def getJob():
    result = s.query(Job).all()
    setCodeByTable(Job)
    return result

def getCodeLst(strComCdGrp,strComCdGrpNm):
    return s.query(ComCdLst).filter(ComCdLst.com_cd_grp.like("%"+strComCdGrp+"%")).filter(ComCdLst.com_cd_grp_nm.like("%"+strComCdGrpNm+"%")).all()

def getCodeDtl(strComCdGrp):
    return s.query(ComCdDtl).filter_by(com_cd_grp=strComCdGrp).all()

def setCodeByTable(tbl):
    for col in tbl.__table__.columns:
        if col.kcom_cd_domain : common.ui.comUi.setCode(col.kcom_cd_grp)
    return True

def getSvc(strSiteCd):
    setCodeByTable(Svc)
    return s.query(Svc).filter_by(site_cd=strSiteCd).all()

def getSvcPasi(strSvcId):
    setCodeByTable(SvcPasi)
    return s.query(SvcPasi).filter_by(svc_id=strSvcId).all()

def getSvcInfo(strSvcId):
    setCodeByTable(Svc)
    setCodeByTable(Site)
    return s.query(Site,Svc).join(Svc.site).where(Svc.svc_id == strSvcId).all()

def getTblLst(strTblNm,strTblDesc,strColNm,strColDesc):
    setCodeByTable(Tbl)
    return s.query(Tbl).filter(Tbl.tbl_nm.like("%"+strTblNm+"%")).filter(Tbl.tbl_desc.like("%"+strTblDesc+"%")).all()

def getColLst(strTblNm):
    setCodeByTable(TblCol)
    return s.query(TblCol).filter_by(tbl_nm=strTblNm).order_by(TblCol.col_seq).all()

def getComCdLst(strComGrpCd):
    return s.query(ComCdLst).filter_by(com_cd_grp=strComGrpCd).first()

def getTbl(strTblNm):
    return s.query(Tbl).filter_by(tbl_nm=strTblNm).first()

def getTblCol(strTblNm):
    return s.query(TblCol).filter_by(tbl_nm=strTblNm).first()

def getTblColParentPK(strTblNm):
    return s.query(TblCol).filter_by(tbl_nm=strTblNm).filter_by(pk_yn='Y').all()

def getTableFinder(dicParam):
    return s.query(Tbl).filter(or_(Tbl.tbl_nm.like("%" + dicParam['searchText'] + "%"),(Tbl.tbl_desc.like("%" +  dicParam['searchText'] + "%")))).all()

def getPasiFinder(dicParam):
    setCodeByTable(SvcPasi)
    setCodeByTable(Svc)
    setCodeByTable(Site)
    setCodeByTable(ComCdDtl)
    return s.query(SvcPasi,Svc,Site,ComCdDtl)\
        .join(SvcPasi.svc)\
        .join(Svc.site)\
        .join(ComCdDtl,and_(Site.site_cd == ComCdDtl.com_cd,ComCdDtl.com_cd_grp == 'SITE'))\
        .where(or_(ComCdDtl.com_cd_nm.like("%" + dicParam['searchText'] + "%")
                    ,Site.site_cd.like("%" + dicParam['searchText'] + "%")\
                    ,Site.bas_url.like("%" + dicParam['searchText'] + "%")\
                    ,Svc.svc_id.like("%" + dicParam['searchText'] + "%") \
                    ,Svc.svc_nm.like("%" + dicParam['searchText'] + "%") \
                    ,Svc.bas_svc_url.like("%" + dicParam['searchText'] + "%") \
                    ,Svc.exmp_url.like("%" + dicParam['searchText'] + "%") \
                    ,SvcPasi.pasi_id.like("%" + dicParam['searchText'] + "%") \
                    ,SvcPasi.pasi_nm.like("%" + dicParam['searchText'] + "%") \
                    ,SvcPasi.parm_load_func_nm.like("%" + dicParam['searchText'] + "%")
                    )).all()

def getSvcPasiItem(strSvcId,strPasiId,InOutClCd):
    return s.query(SvcPasiItem).filter_by(svc_id=strSvcId).filter(SvcPasiItem.pasi_id.in_([strPasiId,'default'])).filter_by(in_out_cl_cd=InOutClCd).all()

if __name__ == "__main__":
    #rslt = getPasiFinder({'searchText':""})
    rslt = getMenuLv(1)
    print(rslt)
    pass