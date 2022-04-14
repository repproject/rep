from PyQt5.QtWidgets import QTableView
import Server.COM
from Server.Basic import *
from UI._uiFiles.UIBasic import *
from common.ui.comUi import *
from DAO.KADM import *
import sys

pgm_id = 'KCOMBAT010'
pgm_nm = '배치관리'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMBAT010(QWidget, KWidget, form_class) :
    job_id = None
    JobSchdExec = None

    def __init__(self):
        try:
            super().__init__()
            self.initUI()
        except: error()

    def initUI(self):
        self.twJob.clicked.connect(self.searchJobSchd)
        self.twJobSchd.clicked.connect(self.searchJobSchdExec)
        self.btn_add_job.clicked.connect(self.addJob)
        self.btn_add_jobSchd.clicked.connect(self.addJobSchd)
        self.btn_save.clicked.connect(self.save)

        Columns = ['job_id', 'job_nm', 'job_desc', 'job_cl_cd', 'use_yn', 'ref1', 'ref2', 'ref3', 'ref4', 'ref5']
        Widths = {'job_id':120, 'job_nm':150, 'job_desc':150, 'job_cl_cd':150, 'use_yn' : 50, 'ref1':50, 'ref2':50, 'ref3':50, 'ref4':50, 'ref5':50}
        self.twJob.setBasic(columns = Columns,widths = Widths,tableClass = Job)

        #set TableWidget by listTable
        self.twJob.setListTable(self.getJob())

        #Table Widget Setting
        #self.twJob.resizeRowsToContents()
        #self.twJob.resize()

    def getJob(self):
        return Server.COM.getJob()

    def searchJobSchd(self):
        self.job_id = self.twJob.getTextByColName(self.twJob.currentRow(), "job_id")

        Columns = ['job_seq','EXEC_PERD_CD','EXEC_MM','EXEC_DD','EXEC_HH','EXEC_MI','EXEC_DAY_CD','CYCL_MI','IMDI_EXEC_YN','USE_YN','DEL_YN','CHG_YN']
        Widths = {'job_seq':30,'EXEC_PERD_CD':80,'EXEC_MM':65,'EXEC_DD':65,'EXEC_HH':65,'EXEC_MI':65,'EXEC_DAY_CD':80,'CYCL_MI':65,'IMDI_EXEC_YN':115,'USE_YN':80,'DEL_YN':80,'CHG_YN':80}
        SetDic = {'job_id': self.job_id}
        self.twJobSchd.setBasic(columns = Columns,widths = Widths,tableClass = JobSchd,setDic=SetDic)
        self.twJobSchd.setListTable(self.getJobSchd(self.job_id))

        # Table Widget Setting
        self.twJobSchd.resizeRowsToContents()

        self.edit_exec_parm1.setText(None)
        self.edit_exec_parm2.setText(None)
        self.edit_exec_parm3.setText(None)
        self.edit_exec_parm4.setText(None)
        self.edit_exec_parm5.setText(None)
        self.edit_exec_parm6.setText(None)
        self.edit_exec_parm7.setText(None)
        self.edit_exec_parm8.setText(None)
        self.edit_exec_parm9.setText(None)
        self.edit_exec_parm10.setText(None)

    def getJobSchd(self,strJobId):
        return Server.COM.getJobSchd(strJobId)

    def searchJobSchdExec(self):
        strJobSeq = self.twJobSchd.getTextByColName(self.twJobSchd.currentRow(), "job_seq")
        self.JobSchdExec = self.getJobSchdExec(self.job_id,strJobSeq)
        if isNotNull(self.JobSchdExec):
            setTable2Edit(self, self.JobSchdExec[0])
        else:
            self.edit_exec_parm1.setText(None)
            self.edit_exec_parm2.setText(None)
            self.edit_exec_parm3.setText(None)
            self.edit_exec_parm4.setText(None)
            self.edit_exec_parm5.setText(None)
            self.edit_exec_parm6.setText(None)
            self.edit_exec_parm7.setText(None)
            self.edit_exec_parm8.setText(None)
            self.edit_exec_parm9.setText(None)
            self.edit_exec_parm10.setText(None)

    def getJobSchdExec(self,strJobId,strJobSeq):
        return Server.COM.getJobSchdExec(strJobId,int(strJobSeq))

    def addJob(self):
        try:
            n = self.twJob.addTWRow()
        except : error()

    def addJobSchd(self):
        try:
            if self.preAddJobSchd():
                n = self.twJobSchd.addTWRow()
                if n > 0:
                    self.twJobSchd.setTextByColName(n, "job_seq",int(self.twJobSchd.getTextByColName(n - 1, 'job_seq')) + 1)
                else: self.twJobSchd.setTextByColName(n, "job_seq",1)
                self.twJobSchd.setTextByColName(n, "use_yn", 'Y')
                self.twJobSchd.setTextByColName(n, "del_yn", 'N')
                self.twJobSchd.setTextByColName(n, "imdi_exec_yn", 'N')
                self.twJobSchd.setTextByColName(n, "chg_yn", 'N')

        except : error()

    def preAddJobSchd(self):
        if self.twJob.currentRow() == -1:
            alert("Job을 선택해야합니다.")
            return False
        return True

    def save(self):
        try:
            if self.preSave():
                self.twJob.mergeRow()
                if self.twJobSchd.currentRow() > -1:
                    self.twJobSchd.mergeRow()
                    if isNull(self.JobSchdExec):
                        dicParam = {}
                        dicParam['job_id'] = self.job_id
                        dicParam['job_seq'] = self.twJobSchd.getTextByColName(self.twJobSchd.currentRow(), "job_seq")
                        kwargs = {**dicParam}
                        self.JobSchdExec = JobSchdExec(**kwargs)

                    setEdit2Table(self,self.JobSchdExec[0])
                    merge(self.JobSchdExec[0])

                else:
                    alert("Job 스케쥴이 미선택 되었습니다.")
                    return False
        except : error()

    def preSave(self):
        if self.twJob.currentRow() == -1:
            alert("Job을선택해야합니다.")
            return False
        return True

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = KCOMBAT010()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()