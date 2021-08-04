from PyQt5.QtWidgets import QTableView
import Server.COM
from UI._uiFiles.KWidget import *
from common.ui.comUi import *
from UI._uiFiles.UIBasic import *
from Server.Basic import *
from DAO.KADM import *

pgm_id = 'KCOMDEV030'
pgm_nm = '사이트관리'
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
        self.twSite.clicked.connect(self.searchSvc)
        self.twSvc.clicked.connect(self.searchSvcPasi)
        self.btn_add_svc.clicked.connect(self.addSvc)
        self.btn_del_svc.clicked.connect(self.delSvc)
        self.btn_add_svc_pasi.clicked.connect(self.addSvcPasi)
        self.btn_del_svc_pasi.clicked.connect(self.delSvcPasi)
        self.search()

    def search(self):
        try:
            Columns = ['site_cd', 'slep_sec', 'bas_url', 'bas_prtc', 'enc_cd']
            Widths = {'site_cd':120, 'slep_sec':50, 'bas_url':200, 'bas_prtc':30, 'enc_cd':50}
            self.twSite.setBasic(columns = Columns, widths = Widths, tableClass = Site)
            self.twSite.setListTable(self.getSites())

            #Table Widget Setting
            self.twSite.resizeRowsToContents()
        except : error()

    def searchSvc(self):
        try:
            strSiteCd = self.sender().getTextByColName(self.sender().currentRow(),"site_cd")

            Columns = ['svc_id', 'BAS_SVC_URL', 'REQ_WAY_CD','exmp_url','SVC_DESC']
            Widths = {'svc_id':150, 'BAS_SVC_URL':300, 'REQ_WAY_CD':70,'exmp_url':300,'SVC_DESC':300}
            SetDic = {'site_cd': strSiteCd}
            self.twSvc.setBasic(columns = Columns, widths = Widths, tableClass = Svc, setDic=SetDic)
            self.twSvc.setListTable(self.getSvc(strSiteCd))
    #        self.twSvcPasi.removeAll()
        except: error()

    def searchSvcPasi(self):
        try:
            strSvcId = self.twSvc.getTextByColName(self.twSvc.currentRow(),"svc_id")

            Columns = ['PASI_ID', 'PASI_WAY_CD','PARM_LOAD_FUNC_NM','SVC_PASI_DESC']
            Widths = {'PASI_ID':100, 'PASI_WAY_CD':70,'PARM_LOAD_FUNC_NM':150,'SVC_PASI_DESC':150}
            SetDic = {'svc_id': strSvcId}
            self.twSvcPasi.setBasic(columns = Columns, widths = Widths, tableClass = SvcPasi, setDic=SetDic)
            self.twSvcPasi.setListTable(self.getSvcPasi(strSvcId))
        except: error()

    def getSvcPasi(self,strSvcId): return Server.COM.getSvcPasi(strSvcId)

    def addSite(self):
        try:
            self.twSite.addTWRow()
        except : error()

    def addSvc(self):
        try:
            if self.preAddSvc():
               n = self.twSvc.addTWRow()
        except : error()

    def addSvcPasi(self):
        try:
            if self.preAddSvcPasi():
               n = self.twSvcPasi.addTWRow()
        except : error()

    def preAddSvc(self):
        if self.twSite.currentItem() == None:
            alert("사이트를 선택하셔야합니다.")
            return False
        return True

    def preAddSvcPasi(self):
        if self.twSvc.currentRow() == -1:
            alert("서비스를 선택하셔야합니다.")
            return False
        return True

    def preDelSvc(self):
        if self.twSvc.currentRow() == -1:
            alert("선택된 서비스가 없습니다.")
            return False
        if self.twSvcPasi.rowCount() > 0:
            alert("파싱 정보를 우선적으로 삭제하셔야 합니다.")
            return False
        return True

    def delSvc(self,table):
        try:
            if self.preDelSvc():
                self.twSvc.deleteRow()
                return True
            return False
        except : error()

    def preDelSvcPasi(self):
        if self.twSvcPasi.currentRow() == -1:
            alert("선택된 서비스 파싱이 없습니다.")
            return False
        return True

    def delSvcPasi(self,table):
        try:
            if self.preDelSvcPasi():
                self.twSvcPasi.deleteRow()
                return True
            return False
        except : error()

    def save(self):
        try:
            self.twSite.mergeRow()
            self.twSite.setTWColor()
            self.twSvc.mergeList()
            self.twSvc.setTWColor()
            self.twSvcPasi.mergeList()
            self.twSvcPasi.setTWColor()
        except : error()

    def getSites(self):
        return Server.COM.getSite()

    def getSvc(self,strSiteCd):
        return Server.COM.getSvc(strSiteCd)

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMDEV030()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()