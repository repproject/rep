from DAO.KTable import *
from sqlalchemy import select
from common.database.testReflect import *
from common.database.repSqlAlchemy import *
import datetime

class Menu(Base,KTable):
    __tablename__ = 'KADM_MENU'

    menu_id = Column(String(10), primary_key=True)
    menu_lv = Column(Integer)
    prnt_seq = Column(Integer)
    menu_nm = Column(String(200))
    up_menu_id = Column(String(10))
    fst_reg_ymd = Column(String(8))
    pgm_id = Column(String(10))

    def __init__(self, menu_id, menu_lv, prnt_seq, menu_nm, up_menu_id, pgm_id):
        KTable.__init__(self)
        self.menu_id = menu_id
        self.menu_lv = menu_lv
        self.prnt_seq = prnt_seq
        self.menu_nm = menu_nm
        self.up_menu_id = up_menu_id
        current_datetime = datetime.datetime.now()
        self.fst_reg_ymd = datetime.datetime.strftime(current_datetime,"%Y%m%d")
        self.pgm_id = pgm_id

    def __repr__(self):
         return "<Menu('%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (self.menu_id, self.menu_lv, self.prnt_seq, self.menu_nm, self.up_menu_id, self.fst_reg_ymd, self.pgm_id) + KTable.__repr__(self)

if __name__ == "__main__" :
    menu = Menu('test',None,None,None,None,None)
    pass