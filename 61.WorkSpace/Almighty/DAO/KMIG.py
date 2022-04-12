from common.database.repSqlAlchemy import *
import common.ui.comUi
from DAO.KADM import *

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
    __tablename__ = 'kmig_deal_dtl'

    gov_legl_dong_cd = KColumn(String(10), nullable = False)
    deal_yymm = KColumn(String(6), nullable = False)
    real_deal_seq = KColumn(Integer, primary_key = True, unique=True, autoincrement=True)
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
        self.gov_legl_dong_cd =  kwargs.pop('gov_legl_dong_cd',None)
        self.deal_yymm =  kwargs.pop('deal_yymm',None)
        #self.real_deal_seq =  kwargs.pop('real_deal_seq',0)
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
        return "<DealDtl('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.gov_legl_dong_cd), str(self.deal_yymm), str(self.real_deal_seq), str(self.real_deal_cmpx_knd), str(self.deal_amt), str(self.cmpl_yy), str(self.deal_yy), str(self.road_nm), str(self.road_nm_cmpx_orgl_num_cd), str(self.road_nm_cmpx_vice_num_cd), str(self.road_nm_sgg_cd), str(self.road_nm_seq_cd), str(self.road_nm_ong_ung_cd), str(self.road_nm_cd), str(self.legl_dong_nm), str(self.legl_dong_orgl_num_cd), str(self.legl_dong_vice_num_cd), str(self.legl_dong_sgg_cd), str(self.legl_dong_umd_cd), str(self.legl_dong_hnum_cd), str(self.real_deal_cmpx_nm), str(self.deal_mm), str(self.deal_ymd), str(self.seq), str(self.only_area), str(self.agnt_whrb_addr), str(self.regn_cd), str(self.hnum), str(self.flr), str(self.rles_rsn_occr_dd), str(self.rles_yn_val) + KTable.__repr__(self))




