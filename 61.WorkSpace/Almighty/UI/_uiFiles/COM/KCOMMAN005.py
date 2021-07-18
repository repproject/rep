from PyQt5.QtWidgets import QTableView
import Server.COM
from UI._uiFiles.KWidget import *
from common.ui.comUi import *
import common.database.Relfect
from UI._uiFiles.UIBasic import *

pgm_id = 'KCOMMAN005'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMMAN005(QWidget,KWidget,form_class) :
    tableComCdLst = None
    tableComCdDtl = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn_search.clicked.connect(self.search)
        self.tableWidgetComCdGrp.clicked.connect(self.search2)
        pass

    def search(self):
        try:
            #column,header 정의
            twColumns = ['com_cd_grp', 'com_cd_grp_nm', 'com_cd_grp_desc', 'up_com_cd_grp', 'del_yn', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
            twHeaders = ['그룹ID', '그룹명', '그룹설명', '상위그룹iD', '삭제여부', '참조1', '참조2', '참조3', '참조4', '참조5']

            #get data
            self.tableComCdLst = self.getCodeLst(self.edt_ComCdGrp.text(),self.edt_ComCdGrpNm.text())
            print(self.tableComCdLst)

            #set TableWidget by listTable
            setTableWidgetByTableList(self.tableWidgetComCdGrp, self.tableComCdLst, twColumns, twHeaders)

            #Table Widget Setting
            self.tableWidgetComCdGrp.resizeColumnsToContents()
            self.tableWidgetComCdGrp.resizeRowsToContents()
        except Exception as e :
            print(pgm_id + ".search Error : " + str(e))

    def search2(self):
        try:
            sender = self.sender()
            strComCdgrp = sender.item(sender.currentRow(),0).text()

            #column,header 정의
            twColumns = ['com_cd_grp', 'com_cd', 'com_cd_nm', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
            twHeaders = ['그룹ID', '코드값', '코드명', '참조1', '참조2', '참조3', '참조4', '참조5']

            #get data
            self.tableComCdDtl = self.getCodeDtl(strComCdgrp)

            #set TableWidget by listTable
            setTableWidgetByTableList(self.tableWidgetComCdDtl, self.tableComCdDtl, twColumns, twHeaders)

            #Table Widget Setting
            self.tableWidgetComCdDtl.resizeColumnsToContents()
            self.tableWidgetComCdDtl.resizeRowsToContents()

        except Exception as e:
            print(e)

    def getCodeLst(self,strComCdGrp,strComCdGrpNm):
        return Server.COM.getCodeLst(strComCdGrp,strComCdGrpNm)

    def getCodeDtl(self,strComCdGrp):
        return Server.COM.getCodeDtl(strComCdGrp)

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMMAN005()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()