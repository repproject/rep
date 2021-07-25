from UI._uiFiles.KWidget import *
import Server.COM
from DAO.KADM import *

pgm_id = 'KCOMDEV030'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV030(QWidget, KWidget, form_class) :
    def __init__(self):
        try:
            super().__init__()
            self.initUI()
        except : error()

    def initUI(self):
        #self.btn_search.clicked.connect(self.search)
        #self.twComCdGrp.clicked.connect(self.search2)
        self.btn_save.clicked.connect(self.save)
        self.btn_add.clicked.connect(self.addSite)
        #self.btn_add2.clicked.connect(self.addDtl)
        self.search()

    def search(self):
        try:
            Columns = ['site_cd', 'slep_sec', 'bas_url', 'bas_prtc', 'enc_cd']
            Widths = {'site_cd':50, 'slep_sec':50, 'bas_url':200, 'bas_prtc':30, 'enc_cd':50}
            self.twSite.setBasic(columns = Columns, widths = Widths, tableClass = Site)
            self.twSite.setListTable(self.getSites())

            #Table Widget Setting
            self.twSite.resizeRowsToContents()
        except : error()

    def addSite(self):
        try:
            self.twSite.addTWRow()
        except : error()

    def save(self):
        try:
            self.twSite.mergeRow()
        except : error()

    def getSites(self):
        return Server.COM.getSite()

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMDEV030()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()