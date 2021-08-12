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
    if tbl.__class__ == [].__class__ :
        for t in tbl:
            for col in t.__table__.columns:
                if col.kcom_cd_domain : common.ui.comUi.setCode(col.kcom_cd_grp)
        return True
    else:
        for col in tbl.__table__.columns:
            if col.kcom_cd_domain: common.ui.comUi.setCode(col.kcom_cd_grp)
        return True

def getSvc(strSiteCd):
    setCodeByTable(Svc)
    return s.query(Svc).filter_by(site_cd=strSiteCd).all()

def getSvcPasi(strSvcId):
    setCodeByTable(SvcPasi)
    return s.query(SvcPasi).filter_by(svc_id=strSvcId).all()

def getSvcInfo(strSvcId):
    setCodeByTable([Svc,Site])
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
    setCodeByTable([SvcPasi,Svc,Site,ComCdDtl])
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
    setCodeByTable(SvcPasiItem)
    return s.query(SvcPasiItem).filter_by(svc_id=strSvcId).filter(SvcPasiItem.pasi_id.in_([strPasiId,'default'])).filter_by(in_out_cl_cd=InOutClCd).all()

def getiItemParm(strSvcId,strPasiId,InOutClCd):
    setCodeByTable([SvcPasiItem,TblCol,Tbl])
    return s.query(SvcPasiItem,TblCol,Tbl).filter_by(svc_id=strSvcId).filter(SvcPasiItem.pasi_id.in_([strPasiId,'default'])).filter_by(in_out_cl_cd=InOutClCd).all()

def getiItemParm2(strSvcId,strPasiId,InOutClCd):
    setCodeByTable([SvcPasiItem,TblCol,Tbl])
    return s.query(SvcPasiItem,TblCol,Tbl).join(SvcPasiItem.tblcol).join(TblCol.tbl).where(and_(SvcPasiItem.pasi_id.in_([strPasiId,'default']),SvcPasiItem.svc_id == strSvcId,SvcPasiItem.in_out_cl_cd == InOutClCd)).all()

def getPasi(strPasiId,strSvcId):
    setCodeByTable([SvcPasi,Svc,Site])
    return s.query(SvcPasi,Svc,Site).join(SvcPasi.svc).join(Svc.site).where(and_(SvcPasi.svc_id == strSvcId,SvcPasi.pasi_id == strPasiId)).first()

def getCdExec(strCdExec):
    setCodeByTable(CdExec)
    return s.query(CdExec).filter(or_(CdExec.cd_exec_id.like("%" + strCdExec + "%"),(CdExec.cd_exec_nm.like("%" + strCdExec + "%")))).all()

def getPasiCdExec(strSvcId,strPasiId):
    setCodeByTable(PasiCdExec)
    return s.query(PasiCdExec).filter_by(svc_id=strSvcId).filter_by(pasi_id=strPasiId).all()

def getCrawlCdExec(strSvcId,strPasiId,upSec):
    setCodeByTable([PasiCdExec,CdExec])
    return s.query(PasiCdExec,CdExec).join(PasiCdExec.cdexec).where(and_(PasiCdExec.svc_id == strSvcId,PasiCdExec.pasi_id == strPasiId, PasiCdExec.up_seq == upSec)).all()

def getTablePasiItem(strSvcId,strPasiId,strItemNm,strInOutClCd):
    setCodeByTable(SvcPasiItemCol)
    return s.query(SvcPasiItemCol).filter_by(svc_id=strSvcId).filter_by(pasi_id=strPasiId).filter_by(item_nm=strItemNm).filter_by(in_out_cl_cd=strInOutClCd).all()

if __name__ == "__main__":
    #rslt = getPasiFinder({'searchText':""})
    rslt = getMenuLv(1)
    print(rslt)
    pass