from PyQt5.QtWidgets import QTableView
import Server.COM
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
        self.tableJob = self.getJob()
        dictCodeList = {}
        for codeKey in self.tableJob[0].codeList:
            self.tableJob[0].codeList[codeKey]

        twColumns = ['job_id', 'job_nm', 'job_desc', 'job_cl_cd', 'use_yn', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
        twHeaders = ['JobID', 'Job명', 'Job설명', '작업구분', '사용여부', '참조1', '참조2', '참조3', '참조4', '참조5']

        self.tableWidgetJob.setRowCount(len(self.tableJob))
        self.tableWidgetJob.setColumnCount(len(twColumns))
        for n, row in enumerate(self.tableJob):
            for m, col in enumerate(twColumns):
                newitem = QTableWidgetItem(getattr(row, col))
                try:
                    row.codeList[col]
                    combobox = QComboBox()


                except KeyError : pass
                self.tableWidgetJob.setItem(n,m,newitem)
        self.tableWidgetJob.setHorizontalHeaderLabels(twHeaders)
        self.tableWidgetJob.resizeColumnsToContents()
        self.tableWidgetJob.resizeRowsToContents()




        #for n, key in enumerate(sorted(self.data.keys())):
        #    print(key)
        #    print(n)
        #    horHeaders.append(key)
        #    for m, item in enumerate(self.data[key]):
        #        newitem = QTableWidgetItem(item)
        #        self.setItem(m, n, newitem)
        #self.setHorizontalHeaderLabels(horHeaders)


        #self.tableViewJob




        # data = {'col1': ['1', '2', '3', '4'],
        #         'col2': ['1', '2', '1', '3'],
        #         'col3': ['1', '1', '2', '1']}
        #self.tableJob[0]

        #self.tableViewJob = TableView(self.tableViewJob,data,0,len(self.tableJob))

    def getJob(self): return Server.COM.getJob()

    #def set

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMMAN003()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()