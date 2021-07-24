from DAO.KTable import *
from DAO.KTable import KTable
from sqlalchemy import select
from common.database.testReflect import *
from common.database.repSqlAlchemy import *
import datetime

Base = declarative_base()

class Job(Base,KTable):
    __tablename__ = 'KADM_JOB'

    job_id = KColumn(String(20), primary_key=True)
    job_nm = KColumn(String(100))
    job_desc = KColumn(String(1000))
    job_cl_cd = KColumn(String(20),kcom_cd_domain = True,kcom_cd_grp='JOB_CL')
    use_yn = KColumn(String(1))
    ref1 = KColumn(String(100))
    ref2 = KColumn(String(100))
    ref3 = KColumn(String(100))
    ref4 = KColumn(String(100))
    ref5 = KColumn(String(100))

    def __init__(self, job_id, job_nm, job_desc, job_cl_cd, use_yn, ref1, ref2, ref3, ref4, ref5):
        KTable.__init__(self)
        self.job_id = job_id
        self.job_nm = job_nm
        self.job_desc = job_desc
        self.job_cl_cd = job_cl_cd
        self.use_yn = use_yn
        self.ref1 = ref1
        self.ref2 = ref2
        self.ref3 = ref3
        self.ref4 = ref4
        self.ref5 = ref5

    def __repr__(self):
         return "<Job('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (self.job_id, self.job_nm, self.job_desc, self.job_cl_cd, self.use_yn, self.ref1, self.ref2, self.ref3, self.ref4, self.ref5) + KTable.__repr__(self)

class Menu(Base,KTable):
    __tablename__ = 'KADM_MENU'

    menu_id = KColumn(String(10), primary_key=True)
    menu_lv = KColumn(Integer)
    prnt_seq = KColumn(Integer)
    menu_nm = KColumn(String(200))
    up_menu_id = KColumn(String(10))
    fst_reg_ymd = KColumn(String(8))
    pgm_id = KColumn(String(10))

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

class ComCdLst(Base,KTable):
    __tablename__ = 'KADM_COM_CD_LST'

    com_cd_grp = KColumn(String(20), primary_key = True, nullable = False)
    com_cd_grp_nm = KColumn(String(100), nullable = False)
    com_cd_grp_desc = KColumn(String(200), nullable = True)
    up_com_cd_grp = KColumn(String(20), nullable = True)
    del_yn = KColumn(String(1), nullable = False)
    ref1 = KColumn(String(100), nullable = True)
    ref2 = KColumn(String(100), nullable = True)
    ref3 = KColumn(String(100), nullable = True)
    ref4 = KColumn(String(100), nullable = True)
    ref5 = KColumn(String(100), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.com_cd_grp = kwargs.pop("com_cd_grp")
        self.com_cd_grp_nm = kwargs.pop("com_cd_grp_nm")
        self.com_cd_grp_desc = kwargs.pop("com_cd_grp_desc","")
        self.up_com_cd_grp = kwargs.pop("up_com_cd_grp","")
        self.del_yn = kwargs.pop("del_yn", 'N')
        self.ref1 = kwargs.pop("ref1","")
        self.ref2 = kwargs.pop("ref2","")
        self.ref3 = kwargs.pop("ref3","")
        self.ref4 = kwargs.pop("ref4","")
        self.ref5 = kwargs.pop("ref5","")

    def __repr__(self):
        return "<ComCdLst('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.com_cd_grp), str(self.com_cd_grp_nm), str(self.com_cd_grp_desc), str(self.up_com_cd_grp), str(self.del_yn), str(self.ref1), str(self.ref2), str(self.ref3), str(self.ref4), str(self.ref5) + KTable.__repr__(self))

class ComCdDtl(Base,KTable):
    __tablename__ = 'KADM_COM_CD_DTL'

    com_cd_grp = KColumn(String(20), primary_key = True, nullable = False)
    com_cd = KColumn(String(20), primary_key = True, nullable = False)
    com_cd_nm = KColumn(String(100), nullable = False)
    com_cd_desc = KColumn(String(1000), nullable = True)
    prnt_seq = KColumn(Integer, nullable = False)
    eff_sta_ymd = KColumn(String(8), nullable = False)
    eff_end_ymd = KColumn(String(8), nullable = False)
    ref1 = KColumn(String(100), nullable = True)
    ref2 = KColumn(String(100), nullable = True)
    ref3 = KColumn(String(100), nullable = True)
    ref4 = KColumn(String(100), nullable = True)
    ref5 = KColumn(String(100), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.com_cd_grp =  kwargs.pop('com_cd_grp')
        self.com_cd =  kwargs.pop('com_cd')
        self.com_cd_nm =  kwargs.pop('com_cd_nm')
        self.com_cd_desc =  kwargs.pop('com_cd_desc','')
        self.prnt_seq =  kwargs.pop('prnt_seq')
        self.eff_sta_ymd =  kwargs.pop('eff_sta_ymd',datetime.datetime.now().strftime('%Y%m%d'))
        self.eff_end_ymd =  kwargs.pop('eff_end_ymd','99991231')
        self.ref1 =  kwargs.pop('ref1','')
        self.ref2 =  kwargs.pop('ref2','')
        self.ref3 =  kwargs.pop('ref3','')
        self.ref4 =  kwargs.pop('ref4','')
        self.ref5 =  kwargs.pop('ref5','')

    def __repr__(self):
        return "<ComCdDtl('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.com_cd_grp), str(self.com_cd), str(self.com_cd_nm), str(self.com_cd_desc), str(self.prnt_seq), str(self.eff_sta_ymd), str(self.eff_end_ymd), str(self.ref1), str(self.ref2), str(self.ref3), str(self.ref4), str(self.ref5) + KTable.__repr__(self))


if __name__ == "__main__" :
    #menu = Menu('test',None,None,None,None,None)
    #list = ['a','b','c','d',1,'e','f','g','h','i','j','k']
    list = {'com_cd_grp' : 'ABC','com_cd_grp_nm' : 'BBB','del_yn' : 'N'}
    dtl = ComCdDtl(list)
    #print(dtl)
    pass