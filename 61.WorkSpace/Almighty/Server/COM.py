from common.database.repSqlAlchemy import *
from common.ui.comUi import *
from DAO.KADM import *
#import DAO.KADM

def getSite(strSiteCode=None):
    if strSiteCode == None : result = s.query(Site).all()
    else : result = s.query(Site).filter_by(site_cd=strSiteCode).all()
    return result

def getMenu():
    result = s.query(Menu).all()
    return result

def getMenuLv(lv):
    stmt = select(Menu).filter_by(menu_lv=lv).order_by(Menu.menu_id)
    result = s.execute(stmt).all()
    return result

def getJob():
    result = s.query(Job).all()
    #Job에 선언된 공통코드를 세팅한다.
    setCodeByTable(Job)
    return result

def getCodeLst(strComCdGrp,strComCdGrpNm):
    return s.query(ComCdLst).filter(ComCdLst.com_cd_grp.like("%"+strComCdGrp+"%")).filter(ComCdLst.com_cd_grp_nm.like("%"+strComCdGrpNm+"%")).all()

def getCodeDtl(strComCdGrp):
    return s.query(ComCdDtl).filter_by(com_cd_grp=strComCdGrp).all()

def setCodeByTable(tbl):
    for col in tbl.__table__.columns:
        if col.kcom_cd_domain : setCode(col.kcom_cd_grp)
    return True

if __name__ == "__main__":
    #print(getSites())
    pass