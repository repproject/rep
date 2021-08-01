from DAO.KTable import *
from sqlalchemy import Integer, ForeignKey, String
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

class Site(Base,KTable):
    __tablename__ = 'KADM_SITE'

    site_cd = KColumn(String(20), primary_key = True, nullable = False, kcom_cd_domain=True, kcom_cd_grp='SITE')
    slep_sec = KColumn(Float, nullable = True)
    bas_url = KColumn(String(1000), nullable = True)
    bas_prtc = KColumn(String(10), nullable = True)
    enc_cd = KColumn(String(20), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.site_cd =  kwargs.pop('site_cd')
        self.slep_sec =  kwargs.pop('slep_sec','')
        self.bas_url =  kwargs.pop('bas_url','')
        self.bas_prtc =  kwargs.pop('bas_prtc','')
        self.enc_cd =  kwargs.pop('enc_cd','')

    def __repr__(self):
        return "<Site('%s', '%s', '%s', '%s', '%s'" % (str(self.site_cd), str(self.slep_sec), str(self.bas_url), str(self.bas_prtc), str(self.enc_cd) + KTable.__repr__(self))

class Svc(Base,KTable):
    __tablename__ = 'KADM_SVC'

    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    site_cd = KColumn(String(20), nullable = False, kcom_cd_domain=True, kcom_cd_grp='SITE')
    #site_cd = KColumn(String(20),ForeignKey("Site.site_cd"))
    bas_svc_url = KColumn(String(1000), nullable = True)
    req_way_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True,kcom_cd_grp='REQ_WAY')
    exmp_url = KColumn(String(1000),nullable = True)
    site = relationship("Site",primaryjoin= site_cd == Site.site_cd, foreign_keys=Site.site_cd)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.svc_id =  kwargs.pop('svc_id')
        self.site_cd = kwargs.pop('site_cd')
        self.bas_svc_url =  kwargs.pop('bas_svc_url','')
        self.req_way_cd =  kwargs.pop('req_way_cd','')
        self.exmp_url = kwargs.pop('exmp_url', '')

    def __repr__(self):
        return "<Svc('%s', '%s', '%s', '%s', '%s'" % (str(self.svc_id), str(self.site_cd), str(self.bas_svc_url), str(self.req_way_cd), str(self.exmp_url) + KTable.__repr__(self))

class SvcParm(Base,KTable):
    __tablename__ = 'KADM_SVC_PARM'

    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    svc_parm_id = KColumn(String(50), primary_key = True, nullable = False)
    svc_parm_val = KColumn(String(200), nullable = True)
    svc_parm_desc = KColumn(String(500), nullable = False)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.svc_id =  kwargs.pop('svc_id')
        self.svc_parm_id =  kwargs.pop('svc_parm_id')
        self.svc_parm_val =  kwargs.pop('svc_parm_val','')
        self.svc_parm_desc =  kwargs.pop('svc_parm_desc')

    def __repr__(self):
        return "<SvcParm('%s', '%s', '%s', '%s'" % (str(self.svc_id), str(self.svc_parm_id), str(self.svc_parm_val), str(self.svc_parm_desc) + KTable.__repr__(self))

class Tbl(Base,KTable):
    __tablename__ = 'KADM_TBL'

    tbl_nm = KColumn(String(50), primary_key = True, nullable = False)
    tbl_desc = KColumn(String(500), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.tbl_nm =  kwargs.pop('tbl_nm')
        self.tbl_desc =  kwargs.pop('tbl_desc','')

    def __repr__(self):
        return "<Tbl('%s', '%s'" % (str(self.tbl_nm), str(self.tbl_desc) + KTable.__repr__(self))

class TblCol(Base,KTable):
    __tablename__ = 'KADM_TBL_COL'

    tbl_nm = KColumn(String(50), primary_key = True, nullable = False)
    col_nm = KColumn(String(50), primary_key = True, nullable = False)
    col_desc = KColumn(String(500), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.tbl_nm =  kwargs.pop('tbl_nm')
        self.col_nm =  kwargs.pop('col_nm')
        self.col_desc =  kwargs.pop('col_desc','')

    def __repr__(self):
        return "<TblCol('%s', '%s', '%s'" % (str(self.tbl_nm), str(self.col_nm), str(self.col_desc) + KTable.__repr__(self))

class SvcPasi(Base,KTable):
    __tablename__ = 'KADM_SVC_PASI'

    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    pasi_id = KColumn(String(50), primary_key = True, nullable = False)
    pasi_way = KColumn(String(20), nullable = False)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.svc_id =  kwargs.pop('svc_id')
        self.pasi_id =  kwargs.pop('pasi_id')
        self.pasi_way =  kwargs.pop('pasi_way')

    def __repr__(self):
        return "<SvcPasi('%s', '%s', '%s'" % (str(self.svc_id), str(self.pasi_id), str(self.pasi_way) + KTable.__repr__(self))

class SvcPasiItem(Base,KTable):
    __tablename__ = 'KADM_SVC_PASI_ITEM'

    pasi_id = KColumn(String(50), primary_key = True, nullable = False)
    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    tbl_nm = KColumn(String(50), nullable = True)
    col_nm = KColumn(String(50), nullable = True)
    item_nm = KColumn(String(200), primary_key = True, nullable = False)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.pasi_id =  kwargs.pop('pasi_id')
        self.svc_id =  kwargs.pop('svc_id')
        self.tbl_nm =  kwargs.pop('tbl_nm','')
        self.col_nm =  kwargs.pop('col_nm','')
        self.item_nm =  kwargs.pop('item_nm')

    def __repr__(self):
        return "<SvcPasiItem('%s', '%s', '%s', '%s', '%s'" % (str(self.pasi_id), str(self.svc_id), str(self.tbl_nm), str(self.col_nm), str(self.item_nm) + KTable.__repr__(self))


if __name__ == "__main__" :
    #menu = Menu('test',None,None,None,None,None)
    #list = ['a','b','c','d',1,'e','f','g','h','i','j','k']
    list = {'svc_id' : 'a','svc_parm_id' : 'BBB','site_cd' : 'N'}
    dtl = SvcParm(svc_id = 'a',svc_parm_id='B',site_cd='D')
    #print(dtl)
    pass