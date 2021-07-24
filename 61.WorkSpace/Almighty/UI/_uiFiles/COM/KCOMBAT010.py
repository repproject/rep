from PyQt5.QtWidgets import QTableView
import Server.COM
from Server.Basic import *
from UI._uiFiles.KWidget import *
from UI._uiFiles.UIBasic import *
from common.ui.comUi import *
from DAO.KADM import *
import sys

pgm_id = 'KCOMBAT010'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMBAT010(QWidget, KWidget, form_class) :
    tableJob = None

    def __init__(self):
        try:
            super().__init__()
            self.initUI()
        except: error()

    def initUI(self):
        Columns = ['job_id', 'job_nm', 'job_desc', 'job_cl_cd', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
        Widths = [70,150,150,100,50,50,50,50,50]
        self.twJob.setBasicList(Columns,Widths,Job)

        #set TableWidget by listTable
        self.twJob.setListTable(self.getJob())

        #Table Widget Setting
        #self.twJob.resizeRowsToContents()
        #self.twJob.resize()

    def getJob(self):
        return Server.COM.getJob()

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMBAT010()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()