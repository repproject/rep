from PyQt5.QtWidgets import QTableView
import Server.COM
from UI._uiFiles.KWidget import *
from common.ui.comUi import *
from common.ui.comPopUp import *
import common.database.Relfect
from UI._uiFiles.UIBasic import *
from Server.Basic import *
from DAO.KADM import *
import copy

pgm_id = 'KCOMDEV020'
pgm_nm = '공통코드관리'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV020(QWidget, KWidget, form_class) :
    def __init__(self):
        try:
            super().__init__()
            self.initUI()
            print(self.twComCdGrp.__class__)
        except : error()

    def initUI(self):
        self.btn_search.clicked.connect(self.search)
        self.twComCdGrp.clicked.connect(self.search2)
        self.btn_save.clicked.connect(self.save)
        self.btn_add.clicked.connect(self.addGrp)
        self.btn_add2.clicked.connect(self.addDtl)

    def search(self):
        try:
            Columns = ['com_cd_grp', 'com_cd_grp_nm', 'com_cd_grp_desc', 'up_com_cd_grp', 'del_yn', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
            Widths = {'com_cd_grp':130, 'com_cd_grp_nm':150, 'com_cd_grp_desc':150, 'up_com_cd_grp':70, 'del_yn':30, 'ref1':50, 'ref2':50, 'ref3':50, 'ref4':50, 'ref5':50}
            self.twComCdGrp.setBasic(columns = Columns, widths = Widths, tableClass = ComCdLst)
            self.twComCdGrp.setListTable(self.getCodeLst(self.edt_ComCdGrp.text(),self.edt_ComCdGrpNm.text()))

            #Table Widget Setting
            self.twComCdGrp.resizeRowsToContents()
        except : error()

    def search2(self):
        try:
            strComCdgrp = self.sender().getTextByColName(self.sender().currentRow(),"com_cd_grp")

            Columns = ['com_cd', 'com_cd_nm', 'com_cd_desc', 'prnt_seq', 'eff_sta_ymd', 'eff_end_ymd', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
            Widths = {'com_cd':130, 'com_cd_nm':50, 'com_cd_desc':150, 'prnt_seq':30, 'eff_sta_ymd':120, 'eff_end_ymd':120, 'ref1':50, 'ref2':50, 'ref3':50, 'ref4':50, 'ref5':50}
            Aligns = {'eff_sta_ymd':4,'eff_end_ymd':4}
            SetDic = {'com_cd_grp':strComCdgrp}

            self.twComCdDtl.setBasic(columns = Columns, widths = Widths, tableClass = ComCdDtl, setDic = SetDic, aligns = Aligns)
            self.twComCdDtl.setListTable(self.getCodeDtl(strComCdgrp))

            #Table Widget Setting
            self.twComCdDtl.resizeRowsToContents()
        except : error()

    def save(self):
        try:
            if self.preSave():
                self.twComCdGrp.mergeRow()
                self.twComCdDtl.mergeList()
        except : error()

    def preSave(self):
        if self.twComCdGrp.currentItem() == None:
            alert("공통코드그룹을 선택하셔야합니다.")
            return False

        if self.twComCdGrp.getTextByColName(self.twComCdGrp.currentRow(),"com_cd_grp") == False:
            alert('공통코드그룹ID가 없습니다.')
            return False

        for n in range(0,self.twComCdDtl.rowCount()):
            if self.twComCdDtl.getTextByColName(n, "com_cd") == None:
                alert('공통코드값이 없습니다.')
                return False

            if self.twComCdDtl.getTextByColName(n, "com_cd_nm") == None:
                alert('공통코드명이 없습니다.')
                return False

            if self.twComCdDtl.getTextByColName(n, "prnt_seq") == None:
                alert('출력순서가 없습니다.')
                return False
        return True

    def addGrp(self):
        try:
            self.twComCdGrp.addTWRow()
        except : error()

    def addDtl(self):
        try:
            if self.preAddDtl():
               n = self.twComCdDtl.addTWRow()
               self.twComCdDtl.setTextByColName(n,"eff_sta_ymd",datetime.datetime.now().strftime('%Y%m%d'))
               self.twComCdDtl.setTextByColName(n,"eff_end_ymd", '99991231')
               prnt_seq = 1
               if n > 0 :
                   prnt_seq = int(self.twComCdDtl.getTextByColName(n-1,'prnt_seq')) + 1
               self.twComCdDtl.setTextByColName(n, "prnt_seq", prnt_seq)
        except : error()

    def preAddDtl(self):
        if self.twComCdGrp.currentItem() == None:
            alert("공통코드그룹을 선택하셔야합니다.")
            return False
        return True

    def getCodeLst(self,strComCdGrp,strComCdGrpNm): return Server.COM.getCodeLst(strComCdGrp,strComCdGrpNm)
    def getCodeDtl(self,strComCdGrp):               return Server.COM.getCodeDtl(strComCdGrp)

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMDEV020()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()