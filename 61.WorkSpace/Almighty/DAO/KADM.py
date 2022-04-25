from DAO.KTable import *
from sqlalchemy import Integer, ForeignKey, String
from common.database.testReflect import *
from common.database.repSqlAlchemy import *
import datetime

Base = declarative_base()

class Tbl(Base,KTable):
    __tablename__ = 'kadm_tbl'

    tbl_nm = KColumn(String(50), primary_key = True, nullable = False)
    tbl_desc = KColumn(String(500), nullable = True)
    cls_nm = KColumn(String(200), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.tbl_nm =  kwargs.pop('tbl_nm')
        self.tbl_desc =  kwargs.pop('tbl_desc','')
        self.cls_nm =  kwargs.pop('cls_nm','')

    def __repr__(self):
        return "<Tbl('%s', '%s', '%s'" % (str(self.tbl_nm), str(self.tbl_desc), str(self.cls_nm) + KTable.__repr__(self))

class TblCol(Base,KTable):
    __tablename__ = 'kadm_tbl_col'

    tbl_nm = KColumn(String(50), primary_key = True, nullable = False)
    col_nm = KColumn(String(50), primary_key = True, nullable = False)
    col_han_nm = KColumn(String(200), nullable = True)
    col_doma_cd = KColumn(String(20), nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'COL_DOMA')
    col_doma_val = KColumn(String(200), nullable = True)
    col_seq = KColumn(Integer, nullable = False)
    pant_tbl_nm = KColumn(String(50), nullable = True)
    pant_col_nm = KColumn(String(50), nullable = True)
    pk_yn = KColumn(String(1), nullable = False)
    bas_val = KColumn(String(200), nullable = True)
    col_desc = KColumn(String(500), nullable = True)

    tbl = relationship('Tbl',primaryjoin = tbl_nm == Tbl.tbl_nm, foreign_keys=Tbl.tbl_nm,passive_deletes=True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.tbl_nm =  kwargs.pop('tbl_nm')
        self.col_nm =  kwargs.pop('col_nm')
        self.col_han_nm =  kwargs.pop('col_han_nm','')
        self.col_doma_cd =  kwargs.pop('col_doma_cd','NA')
        self.col_doma_val =  kwargs.pop('col_doma_val','')
        self.col_seq =  kwargs.pop('col_seq')
        self.pant_tbl_nm =  kwargs.pop('pant_tbl_nm','')
        self.pant_col_nm =  kwargs.pop('pant_col_nm','')
        self.pk_yn =  kwargs.pop('pk_yn','N')
        self.bas_val =  kwargs.pop('bas_val','')
        self.col_desc =  kwargs.pop('col_desc','')

    def __repr__(self):
        return "<TblCol('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.tbl_nm), str(self.col_nm), str(self.col_han_nm), str(self.col_doma_cd), str(self.col_doma_val), str(self.col_seq), str(self.pant_tbl_nm), str(self.pant_col_nm), str(self.pk_yn), str(self.bas_val), str(self.col_desc) + KTable.__repr__(self))

class Site(Base,KTable):
    __tablename__ = 'kadm_site'

    site_cd = KColumn(String(20), primary_key = True, nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'SITE')
    slep_sec = KColumn(Float, nullable = True)
    bas_url = KColumn(String(1000), nullable = True)
    bas_prtc = KColumn(String(10), nullable = True)
    enc_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'ENC')
    han_enc_yn = KColumn(String(1), nullable = False)
    site_desc = KColumn(String(500), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.site_cd =  kwargs.pop('site_cd')
        self.slep_sec =  kwargs.pop('slep_sec',None)
        self.bas_url =  kwargs.pop('bas_url',None)
        self.bas_prtc =  kwargs.pop('bas_prtc',None)
        self.enc_cd =  kwargs.pop('enc_cd',None)
        self.han_enc_yn =  kwargs.pop('han_enc_yn')
        self.site_desc =  kwargs.pop('site_desc',None)

    def __repr__(self):
        return "<Site('%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.site_cd), str(self.slep_sec), str(self.bas_url), str(self.bas_prtc), str(self.enc_cd), str(self.han_enc_yn), str(self.site_desc) + KTable.__repr__(self))

class Svc(Base,KTable):
    __tablename__ = 'kadm_svc'

    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    site_cd = KColumn(String(20), nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'SITE')
    svc_nm = KColumn(String(200), nullable=True)
    bas_svc_url = KColumn(String(1000), nullable = True)
    req_way_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'REQ_WAY')
    exmp_url = KColumn(String(1000), nullable = True)
    svc_desc = KColumn(String(500), nullable = True)

    site = relationship('Site',primaryjoin = site_cd == Site.site_cd, foreign_keys=Site.site_cd,passive_deletes=True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.svc_id =  kwargs.pop('svc_id')
        self.site_cd =  kwargs.pop('site_cd')
        self.bas_svc_url =  kwargs.pop('bas_svc_url','')
        self.req_way_cd =  kwargs.pop('req_way_cd','')
        self.exmp_url =  kwargs.pop('exmp_url','')
        self.svc_desc =  kwargs.pop('svc_desc','')

    def __repr__(self):
        return "<Svc('%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.svc_id), str(self.site_cd), str(self.bas_svc_url), str(self.req_way_cd), str(self.exmp_url), str(self.svc_desc) + KTable.__repr__(self))

class SvcPasi(Base,KTable):
    __tablename__ = 'kadm_svc_pasi'

    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    pasi_id = KColumn(String(50), primary_key = True, nullable = False)
    pasi_nm = KColumn(String(200), nullable = True)
    pasi_way_cd = KColumn(String(20), nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'PASI_WAY')
    parm_load_func_nm = KColumn(String(200), nullable = True)
    svc_pasi_desc = KColumn(String(500), nullable = True)

    svc = relationship('Svc',primaryjoin = svc_id == Svc.svc_id, foreign_keys=Svc.svc_id,passive_deletes=True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.svc_id =  kwargs.pop('svc_id')
        self.pasi_id =  kwargs.pop('pasi_id')
        self.pasi_nm =  kwargs.pop('pasi_nm','')
        self.pasi_way_cd =  kwargs.pop('pasi_way_cd')
        self.parm_load_func_nm =  kwargs.pop('parm_load_func_nm','')
        self.svc_pasi_desc =  kwargs.pop('svc_pasi_desc','')

    def __repr__(self):
        return "<SvcPasi('%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.svc_id), str(self.pasi_id), str(self.pasi_nm), str(self.pasi_way_cd), str(self.parm_load_func_nm), str(self.svc_pasi_desc) + KTable.__repr__(self))

class SvcPasiItem(Base,KTable):
    __tablename__ = 'kadm_svc_pasi_item'

    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    pasi_id = KColumn(String(50), primary_key = True, nullable = False)
    in_out_cl_cd = KColumn(String(20), primary_key = True, nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'IN_OUT_CL')
    item_nm = KColumn(String(200), primary_key = True, nullable = False)
    item_val = KColumn(String(200), nullable = True)
    item_src_cl_cd = KColumn(String(20), nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'ITEM_SRC_CL')
    tbl_nm = KColumn(String(50), nullable = True)
    col_nm = KColumn(String(50), nullable = True)
    item_desc = KColumn(String(500), nullable = True)
    excp_str = KColumn(String(200), nullable = True)
    dlmi_str = KColumn(String(200), nullable = True)
    del_yn = KColumn(String(1), nullable = True)

    svcpasi = relationship('SvcPasi',primaryjoin = and_(svc_id==SvcPasi.svc_id , pasi_id==SvcPasi.pasi_id), foreign_keys = [SvcPasi.svc_id , SvcPasi.pasi_id], passive_deletes = True)
    tblcol = relationship('TblCol',primaryjoin = and_(tbl_nm==TblCol.tbl_nm , col_nm==TblCol.col_nm), foreign_keys = [TblCol.tbl_nm , TblCol.col_nm], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.svc_id =  kwargs.pop('svc_id')
        self.pasi_id =  kwargs.pop('pasi_id')
        self.in_out_cl_cd =  kwargs.pop('in_out_cl_cd')
        self.item_nm =  kwargs.pop('item_nm')
        self.item_val =  kwargs.pop('item_val',None)
        self.item_src_cl_cd =  kwargs.pop('item_src_cl_cd','NA')
        self.tbl_nm =  kwargs.pop('tbl_nm',None)
        self.col_nm =  kwargs.pop('col_nm',None)
        self.item_desc =  kwargs.pop('item_desc',None)
        self.excp_str =  kwargs.pop('excp_str',None)
        self.dlmi_str =  kwargs.pop('dlmi_str',None)
        self.del_yn =  kwargs.pop('del_yn','N')

    def __repr__(self):
        return "<SvcPasiItem('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.svc_id), str(self.pasi_id), str(self.in_out_cl_cd), str(self.item_nm), str(self.item_val), str(self.item_src_cl_cd), str(self.tbl_nm), str(self.col_nm), str(self.item_desc), str(self.excp_str), str(self.dlmi_str), str(self.del_yn) + KTable.__repr__(self))

class SvcPasiItemCol(Base,KTable):
    __tablename__ = 'kadm_svc_pasi_item_col'

    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    pasi_id = KColumn(String(50), primary_key = True, nullable = False)
    in_out_cl_cd = KColumn(String(20), primary_key = True, nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'IN_OUT_CL')
    item_nm = KColumn(String(200), primary_key = True, nullable = False)
    tbl_nm = KColumn(String(50), primary_key = True, nullable = False)
    col_nm = KColumn(String(50), primary_key = True, nullable = False)

    svcpasiitem = relationship('SvcPasiItem',primaryjoin = and_(svc_id==SvcPasiItem.svc_id , pasi_id==SvcPasiItem.pasi_id , in_out_cl_cd==SvcPasiItem.in_out_cl_cd , item_nm==SvcPasiItem.item_nm), foreign_keys = [SvcPasiItem.svc_id , SvcPasiItem.pasi_id , SvcPasiItem.in_out_cl_cd , SvcPasiItem.item_nm], passive_deletes = True)
    tblcol = relationship('TblCol',primaryjoin = and_(tbl_nm==TblCol.tbl_nm , col_nm==TblCol.col_nm), foreign_keys = [TblCol.tbl_nm , TblCol.col_nm], passive_deletes = True, overlaps="tblcol")

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.svc_id =  kwargs.pop('svc_id')
        self.pasi_id =  kwargs.pop('pasi_id')
        self.in_out_cl_cd =  kwargs.pop('in_out_cl_cd')
        self.item_nm =  kwargs.pop('item_nm')
        self.tbl_nm =  kwargs.pop('tbl_nm')
        self.col_nm =  kwargs.pop('col_nm')

    def __repr__(self):
        return "<SvcPasiItemCol('%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.svc_id), str(self.pasi_id), str(self.in_out_cl_cd), str(self.item_nm), str(self.tbl_nm), str(self.col_nm) + KTable.__repr__(self))

class CdExec(Base,KTable):
    __tablename__ = 'kadm_cd_exec'

    cd_exec_id = KColumn(String(50), primary_key = True, nullable = False)
    cd_exec_nm = KColumn(String(200), nullable = True)
    cd_exec_cl_cd = KColumn(String(20), nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'CD_EXEC_CL')
    exec_cd_cnts = KColumn(String(4000), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.cd_exec_id =  kwargs.pop('cd_exec_id')
        self.cd_exec_nm =  kwargs.pop('cd_exec_nm','')
        self.cd_exec_cl_cd =  kwargs.pop('cd_exec_cl_cd')
        self.exec_cd_cnts =  kwargs.pop('exec_cd_cnts','')

    def __repr__(self):
        return "<CdExec('%s', '%s', '%s', '%s'" % (str(self.cd_exec_id), str(self.cd_exec_nm), str(self.cd_exec_cl_cd), str(self.exec_cd_cnts) + KTable.__repr__(self))

class PasiCdExec(Base,KTable):
    __tablename__ = 'kadm_pasi_cd_exec'

    svc_id = KColumn(String(500), primary_key = True, nullable = False)
    pasi_id = KColumn(String(50), primary_key = True, nullable = False)
    seq = KColumn(Integer, primary_key = True, nullable = False)
    cd_exec_id = KColumn(String(50), nullable = False)
    cd_exec_seq = KColumn(Integer, nullable = True)
    up_seq = KColumn(Integer, nullable = True)
    exec_parm_val = KColumn(String(200), nullable = True)


    svcpasi = relationship('SvcPasi',primaryjoin = and_(svc_id==SvcPasi.svc_id , pasi_id==SvcPasi.pasi_id), foreign_keys = [SvcPasi.svc_id , SvcPasi.pasi_id], passive_deletes = True, overlaps="svcpasi")
    cdexec = relationship('CdExec',primaryjoin = cd_exec_id==CdExec.cd_exec_id, foreign_keys = [CdExec.cd_exec_id], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.svc_id =  kwargs.pop('svc_id')
        self.pasi_id =  kwargs.pop('pasi_id')
        self.cd_exec_id =  kwargs.pop('cd_exec_id')
        self.cd_exec_seq =  kwargs.pop('cd_exec_seq','')
        self.up_seq =  kwargs.pop('up_seq','')
        self.exec_parm_val =  kwargs.pop('exec_parm_val','')
        self.seq =  kwargs.pop('seq')

    def __repr__(self):
        return "<PasiCdExec('%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.svc_id), str(self.pasi_id), str(self.cd_exec_id), str(self.cd_exec_seq), str(self.up_seq), str(self.exec_parm_val), str(self.seq) + KTable.__repr__(self))

class Job(Base,KTable):
    __tablename__ = 'kadm_job'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    job_nm = KColumn(String(100), nullable = False)
    job_desc = KColumn(String(1000), nullable = True)
    job_cl_cd = KColumn(String(20), nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'JOB_CL')
    use_yn = KColumn(String(1), nullable = False)
    ref1 = KColumn(String(100), nullable = True)
    ref2 = KColumn(String(100), nullable = True)
    ref3 = KColumn(String(100), nullable = True)
    ref4 = KColumn(String(100), nullable = True)
    ref5 = KColumn(String(100), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.job_nm =  kwargs.pop('job_nm')
        self.job_desc =  kwargs.pop('job_desc',None)
        self.job_cl_cd =  kwargs.pop('job_cl_cd')
        self.use_yn =  kwargs.pop('use_yn','Y')
        self.ref1 =  kwargs.pop('ref1',None)
        self.ref2 =  kwargs.pop('ref2',None)
        self.ref3 =  kwargs.pop('ref3',None)
        self.ref4 =  kwargs.pop('ref4',None)
        self.ref5 =  kwargs.pop('ref5',None)

    def __repr__(self):
        return "<Job('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.job_nm), str(self.job_desc), str(self.job_cl_cd), str(self.use_yn), str(self.ref1), str(self.ref2), str(self.ref3), str(self.ref4), str(self.ref5) + KTable.__repr__(self))

class JobSchd(Base,KTable):
    __tablename__ = 'kadm_job_schd'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    job_seq = KColumn(Integer, primary_key = True, nullable = False)
    exec_perd_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'EXEC_PERD')
    exec_mm = KColumn(String(2), nullable = True)
    exec_dd = KColumn(String(8), nullable = True)
    exec_hh = KColumn(String(2), nullable = True)
    exec_mi = KColumn(String(2), nullable = True)
    exec_day_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'EXEC_DAY')
    cycl_mi = KColumn(String(2), nullable = True)
    imdi_exec_yn = KColumn(String(1), nullable = True)
    use_yn = KColumn(String(1), nullable = True)
    del_yn = KColumn(String(1), nullable = True)
    chg_yn = KColumn(String(1), nullable=False)

    job = relationship('Job',primaryjoin = job_id==Job.job_id, foreign_keys = [Job.job_id], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.job_seq =  kwargs.pop('job_seq')
        self.exec_perd_cd =  kwargs.pop('exec_perd_cd',None)
        self.exec_mm =  kwargs.pop('exec_mm',None)
        self.exec_dd =  kwargs.pop('exec_dd',None)
        self.exec_hh =  kwargs.pop('exec_hh',None)
        self.exec_mi =  kwargs.pop('exec_mi',None)
        self.exec_day_cd =  kwargs.pop('exec_day_cd',None)
        self.cycl_mi =  kwargs.pop('cycl_mi',None)
        self.imdi_exec_yn =  kwargs.pop('imdi_exec_yn',None)
        self.use_yn =  kwargs.pop('use_yn',None)
        self.del_yn =  kwargs.pop('del_yn',None)
        self.chg_yn = kwargs.pop('del_yn', 'N')

    def __repr__(self):
        return "<JobSchd('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.job_seq), str(self.exec_perd_cd), str(self.exec_mm), str(self.exec_dd), str(self.exec_hh), str(self.exec_mi), str(self.exec_day_cd), str(self.cycl_mi), str(self.imdi_exec_yn), str(self.use_yn), str(self.del_yn), str(self.chg_yn) + KTable.__repr__(self))

class JobExec(Base,KTable):
    __tablename__ = 'kadm_job_exec'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_dtm = KColumn(String(14), primary_key = True, nullable = False)
    exec_stat_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'EXEC_STAT')
    sta_dtm = KColumn(String(14), nullable = True)
    end_dtm = KColumn(String(14), nullable = True)
    exec_parm1 = KColumn(String(200), nullable = True)
    exec_parm2 = KColumn(String(200), nullable = True)
    exec_parm3 = KColumn(String(200), nullable = True)
    exec_parm4 = KColumn(String(200), nullable = True)
    exec_parm5 = KColumn(String(200), nullable = True)
    exec_parm6 = KColumn(String(200), nullable = True)
    exec_parm7 = KColumn(String(200), nullable = True)
    exec_parm8 = KColumn(String(200), nullable = True)
    exec_parm9 = KColumn(String(200), nullable = True)
    exec_parm10 = KColumn(String(200), nullable = True)
    msg_cnts = KColumn(String(4000), nullable = True)

    job = relationship('Job',primaryjoin = job_id==Job.job_id, foreign_keys = [Job.job_id], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.exec_stat_cd =  kwargs.pop('exec_stat_cd',None)
        self.sta_dtm =  kwargs.pop('sta_dtm',None)
        self.end_dtm =  kwargs.pop('end_dtm',None)
        self.exec_parm1 =  kwargs.pop('exec_parm1',None)
        self.exec_parm2 =  kwargs.pop('exec_parm2',None)
        self.exec_parm3 =  kwargs.pop('exec_parm3',None)
        self.exec_parm4 =  kwargs.pop('exec_parm4',None)
        self.exec_parm5 =  kwargs.pop('exec_parm5',None)
        self.exec_parm6 =  kwargs.pop('exec_parm6',None)
        self.exec_parm7 =  kwargs.pop('exec_parm7',None)
        self.exec_parm8 =  kwargs.pop('exec_parm8',None)
        self.exec_parm9 =  kwargs.pop('exec_parm9',None)
        self.exec_parm10 =  kwargs.pop('exec_parm10',None)
        self.msg_cnts =  kwargs.pop('msg_cnts',None)

    def __repr__(self):
        return "<JobExec('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.exec_stat_cd), str(self.sta_dtm), str(self.end_dtm), str(self.exec_parm1), str(self.exec_parm2), str(self.exec_parm3), str(self.exec_parm4), str(self.exec_parm5), str(self.exec_parm6), str(self.exec_parm7), str(self.exec_parm8), str(self.exec_parm9), str(self.exec_parm10), str(self.msg_cnts) + KTable.__repr__(self))

class JobSchdExec(Base, KTable):
    __tablename__ = 'kadm_job_schd_exec'

    job_id = KColumn(String(20), primary_key=True, nullable=False)
    job_seq = KColumn(Integer, primary_key=True, nullable=False)
    exec_parm1 = KColumn(String(200), nullable=True)
    exec_parm2 = KColumn(String(200), nullable=True)
    exec_parm3 = KColumn(String(200), nullable=True)
    exec_parm4 = KColumn(String(200), nullable=True)
    exec_parm5 = KColumn(String(200), nullable=True)
    exec_parm6 = KColumn(String(200), nullable=True)
    exec_parm7 = KColumn(String(200), nullable=True)
    exec_parm8 = KColumn(String(200), nullable=True)
    exec_parm9 = KColumn(String(200), nullable=True)
    exec_parm10 = KColumn(String(200), nullable=True)

    jobschd = relationship('JobSchd', primaryjoin=and_(job_id == JobSchd.job_id, job_seq == JobSchd.job_seq),
                           foreign_keys=[JobSchd.job_id, JobSchd.job_seq], passive_deletes=True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id = kwargs.pop('job_id')
        self.job_seq = kwargs.pop('job_seq')
        self.exec_parm1 = kwargs.pop('exec_parm1', None)
        self.exec_parm2 = kwargs.pop('exec_parm2', None)
        self.exec_parm3 = kwargs.pop('exec_parm3', None)
        self.exec_parm4 = kwargs.pop('exec_parm4', None)
        self.exec_parm5 = kwargs.pop('exec_parm5', None)
        self.exec_parm6 = kwargs.pop('exec_parm6', None)
        self.exec_parm7 = kwargs.pop('exec_parm7', None)
        self.exec_parm8 = kwargs.pop('exec_parm8', None)
        self.exec_parm9 = kwargs.pop('exec_parm9', None)
        self.exec_parm10 = kwargs.pop('exec_parm10', None)

    def __repr__(self):
        return "<JobSchdExec('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (
        str(self.job_id), str(self.job_seq), str(self.exec_parm1), str(self.exec_parm2), str(self.exec_parm3),
        str(self.exec_parm4), str(self.exec_parm5), str(self.exec_parm6), str(self.exec_parm7),
        str(self.exec_parm8), str(self.exec_parm9), str(self.exec_parm10) + KTable.__repr__(self))


class Act(Base,KTable):
    __tablename__ = 'kadm_act'

    act_id = KColumn(String(20), primary_key = True, nullable = False)
    act_nm = KColumn(String(100), nullable = False)
    act_desc = KColumn(String(1000), nullable = True)
    use_yn = KColumn(String(1), nullable = False)
    ref1 = KColumn(String(100), nullable = True)
    ref2 = KColumn(String(100), nullable = True)
    ref3 = KColumn(String(100), nullable = True)
    ref4 = KColumn(String(100), nullable = True)
    ref5 = KColumn(String(100), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.act_id =  kwargs.pop('act_id')
        self.act_nm =  kwargs.pop('act_nm')
        self.act_desc =  kwargs.pop('act_desc',None)
        self.use_yn =  kwargs.pop('use_yn')
        self.ref1 =  kwargs.pop('ref1',None)
        self.ref2 =  kwargs.pop('ref2',None)
        self.ref3 =  kwargs.pop('ref3',None)
        self.ref4 =  kwargs.pop('ref4',None)
        self.ref5 =  kwargs.pop('ref5',None)

    def __repr__(self):
        return "<Act('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.act_id), str(self.act_nm), str(self.act_desc), str(self.use_yn), str(self.ref1), str(self.ref2), str(self.ref3), str(self.ref4), str(self.ref5) + KTable.__repr__(self))

class JobAct(Base,KTable):
    __tablename__ = 'kadm_job_act'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    act_id = KColumn(String(20), primary_key = True, nullable = False)
    job_act_rel_desc = KColumn(String(1000), nullable = True)
    exec_seq = KColumn(Integer, nullable = False)
    use_yn = KColumn(String(1), nullable = False)

    job = relationship('Job',primaryjoin = job_id==Job.job_id, foreign_keys = [Job.job_id], passive_deletes = True,overlaps="job")
    act = relationship('Act',primaryjoin = act_id==Act.act_id, foreign_keys = [Act.act_id], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.act_id =  kwargs.pop('act_id')
        self.job_act_rel_desc =  kwargs.pop('job_act_rel_desc',None)
        self.exec_seq =  kwargs.pop('exec_seq')
        self.use_yn =  kwargs.pop('use_yn')

    def __repr__(self):
        return "<JobAct('%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.act_id), str(self.job_act_rel_desc), str(self.exec_seq), str(self.use_yn) + KTable.__repr__(self))

class JobActExec(Base,KTable):
    __tablename__ = 'kadm_job_act_exec'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_dtm = KColumn(DATE, primary_key = True, nullable = False)
    act_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_stat_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'EXEC_STAT')
    sta_dtm = KColumn(DATE, nullable = True)
    end_dtm = KColumn(DATE, nullable = True)
    exec_parm1 = KColumn(String(200), nullable = True)
    exec_parm2 = KColumn(String(200), nullable = True)
    exec_parm3 = KColumn(String(200), nullable = True)
    exec_parm4 = KColumn(String(200), nullable = True)
    exec_parm5 = KColumn(String(200), nullable = True)
    exec_parm6 = KColumn(String(200), nullable = True)
    exec_parm7 = KColumn(String(200), nullable = True)
    exec_parm8 = KColumn(String(200), nullable = True)
    exec_parm9 = KColumn(String(200), nullable = True)
    exec_parm10 = KColumn(String(200), nullable = True)

    jobact = relationship('JobAct',primaryjoin = and_(job_id==JobAct.job_id , act_id==JobAct.act_id), foreign_keys = [JobAct.job_id , JobAct.act_id], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.act_id =  kwargs.pop('act_id')
        self.exec_stat_cd =  kwargs.pop('exec_stat_cd',None)
        self.sta_dtm =  kwargs.pop('sta_dtm',None)
        self.end_dtm =  kwargs.pop('end_dtm',None)
        self.exec_parm1 =  kwargs.pop('exec_parm1',None)
        self.exec_parm2 =  kwargs.pop('exec_parm2',None)
        self.exec_parm3 =  kwargs.pop('exec_parm3',None)
        self.exec_parm4 =  kwargs.pop('exec_parm4',None)
        self.exec_parm5 =  kwargs.pop('exec_parm5',None)
        self.exec_parm6 =  kwargs.pop('exec_parm6',None)
        self.exec_parm7 =  kwargs.pop('exec_parm7',None)
        self.exec_parm8 =  kwargs.pop('exec_parm8',None)
        self.exec_parm9 =  kwargs.pop('exec_parm9',None)
        self.exec_parm10 =  kwargs.pop('exec_parm10',None)

    def __repr__(self):
        return "<JobActExec('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.act_id), str(self.exec_stat_cd), str(self.sta_dtm), str(self.end_dtm), str(self.exec_parm1), str(self.exec_parm2), str(self.exec_parm3), str(self.exec_parm4), str(self.exec_parm5), str(self.exec_parm6), str(self.exec_parm7), str(self.exec_parm8), str(self.exec_parm9), str(self.exec_parm10) + KTable.__repr__(self))

class Func(Base,KTable):
    __tablename__ = 'kadm_func'

    func_id = KColumn(String(20), primary_key = True, nullable = False)
    func_nm = KColumn(String(100), nullable = False)
    func_desc = KColumn(String(1000), nullable = True)
    func_cl_cd = KColumn(String(20), nullable = False, kcom_cd_domain = True, kcom_cd_grp = 'FUNC_CL')
    tgt_tbl_nm = KColumn(String(50), nullable = True)
    src_func_nm = KColumn(String(100), nullable = True)
    use_yn = KColumn(String(1), nullable = False)
    ref1 = KColumn(String(100), nullable = True)
    ref2 = KColumn(String(100), nullable = True)
    ref3 = KColumn(String(100), nullable = True)
    ref4 = KColumn(String(100), nullable = True)
    ref5 = KColumn(String(100), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.func_id =  kwargs.pop('func_id')
        self.func_nm =  kwargs.pop('func_nm')
        self.func_desc =  kwargs.pop('func_desc',None)
        self.func_cl_cd =  kwargs.pop('func_cl_cd')
        self.tgt_tbl_nm =  kwargs.pop('tgt_tbl_nm',None)
        self.src_func_nm =  kwargs.pop('src_func_nm',None)
        self.use_yn =  kwargs.pop('use_yn')
        self.ref1 =  kwargs.pop('ref1',None)
        self.ref2 =  kwargs.pop('ref2',None)
        self.ref3 =  kwargs.pop('ref3',None)
        self.ref4 =  kwargs.pop('ref4',None)
        self.ref5 =  kwargs.pop('ref5',None)

    def __repr__(self):
        return "<Func('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.func_id), str(self.func_nm), str(self.func_desc), str(self.func_cl_cd), str(self.tgt_tbl_nm), str(self.src_func_nm), str(self.use_yn), str(self.ref1), str(self.ref2), str(self.ref3), str(self.ref4), str(self.ref5) + KTable.__repr__(self))

class ActFunc(Base,KTable):
    __tablename__ = 'kadm_act_func'

    act_id = KColumn(String(20), primary_key = True, nullable = False)
    func_id = KColumn(String(20), primary_key = True, nullable = False)
    act_func_rel_desc = KColumn(String(1000), nullable = True)
    exec_seq = KColumn(Integer, nullable = False)
    use_yn = KColumn(String(1), nullable = False)

    act = relationship('Act',primaryjoin = act_id==Act.act_id, foreign_keys = [Act.act_id], passive_deletes = True,overlaps="act") #
    func = relationship('Func',primaryjoin = func_id==Func.func_id, foreign_keys = [Func.func_id], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.act_id =  kwargs.pop('act_id')
        self.func_id =  kwargs.pop('func_id')
        self.act_func_rel_desc =  kwargs.pop('act_func_rel_desc',None)
        self.exec_seq =  kwargs.pop('exec_seq')
        self.use_yn =  kwargs.pop('use_yn')

    def __repr__(self):
        return "<ActFunc('%s', '%s', '%s', '%s', '%s'" % (str(self.act_id), str(self.func_id), str(self.act_func_rel_desc), str(self.exec_seq), str(self.use_yn) + KTable.__repr__(self))

class JobFuncExec(Base,KTable):
    __tablename__ = 'kadm_job_func_exec'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    act_id = KColumn(String(20), primary_key = True, nullable = False)
    func_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_dtm = KColumn(String(14), primary_key = True, nullable = False)
    exec_stat_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'EXEC_STAT')
    sta_dtm = KColumn(String(14), nullable = True)
    end_dtm = KColumn(String(14), nullable = True)
    exec_parm1 = KColumn(String(200), nullable = True)
    exec_parm2 = KColumn(String(200), nullable = True)
    exec_parm3 = KColumn(String(200), nullable = True)
    exec_parm4 = KColumn(String(200), nullable = True)
    exec_parm5 = KColumn(String(200), nullable = True)
    exec_parm6 = KColumn(String(200), nullable = True)
    exec_parm7 = KColumn(String(200), nullable = True)
    exec_parm8 = KColumn(String(200), nullable = True)
    exec_parm9 = KColumn(String(200), nullable = True)
    exec_parm10 = KColumn(String(200), nullable = True)

    job = relationship('Job',primaryjoin = job_id==Job.job_id, foreign_keys = [Job.job_id], passive_deletes = True,overlaps="job")
    act = relationship('Act',primaryjoin = act_id==Act.act_id, foreign_keys = [Act.act_id], passive_deletes = True,overlaps="act")
    func = relationship('Func',primaryjoin = func_id==Func.func_id, foreign_keys = [Func.func_id], passive_deletes = True,overlaps="func")

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.act_id =  kwargs.pop('act_id')
        self.func_id =  kwargs.pop('func_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.exec_stat_cd =  kwargs.pop('exec_stat_cd',None)
        self.sta_dtm =  kwargs.pop('sta_dtm',None)
        self.end_dtm =  kwargs.pop('end_dtm',None)
        self.exec_parm1 =  kwargs.pop('exec_parm1',None)
        self.exec_parm2 =  kwargs.pop('exec_parm2',None)
        self.exec_parm3 =  kwargs.pop('exec_parm3',None)
        self.exec_parm4 =  kwargs.pop('exec_parm4',None)
        self.exec_parm5 =  kwargs.pop('exec_parm5',None)
        self.exec_parm6 =  kwargs.pop('exec_parm6',None)
        self.exec_parm7 =  kwargs.pop('exec_parm7',None)
        self.exec_parm8 =  kwargs.pop('exec_parm8',None)
        self.exec_parm9 =  kwargs.pop('exec_parm9',None)
        self.exec_parm10 =  kwargs.pop('exec_parm10',None)

    def __repr__(self):
        return "<JobFuncExec('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.act_id), str(self.func_id), str(self.exec_dtm), str(self.exec_stat_cd), str(self.sta_dtm), str(self.end_dtm), str(self.exec_parm1), str(self.exec_parm2), str(self.exec_parm3), str(self.exec_parm4), str(self.exec_parm5), str(self.exec_parm6), str(self.exec_parm7), str(self.exec_parm8), str(self.exec_parm9), str(self.exec_parm10) + KTable.__repr__(self))

class FuncTgtTbl(Base,KTable):
    __tablename__ = 'kadm_func_tgt_tbl'

    func_id = KColumn(String(20), primary_key = True, nullable = False)
    tbl_nm = KColumn(String(50), primary_key = True, nullable = False)
    finl_chg_yymm = KColumn(String(6), nullable = True)
    finl_chg_ymd = KColumn(String(8), nullable = True)

    func = relationship('Func',primaryjoin = func_id==Func.func_id, foreign_keys = [Func.func_id], passive_deletes = True,overlaps="func")
    tbl = relationship('Tbl',primaryjoin = tbl_nm==Tbl.tbl_nm, foreign_keys = [Tbl.tbl_nm], passive_deletes = True,overlaps="tbl")

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.func_id =  kwargs.pop('func_id')
        self.tbl_nm =  kwargs.pop('tbl_nm')
        self.finl_chg_yymm =  kwargs.pop('finl_chg_yymm',None)
        self.finl_chg_ymd =  kwargs.pop('finl_chg_ymd',None)

    def __repr__(self):
        return "<FuncTgtTbl('%s', '%s', '%s', '%s'" % (str(self.func_id), str(self.tbl_nm), str(self.finl_chg_yymm), str(self.finl_chg_ymd) + KTable.__repr__(self))

class Menu(Base,KTable):
    __tablename__ = 'kadm_menu'

    menu_id = KColumn(String(10), primary_key = True, nullable = False)
    menu_lv = KColumn(Integer, nullable = True)
    prnt_seq = KColumn(Integer, nullable = True)
    menu_nm = KColumn(String(200), nullable = True)
    up_menu_id = KColumn(String(10), nullable = True)
    fst_reg_ymd = KColumn(String(8), nullable = True)
    pgm_id = KColumn(String(10), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.menu_id =  kwargs.pop('menu_id')
        self.menu_lv =  kwargs.pop('menu_lv',None)
        self.prnt_seq =  kwargs.pop('prnt_seq',None)
        self.menu_nm =  kwargs.pop('menu_nm',None)
        self.up_menu_id =  kwargs.pop('up_menu_id',None)
        self.fst_reg_ymd =  kwargs.pop('fst_reg_ymd',None)
        self.pgm_id =  kwargs.pop('pgm_id',None)

    def __repr__(self):
        return "<Menu('%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.menu_id), str(self.menu_lv), str(self.prnt_seq), str(self.menu_nm), str(self.up_menu_id), str(self.fst_reg_ymd), str(self.pgm_id) + KTable.__repr__(self))

class ComCdLst(Base,KTable):
    __tablename__ = 'kadm_com_cd_lst'

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
        self.com_cd_grp =  kwargs.pop('com_cd_grp')
        self.com_cd_grp_nm =  kwargs.pop('com_cd_grp_nm')
        self.com_cd_grp_desc =  kwargs.pop('com_cd_grp_desc',None)
        self.up_com_cd_grp =  kwargs.pop('up_com_cd_grp',None)
        self.del_yn =  kwargs.pop('del_yn','N')
        self.ref1 =  kwargs.pop('ref1',None)
        self.ref2 =  kwargs.pop('ref2',None)
        self.ref3 =  kwargs.pop('ref3',None)
        self.ref4 =  kwargs.pop('ref4',None)
        self.ref5 =  kwargs.pop('ref5',None)

    def __repr__(self):
        return "<ComCdLst('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.com_cd_grp), str(self.com_cd_grp_nm), str(self.com_cd_grp_desc), str(self.up_com_cd_grp), str(self.del_yn), str(self.ref1), str(self.ref2), str(self.ref3), str(self.ref4), str(self.ref5) + KTable.__repr__(self))

class ComCdDtl(Base,KTable):
    __tablename__ = 'kadm_com_cd_dtl'

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

    comcdlst = relationship('ComCdLst',primaryjoin = com_cd_grp==ComCdLst.com_cd_grp, foreign_keys = [ComCdLst.com_cd_grp], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.com_cd_grp =  kwargs.pop('com_cd_grp')
        self.com_cd =  kwargs.pop('com_cd')
        self.com_cd_nm =  kwargs.pop('com_cd_nm')
        self.com_cd_desc =  kwargs.pop('com_cd_desc',None)
        self.prnt_seq =  kwargs.pop('prnt_seq')
        self.eff_sta_ymd =  kwargs.pop('eff_sta_ymd')
        self.eff_end_ymd =  kwargs.pop('eff_end_ymd')
        self.ref1 =  kwargs.pop('ref1',None)
        self.ref2 =  kwargs.pop('ref2',None)
        self.ref3 =  kwargs.pop('ref3',None)
        self.ref4 =  kwargs.pop('ref4',None)
        self.ref5 =  kwargs.pop('ref5',None)

    def __repr__(self):
        return "<ComCdDtl('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.com_cd_grp), str(self.com_cd), str(self.com_cd_nm), str(self.com_cd_desc), str(self.prnt_seq), str(self.eff_sta_ymd), str(self.eff_end_ymd), str(self.ref1), str(self.ref2), str(self.ref3), str(self.ref4), str(self.ref5) + KTable.__repr__(self))

class StdYymm(Base,KTable):
    __tablename__ = 'kadm_std_yymm'

    std_yymm = KColumn(String(6), primary_key = True, nullable = False)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.std_yymm =  kwargs.pop('std_yymm')

    def __repr__(self):
        return "<StdYymm('%s'" % (str(self.std_yymm) + KTable.__repr__(self))

class TlgrUser(Base,KTable):
    __tablename__ = 'kadm_tlgr_user'

    tlgr_user_id = KColumn(String(10), primary_key = True, nullable = False)
    tlgr_user_nm = KColumn(String(50), nullable = True)
    rcv_tgt_yn = KColumn(String(1), nullable = False)
    send_cl_cd = KColumn(String(2), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    seq = KColumn(Integer, nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.tlgr_user_id =  kwargs.pop('tlgr_user_id')
        self.tlgr_user_nm =  kwargs.pop('tlgr_user_nm',None)
        self.rcv_tgt_yn =  kwargs.pop('rcv_tgt_yn')
        self.send_cl_cd =  kwargs.pop('send_cl_cd','M')
        self.seq =  kwargs.pop('seq','100')

    def __repr__(self):
        return "<TlgrUser('%s', '%s', '%s', '%s', '%s'" % (str(self.tlgr_user_id), str(self.tlgr_user_nm), str(self.rcv_tgt_yn), str(self.send_cl_cd), str(self.seq) + KTable.__repr__(self))

