from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *
from DAO.KRED import *

class BbLv1Regn(Base,KTable):
    __tablename__ = 'kmig_bb_lv1_regn'

    bb_lv1_regn_cd = KColumn(String(50), primary_key = True, nullable = False)
    bb_lv1_regn_nm = KColumn(String(50), nullable = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.bb_lv1_regn_cd =  kwargs.pop('bb_lv1_regn_cd')
        self.bb_lv1_regn_nm =  kwargs.pop('bb_lv1_regn_nm',None)

    def __repr__(self):
        return "<BbLv1Regn('%s', '%s'" % (str(self.bb_lv1_regn_cd), str(self.bb_lv1_regn_nm) + KTable.__repr__(self))

class BbLv2Regn(Base, KTable):
    __tablename__ = 'kmig_bb_lv2_regn'

    bb_lv1_regn_cd = KColumn(String(50), primary_key=True, nullable=False)
    bb_lv2_regn_cd = KColumn(String(50), primary_key=True, nullable=False)
    bb_lv2_regn_nm = KColumn(String(50), nullable=True)
    bb_lv1_regn_nm = KColumn(String(50), nullable=True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.bb_lv1_regn_cd = kwargs.pop('bb_lv1_regn_cd')
        self.bb_lv2_regn_cd = kwargs.pop('bb_lv2_regn_cd')
        self.bb_lv2_regn_nm = kwargs.pop('bb_lv2_regn_nm', None)
        self.bb_lv1_regn_nm = kwargs.pop('bb_lv1_regn_nm', None)

    def __repr__(self):
        return "<BbLv2Regn('%s', '%s', '%s', '%s'" % (
        str(self.bb_lv1_regn_cd), str(self.bb_lv2_regn_cd), str(self.bb_lv2_regn_nm),
        str(self.bb_lv1_regn_nm) + KTable.__repr__(self))

class BbLv3Regn(Base,KTable):
    __tablename__ = 'kmig_bb_lv3_regn'

    bb_lv1_regn_cd = KColumn(String(50), primary_key = True, nullable = False)
    bb_lv2_regn_cd = KColumn(String(50), primary_key = True, nullable = False)
    bb_lv3_regn_cd = KColumn(String(50), primary_key = True, nullable = False)
    bb_lv3_regn_nm = KColumn(String(50), nullable = True)
    bb_lv1_regn_nm = KColumn(String(50), nullable = True)
    bb_lv2_regn_nm = KColumn(String(50), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.bb_lv1_regn_cd =  kwargs.pop('bb_lv1_regn_cd')
        self.bb_lv2_regn_cd =  kwargs.pop('bb_lv2_regn_cd')
        self.bb_lv3_regn_cd =  kwargs.pop('bb_lv3_regn_cd')
        self.bb_lv3_regn_nm =  kwargs.pop('bb_lv3_regn_nm',None)
        self.bb_lv1_regn_nm =  kwargs.pop('bb_lv1_regn_nm',None)
        self.bb_lv2_regn_nm =  kwargs.pop('bb_lv2_regn_nm',None)

    def __repr__(self):
        return "<BbLv3Regn('%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.bb_lv1_regn_cd), str(self.bb_lv2_regn_cd), str(self.bb_lv3_regn_cd), str(self.bb_lv3_regn_nm), str(self.bb_lv1_regn_nm), str(self.bb_lv2_regn_nm) + KTable.__repr__(self))

class BbCmpx(Base,KTable):
    __tablename__ = 'kmig_bb_cmpx'

    bb_cmpx_id = KColumn(String(8), primary_key = True, nullable = False)
    bb_cmpx_nm = KColumn(String(100), nullable = True)
    tot_hshl_cnt = KColumn(Integer, nullable = True)
    cmpl_yymm = KColumn(String(6), nullable = True)
    bld_co_nm = KColumn(String(200), nullable = True)
    tot_dong_flr_nm = KColumn(String(200), nullable = True)
    tot_park_cnt = KColumn(Integer, nullable = True)
    heat_way = KColumn(String(1000), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.bb_cmpx_id =  kwargs.pop('bb_cmpx_id')
        self.bb_cmpx_nm =  kwargs.pop('bb_cmpx_nm',None)
        self.tot_hshl_cnt =  kwargs.pop('tot_hshl_cnt',None)
        self.cmpl_yymm =  kwargs.pop('cmpl_yymm',None)
        self.bld_co_nm =  kwargs.pop('bld_co_nm',None)
        self.tot_dong_flr_nm =  kwargs.pop('tot_dong_flr_nm',None)
        self.tot_park_cnt =  kwargs.pop('tot_park_cnt',None)
        self.heat_way =  kwargs.pop('heat_way',None)

    def __repr__(self):
        return "<BbCmpx('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.bb_cmpx_id), str(self.bb_cmpx_nm), str(self.tot_hshl_cnt), str(self.cmpl_yymm), str(self.bld_co_nm), str(self.tot_dong_flr_nm), str(self.tot_park_cnt), str(self.heat_way) + KTable.__repr__(self))

class BbRegnCmpxRel(Base, KTable):
    __tablename__ = 'kmig_bb_regn_cmpx_rel'

    bb_lv1_regn_cd = KColumn(String(50), primary_key=True, nullable=False)
    bb_lv2_regn_cd = KColumn(String(50), primary_key=True, nullable=False)
    bb_lv3_regn_cd = KColumn(String(50), primary_key=True, nullable=False)
    bb_cmpx_id = KColumn(String(8), primary_key=True, nullable=False)

    bblv3regn = relationship('BbLv3Regn', primaryjoin=and_(bb_lv1_regn_cd == BbLv3Regn.bb_lv1_regn_cd,
                                                           bb_lv2_regn_cd == BbLv3Regn.bb_lv2_regn_cd,
                                                           bb_lv3_regn_cd == BbLv3Regn.bb_lv3_regn_cd),
                             foreign_keys=[BbLv3Regn.bb_lv1_regn_cd, BbLv3Regn.bb_lv2_regn_cd,
                                           BbLv3Regn.bb_lv3_regn_cd], passive_deletes=True)
    bbcmpx = relationship('BbCmpx', primaryjoin=bb_cmpx_id == BbCmpx.bb_cmpx_id, foreign_keys=[BbCmpx.bb_cmpx_id],
                          passive_deletes=True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.bb_lv1_regn_cd = kwargs.pop('bb_lv1_regn_cd')
        self.bb_lv2_regn_cd = kwargs.pop('bb_lv2_regn_cd')
        self.bb_lv3_regn_cd = kwargs.pop('bb_lv3_regn_cd')
        self.bb_cmpx_id = kwargs.pop('bb_cmpx_id')

    def __repr__(self):
        return "<BbRegnCmpxRel('%s', '%s', '%s', '%s'" % (
        str(self.bb_lv1_regn_cd), str(self.bb_lv2_regn_cd), str(self.bb_lv3_regn_cd),
        str(self.bb_cmpx_id) + KTable.__repr__(self))

class BbCmpxTyp(Base,KTable):
    __tablename__ = 'kmig_bb_cmpx_typ'

    bb_cmpx_id = KColumn(String(8), primary_key = True, nullable = False)
    bb_cmpx_typ_seq = KColumn(Integer, primary_key = True, nullable = False)
    cmpx_typ_nm = KColumn(String(200), nullable = True)
    sply_area = KColumn(String(50), nullable = True)

    bbcmpx = relationship('BbCmpx',primaryjoin = bb_cmpx_id==BbCmpx.bb_cmpx_id, foreign_keys = [BbCmpx.bb_cmpx_id], passive_deletes = True, overlaps="bbcmpx")

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.bb_cmpx_id =  kwargs.pop('bb_cmpx_id')
        self.bb_cmpx_typ_seq =  kwargs.pop('bb_cmpx_typ_seq')
        self.cmpx_typ_nm =  kwargs.pop('cmpx_typ_nm',None)
        self.sply_area =  kwargs.pop('sply_area',None)

    def __repr__(self):
        return "<BbCmpxTyp('%s', '%s', '%s', '%s'" % (str(self.bb_cmpx_id), str(self.bb_cmpx_typ_seq), str(self.cmpx_typ_nm), str(self.sply_area) + KTable.__repr__(self))

class BbCmpxTypMonPrc(Base,KTable):
    __tablename__ = 'kmig_bb_cmpx_typ_mon_prc'

    bb_cmpx_id = KColumn(String(8), primary_key = True, nullable = False)
    bb_cmpx_typ_seq = KColumn(Integer, primary_key = True, nullable = False)
    std_yymm = KColumn(String(6), primary_key = True, nullable = False)
    std_ymd = KColumn(String(8), nullable = True)
    down_prc = KColumn(Integer, nullable = True)
    up_prc = KColumn(Integer, nullable = True)
    chg_prc = KColumn(Integer, nullable = True)
    down_js_prc = KColumn(Integer, nullable = True)
    up_js_prc = KColumn(Integer, nullable = True)
    chg_js_prc = KColumn(Integer, nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.bb_cmpx_id =  kwargs.pop('bb_cmpx_id')
        self.bb_cmpx_typ_seq =  kwargs.pop('bb_cmpx_typ_seq')
        self.std_yymm =  kwargs.pop('std_yymm')
        self.std_ymd =  kwargs.pop('std_ymd',None)
        self.down_prc =  kwargs.pop('down_prc',None)
        self.up_prc =  kwargs.pop('up_prc',None)
        self.chg_prc =  kwargs.pop('chg_prc',None)
        self.down_js_prc =  kwargs.pop('down_js_prc',None)
        self.up_js_prc =  kwargs.pop('up_js_prc',None)
        self.chg_js_prc =  kwargs.pop('chg_js_prc',None)

    def __repr__(self):
        return "<BbCmpxTypMonPrc('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.bb_cmpx_id), str(self.bb_cmpx_typ_seq), str(self.std_yymm), str(self.std_ymd), str(self.down_prc), str(self.up_prc), str(self.chg_prc), str(self.down_js_prc), str(self.up_js_prc), str(self.chg_js_prc) + KTable.__repr__(self))

class DealDtl(Base,KTable):
    """
        customized Table Class
    """
    __tablename__ = 'kmig_deal_dtl'

    job_id = KColumn(String(20), nullable = False)
    exec_dtm = KColumn(DATE, nullable = False)
    gov_legl_dong_cd = KColumn(String(10), nullable = False)
    deal_yymm = KColumn(String(6), nullable = False)
    real_deal_seq = KColumn(Integer, primary_key = True, nullable = False, unique=True, autoincrement=True)
    real_deal_cmpx_knd = KColumn(String(20), nullable = True)
    deal_amt = KColumn(Integer, nullable = True)
    cmpl_yy = KColumn(String(4), nullable = True)
    deal_yy = KColumn(String(4), nullable = True)
    road_nm = KColumn(String(200), nullable = True)
    road_nm_cmpx_orgl_num_cd = KColumn(String(20), nullable = True)
    road_nm_cmpx_vice_num_cd = KColumn(String(20), nullable = True)
    road_nm_sgg_cd = KColumn(String(20), nullable = True)
    road_nm_seq_cd = KColumn(Integer, nullable = True)
    road_nm_ong_ung_cd = KColumn(String(20), nullable = True)
    road_nm_cd = KColumn(String(20), nullable = True)
    legl_dong_nm = KColumn(String(200), nullable = True)
    legl_dong_orgl_num_cd = KColumn(String(20), nullable = True)
    legl_dong_vice_num_cd = KColumn(String(20), nullable = True)
    legl_dong_sgg_cd = KColumn(String(20), nullable = True)
    legl_dong_umd_cd = KColumn(String(20), nullable = True)
    legl_dong_hnum_cd = KColumn(String(20), nullable = True)
    real_deal_cmpx_nm = KColumn(String(100), nullable = True)
    deal_mm = KColumn(String(2), nullable = True)
    deal_ymd = KColumn(String(8), nullable = True)
    seq = KColumn(Integer, nullable = True)
    only_area = KColumn(FLOAT, nullable = True)
    agnt_whrb_addr = KColumn(String(255), nullable = True)
    regn_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    hnum = KColumn(String(10), nullable = True)
    flr = KColumn(String(200), nullable = True)
    rles_rsn_occr_dd = KColumn(String(8), nullable = True)
    rles_yn_val = KColumn(String(200), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id',None)
        self.exec_dtm =  kwargs.pop('exec_dtm',None)
        self.gov_legl_dong_cd =  kwargs.pop('gov_legl_dong_cd',None)
        self.deal_yymm =  kwargs.pop('deal_yymm',None)
        #self.real_deal_seq =  kwargs.pop('real_deal_seq')
        self.real_deal_cmpx_knd =  kwargs.pop('real_deal_cmpx_knd',None)
        self.deal_amt =  kwargs.pop('deal_amt',None)
        self.cmpl_yy =  kwargs.pop('cmpl_yy',None)
        self.deal_yy =  kwargs.pop('deal_yy',None)
        self.road_nm =  kwargs.pop('road_nm',None)
        self.road_nm_cmpx_orgl_num_cd =  kwargs.pop('road_nm_cmpx_orgl_num_cd',None)
        self.road_nm_cmpx_vice_num_cd =  kwargs.pop('road_nm_cmpx_vice_num_cd',None)
        self.road_nm_sgg_cd =  kwargs.pop('road_nm_sgg_cd',None)
        self.road_nm_seq_cd =  kwargs.pop('road_nm_seq_cd',None)
        self.road_nm_ong_ung_cd =  kwargs.pop('road_nm_ong_ung_cd',None)
        self.road_nm_cd =  kwargs.pop('road_nm_cd',None)
        self.legl_dong_nm =  kwargs.pop('legl_dong_nm',None)
        self.legl_dong_orgl_num_cd =  kwargs.pop('legl_dong_orgl_num_cd',None)
        self.legl_dong_vice_num_cd =  kwargs.pop('legl_dong_vice_num_cd',None)
        self.legl_dong_sgg_cd =  kwargs.pop('legl_dong_sgg_cd',None)
        self.legl_dong_umd_cd =  kwargs.pop('legl_dong_umd_cd',None)
        self.legl_dong_hnum_cd =  kwargs.pop('legl_dong_hnum_cd',None)
        self.real_deal_cmpx_nm =  kwargs.pop('real_deal_cmpx_nm',None)
        self.deal_mm =  kwargs.pop('deal_mm',None)
        self.deal_ymd =  kwargs.pop('deal_ymd',None)
        self.seq =  kwargs.pop('seq',None)
        self.only_area =  kwargs.pop('only_area',None)
        self.agnt_whrb_addr =  kwargs.pop('agnt_whrb_addr',None)
        self.regn_cd =  kwargs.pop('regn_cd',None)
        self.hnum =  kwargs.pop('hnum',None)
        self.flr =  kwargs.pop('flr',None)
        self.rles_rsn_occr_dd =  kwargs.pop('rles_rsn_occr_dd',None)
        self.rles_yn_val =  kwargs.pop('rles_yn_val',None)

    def __repr__(self):
        return "<DealDtl('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.gov_legl_dong_cd), str(self.deal_yymm), str(self.real_deal_seq), str(self.real_deal_cmpx_knd), str(self.deal_amt), str(self.cmpl_yy), str(self.deal_yy), str(self.road_nm), str(self.road_nm_cmpx_orgl_num_cd), str(self.road_nm_cmpx_vice_num_cd), str(self.road_nm_sgg_cd), str(self.road_nm_seq_cd), str(self.road_nm_ong_ung_cd), str(self.road_nm_cd), str(self.legl_dong_nm), str(self.legl_dong_orgl_num_cd), str(self.legl_dong_vice_num_cd), str(self.legl_dong_sgg_cd), str(self.legl_dong_umd_cd), str(self.legl_dong_hnum_cd), str(self.real_deal_cmpx_nm), str(self.deal_mm), str(self.deal_ymd), str(self.seq), str(self.only_area), str(self.agnt_whrb_addr), str(self.regn_cd), str(self.hnum), str(self.flr), str(self.rles_rsn_occr_dd), str(self.rles_yn_val) + KTable.__repr__(self))

class MigVlaDeal(Base,KTable):
    __tablename__ = 'kmig_vla_deal'

    job_id = KColumn(String(20), nullable = False)
    exec_dtm = KColumn(String(14), nullable = False)
    gov_legl_dong_cd = KColumn(String(10), nullable = False)
    deal_yymm = KColumn(String(6), nullable = False)
    vla_real_deal_seq = KColumn(INTEGER, primary_key = True, nullable = False, unique=True, autoincrement=True)
    deal_amt_val = KColumn(String(200), nullable = True)
    cmpl_yy = KColumn(String(4), nullable = True)
    yy = KColumn(String(4), nullable = True)
    rola_area_val = KColumn(String(200), nullable = True)
    legl_dong_nm = KColumn(String(200), nullable = True)
    vla_val = KColumn(String(200), nullable = True)
    mm = KColumn(String(2), nullable = True)
    ymd = KColumn(String(8), nullable = True)
    only_area = KColumn(FLOAT, nullable = True)
    hnum = KColumn(String(100), nullable = True)
    regn_cd = KColumn(String(20), nullable = True)
    flr = KColumn(String(200), nullable = True)
    rles_yn = KColumn(String(1), nullable = True)
    rles_rsn_occr_ymd = KColumn(String(8), nullable = True)
    deal_typ = KColumn(String(200), nullable = True)
    agnt_addr = KColumn(String(255), nullable = True)

    legldong = relationship('LeglDong',primaryjoin = gov_legl_dong_cd==LeglDong.legl_dong_cd, foreign_keys = [LeglDong.legl_dong_cd], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.gov_legl_dong_cd =  kwargs.pop('gov_legl_dong_cd')
        self.deal_yymm =  kwargs.pop('deal_yymm')
#        self.vla_real_deal_seq =  kwargs.pop('vla_real_deal_seq')
        self.deal_amt_val =  kwargs.pop('deal_amt_val',None)
        self.cmpl_yy =  kwargs.pop('cmpl_yy',None)
        self.yy =  kwargs.pop('yy',None)
        self.rola_area_val =  kwargs.pop('rola_area_val',None)
        self.legl_dong_nm =  kwargs.pop('legl_dong_nm',None)
        self.vla_val =  kwargs.pop('vla_val',None)
        self.mm =  kwargs.pop('mm',None)
        self.ymd =  kwargs.pop('ymd',None)
        self.only_area =  kwargs.pop('only_area',None)
        self.hnum =  kwargs.pop('hnum',None)
        self.regn_cd =  kwargs.pop('regn_cd',None)
        self.flr =  kwargs.pop('flr',None)
        self.rles_yn =  kwargs.pop('rles_yn',None)
        self.rles_rsn_occr_ymd =  kwargs.pop('rles_rsn_occr_ymd',None)
        self.deal_typ =  kwargs.pop('deal_typ',None)
        self.agnt_addr =  kwargs.pop('agnt_addr',None)

    def __repr__(self):
        return "<MigVlaDeal('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.gov_legl_dong_cd), str(self.deal_yymm), str(self.vla_real_deal_seq), str(self.deal_amt_val), str(self.cmpl_yy), str(self.yy), str(self.rola_area_val), str(self.legl_dong_nm), str(self.vla_val), str(self.mm), str(self.ymd), str(self.only_area), str(self.hnum), str(self.regn_cd), str(self.flr), str(self.rles_yn), str(self.rles_rsn_occr_ymd), str(self.deal_typ), str(self.agnt_addr) + KTable.__repr__(self))


class MigNvCmpx(Base,KTable):
    __tablename__ = 'kmig_nv_cmpx'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_dtm = KColumn(String(14), primary_key = True, nullable = False)
    nv_cmpx_id = KColumn(String(6), primary_key = True, nullable = False)
    nv_cmpx_nm = KColumn(String(100), nullable = True)
    gov_legl_dong_cd = KColumn(String(10), nullable = True)
    nv_cmpx_knd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'NV_CMPX_KND')
    bas_addr = KColumn(String(255), nullable = True)
    dtl_addr = KColumn(String(255), nullable = True)
    road_nm_bas_addr = KColumn(String(255), nullable = True)
    road_nm_dtl_addr = KColumn(String(255), nullable = True)
    addr = KColumn(String(255), nullable = True)
    x_coor_val = KColumn(FLOAT, nullable = True)
    y_coor_val = KColumn(FLOAT, nullable = True)
    tot_hshl_cnt = KColumn(Integer, nullable = True)
    tot_rent_hshl_cnt = KColumn(Integer, nullable = True)
    tot_dong_cnt = KColumn(Integer, nullable = True)
    max_flr = KColumn(Integer, nullable = True)
    min_flr = KColumn(Integer, nullable = True)
    cmpl_yymm = KColumn(String(6), nullable = True)
    sale_cnt = KColumn(Integer, nullable = True)
    js_cnt = KColumn(Integer, nullable = True)
    ws_cnt = KColumn(Integer, nullable = True)
    shrt_rent_cnt = KColumn(Integer, nullable = True)
    bld_co_nm = KColumn(String(200), nullable = True)
    tot_park_cnt = KColumn(Integer, nullable = True)
    hshl_per_park_cnt = KColumn(Integer, nullable = True)
    heat_way = KColumn(String(1000), nullable = True)
    heat_fuel = KColumn(String(1000), nullable = True)
    far = KColumn(String(1000), nullable = True)
    btlr = KColumn(String(1000), nullable = True)
    mbig_sply_area = KColumn(Float, nullable = True)
    msml_sply_area = KColumn(Float, nullable = True)
    cmpx_reg_val = KColumn(String(200), nullable = True)
    area_lst = KColumn(String(1000), nullable = True)
    mgmt_co_tel = KColumn(String(30), nullable = True)
    sbwy_info = KColumn(String(1000), nullable = True)
    wasp_pipe_rplc = KColumn(String(200), nullable = True)
    whl_dong_cnt = KColumn(Integer, nullable = True)
    bmak_yn = KColumn(String(1), nullable = True)
    mig_rsn = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = 'MIG_RSN')

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.nv_cmpx_id =  kwargs.pop('nv_cmpx_id')
        self.nv_cmpx_nm =  kwargs.pop('nv_cmpx_nm',None)
        self.gov_legl_dong_cd =  kwargs.pop('gov_legl_dong_cd',None)
        self.nv_cmpx_knd =  kwargs.pop('nv_cmpx_knd',None)
        self.bas_addr =  kwargs.pop('bas_addr',None)
        self.dtl_addr =  kwargs.pop('dtl_addr',None)
        self.road_nm_bas_addr =  kwargs.pop('road_nm_bas_addr',None)
        self.road_nm_dtl_addr =  kwargs.pop('road_nm_dtl_addr',None)
        self.addr =  kwargs.pop('addr',None)
        self.x_coor_val =  kwargs.pop('x_coor_val',None)
        self.y_coor_val =  kwargs.pop('y_coor_val',None)
        self.tot_hshl_cnt =  kwargs.pop('tot_hshl_cnt',None)
        self.tot_rent_hshl_cnt =  kwargs.pop('tot_rent_hshl_cnt',None)
        self.tot_dong_cnt =  kwargs.pop('tot_dong_cnt',None)
        self.max_flr =  kwargs.pop('max_flr',None)
        self.min_flr =  kwargs.pop('min_flr',None)
        self.cmpl_yymm =  kwargs.pop('cmpl_yymm',None)
        self.sale_cnt =  kwargs.pop('sale_cnt',None)
        self.js_cnt =  kwargs.pop('js_cnt',None)
        self.ws_cnt =  kwargs.pop('ws_cnt',None)
        self.shrt_rent_cnt =  kwargs.pop('shrt_rent_cnt',None)
        self.bld_co_nm =  kwargs.pop('bld_co_nm',None)
        self.tot_park_cnt =  kwargs.pop('tot_park_cnt',None)
        self.hshl_per_park_cnt =  kwargs.pop('hshl_per_park_cnt',None)
        self.heat_way =  kwargs.pop('heat_way',None)
        self.heat_fuel =  kwargs.pop('heat_fuel',None)
        self.far =  kwargs.pop('far',None)
        self.btlr =  kwargs.pop('btlr',None)
        self.mbig_sply_area =  kwargs.pop('mbig_sply_area',None)
        self.msml_sply_area =  kwargs.pop('msml_sply_area',None)
        self.cmpx_reg_val =  kwargs.pop('cmpx_reg_val',None)
        self.area_lst =  kwargs.pop('area_lst',None)
        self.mgmt_co_tel =  kwargs.pop('mgmt_co_tel',None)
        self.sbwy_info =  kwargs.pop('sbwy_info',None)
        self.wasp_pipe_rplc =  kwargs.pop('wasp_pipe_rplc',None)
        self.whl_dong_cnt =  kwargs.pop('whl_dong_cnt',None)
        self.bmak_yn =  kwargs.pop('bmak_yn',None)
        self.mig_rsn =  kwargs.pop('mig_rsn',None)

    def __repr__(self):
        return "<MigNvCmpx('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.nv_cmpx_id), str(self.nv_cmpx_nm), str(self.gov_legl_dong_cd), str(self.nv_cmpx_knd), str(self.bas_addr), str(self.dtl_addr), str(self.road_nm_bas_addr), str(self.road_nm_dtl_addr), str(self.addr), str(self.x_coor_val), str(self.y_coor_val), str(self.tot_hshl_cnt), str(self.tot_rent_hshl_cnt), str(self.tot_dong_cnt), str(self.max_flr), str(self.min_flr), str(self.cmpl_yymm), str(self.sale_cnt), str(self.js_cnt), str(self.ws_cnt), str(self.shrt_rent_cnt), str(self.bld_co_nm), str(self.tot_park_cnt), str(self.hshl_per_park_cnt), str(self.heat_way), str(self.heat_fuel), str(self.far), str(self.btlr), str(self.mbig_sply_area), str(self.msml_sply_area), str(self.cmpx_reg_val), str(self.area_lst), str(self.mgmt_co_tel), str(self.sbwy_info), str(self.wasp_pipe_rplc), str(self.whl_dong_cnt), str(self.bmak_yn), str(self.mig_rsn) + KTable.__repr__(self))

class MigNvCmpxTyp(Base,KTable):
    __tablename__ = 'kmig_nv_cmpx_typ'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_dtm = KColumn(String(14), primary_key = True, nullable = False)
    nv_cmpx_id = KColumn(String(6), primary_key = True, nullable = False)
    nv_cmpx_typ_seq = KColumn(Integer, primary_key = True, nullable = False)
    cmpx_typ_nm = KColumn(String(200), nullable = True)
    sply_area = KColumn(FLOAT, nullable = True)
    only_area = KColumn(FLOAT, nullable = True)
    only_pyng_nm = KColumn(String(200), nullable = True)
    cmpx_typ_pyng_nm = KColumn(String(200), nullable = True)
    gpln_cors = KColumn(String(1000), nullable = True)
    door_strc = KColumn(String(200), nullable = True)
    room_cnt_str = KColumn(String(200), nullable = True)
    bath_cnt_str = KColumn(String(200), nullable = True)
    soh_hshl_cnt = KColumn(Integer, nullable = True)
    sply_area_num = KColumn(Float, nullable = True)
    only_area_num = KColumn(Float, nullable = True)
    ret_typ_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    avg_mntn_amt = KColumn(Integer, nullable = True)
    smmr_mntn_amt = KColumn(Integer, nullable = True)
    wntr_mntn_amt = KColumn(Integer, nullable = True)
    deal_lmit_ymd = KColumn(String(8), nullable = True)
    deal_psbl_ymd = KColumn(String(8), nullable = True)
    dcnt_prc_str = KColumn(String(200), nullable = True)

    nvcmpx = relationship('MigNvCmpx',primaryjoin = and_(job_id==MigNvCmpx.job_id , exec_dtm==MigNvCmpx.exec_dtm , nv_cmpx_id==MigNvCmpx.nv_cmpx_id), foreign_keys = [MigNvCmpx.job_id ,MigNvCmpx.exec_dtm , MigNvCmpx.nv_cmpx_id], passive_deletes = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.nv_cmpx_id =  kwargs.pop('nv_cmpx_id')
        self.nv_cmpx_typ_seq =  kwargs.pop('nv_cmpx_typ_seq')
        self.cmpx_typ_nm =  kwargs.pop('cmpx_typ_nm',None)
        self.sply_area =  kwargs.pop('sply_area',None)
        self.only_area =  kwargs.pop('only_area',None)
        self.only_pyng_nm =  kwargs.pop('only_pyng_nm',None)
        self.cmpx_typ_pyng_nm =  kwargs.pop('cmpx_typ_pyng_nm',None)
        self.gpln_cors =  kwargs.pop('gpln_cors',None)
        self.door_strc =  kwargs.pop('door_strc',None)
        self.room_cnt_str =  kwargs.pop('room_cnt_str',None)
        self.bath_cnt_str =  kwargs.pop('bath_cnt_str',None)
        self.soh_hshl_cnt =  kwargs.pop('soh_hshl_cnt',None)
        self.sply_area_num =  kwargs.pop('sply_area_num',None)
        self.only_area_num =  kwargs.pop('only_area_num',None)
        self.ret_typ_cd =  kwargs.pop('ret_typ_cd',None)
        self.avg_mntn_amt =  kwargs.pop('avg_mntn_amt',None)
        self.smmr_mntn_amt =  kwargs.pop('smmr_mntn_amt',None)
        self.wntr_mntn_amt =  kwargs.pop('wntr_mntn_amt',None)
        self.deal_lmit_ymd =  kwargs.pop('deal_lmit_ymd',None)
        self.deal_psbl_ymd =  kwargs.pop('deal_psbl_ymd',None)
        self.dcnt_prc_str =  kwargs.pop('dcnt_prc_str',None)

    def __repr__(self):
        return "<MigNvCmpxTyp('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.nv_cmpx_id), str(self.nv_cmpx_typ_seq), str(self.cmpx_typ_nm), str(self.sply_area), str(self.only_area), str(self.only_pyng_nm), str(self.cmpx_typ_pyng_nm), str(self.gpln_cors), str(self.door_strc), str(self.room_cnt_str), str(self.bath_cnt_str), str(self.soh_hshl_cnt), str(self.sply_area_num), str(self.only_area_num), str(self.ret_typ_cd), str(self.avg_mntn_amt), str(self.smmr_mntn_amt), str(self.wntr_mntn_amt), str(self.deal_lmit_ymd), str(self.deal_psbl_ymd), str(self.dcnt_prc_str) + KTable.__repr__(self))

class OlvRoadNm(Base,KTable):
    __tablename__ = 'kmig_olv_road_nm'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_dtm = KColumn(String(14), primary_key = True, nullable = False)
    gov_legl_dong_cd = KColumn(String(10), nullable = False)
    road_nm_cd = KColumn(String(20), primary_key = True, nullable = False)
    road_nm = KColumn(String(200), nullable = True)
    munt_parm_val = KColumn(String(200), nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.gov_legl_dong_cd =  kwargs.pop('gov_legl_dong_cd')
        self.road_nm_cd =  kwargs.pop('road_nm_cd')
        self.road_nm =  kwargs.pop('road_nm',None)
        self.munt_parm_val =  kwargs.pop('munt_parm_val',None)

    def __repr__(self):
        return "<OlvRoadNm('%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.gov_legl_dong_cd), str(self.road_nm_cd), str(self.road_nm), str(self.munt_parm_val) + KTable.__repr__(self))

class OlvApt(Base,KTable):
    __tablename__ = 'kmig_olv_apt'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_dtm = KColumn(String(14), primary_key = True, nullable = False)
    road_nm_cd = KColumn(String(20), nullable = False)
    apt_cd = KColumn(String(20), primary_key = True, nullable = False)
    apt_nm = KColumn(String(200), nullable = True)
    hnum = KColumn(String(100), nullable = True)
    noti_dd = KColumn(String(8), nullable = True)
    x_coor_val = KColumn(FLOAT, nullable = True)
    y_coor_val = KColumn(FLOAT, nullable = True)


    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.road_nm_cd =  kwargs.pop('road_nm_cd')
        self.apt_cd =  kwargs.pop('apt_cd')
        self.apt_nm =  kwargs.pop('apt_nm',None)
        self.hnum =  kwargs.pop('hnum',None)
        self.noti_dd =  kwargs.pop('noti_dd',None)
        self.x_coor_val =  kwargs.pop('x_coor_val',None)
        self.y_coor_val =  kwargs.pop('y_coor_val',None)

    def __repr__(self):
        return "<OlvApt('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.road_nm_cd), str(self.apt_cd), str(self.apt_nm), str(self.hnum), str(self.noti_dd), str(self.x_coor_val), str(self.y_coor_val) + KTable.__repr__(self))

class MigNvCmpxAtcl(Base,KTable):
    __tablename__ = 'kmig_nv_cmpx_atcl'

    job_id = KColumn(String(20), primary_key = True, nullable = False)
    exec_dtm = KColumn(String(14), primary_key = True, nullable = False)
    atcl_num = KColumn(Integer, primary_key = True, nullable = False)
    nv_cmpx_id = KColumn(String(6), nullable = False)
    nv_cmpx_typ_seq = KColumn(Integer, nullable = False)
    gov_legl_dong_cd = KColumn(String(10), nullable = True)
    atcl_nm = KColumn(String(200), nullable = True)
    nv_cmpx_nm = KColumn(String(100), nullable = True)
    nv_cmpx_knd = KColumn(String(20), nullable = True)
    nv_cmpx_knd_nm = KColumn(String(200), nullable = True)
    cmpx_typ_nm = KColumn(String(200), nullable = True)
    nv_atcl_cmpx_typ_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    nv_atcl_cmpx_typ_nm = KColumn(String(200), nullable = True)
    nv_atcl_up_cmpx_typ_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    sply_area_str = KColumn(String(200), nullable = True)
    only_area_str = KColumn(String(200), nullable = True)
    nv_atcl_stat_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    nv_atcl_stat_nm = KColumn(String(200), nullable = True)
    deal_cmpl_yn = KColumn(String(1), nullable = True)
    nv_deal_typ_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    nv_deal_typ_nm = KColumn(String(200), nullable = True)
    nv_vrfy_typ_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    flr_info = KColumn(String(1000), nullable = True)
    prc_chg_stat_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    prc_chg_yn = KColumn(String(1), nullable = True)
    deal_prc_nm = KColumn(String(200), nullable = True)
    prc_info = KColumn(String(1000), nullable = True)
    deal_prc_info = KColumn(String(1000), nullable = True)
    prmu_prc_nm = KColumn(String(200), nullable = True)
    same_addr_prmu_mbig_prc_nm = KColumn(String(200), nullable = True)
    same_addr_prmu_msml_prc_nm = KColumn(String(200), nullable = True)
    rent_prc_nm = KColumn(String(200), nullable = True)
    deal_prc_num = KColumn(String(50), nullable = True)
    deal_han_prc_nm = KColumn(String(200), nullable = True)
    rent_prc_num = KColumn(String(50), nullable = True)
    deal_rent_prc_nm = KColumn(String(200), nullable = True)
    own_user_deal_chk_yn = KColumn(String(1), nullable = True)
    exps_nm = KColumn(String(200), nullable = True)
    atcl_chk_ymd = KColumn(String(8), nullable = True)
    deal_cmpl_ymd = KColumn(String(8), nullable = True)
    atcl_desc = KColumn(String(500), nullable = True)
    dong_nm = KColumn(String(200), nullable = True)
    same_addr_cnt = KColumn(Integer, nullable = True)
    same_addr_drct_cnt = KColumn(Integer, nullable = True)
    same_addr_mbig_prc_nm = KColumn(String(200), nullable = True)
    same_addr_mbig_scnd_prc_nm = KColumn(String(200), nullable = True)
    same_addr_msml_prc_nm = KColumn(String(200), nullable = True)
    same_addr_msml_scnd_prc_nm = KColumn(String(200), nullable = True)
    same_addr_hash_val = KColumn(String(200), nullable = True)
    msml_mvi_fee_val = KColumn(String(200), nullable = True)
    mbig_mvi_fee_val = KColumn(String(200), nullable = True)
    sbwy_info = KColumn(String(1000), nullable = True)
    svc_desc = KColumn(String(500), nullable = True)
    cl_nm = KColumn(String(200), nullable = True)
    et_room_cnt = KColumn(String(50), nullable = True)
    prvd_co_id = KColumn(String(50), nullable = True)
    prvd_co_nm = KColumn(String(200), nullable = True)
    prvd_co_cnt = KColumn(Integer, nullable = True)
    prvd_atcl_addr = KColumn(String(255), nullable = True)
    prvd_atcl_link_url = KColumn(String(1000), nullable = True)
    prvd_atcl_link_titl_use_yn = KColumn(String(1), nullable = True)
    prvd_atcl_link_use_prvd_co_nm_yn = KColumn(String(1), nullable = True)
    prvd_mbl_atcl_url = KColumn(String(1000), nullable = True)
    prvd_mbl_link_titl_use_yn = KColumn(String(1), nullable = True)
    prvd_mbl_link_prvd_co_nm_use_yn = KColumn(String(1), nullable = True)
    prvd_co_vo_str = KColumn(String(1000), nullable = True)
    x_coor_val = KColumn(Float, nullable = True)
    y_coor_val = KColumn(Float, nullable = True)
    loc_mark_yn = KColumn(String(1), nullable = True)
    lrea_nm = KColumn(String(200), nullable = True)
    lrea_id = KColumn(String(50), nullable = True)
    drct_deal_yn = KColumn(String(1), nullable = True)
    sell_user_cell_num = KColumn(String(12), nullable = True)
    dtl_addr = KColumn(String(255), nullable = True)
    dtl_addr_yn = KColumn(String(1), nullable = True)
    owner_chk_yn = KColumn(String(1), nullable = True)
    rpsn_img_url = KColumn(String(1000), nullable = True)
    rpsn_img_typ_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    rpsn_img_thmb_nm = KColumn(String(200), nullable = True)
    img_cnt = KColumn(Integer, nullable = True)
    sell_user_nm = KColumn(String(200), nullable = True)
    tag_lst_str = KColumn(String(200), nullable = True)
    mi_nm = KColumn(String(200), nullable = True)
    real_deal_yymm = KColumn(String(6), nullable = True)
    real_deal_ymd_clct_cd = KColumn(String(20), nullable = True, kcom_cd_domain = True, kcom_cd_grp = '')
    real_deal_ymd_clct_nm = KColumn(String(200), nullable = True)
    real_deal_prc_nm = KColumn(String(200), nullable = True)
    real_deal_dpst_nm = KColumn(String(200), nullable = True)
    real_deal_rent_prc_nm = KColumn(String(200), nullable = True)

    mignvcmpxtyp = relationship('MigNvCmpxTyp',primaryjoin = and_(job_id==MigNvCmpxTyp.job_id , exec_dtm==MigNvCmpxTyp.exec_dtm , nv_cmpx_id==MigNvCmpxTyp.nv_cmpx_id , nv_cmpx_typ_seq==MigNvCmpxTyp.nv_cmpx_typ_seq), foreign_keys = [MigNvCmpxTyp.job_id , MigNvCmpxTyp.exec_dtm , MigNvCmpxTyp.nv_cmpx_id , MigNvCmpxTyp.nv_cmpx_typ_seq], passive_deletes = True)

    def __init__(self, *args, **kwargs):
        KTable.__init__(self)
        self.job_id =  kwargs.pop('job_id')
        self.exec_dtm =  kwargs.pop('exec_dtm')
        self.atcl_num =  kwargs.pop('atcl_num')
        self.nv_cmpx_id =  kwargs.pop('nv_cmpx_id')
        self.nv_cmpx_typ_seq =  kwargs.pop('nv_cmpx_typ_seq')
        self.gov_legl_dong_cd =  kwargs.pop('gov_legl_dong_cd',None)
        self.atcl_nm =  kwargs.pop('atcl_nm',None)
        self.nv_cmpx_nm =  kwargs.pop('nv_cmpx_nm',None)
        self.nv_cmpx_knd =  kwargs.pop('nv_cmpx_knd',None)
        self.nv_cmpx_knd_nm =  kwargs.pop('nv_cmpx_knd_nm',None)
        self.cmpx_typ_nm =  kwargs.pop('cmpx_typ_nm',None)
        self.nv_atcl_cmpx_typ_cd =  kwargs.pop('nv_atcl_cmpx_typ_cd',None)
        self.nv_atcl_cmpx_typ_nm =  kwargs.pop('nv_atcl_cmpx_typ_nm',None)
        self.nv_atcl_up_cmpx_typ_cd =  kwargs.pop('nv_atcl_up_cmpx_typ_cd',None)
        self.sply_area_str =  kwargs.pop('sply_area_str',None)
        self.only_area_str =  kwargs.pop('only_area_str',None)
        self.nv_atcl_stat_cd =  kwargs.pop('nv_atcl_stat_cd',None)
        self.nv_atcl_stat_nm =  kwargs.pop('nv_atcl_stat_nm',None)
        self.deal_cmpl_yn =  kwargs.pop('deal_cmpl_yn',None)
        self.nv_deal_typ_cd =  kwargs.pop('nv_deal_typ_cd',None)
        self.nv_deal_typ_nm =  kwargs.pop('nv_deal_typ_nm',None)
        self.nv_vrfy_typ_cd =  kwargs.pop('nv_vrfy_typ_cd',None)
        self.flr_info =  kwargs.pop('flr_info',None)
        self.prc_chg_stat_cd =  kwargs.pop('prc_chg_stat_cd',None)
        self.prc_chg_yn =  kwargs.pop('prc_chg_yn',None)
        self.deal_prc_nm =  kwargs.pop('deal_prc_nm',None)
        self.prc_info =  kwargs.pop('prc_info',None)
        self.deal_prc_info =  kwargs.pop('deal_prc_info',None)
        self.prmu_prc_nm =  kwargs.pop('prmu_prc_nm',None)
        self.same_addr_prmu_mbig_prc_nm =  kwargs.pop('same_addr_prmu_mbig_prc_nm',None)
        self.same_addr_prmu_msml_prc_nm =  kwargs.pop('same_addr_prmu_msml_prc_nm',None)
        self.rent_prc_nm =  kwargs.pop('rent_prc_nm',None)
        self.deal_prc_num =  kwargs.pop('deal_prc_num',None)
        self.deal_han_prc_nm =  kwargs.pop('deal_han_prc_nm',None)
        self.rent_prc_num =  kwargs.pop('rent_prc_num',None)
        self.deal_rent_prc_nm =  kwargs.pop('deal_rent_prc_nm',None)
        self.own_user_deal_chk_yn =  kwargs.pop('own_user_deal_chk_yn',None)
        self.exps_nm =  kwargs.pop('exps_nm',None)
        self.atcl_chk_ymd =  kwargs.pop('atcl_chk_ymd',None)
        self.deal_cmpl_ymd =  kwargs.pop('deal_cmpl_ymd',None)
        self.atcl_desc =  kwargs.pop('atcl_desc',None)
        self.dong_nm =  kwargs.pop('dong_nm',None)
        self.same_addr_cnt =  kwargs.pop('same_addr_cnt',None)
        self.same_addr_drct_cnt =  kwargs.pop('same_addr_drct_cnt',None)
        self.same_addr_mbig_prc_nm =  kwargs.pop('same_addr_mbig_prc_nm',None)
        self.same_addr_mbig_scnd_prc_nm =  kwargs.pop('same_addr_mbig_scnd_prc_nm',None)
        self.same_addr_msml_prc_nm =  kwargs.pop('same_addr_msml_prc_nm',None)
        self.same_addr_msml_scnd_prc_nm =  kwargs.pop('same_addr_msml_scnd_prc_nm',None)
        self.same_addr_hash_val =  kwargs.pop('same_addr_hash_val',None)
        self.msml_mvi_fee_val =  kwargs.pop('msml_mvi_fee_val',None)
        self.mbig_mvi_fee_val =  kwargs.pop('mbig_mvi_fee_val',None)
        self.sbwy_info =  kwargs.pop('sbwy_info',None)
        self.svc_desc =  kwargs.pop('svc_desc',None)
        self.cl_nm =  kwargs.pop('cl_nm',None)
        self.et_room_cnt =  kwargs.pop('et_room_cnt',None)
        self.prvd_co_id =  kwargs.pop('prvd_co_id',None)
        self.prvd_co_nm =  kwargs.pop('prvd_co_nm',None)
        self.prvd_co_cnt =  kwargs.pop('prvd_co_cnt',None)
        self.prvd_atcl_addr =  kwargs.pop('prvd_atcl_addr',None)
        self.prvd_atcl_link_url =  kwargs.pop('prvd_atcl_link_url',None)
        self.prvd_atcl_link_titl_use_yn =  kwargs.pop('prvd_atcl_link_titl_use_yn',None)
        self.prvd_atcl_link_use_prvd_co_nm_yn =  kwargs.pop('prvd_atcl_link_use_prvd_co_nm_yn',None)
        self.prvd_mbl_atcl_url =  kwargs.pop('prvd_mbl_atcl_url',None)
        self.prvd_mbl_link_titl_use_yn =  kwargs.pop('prvd_mbl_link_titl_use_yn',None)
        self.prvd_mbl_link_prvd_co_nm_use_yn =  kwargs.pop('prvd_mbl_link_prvd_co_nm_use_yn',None)
        self.prvd_co_vo_str =  kwargs.pop('prvd_co_vo_str',None)
        self.x_coor_val =  kwargs.pop('x_coor_val',None)
        self.y_coor_val =  kwargs.pop('y_coor_val',None)
        self.loc_mark_yn =  kwargs.pop('loc_mark_yn',None)
        self.lrea_nm =  kwargs.pop('lrea_nm',None)
        self.lrea_id =  kwargs.pop('lrea_id',None)
        self.drct_deal_yn =  kwargs.pop('drct_deal_yn',None)
        self.sell_user_cell_num =  kwargs.pop('sell_user_cell_num',None)
        self.dtl_addr =  kwargs.pop('dtl_addr',None)
        self.dtl_addr_yn =  kwargs.pop('dtl_addr_yn',None)
        self.owner_chk_yn =  kwargs.pop('owner_chk_yn',None)
        self.rpsn_img_url =  kwargs.pop('rpsn_img_url',None)
        self.rpsn_img_typ_cd =  kwargs.pop('rpsn_img_typ_cd',None)
        self.rpsn_img_thmb_nm =  kwargs.pop('rpsn_img_thmb_nm',None)
        self.img_cnt =  kwargs.pop('img_cnt',None)
        self.sell_user_nm =  kwargs.pop('sell_user_nm',None)
        self.tag_lst_str =  kwargs.pop('tag_lst_str',None)
        self.mi_nm =  kwargs.pop('mi_nm',None)
        self.real_deal_yymm =  kwargs.pop('real_deal_yymm',None)
        self.real_deal_ymd_clct_cd =  kwargs.pop('real_deal_ymd_clct_cd',None)
        self.real_deal_ymd_clct_nm =  kwargs.pop('real_deal_ymd_clct_nm',None)
        self.real_deal_prc_nm =  kwargs.pop('real_deal_prc_nm',None)
        self.real_deal_dpst_nm =  kwargs.pop('real_deal_dpst_nm',None)
        self.real_deal_rent_prc_nm =  kwargs.pop('real_deal_rent_prc_nm',None)

    def __repr__(self):
        return "<MigNvCmpxAtcl('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.job_id), str(self.exec_dtm), str(self.atcl_num), str(self.nv_cmpx_id), str(self.nv_cmpx_typ_seq), str(self.gov_legl_dong_cd), str(self.atcl_nm), str(self.nv_cmpx_nm), str(self.nv_cmpx_knd), str(self.nv_cmpx_knd_nm), str(self.cmpx_typ_nm), str(self.nv_atcl_cmpx_typ_cd), str(self.nv_atcl_cmpx_typ_nm), str(self.nv_atcl_up_cmpx_typ_cd), str(self.sply_area_str), str(self.only_area_str), str(self.nv_atcl_stat_cd), str(self.nv_atcl_stat_nm), str(self.deal_cmpl_yn), str(self.nv_deal_typ_cd), str(self.nv_deal_typ_nm), str(self.nv_vrfy_typ_cd), str(self.flr_info), str(self.prc_chg_stat_cd), str(self.prc_chg_yn), str(self.deal_prc_nm), str(self.prc_info), str(self.deal_prc_info), str(self.prmu_prc_nm), str(self.same_addr_prmu_mbig_prc_nm), str(self.same_addr_prmu_msml_prc_nm), str(self.rent_prc_nm), str(self.deal_prc_num), str(self.deal_han_prc_nm), str(self.rent_prc_num), str(self.deal_rent_prc_nm), str(self.own_user_deal_chk_yn), str(self.exps_nm), str(self.atcl_chk_ymd), str(self.deal_cmpl_ymd), str(self.atcl_desc), str(self.dong_nm), str(self.same_addr_cnt), str(self.same_addr_drct_cnt), str(self.same_addr_mbig_prc_nm), str(self.same_addr_mbig_scnd_prc_nm), str(self.same_addr_msml_prc_nm), str(self.same_addr_msml_scnd_prc_nm), str(self.same_addr_hash_val), str(self.msml_mvi_fee_val), str(self.mbig_mvi_fee_val), str(self.sbwy_info), str(self.svc_desc), str(self.cl_nm), str(self.et_room_cnt), str(self.prvd_co_id), str(self.prvd_co_nm), str(self.prvd_co_cnt), str(self.prvd_atcl_addr), str(self.prvd_atcl_link_url), str(self.prvd_atcl_link_titl_use_yn), str(self.prvd_atcl_link_use_prvd_co_nm_yn), str(self.prvd_mbl_atcl_url), str(self.prvd_mbl_link_titl_use_yn), str(self.prvd_mbl_link_prvd_co_nm_use_yn), str(self.prvd_co_vo_str), str(self.x_coor_val), str(self.y_coor_val), str(self.loc_mark_yn), str(self.lrea_nm), str(self.lrea_id), str(self.drct_deal_yn), str(self.sell_user_cell_num), str(self.dtl_addr), str(self.dtl_addr_yn), str(self.owner_chk_yn), str(self.rpsn_img_url), str(self.rpsn_img_typ_cd), str(self.rpsn_img_thmb_nm), str(self.img_cnt), str(self.sell_user_nm), str(self.tag_lst_str), str(self.mi_nm), str(self.real_deal_yymm), str(self.real_deal_ymd_clct_cd), str(self.real_deal_ymd_clct_nm), str(self.real_deal_prc_nm), str(self.real_deal_dpst_nm), str(self.real_deal_rent_prc_nm) + KTable.__repr__(self))


