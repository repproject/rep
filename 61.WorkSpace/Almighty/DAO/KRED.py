from DAO.KTable import *
from sqlalchemy import Integer, ForeignKey, String
from common.database.testReflect import *
from common.database.repSqlAlchemy import *
import datetime

class LeglDong(Base,KTable):
    __tablename__ = 'kred_legl_dong'

    legl_dong_cd = KColumn(String(10), primary_key = True, nullable = False)
    legl_dong_nm = KColumn(String(200), nullable = True)
    legl_dong_whl_nm = KColumn(String(200), nullable = True)
    up_legl_dong_cd = KColumn(String(10), nullable = True)
    lv_cd = KColumn(String(20), nullable = True)
    sort_seq = KColumn(Integer, nullable = True)
    reg_ymd = KColumn(String(8), nullable = True)
    clos_ymd = KColumn(String(8), nullable = True)
    finl_job_ymd = KColumn(String(8), nullable = True)
    rsdt_legl_dong_cd = KColumn(String(10), nullable = True)
    legl_jijc_legl_dong_cd = KColumn(String(10), nullable = True)
    use_yn = KColumn(String(1), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.legl_dong_cd =  kwargs.pop('legl_dong_cd')
        self.legl_dong_nm =  kwargs.pop('legl_dong_nm',None)
        self.legl_dong_whl_nm =  kwargs.pop('legl_dong_whl_nm',None)
        self.up_legl_dong_cd =  kwargs.pop('up_legl_dong_cd',None)
        self.lv_cd =  kwargs.pop('lv_cd',None)
        self.sort_seq =  kwargs.pop('sort_seq',None)
        self.reg_ymd =  kwargs.pop('reg_ymd',None)
        self.clos_ymd =  kwargs.pop('clos_ymd',None)
        self.finl_job_ymd =  kwargs.pop('finl_job_ymd',None)
        self.rsdt_legl_dong_cd =  kwargs.pop('rsdt_legl_dong_cd',None)
        self.legl_jijc_legl_dong_cd =  kwargs.pop('legl_jijc_legl_dong_cd',None)
        self.use_yn =  kwargs.pop('use_yn','Y')

    def __repr__(self):
        return "<LeglDong('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.legl_dong_cd), str(self.legl_dong_nm), str(self.legl_dong_whl_nm), str(self.up_legl_dong_cd), str(self.lv_cd), str(self.sort_seq), str(self.reg_ymd), str(self.clos_ymd), str(self.finl_job_ymd), str(self.rsdt_legl_dong_cd), str(self.legl_jijc_legl_dong_cd), str(self.use_yn) + KTable.__repr__(self))
