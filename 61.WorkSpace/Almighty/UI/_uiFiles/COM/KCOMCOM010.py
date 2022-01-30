from PyQt5.QtWidgets import QTableView
import Server.COM
from common.ui.comUi import *
import common.database.Relfect
from UI._uiFiles.UIBasic import *
from Server.Basic import *
from DAO.KADM import *
import copy


pgm_id = 'KCOMCOM010'
pgm_nm = '공통팝업'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMCOM010(QDialog, KWidget, form_class) :
    dicParam = {}
    dicResult = {}

    def __init__(self,parent,dicParm):
        super().__init__(parent)
        super().__init__()
        self.dicParam = dicParm
        self.initUI()
        self.search()

    def initUI(self):
        # TableWidget.convert_to_TableWidget(self.twFinder)
        # self.twFinder.init()

        self.edt_pop.setText(self.dicParam['searchText'])
        self.twFinder.setColumnCount(len(self.dicParam['Headers']))
        self.twFinder.setHorizontalHeaderLabels(self.dicParam['Headers'])
        self.twFinder.setBasic(columns = self.dicParam['Columns'], headers = self.dicParam['Headers']
                               , tableClass = self.dicParam['tableClass'], widths = self.dicParam['Widths'])

        #self.tw.clicked.connect(self.select)
        self.btn_search.clicked.connect(self.search)
        self.twFinder.doubleClicked.connect(self.selected)

    def search(self):
        self.dicParam['searchText'] =  self.edt_pop.text()
        #Server 함수 호출
        strExec = self.dicParam['Function']+"(self.dicParam)"
        rslt = eval(strExec)
        self.twFinder.setListTable(rslt)
        self.twFinder.resizeRowsToContents()

    def selected(self):
        self.dicResult = self.twFinder.getRowDic(self.twFinder.currentRow())
        self.close()

    def getResult(self):
        return self.dicResult

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.search()
        else:
            pass

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMCOM010()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()