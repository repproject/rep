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



