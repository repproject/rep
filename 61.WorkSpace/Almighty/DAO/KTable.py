from common.common.User import *
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from common.database.testReflect import *
import datetime
#import UI._uiFiles.COM.KCOMMAN010

Base = declarative_base()

class KColumn(Column):
    kcom_cd_domain = False
    kcom_cd_grp = None

    def __init__(self, *args, **kwargs):
        self.kcom_cd_domain = kwargs.pop("kcom_cd_domain", False)
        self.kcom_cd_grp = kwargs.pop("kcom_cd_grp", None)
        Column.__init__(self, *args, **kwargs)
        pass

    def __repr__(self):
        return super().__repr__()+"\n" + "kcom_cd_domain : " + str(self.kcom_cd_domain) + "\n kcom_cd_grp : " + str(self.kcom_cd_grp)

class last1PriorityColumn(KColumn):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._creation_order = 9999990

class last2PriorityColumn(KColumn):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._creation_order = 9999991

class last3PriorityColumn(KColumn):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._creation_order = 9999992

class last4PriorityColumn(KColumn):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._creation_order = 9999993

class KTable():
    reg_user_id = last1PriorityColumn(Integer,default=user.getUserId())
    reg_dtm = last2PriorityColumn(DATETIME,server_default=text('NOW()'))
    chg_user_id = last3PriorityColumn(Integer,default=user.getUserId())
    chg_dtm = last4PriorityColumn(DATETIME,server_default=text('NOW()'))

    def __init__(self):
        self.init()

    def init(self):
        self.reg_user_id = user.getUserId()
        self.reg_dtm = datetime.datetime.now()
        self.chg_user_id = user.getUserId()
        self.chg_dtm = datetime.datetime.now()

    def updateChg(self):
        self.chg_user_id = user.getUserId()
        self.chg_dtm = datetime.datetime.now()

    def __repr__(self):
        return ",'%s', '%s', '%s', '%s')>" % (self.reg_user_id, self.reg_dtm, self.chg_user_id, self.chg_dtm)

if __name__ == "__main__":
    pass
