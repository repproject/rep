from PyQt5.QtWidgets import QTableView
import Server.COM
from common.ui.comUi import *
from UI._uiFiles.UIBasic import *
from Server.Basic import *
from DAO.KADM import *

pgm_id = 'KCOMBAT020'
pgm_nm = '작업액션기능관리'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMBAT020(QWidget, KWidget, form_class) :
    def __init__(self):
        try:
            super().__init__()
            self.initUI()
        except : error()

    def initUI(self):

        self.btn_add_job.clicked.connect(self.addJob)
        self.btn_save_job.clicked.connect(self.saveJob)
        self.btn_add_act.clicked.connect(self.addAct)
        self.btn_save_act.clicked.connect(self.saveAct)
        self.btn_add_func.clicked.connect(self.addFunc)
        self.btn_save_func.clicked.connect(self.saveFunc)

        self.twJob.clicked.connect(self.searchJobAct)
        self.btn_add_job_act.clicked.connect(self.addJobAct)
        self.btn_save_job_act.clicked.connect(self.saveJobAct)

        self.twAct.clicked.connect(self.searchActFunc)
        self.twJobAct.clicked.connect(self.searchActFunc)
        self.btn_add_act_func.clicked.connect(self.addActFunc)
        self.btn_save_act_func.clicked.connect(self.saveActFunc)

        self.twFunc.clicked.connect(self.searchFuncTbl)
        self.twActFunc.clicked.connect(self.searchFuncTbl)
        self.btn_add_func_tbl.clicked.connect(self.addFuncTbl)
        self.btn_save_func_tbl.clicked.connect(self.saveFuncTbl)

        Columns = ['job_id', 'job_nm', 'job_desc', 'job_cl_cd', 'use_yn', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
        Widths = {'job_id':100, 'job_nm':150, 'job_desc':150, 'job_cl_cd':150, 'use_yn':50, 'ref1':50, 'ref2':50, 'ref3':50, 'ref4':50, 'ref5':50}
        self.twJob.setBasic(columns = Columns,widths = Widths,tableClass = Job)

        self.searchJob()

        Columns = ['act_id', 'act_nm', 'act_desc', 'use_yn', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
        Widths = {'act_id':100, 'act_nm':150, 'act_desc':150, 'use_yn':50, 'ref1':50, 'ref2':50, 'ref3':50, 'ref4':50, 'ref5':50}
        self.twAct.setBasic(columns = Columns,widths = Widths,tableClass = Act)

        self.searchAct()

        Columns3 = ['func_id', 'func_nm', 'func_desc', 'func_cl_cd', 'src_func_nm', 'use_yn', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
        Widths3 = {'func_id':150, 'func_nm':200, 'func_desc':150, 'func_cl_cd':100, 'src_func_nm':200, 'use_yn':50, 'ref1':50, 'ref2':50, 'ref3':50, 'ref4':50, 'ref5':50}
        self.twFunc.setBasic(columns = Columns3,widths = Widths3,tableClass = Func)

        self.searchFunc()

    def searchJob(self):
        try:
            self.twJob.setListTable(self.getJob())
            #Table Widget Setting
            self.twJobAct.removeAll()
            self.twActFunc.removeAll()
            self.twFuncTbl.removeAll()
        except : error()

    def getJob(self) : return Server.COM.getJob()

    def addJob(self):
        try:
            self.twJob.addTWRow()
        except : error()

    def saveJob(self):
        try:
            if self.preSaveJob():
                self.twJob.mergeRow()
        except : error()

    def preSaveJob(self):
        if self.twJob.currentRow() == -1:
            alert("Job을 선택해야합니다.")
            return False
        return True

    def searchAct(self):
        try:
            self.twAct.setListTable(self.getAct())
            #Table Widget Setting
            self.twActFunc.removeAll()
            self.twFuncTbl.removeAll()
        except : error()

    def getAct(self) : return Server.COM.getAct()

    def addAct(self):
        try:
            n = self.twAct.addTWRow()
            self.twAct.setTextByColName(n, 'use_yn', 'Y')
        except : error()

    def saveAct(self):
        try:
            if self.preSaveAct():
                self.twAct.mergeRow()
        except : error()

    def preSaveAct(self):
        if self.twAct.currentRow() == -1:
            alert("Act를 선택해야합니다.")
            return False
        return True

    def searchFunc(self):
        try:
            self.twFunc.setListTable(self.getFunc())
            #Table Widget Setting
            self.twFuncTbl.removeAll()
        except : error()

    def getFunc(self) : return Server.COM.getFunc()

    def addFunc(self):
        try:
            self.twFunc.addTWRow()
        except : error()

    def saveFunc(self):
        try:
            if self.preSaveFunc():
                self.twFunc.mergeRow()
        except : error()

    def preSaveFunc(self):
        if self.twFunc.currentRow() == -1:
            alert("Func를 선택해야합니다.")
            return False
        return True

    def searchJobAct(self):
        try:
            strJobId = self.twJob.getTextByColName(self.twJob.currentRow(),"job_id")
            Columns3 = ['ACT_ID', 'JOB_ACT_REL_DESC', 'EXEC_SEQ', 'USE_YN']
            Widths3 = {'ACT_ID':100, 'JOB_ACT_REL_DESC':200, 'EXEC_SEQ':70, 'USE_YN':50}
            SetDic = {'job_id':strJobId}
            self.twJobAct.setBasic(columns=Columns3, widths=Widths3, tableClass=JobAct, setDic=SetDic)
            self.twJobAct.setListTable(self.getJobAct(strJobId))

            #Table Widget Setting
            self.twActFunc.removeAll()
            self.twFuncTbl.removeAll()

        except : error()

    def getJobAct(self,strJobId) : return Server.COM.getJobAct(strJobId)

    def addJobAct(self):
        try:
            if self.preaddJobAct():
                act_id = self.twAct.getTextByColName(self.twAct.currentRow(),'act_id')
                n = self.twJobAct.addTWRow()
                self.twJobAct.setTextByColName(n, 'act_id', act_id)
                self.twJobAct.setTextByColName(n, 'use_yn', 'Y')
                if n == 0: self.twJobAct.setTextByColName(n, 'exec_seq', 1)
                else : self.twJobAct.getTextByColName(n-1, 'exec_seq')
        except : error()

    def preaddJobAct(self):
        if self.twJob.currentRow() == -1:
            alert("Job을 선택해야합니다.")
            return False
        if self.twAct.currentRow() == -1:
            alert("Act를 선택해야합니다.")
            return False
        act_id = self.twAct.getTextByColName(self.twAct.currentRow(), 'act_id')
        for i in range(self.twJobAct.rowCount()):
            if self.twJobAct.getTextByColName(i, 'act_id') == act_id:
                alert("중복된 Act 입니다.")
                return False

        return True

    def saveJobAct(self):
        try:
            if self.preSaveJobAct():
                self.twJobAct.mergeRow()
        except : error()

    def preSaveJobAct(self):
        if self.twJobAct.currentRow() == -1:
            alert("JobAct를 선택해야합니다.")
            return False
        return True

    def searchActFunc(self):
        try:
            strActId = self.sender().getTextByColName(self.sender().currentRow(),"act_id")
            Columns3 = ['FUNC_ID','ACT_FUNC_REL_DESC','EXEC_SEQ','USE_YN']
            Widths3 = {'FUNC_ID':100,'ACT_FUNC_REL_DESC':200,'EXEC_SEQ':50,'USE_YN':50}
            SetDic = {'act_id':strActId}
            self.twActFunc.setBasic(columns=Columns3, widths=Widths3, tableClass=ActFunc, setDic=SetDic)

            self.twActFunc.setListTable(self.getActFunc(strActId))
            #Table Widget Setting
            self.twFuncTbl.removeAll()
        except : error()

    def getActFunc(self,strActId) : return Server.COM.getActFunc(strActId)

    def addActFunc(self):
        try:
            if self.preaddActFunc():
                func_id = self.twFunc.getTextByColName(self.twFunc.currentRow(),'func_id')
                n = self.twActFunc.addTWRow()
                self.twActFunc.setTextByColName(n, 'func_id', func_id)
                self.twActFunc.setTextByColName(n, 'use_yn', 'Y')
                if n == 0: self.twActFunc.setTextByColName(n, 'exec_seq', 1)
                else : self.twActFunc.getTextByColName(n-1, 'exec_seq')
        except : error()

    def preaddActFunc(self):
        if isNull(self.twActFunc.setDic.get('act_id',None)):
            alert("Act를 선택해야합니다.")
            return False
        return True

    def saveActFunc(self):
        try:
            if self.preSaveActFunc():
                self.twActFunc.mergeRow()
        except : error()

    def preSaveActFunc(self):
        if self.twActFunc.currentRow() == -1:
            alert("Action을 선택해야합니다.")
            return False
        return True

    def searchFuncTbl(self):
        try:
            strFuncId = self.sender().getTextByColName(self.sender().currentRow(),"func_id")
            Columns3 = ['TBL_NM','tbl_desc','FINL_CHG_YYMM','FINL_CHG_YMD']
            Widths3 = {'TBL_NM':200,'tbl_desc':200,'FINL_CHG_YYMM':100,'FINL_CHG_YMD':100}
            SetDic = {'func_id':strFuncId}
            self.twFuncTbl.setBasic(columns=Columns3, widths=Widths3, tableClass=FuncTgtTbl, setDic=SetDic)

            self.twFuncTbl.setListTable(self.getFuncTbl(strFuncId))
            #Table Widget Setting
        except : error()

    def getFuncTbl(self,strFuncId) : return Server.COM.getFuncTbl(strFuncId)

    def addFuncTbl(self):
        try:
            if self.preaddFuncTbl():
                self.twFuncTbl.addTWRow()
        except : error()

    def preaddFuncTbl(self):
        if isNull(self.twFuncTbl.setDic.get('func_id',None)):
            alert("Func를 선택해야합니다.")
            return False
        return True

    def saveFuncTbl(self):
        try:
            if self.preSaveFuncTbl():
                self.twFuncTbl.mergeRow()
        except : error()

    def preSaveFuncTbl(self):
        if self.twFuncTbl.currentRow() == -1:
            alert("행을 선택해야합니다.")
            return False
        return True

    # def addJobActSelection(self):
    #     try :
    #         if self.preAddJobActSelection():
    #             act_id = self.twAct.getTextByColName(self.twAct.currentRow(),'act_id')
    #             n = self.twJobAct.addTWRow()
    #             self.twJobAct.setTextByColName(n,'act_id',act_id)
    #     except: error()
    #
    # def preAddJobActSelection(self):
    #     if self.twJob.currentRow() == -1:
    #         alert("Job을 선택하셔야합니다.")
    #         return False
    #     if self.twAct.currentRow() == -1:
    #         alert("Act를 선택하셔야합니다.")
    #         return False
    #     return True

























    def searchSvc(self):
        try:
            strSiteCd = self.sender().getTextByColName(self.sender().currentRow(),"site_cd")

            Columns = ['svc_id', 'BAS_SVC_URL', 'REQ_WAY_CD', 'exmp_url', 'SVC_DESC']
            Widths = {'svc_id': 150, 'BAS_SVC_URL': 300, 'REQ_WAY_CD': 70, 'exmp_url': 300, 'SVC_DESC': 300}
            SetDic = {'site_cd': strSiteCd}
            self.twSvc.setBasic(columns=Columns, widths=Widths, tableClass=Svc, setDic=SetDic)

            self.twSvc.setListTable(self.getSvc(strSiteCd))
            self.twSvcPasi.removeAll()
        except: error()

    def searchSvcPasi(self):
        try:
            strSvcId = self.twSvc.getTextByColName(self.twSvc.currentRow(),"svc_id")

            Columns = ['PASI_ID', 'PASI_NM', 'PASI_WAY_CD','PARM_LOAD_FUNC_NM','SVC_PASI_DESC']
            Widths = {'PASI_ID':120, 'PASI_NM':100,'PASI_WAY_CD':80,'PARM_LOAD_FUNC_NM':200,'SVC_PASI_DESC':150}
            SetDic = {'svc_id': strSvcId}

            self.twSvcPasi.setBasic(columns = Columns, widths = Widths, tableClass = SvcPasi, setDic=SetDic)
            self.twSvcPasi.setListTable(self.getSvcPasi(strSvcId))
        except: error()

    def getSvcPasi(self,strSvcId): return Server.COM.getSvcPasi(strSvcId)



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



    def getSites(self):
        return Server.COM.getSite()

    def getSvc(self,strSiteCd):
        return Server.COM.getSvc(strSiteCd)



    #def preJobActSelection(self):



if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMBAT020()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()