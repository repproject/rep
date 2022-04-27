from UI._uiFiles.UIBasic import *
from PyQt5.QtWidgets import QTableView
import common.database.Relfect
from DAO.KADM import *


pgm_id = 'KCOMDEV040'
pgm_nm = '테이블관리'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMDEV040(QWidget, KWidget, form_class) :
    meta = None
    isAllSearch = False #조회여부를 판단하기 위한 문구

    def __init__(self):
        try:
            super().__init__()
            self.initUI()
        except : error()

    def initUI(self):
        self.btn_search.clicked.connect(self.search)
        self.btn_add_tbl.clicked.connect(self.addTbl)
        self.btn_save_tbl.clicked.connect(self.saveTbl)
        self.btn_del_tbl.clicked.connect(self.delTbl)
        self.btn_reflect_tbl.clicked.connect(self.reflectTbl)
        self.twTbl.clicked.connect(self.search2)
        self.btn_reflect_col.clicked.connect(self.reflectCol)
        self.btn_save_col.clicked.connect(self.saveCol)
        self.btn_del_col.clicked.connect(self.delCol)
        #self.twCol.clicked.connect(self.search2)

    def search(self):
        try:
            Columns = ['tbl_nm', 'tbl_desc', 'cls_nm']
            Widths = {'tbl_nm':120, 'tbl_desc':250, 'cls_nm':60}
            self.twTbl.setBasic(columns = Columns, widths = Widths, tableClass = Tbl)
            self.twTbl.setListTable(self.getTblLst(self.edt_tbl_nm.text(),self.edt_tbl_desc.text(),self.edt_col_nm.text(),self.edt_col_desc.text()))
        except : error()

    def getTblLst(self,strTblNm,strTblDesc,strColNm,strColDesc):
        if len(strTblNm) == 0 and len(strTblDesc) == 0 and len(strColNm) == 0 and len(strColDesc) == 0:
            self.isAllSearch = True
        return Server.COM.getTblLst(strTblNm,strTblDesc)

    def reflectTbl(self):
        try:
            isExistNewReflect = False
            if self.preReflectTbl():
                self.meta = common.database.Relfect.makeMeta()
                for tblNm in self.meta.tables.keys():
                    isExist = False
                    for i in range(0,self.twTbl.rowCount()):
                        if self.twTbl.item(i,0).text() == tblNm: isExist = True
                    if isExist == False:
                        n = self.twTbl.addTWRow()
                        self.twTbl.setTextByColName(n,"tbl_nm",tblNm)
                        self.twTbl.setTextByColName(n,"tbl_desc",self.meta.tables[tblNm].comment)
                        clsNm = ''
                        i = 0
                        for t in str(tblNm).split('_'):
                            if i > 0:
                                clsNm = clsNm + t[0].upper()
                                clsNm = clsNm + t[1:].lower()
                            i=i+1
                        self.twTbl.setTextByColName(n, "cls_nm", clsNm)
                        isExistNewReflect = True
                if isExistNewReflect == False: alert('반영할 테이블이 없습니다.')
        except: error()

    def preReflectTbl(self):
        if self.isAllSearch == False:
            alert('전체 조회 후 Reflect 가능합니다.')
            return False
        return True

    def search2(self):
        try:
            strTblNm = self.twTbl.getTextByColName(self.twTbl.currentRow(),"tbl_nm")

            Columns = ['col_nm', 'COL_HAN_NM','COL_DOMA_CD','COL_DOMA_VAL','COL_SEQ','PANT_TBL_NM','PANT_COL_NM','PK_YN','BAS_VAL','COL_DESC']
            Widths = {'col_nm':140, 'COL_HAN_NM':100 , 'COL_DOMA_CD':60,'COL_DOMA_VAL':90,'COL_SEQ':30,'PANT_TBL_NM':80,'PANT_COL_NM':80,'PK_YN':30,'BAS_VAL':70,'COL_DESC':100}
            SetDic = {'tbl_nm':strTblNm}

            self.twCol.setBasic(columns = Columns, widths = Widths, tableClass = TblCol, setDic = SetDic)
            self.twCol.setListTable(self.getColLst(strTblNm))

            #Table Widget Setting
            self.twCol.resizeRowsToContents()
        except : error()

    def getColLst(self,strTblNm): return Server.COM.getColLst(strTblNm)

    def reflectCol(self):
        try:
            if self.preReflectCol():
                isExistNewReflect = False
                strTblNm = self.twTbl.getTextByColName(self.twTbl.currentRow(), "tbl_nm")
                self.meta = common.database.Relfect.makeMeta()
                dicRtn = self.getParentTblCol(strTblNm)
                for col in self.meta.tables[strTblNm].c:
                    colname = str(col).split('.')[1].lower()
                    isExist = False
                    for i in range(0,self.twCol.rowCount()):
                        if self.twCol.getCellObject(i,0).text() == colname: isExist = True
                    if isExist == False:
                        n = self.twCol.addTWRow()
                        self.twCol.setTextByColName(n,"col_seq", str(self.twCol.rowCount()))
                        if colname.split('_')[-1] == "cd":
                            self.twCol.setTextByColName(n, "col_doma_cd", "코드")
                            strCd = "_".join(colname.split('_')[:-1]).upper()
                            if self.getComCdLst(strCd) != None:
                                self.twCol.setTextByColName(n, "col_doma_val", strCd)
                        else:
                            self.twCol.setTextByColName(n,"col_doma_cd", "없음")
                        self.twCol.setTextByColName(n,"col_nm",colname)
                        self.twCol.setTextByColName(n,"col_han_nm",col.comment)
                        if col.primary_key : self.twCol.setTextByColName(n,"pk_yn",'Y')
                        else : self.twCol.setTextByColName(n,"pk_yn",'N')
                        if col.server_default != None : self.twCol.setTextByColName(n,"bas_val",col.server_default.arg.text.replace("'",""))
                        if colname in dicRtn.keys():
                            self.twCol.setTextByColName(n, "pant_tbl_nm", dicRtn[colname])
                            self.twCol.setTextByColName(n, "pant_col_nm", colname)

                        isExistNewReflect = True
        except: error()

    def getComCdLst(self,strCd): return Server.COM.getComCdLst(strCd)

    def getParentTblCol(self,strTblNm):
        pantTblNm = "_".join(strTblNm.split('_')[:-1])
        if len(pantTblNm) == 0: return {}
        TblCol = Server.COM.getTblColParentPK(pantTblNm)
        if len(TblCol) == 0 : return {}
        dicRtn = {}
        for tc in TblCol:
            dicRtn[tc.col_nm] = tc.tbl_nm
        return dicRtn

    def preReflectCol(self):
        if self.twTbl.currentRow() == -1:
            alert('테이블 선택 후 Reflect 가능합니다.')
            return False
        return True

    def saveTbl(self):
        try:
            if self.preSave():
                self.twTbl.mergeList()
        except : error()

    def preSave(self):
        for n in range(0,self.twTbl.rowCount()):
            if self.twTbl.getTextByColName(n, "tbl_nm") == None:
                alert('테이블명이 없습니다.')
                return False
        return True

    def saveCol(self):
        try:
            if self.preSaveCol():
                self.twCol.mergeList()
                self.search2()
        except : error()

    def preSaveCol(self):
        if self.twTbl.currentRow() == -1:
            alert('테이블 선택 후 저장 가능합니다.')
            return False

        for n in range(0,self.twCol.rowCount()):
            colNm = self.twCol.getTextByColName(n, "col_nm")
            if colNm == None:
                alert('컬럼명이 없습니다.')
                return False
            if self.twCol.getTextByColName(n, "col_doma_cd") == "코드" and self.twCol.getTextByColName(n, "col_doma_val" == None):
                alert('코드는 도메인 값이 필수입니다.')
                return False
        return True

    def addTbl(self):
        try:
            self.twTbl.addTWRow()
        except : error()

    def delTbl(self):
        try:
            if self.preDelTbl():
                self.twTbl.deleteRow()
        except: error()

    def preDelTbl(self):
        if self.twTbl.currentItem() == None:
            alert("테이블을 선택하셔야합니다.")
            return False

        if self.twTbl.getRowTable(self.twTbl.currentRow()) != None:
            alert("신규로 생성한 행만 삭제 가능합니다.")
            return False
        return True

    def delCol(self):
        try:
            if self.preDelCol():
                self.twCol.deleteRow()
        except: error()

    def preDelCol(self):
        if self.twCol.currentItem() == None:
            alert("컬럼을 선택하셔야합니다.")
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
    myWindow = KCOMDEV040()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()