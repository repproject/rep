from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
from common.ui.comUi import *

pgm_id = None

class KWidget() :
    pgm_id = None

    def __init__(self):
        self.setupUi(self)
        self.pgm_id = pgm_id
        self.setQObjectToCustomizedClass()

    def setQObjectToCustomizedClass(self):
        #print(self.__dict__.keys())
        for key in self.__dict__.keys():
            #QTableWidget to customized TableWidget
            #print(key)
            #print(self.__dict__[key].__class__)
            if self.__dict__[key].__class__ == QTableWidget:
                TableWidget.convert_to_TableWidget(self.__dict__[key])
                self.__dict__[key].init() #위함수로 init이 호출되지 않아 별도 호출



