from PyQt5.QtWidgets import QTableView
import Server.COM
from UI._uiFiles.KWidget import *
from common.ui.comUi import *
import common.database.Relfect
from UI._uiFiles.UIBasic import *
from Server.Basic import *
from DAO.KADM import *
import copy

pgm_id = 'KCOMDEV020'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV020(QWidget, KWidget, form_class) :
    def __init__(self):
        try:
            super().__init__()
            self.initUI()
        except : error()

    def initUI(self):
        self.btn_search.clicked.connect(self.search)
        self.twComCdGrp.clicked.connect(self.search2)
        self.btn_save.clicked.connect(self.save)
        self.btn_add.clicked.connect(self.addGrp)

    def search(self):
        try:
            Columns = ['com_cd_grp', 'com_cd_grp_nm', 'com_cd_grp_desc', 'up_com_cd_grp', 'del_yn', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
            self.twComCdGrp.setColumns(Columns) #tableWidget객체에 컬럼목록 세팅
            self.twComCdGrp.setTableClass(ComCdLst)  #tableWidget객체에 대상 테이블 클래스 세팅

            self.twComCdGrp.setListTable(self.getCodeLst(self.edt_ComCdGrp.text(),self.edt_ComCdGrpNm.text()))

            #Table Widget Setting
            self.twComCdGrp.resizeRowsToContents()
        except : error()

    def search2(self):
        try:
            strComCdgrp = self.sender().item(self.sender().currentRow(),0).text()

            Columns = ['com_cd', 'com_cd_nm', 'eff_sta_ymd', 'eff_end_ymd', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
            self.twComCdDtl.setColumns(Columns)
            self.twComCdDtl.setTableClass(ComCdDtl)

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

        if self.twComCdGrp.getTextByColName(self.twComCdGrp.currentRow(),'com_cd_grp') == False:
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

    def addGrp(self):
        try:
            self.twComCdGrp.addTWRow()
        except : error()

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