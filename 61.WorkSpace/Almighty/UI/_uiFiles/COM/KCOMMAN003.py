from PyQt5.QtWidgets import QTableView
import Server.COM
from Server.Basic import *
from UI._uiFiles.KWidget import *
from UI._uiFiles.UIBasic import *
from common.ui.comUi import *
import sys

pgm_id = 'KCOMMAN003'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMMAN003(QWidget,KWidget,form_class) :
    tableJob = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        #column,header 정의
        twColumns = ['job_id', 'job_nm', 'job_desc', 'job_cl_cd', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
        twHeaders = ['JobID', 'Job명', 'Job설명', '작업구분', '참조1', '참조2', '참조3', '참조4', '참조5']

        #get data
        self.tableJob = self.getJob()

        #set TableWidget by listTable
        setTableWidgetByTableList(self.tableWidgetJob,self.tableJob,twColumns,twHeaders)

        #Table Widget Setting
        self.tableWidgetJob.resizeColumnsToContents()
        self.tableWidgetJob.resizeRowsToContents()

    def getJob(self): return Server.COM.getJob()

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMMAN003()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()