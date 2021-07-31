from PyQt5.QtWidgets import QTableView
import Server.COM
from UI._uiFiles.KWidget import *
from common.ui.comUi import *
import common.database.Relfect
from UI._uiFiles.UIBasic import *
import sys

pgm_id = 'KCOMDEV010'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV010(QWidget, KWidget, form_class) :
    #meta = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.meta = common.database.Relfect.makeMeta()
        self.btn_search.clicked.connect(self.search)
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
            classDeclare = common.database.Relfect.getClassTable(self.meta,className,tableName)
            self.textEditClass.setText(classDeclare)
        except Exception as e:
            print(e)
        return True


if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMDEV010()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()