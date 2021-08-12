from typing import Dict, List, Any, Union
import DAO.KADM
from PyQt5.QtWidgets import QTableView
import Server.COM
from common.ui.comUi import *
import common.database.Relfect
from UI._uiFiles.UIBasic import *
from common.ui.comPopUp import *
import sys

pgm_id = 'KCOMDEV010'
pgm_nm = '테이블클래스생성'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV010(QWidget, KWidget, form_class) :
    meta = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.meta = common.database.Relfect.makeMeta()
        self.btn_search.clicked.connect(self.search)
        self.tbTable.clicked.connect(self.findTable)
        pass

    def search(self):
        try:
            className = self.edt_class.text()
            if len(className) == 0:
                alert("클래스명이 입력되지 않았습니다.")
                return False
            tableName = self.edt_table.text()
            if len(tableName) == 0:
                alert("테이블명이 입력되지 않았습니다.")
                return False
            if self.getTbl(tableName) == None:
                alert("테이블이 등록되지 않았습니다.")
                return False
            if self.getTblCol(tableName) == None:
                alert("테이블의 컬럼이 등록되지 않았습니다.")

            classDeclare = common.database.Relfect.getClassTable(self.meta,className,tableName)
            self.textEditClass.setText(classDeclare)
        except : error()
        return True

    def getTbl(self,strTbl): return Server.COM.getTbl(strTbl)
    def getTblCol(self,strTbl): return Server.COM.getTblCol(strTbl)

    def findTable(self):
        try:
            dicParam = {}
            dicParam['searchText'] = self.edt_table.text()
            dicParam['Columns'] = ['tbl_nm','tbl_desc','CLS_NM']
            dicParam['Headers'] = ['테이블명', '테이블설명','클래스명']
            dicParam['Widths'] = {'tbl_nm':150, 'tbl_desc':200, 'CLS_NM':150}
            dicParam['tableClass'] = DAO.KADM.Tbl
            dicParam['Function'] = 'Server.COM.getTableFinder'
            result = finderPop(self,dicParam)
            self.edt_table.setText(result['tbl_nm'])
            self.edt_table_nm.setText(result['tbl_desc'])
            self.edt_class.setText(result['cls_nm'])
            self.search()
        except: error()

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.search()
        else:
            pass

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMDEV010()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()