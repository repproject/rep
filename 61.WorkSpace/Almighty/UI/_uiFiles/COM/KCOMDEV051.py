from PyQt5.QtWidgets import QTableView
import Server.COM
from common.ui.comUi import *
from common.ui.comPopUp import *
import common.database.Relfect
from UI._uiFiles.UIBasic import *
from Server.Basic import *
from DAO.KADM import *
import copy

pgm_id = 'KCOMDEV051'
pgm_nm = '서비스파싱항목컬럼'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV051(QDialog, KWidget, form_class) :
    dicParam = {}
    dicResult = {}

    def __init__(self,parent,dicParm):
        super().__init__(parent)
        super().__init__()
        self.dicParam = dicParm
        self.initUI()
        self.search()

    def initUI(self):
        self.btn_add.clicked.connect(self.add)
        self.btn_del.clicked.connect(self.delCol)
        self.btn_save.clicked.connect(self.save)

        Columns = ['TBL_NM', 'COL_NM']
        Widths = {'TBL_NM': 200, 'COL_NM': 200}
        self.twSvcPasiItemCol.setBasic(columns=Columns, widths=Widths, tableClass=SvcPasiItemCol, setDic=self.dicParam)

    def search(self):
        self.twSvcPasiItemCol.setListTable(self.getTablePasiItem(self.dicParam['svc_id'],self.dicParam['pasi_id'],self.dicParam['item_nm'],self.dicParam['in_out_cl_cd']))
        self.twSvcPasiItemCol.resizeRowsToContents()

    def getTablePasiItem(self,strSvcId, strPasiId, strItemNm, strInOutClCd):
        return Server.COM.getTablePasiItem(strSvcId, strPasiId, strItemNm, strInOutClCd)

    def add(self):
        try:
            n = self.twSvcPasiItemCol.addTWRow()
        except : error()

    def delCol(self):
        try:
            if self.predelCol():
                self.twSvcPasiItemCol.deleteRow()
        except: error()

    def predelCol(self):
        if self.twSvcPasiItemCol.currentItem() == None:
            alert("컬럼을 선택하셔야합니다.")
            return False
        return True

    def save(self):
        try:
            if self.preSave():
                self.twSvcPasiItemCol.mergeList()
        except : error()

    def preSave(self):
        for n in range(0,self.twSvcPasiItemCol.rowCount()):
            if isNull(self.twSvcPasiItemCol.getTextByColName(n, "tbl_nm")):
                alert('테이블명이 없습니다.')
                return False
            if isNull(self.twSvcPasiItemCol.getTextByColName(n, "col_nm")):
                alert('컬럼명이 없습니다.')
                return False
        return True

    def getResult(self):
        for n in range(self.twSvcPasiItemCol.rowCount()):
            if self.twSvcPasiItemCol.isNewRow(n) == False:
                return True
        return False

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMDEV051()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()