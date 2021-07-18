from common.database.repSqlAlchemy import *
from DAO.KADM import *
from common.ui.comUi import *

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
    setCodebyTable(Job)
    return result

def getCodeLst(strComCdGrp,strComCdGrpNm):
    return s.query(ComCdLst).filter(ComCdLst.com_cd_grp.like("%"+strComCdGrp+"%")).filter(ComCdLst.com_cd_grp_nm.like("%"+strComCdGrpNm+"%")).all()

def getCodeDtl(strComCdGrp):
    print('getCodeDtl : ' + strComCdGrp)
    return s.query(ComCdDtl).filter_by(com_cd_grp=strComCdGrp).all()

def setCodebyTable(tbl):
    for col in tbl.__table__.columns:
        if col.kcom_cd_domain : setCode(col.kcom_cd_grp)
    return True

if __name__ == "__main__":
    print(getCodeDtl('JOB_CL'))
    pass