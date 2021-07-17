from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from common.database.testReflect import *
import datetime
import UI._uiFiles.COM.KCOMMAN001

Base = declarative_base()


class KColumn(Column):

    def __init__(self, *args, **kwargs):
        Column.__init__(self, *args, **kwargs)
        pass

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
    reg_user_id = last1PriorityColumn(Integer)
    reg_dtm = last2PriorityColumn(DATETIME)
    chg_user_id = last3PriorityColumn(Integer)
    chg_dtm = last4PriorityColumn(DATETIME)

    def __init__(self):
        self.init()

    def init(self):
        self.reg_user_id = UI._uiFiles.COM.KCOMMAN001.user_id
        self.reg_dtm = datetime.datetime.now()
        self.chg_user_id = UI._uiFiles.COM.KCOMMAN001.user_id
        self.chg_dtm = datetime.datetime.now()

    def __repr__(self):
        return ",'%s', '%s', '%s', '%s')>" % (self.reg_user_id, self.reg_dtm, self.chg_user_id, self.chg_dtm)


if __name__ == "__main__":
    pass
