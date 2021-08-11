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
        self.bb_lv1_regn_nm =  kwargs.pop('bb_lv1_regn_nm','')

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
        self.bb_lv2_regn_nm = kwargs.pop('bb_lv2_regn_nm', '')
        self.bb_lv1_regn_nm = kwargs.pop('bb_lv1_regn_nm', '')

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
        self.bb_lv3_regn_nm =  kwargs.pop('bb_lv3_regn_nm','')
        self.bb_lv1_regn_nm =  kwargs.pop('bb_lv1_regn_nm','')
        self.bb_lv2_regn_nm =  kwargs.pop('bb_lv2_regn_nm','')

    def __repr__(self):
        return "<BbLv3Regn('%s', '%s', '%s', '%s', '%s', '%s'" % (str(self.bb_lv1_regn_cd), str(self.bb_lv2_regn_cd), str(self.bb_lv3_regn_cd), str(self.bb_lv3_regn_nm), str(self.bb_lv1_regn_nm), str(self.bb_lv2_regn_nm) + KTable.__repr__(self))

