from UI._uiFiles.UIBasic import *
from PyQt5.QtWidgets import QTableView
import common.database.Relfect
from DAO.KADM import *

pgm_id = 'KCOMDEV050'
pgm_nm = '파싱관리'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV050(QWidget, KWidget, form_class) :
    result = None
    svc_id = None
    pasi_id = None

    def __init__(self):
        try:
            super().__init__()
            self.initUI()
        except : error()

    def initUI(self):
        self.tbPasi.clicked.connect(self.findPasi)
        self.btn_search.clicked.connect(self.search)
        self.btn_save.clicked.connect(self.save)
        self.btn_add_in.clicked.connect(self.addIn)
        self.btn_add_in_2.clicked.connect(self.addInDefault)
        self.btn_del_in.clicked.connect(self.delIn)
        self.btn_add_out.clicked.connect(self.addOut)
        self.btn_add_out_2.clicked.connect(self.addOutDefault)
        self.btn_del_out.clicked.connect(self.delOut)

    def findPasi(self):
        try:
            dicParam = {}
            dicParam['searchText'] = self.edit_pasi_id.text()
            dicParam['Columns'] = ['pasi_id','pasi_nm','svc_id','svc_nm','site_cd','bas_url','bas_svc_url','exmp_url','parm_load_func_nm']
            dicParam['Headers'] = ['파싱ID', '파싱명','서비스ID', '서비스명', '사이트코드', '기본URL','기존서비스URL','예제URL','인자로드함수명']
            dicParam['Widths'] = {'pasi_id' : 100, 'pasi_nm' : 100, 'svc_id' : 70, 'svc_nm' : 100, 'site_cd' : 120, 'bas_url' : 100,
                                   'bas_svc_url' : 100, 'exmp_url' : 1000, 'parm_load_func_nm':100}
            dicParam['tableClass'] = DAO.KADM.SvcPasi
            dicParam['Function'] = 'Server.COM.getPasiFinder'
            result = finderPop(self,dicParam)
            if isNotNull(result):
                self.result = result
                self.svc_id = result['svc_id']
                setDic2Edit(self,result)
                self.search()
        except: error()

    def search(self):
        try:
            if self.preSearch():
                Columns = ['PASI_ID','ITEM_NM', 'ITEM_VAL', 'TBL_NM', 'COL_NM', 'ITEM_DESC']
                Widths = {'PASI_ID':100,'ITEM_NM':120, 'ITEM_VAL':100, 'TBL_NM':150, 'COL_NM':150, 'ITEM_DESC':200}
                SetDic = {'svc_id': self.svc_id,'in_out_cl_cd':'I'}
                self.pasi_id = self.edit_pasi_id.text()
                self.twIn.setBasic(columns = Columns, widths = Widths, tableClass = SvcPasiItem, setDic = SetDic)
                self.twIn.setListTable(self.getSvcPasiItem(self.svc_id,self.pasi_id,'I'))

                Columns2 = ['PASI_ID','ITEM_NM', 'ITEM_VAL', 'ITEM_SRC_CL_CD', 'TBL_NM', 'COL_NM', 'ITEM_DESC']
                Widths2 = {'PASI_ID':100,'ITEM_NM':120, 'ITEM_VAL':100, 'ITEM_SRC_CL_CD':70, 'TBL_NM':150, 'COL_NM':150, 'ITEM_DESC':200}
                SetDic2 = {'svc_id': self.svc_id, 'in_out_cl_cd': 'O'}
                self.twOut.setBasic(columns = Columns2, widths = Widths2, tableClass = SvcPasiItem, setDic = SetDic2)
                self.twOut.setListTable(self.getSvcPasiItem(self.svc_id,self.pasi_id,'O'))
        except : error()

    def preSearch(self):
        if isNull(self.svc_id):
            alert("서비스ID 값이 없습니다.")
            return False
        if isNull(self.edit_pasi_id.text()):
            alert("파싱ID가 없습니다.")
            return False
        return True

    def getSvcPasiItem(self,strSvcId,strPasiId,InOutClCd):
        return Server.COM.getSvcPasiItem(strSvcId,strPasiId,InOutClCd)

    def save(self):
        try:
            if self.preSave():
                #소문자 세팅
                for n in range(self.twIn.rowCount): self.twIn.setTextByColName(n,"col_nm",str(self.twIn.getTextByColName(n,"col_nm")).lower())
                for n in range(self.twOut.rowCount):self.twOut.setTextByColName(n,"col_nm",str(self.twOut.getTextByColName(n,"col_nm")).lower())
                self.twIn.mergeList()
                self.twOut.mergeList()
        except : error()

    def preSave(self):
        for n in range(0,self.twIn.rowCount()):
            if isNull(self.twIn.getTextByColName(n, "item_nm")):
                alert('아이템명이 없습니다.')
                return False
        return True

    def addIn(self):
        try:
            n = self.twIn.addTWRow()
            for m, col in enumerate(self.twIn.columns):
                self.twIn.setTextByColName(n,"pasi_id",self.pasi_id)
        except : error()

    def addInDefault(self):
        try:
            n = self.twIn.addTWRow()
            self.twIn.setTextByColName(n, "pasi_id", 'default')
        except : error()

    def delIn(self):
        try:
            if self.preDelIn():
                self.twIn.deleteRow()
        except: error()

    def preDelIn(self):
        if self.twIn.currentItem() == None:
            alert("iN 항목을 선택하셔야합니다.")
            return False
        return True

    def addOut(self):
        try:
            n = self.twOut.addTWRow()
            self.twOut.setTextByColName(n,"pasi_id",self.edit_pasi_id.text())
        except : error()

    def addOutDefault(self):
        try:
            n = self.twOut.addTWRow()
            self.twOut.setTextByColName(n, "pasi_id", 'default')
        except : error()

    def delOut(self):
        try:
            if self.preDelOut():
                self.twOut.deleteRow()
        except: error()

    def preDelOut(self):
        if self.twOut.currentItem() == None:
            alert("OUT 항목을 선택하셔야합니다.")
            return False
        return True

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMDEV050()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()