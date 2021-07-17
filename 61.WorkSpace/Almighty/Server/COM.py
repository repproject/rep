from common.database.repSqlAlchemy import *
from DAO.KADM import *

def getMenu():
    result = s.query(Menu).all()
    return result

def getMenuLv(lv):
    stmt = select(Menu).filter_by(menu_lv=lv).order_by(Menu.menu_id)
    result = s.execute(stmt).all()
    return result

def getJob():
    result = s.query(Job).all()
    return result

if __name__ == "__main__":
    pass