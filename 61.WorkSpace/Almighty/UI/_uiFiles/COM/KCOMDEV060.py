from UI._uiFiles.UIBasic import *
from PyQt5.QtWidgets import QTableView
import common.database.Relfect
from DAO.KADM import *

pgm_id = 'KCOMDEV060'
pgm_nm = '코드실행관리'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV060(QWidget, KWidget, form_class) :
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
        self.btn_save_2.clicked.connect(self.saveCdExec)
        self.btn_save.clicked.connect(self.save)

        self.btn_add_cd.clicked.connect(self.addCd)
        self.btn_del_cd.clicked.connect(self.delCd)

        self.clbPasiCdExec.clicked.connect(self.addPasiCd)
        self.btn_del_pasi.clicked.connect(self.delPasiCd)


        Columns = ['cd_exec_id', 'cd_exec_nm', 'cd_exec_cl_cd', 'exec_cd_cnts']
        Widths = {'cd_exec_id': 100, 'cd_exec_nm': 150, 'cd_exec_cl_cd': 100, 'exec_cd_cnts': 200}
        self.twCdExec.setBasic(columns=Columns, widths=Widths, tableClass=CdExec)
        self.search()

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
                self.pasi_id = result['pasi_id']
                setDic2Edit(self,result)
                self.search()
        except: error()

    def search(self):
        try:
            if self.preSearch():
                strCdExec = self.editCdExec.text()
                self.twCdExec.setListTable(self.getCdExec(strCdExec))

                self.svc_id = self.edit_svc_id.text()
                self.pasi_id = self.edit_pasi_id.text()
                Columns2 = ['seq','cd_exec_id', 'cd_exec_seq', 'up_seq', 'exec_parm_val']
                Widths2 = {'seq':100,'cd_exec_id':120, 'cd_exec_seq':100, 'up_seq':70, 'exec_parm_val':150}
                SetDic2 = {'svc_id': self.svc_id, 'pasi_id': self.pasi_id}
                self.twPasiCdExec.setBasic(columns = Columns2, widths = Widths2, tableClass = PasiCdExec, setDic = SetDic2)
                self.twPasiCdExec.setListTable(self.getPasiCdExec(self.svc_id,self.pasi_id))
        except : error()

    def preSearch(self):
        return True

    def getCdExec(self,strCdExec):return Server.COM.getCdExec(strCdExec)
    def getPasiCdExec(self,strSvcId,strPasiId):return Server.COM.getPasiCdExec(strSvcId,strPasiId)

    def saveCdExec(self):
        try:
            if self.preSaveCdExec():
                if self.twCdExec.getRowTable() == None:
                    self.twCdExec.insertRowDB()
                else:
                    self.twCdExec.mergeRow()
        except : error()

    def preSaveCdExec(self):
        if self.twCdExec.currentRow() == -1:
            alert('선택된 코드실행이 없습니다.')
            return False

        if isNull(self.twCdExec.getTextByColName(self.twCdExec.currentRow(),"cd_exec_id")):
            alert('코드실행ID가 빈값입니다')
            return False
        return True

    def addCd(self):
        try:
            n = self.twCdExec.addTWRow()
        except : error()

    def delCd(self):
        try:
            if self.predelCd():
                self.twCdExec.deleteRow()
        except: error()

    def predelCd(self):
        if self.twCdExec.currentItem() == None:
            alert("iN 항목을 선택하셔야합니다.")
            return False
        return True

    def addPasiCd(self):
        try:
            n = self.twPasiCdExec.addTWRow()
            self.twPasiCdExec.setTextByColName(n,"cd_exec_id",self.twCdExec.getTextByColName(self.twCdExec.currentRow(),"cd_exec_id"))
            self.twPasiCdExec.setTextByColName(n, "up_seq",0)
        except : error()

    def save(self):
        try:
            if self.preSave():
                self.twPasiCdExec.mergeRow(self.twPasiCdExec.currentRow())
        except : error()

    def preSave(self):
        if self.twPasiCdExec.currentRow() == -1:
            alert('선택된 파싱코드실행이 없습니다.')
            return False

        if isNull(self.twPasiCdExec.getTextByColName(self.twPasiCdExec.currentRow(),"cd_exec_id")):
            alert('코드실행ID가 빈값입니다')
            return False

        if isNull(self.twPasiCdExec.getTextByColName(self.twPasiCdExec.currentRow(),"seq")):
            alert('일련번호가 빈값입니다')
            return False
        return True

    def delPasiCd(self):
        try:
            if self.preDelPasiCd():
                self.twPasiCdExec.deleteRow()
        except: error()

    def preDelPasiCd(self):
        if self.twPasiCdExec.currentItem() == None:
            alert("OUT 항목을 선택하셔야합니다.")
            return False
        return True

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.search()
        else:
            pass

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMDEV060()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()