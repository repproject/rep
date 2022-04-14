from Server.Basic import *
import traceback
import copy
import Server.COM
import Server.module
from common.common.Func import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5 import QtGui

basic_ui_route = 'UI._uiFiles.COM'
basic_ui_dictionary = "C:/Users/Ceasar.DESKTOP-AQTREV4/PycharmProjects/rep/61.WorkSpace/Almighty/UI/_uiFiles/COM/"

###############공통코드################
dicCodeList ={} #코드목록
dicCode = {}

#############공통##################
class KWidget() :
    pgm_id = None

    def __init__(self):
        if hasattr(self,"setupUi"):
            self.setupUi(self)
        self.setQObjectToCustomizedClass()

    def setQObjectToCustomizedClass(self):
        for key in self.__dict__.keys():
            if self.__dict__[key].__class__ == QTableWidget:
                TableWidget.convert_to_TableWidget(self.__dict__[key])
                self.__dict__[key].init() #위함수로 init이 호출되지 않아 별도 호출

    def search(self):
        pass

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.search()
        else:
            pass

###############Edit#########################
def setTable2Edit(form,table):
    r"""
        Table 객체의 컬럼명과 일치하는 form에 존재하는 LineEdit의 text값을 setting한다.
        주로 DB에서 조회한 값을 세팅할 때 사용한다.
        전제조건 : LineEdit의 ObjectName이 edit_ + 컬럼명으로 시작해야한다.
    :param form: object of form
    :param table: one object of table
    :return: True/False
    """
    for col in table.__table__.c:
        colname = str(col).split('.')[1]
        try:
            text = str(getattr(table,colname))
            getattr(form,'edit_'+colname).setText(text)
        except AttributeError as ae:
            setTable2EditErrorList = (
            "object has no attribute 'edit_reg_user_id'",
            "object has no attribute 'edit_reg_dtm'",
            "object has no attribute 'edit_chg_user_id'",
            "object has no attribute 'edit_chg_dtm'")
            if str(ae)[13:] not in setTable2EditErrorList: error()
        except : error()
    return True

def setDic2Edit(form,dic):
    r"""
        Dictionary의 key값과 일치하는 form에 존재하는 LineEdit의 text값을 setting한다.
        주로 DB에서 조회한 값을 세팅할 때 사용한다.
        전제조건 : LineEdit의 ObjectName이 edit_ + 컬럼명으로 시작해야한다.
    :param form: object of form
    :param dic : dictionary
    :return: True/False
    """
    for key in dic.keys():
        try:
            text = dic[key]
            getattr(form,'edit_'+key).setText(text)
        except AttributeError as ae: pass
        except : error()
    return True

def setEdit2Table(form,table):
    r"""
        form에 존재하는 LineEdit 객체의 text값을 Table객체 값으로 반환한다.
        주로 변경된값을 DB에 반영하기 위해 사용한다.
    :param form: object of form
    :param table: one object of table
    :return: True
    """
    for col in table.__table__.c:
        colname = str(col).split('.')[1]
        try:
            text = getattr(form,"edit_"+colname).text()
            setattr(table,colname,text)
        except AttributeError as ae : pass
        except : error()
    return True

def error():logging.error(traceback.format_exc())

############### Code ################
def setCode(grp):   #코드세팅
    r"""
        공통코드그룹ID를 받아 공통코드 공통리스트 전역변수에 반영한다.
    :param grp : 공통코드그룹ID
    :return: True/False
    """
    if grp not in dicCodeList.keys():
        result = Server.COM.getCodeDtl(grp)
        code = {}
        for cd in result:
            code[cd.com_cd] = cd.com_cd_nm
        dicCodeList[grp] = code
        return True
    else:
        return False

def getCode(grp):
    r"""
        공통코드그룹ID로 코드값을 dictionary로 return 한다.
    :param grp : 공통코드그룹ID
    :return: dictionary {com_cd:com_cd_nm}
    """
    #이미 코드가 존재하면 존재하는 리스트값으로 return
    if grp in dicCodeList.keys(): return dicCodeList[grp]
    setCode(grp)
    return dicCodeList[grp]

############Table############
class TableListBind():
    listTable = []
    columns = None
    tableClass = None
    dicColAttr = {}
    setDic = {}
    isRowType = False
    isSet = False

    def __init__(self, listTable=None, columns=None):
        try:
            super().__init__()
            self.setColumns(columns)
            self.setlistTable(listTable)
            self.setDic = copy.deepcopy(dict())
        except : error()

    def setListTable(self, listTable):
        if isNull(self.getColumns()):
            logging.error("setListTable 지정된 컬럼이 없습니다. setColumns, setBasic이 필수입니다.")
            raise TypeError
            return False

        self.listTable = listTable
        self.setIsRowType()
        self.setDicColAttr()
        self.isSet = True

    def setIsRowType(self):
        r"""
            Query에 대한 result가 Row Class(주로 MultiTable인경우 해당)을 구분하기 위해
            isRowType 변수를 세팅하는 함수. 바인딩된 listTable이 초기화 되는 경우 실행 필요
        :return:
        """
        if self.listTable != None:
            if len(self.listTable) > 0 :
                if str(type(self.listTable[0])) == "<class 'sqlalchemy.engine.row.Row'>":
                    self.isRowType = True
                else : self.isRowType = False
            else: self.isRowType = False
        else : self.isRowType = False

    def setColumns(self, columns):
        self.columns = []
        for col in columns:
            self.columns.append(col.lower())
        self.setDicColAttr()

    def setDicColAttr(self):
        r"""
            컬럼으로부터 필요한 정보를 가져오기 위한 세팅 정보
            1. 테이블이 여러개인 경우 어떤 순서의 테이블이 필요한지 정의
        :return:
        """
        if self.isRowType:
            for i,tb in enumerate(self.listTable[0]):
                for col in tb.__table__.c:
                    colName = str(col).split('.')[1]
                    if self.dicColAttr.get(colName):
                        if self.dicColAttr[colName].get('isCompleteSet',False) == False:
                            self.dicColAttr[colName] = {}
                            self.dicColAttr[colName]['tablename'] = tb.__class__.__name__
                            self.dicColAttr[colName]['tableClass'] = tb.__class__
                            self.dicColAttr[colName]['tableseq'] = i #사용
                            self.dicColAttr[colName]['isCompleteSet'] = True #사용
        else:
            for colname in self.columns:
                self.dicColAttr[colname] = {}
                self.dicColAttr[colname]['tablename'] = self.tableClass.__name__
                self.dicColAttr[colname]['tableClass'] = self.tableClass
                self.dicColAttr[colname]['tableseq'] = -1  # 사용
                self.dicColAttr[colname]['isCompleteSet'] = False

    def getTableSeqByColName(self,colname):
        r"""
            sql로 받은 result의 table이 몇번째인지
        :param colname: 컬럼명
        :return:
        """
        if self.isRowType:
            return self.dicColAttr[colname]['tableseq']
        else : return -1

    def getTableClass(self,colname):
        r"""
            해당 컬럼이 어떤 tableClass인지 확인
        :param colname: 컬럼명
        :return:
        """
        if self.isRowType:
            return self.dicColAttr[colname]['tableClass']
        else : return None

    def setSetDic(self,setdic):
        r"""
            테이블을 저장하기 위해 기본적으로 세팅해야 하는 컬럼값을 정의
            주로 PK가 해당
        :param setdic:
        :return:
        """
        sd = {}
        for key in setdic.keys():
             sd[key.lower()] = setdic[key]
        self.setDic = copy.deepcopy(sd)

    def setTableClass(self, tableClass):
        if tableClass != None:
            self.tableClass = tableClass
            Server.COM.setCodeByTable(tableClass)

    def getColumns(self):              return self.columns
    def getlistTable(self):            return self.listTable
    def getTableByColSeq(self,colname,table):
        if self.isRowType:
            return table[self.getTableSeqByColName(colname)]
        else : return table

class TableBind():
    table = None
    colName = None

    def __init__(self, table=None, colName=None):
        try:
            self.setTable(table)
            self.setColName(colName)
        except : error()

    def setTable(self, table):     self.table = table
    def setColName(self, colName): self.colName = colName
    def getColName(self):          return self.colName
    def getTable(self):            return self.table

############TableWidget##############
class TableWidgetItem(QTableWidgetItem,TableBind):
    def __init__(self,text=None,table=None,colName=None):
        try:
            QTableWidgetItem.__init__(self,text)
            TableBind.__init__(self,table,colName)
        except : error()

class TableWidget(QTableWidget,TableListBind):
    widths = {}
    algins = {}

    def __init__(self,table = None, listTable = None, columns = None):
        try:
            super(TableWidget,self).__init__(listTable,columns)
            self.init()
        except : error()

    def init(self):
        self.setQObjectToCustomizedClass()

    def setQObjectToCustomizedClass(self):
        # print(self.__dict__.keys())
        for key in self.__dict__.keys():
            # QTableWidget to customized TableWidget
            # print(key)
            # print(self.__dict__[key].__class__)
            if self.__dict__[key].__class__ == QTableWidget:
                TableWidget.convert_to_TableWidget(self.__dict__[key])
                self.__dict__[key].init()  # 위함수로 init이 호출되지 않아 별도 호출

    pass

    def setBasic(self,*args,**kwargs):
        self.setTableClass(kwargs.pop("tableClass",None))
        self.setColumns(kwargs.pop("columns"))
        self.setWidths(kwargs.pop("widths",{}))
        self.setSetDic(kwargs.pop("setDic", {}))
        self.setHeaders(kwargs.pop("headers",[]))
        self.setAligns(kwargs.pop("aligns", {}))

    def setHeaders(self,headers):
        if len(headers) > 0 : self.setHorizontalHeaderLabels(headers)

    def setListTable(self,listTable):
        self.removeAllRows()
        super(TableWidget,self).setListTable(listTable)
        self.setByTableList()

    def setWidths(self,widths):
        for key in widths.keys():
            self.widths[key.lower()] = widths[key]
            self.setColumnWidth(self.columns.index(key.lower()),self.widths[key.lower()])

    def setAligns(self,aligns): self.aligns    = aligns

    def setByTableList(self):
        try:
            self.setRowCount(len(self.listTable))
            for n, row in enumerate(self.listTable): self.setTWRow(n, self.listTable[n])
            return True
        except :
            if self.listTable == None : self.setRowCount(0)
            error()
            return False

    def setTWRow(self, n, table=None):
        r"""
            Row가 추가 된 경우 Setting
        :param n: 몇번째 Row를 추가할 것인지
        :param table: Setting할 table값(없으면 신규)
        :return:
        """
        try:
            for m, col in enumerate(self.columns):
                colClass = getattr(self.dicColAttr[col]['tableClass'], col)
                if colClass.kcom_cd_domain:  # com_cd  도메인인경우
                    combobox = ComboBox(colClass.kcom_cd_grp,self,self.getTableByColSeq(col,table),col.lower())
                    try:
                        combobox.setFixedWidth(self.widths[self.columns[m]])
                    except KeyError as ke : pass
                    try:
                        if table != None :
                            combobox.setCurrentText(combobox.dicCode[getattr(self.getTableByColSeq(col,table), col)])
                        else : combobox.setCurrentIndex(0)
                    except KeyError as ke:
                        combobox.setCurrentIndex(0)
                        if table != None :
                            print("공통코드 미등록 >> " + colClass.kcom_cd_grp + " : " + str(getattr(self.getTableByColSeq(col,table), col)))
                            error()
                        else:
                            print("공통코드 미등록 >> " + colClass.kcom_cd_grp + " : table is None ")
                            error()
                    self.setCellWidget(n, m, combobox)
                if table == None : text = ""
                else :
                    text = getattr(self.getTableByColSeq(col,table), col)
                    if text == None :
                        text = ""
                newitem = TableWidgetItem(str(text), self.getTableByColSeq(col,table), col.lower())
                if table == None : newitem.setBackground(QtGui.QColor("yellow"))
                if col in self.aligns.keys() : newitem.setTextAlignment(self.aligns[col])
                self.setItem(n, m, newitem)
        except Exception as e: error()

    def setTWColor(self,colorName="white"):
        for i in range(self.rowCount()):
            self.setTWRowColor(i,"white")

    def setTWRowColor(self,n,colorName="white"):
        for i in range(self.columnCount()):
            try:
                self.item(n,i).setBackground(QtGui.QColor(colorName))
            except:error()

    def insertTWRow(self, n):
        self.insertRow(n)
        self.setTWRow(n)

    def addTWRow(self):
        n = self.rowCount()
        self.insertTWRow(n)
        return n

    def deleteRow(self,n=None):
        r"""
        :param n: 삭제할 행(없으면 현재 행)
        :return:
        """
        if n == None: n = self.currentRow()
        table = self.getRowTable(n)
            #self.item(n, 0).table
        if table != None: deleteBasic(table)
        self.removeRow(n)
        commit()
        return True

    def getRowTable(self,n=None):
        if n == None : n = self.currentRow()
        w = self.getCellObject(n,0)
        if w == None : return None
        return w.table

    def isNewRow(self,n=None):
        if n == None: n = self.currentRow()
        if self.getRowTable(n) == None:
            return True
        return False

    def getRowDic(self,n=None):
        dic = {}
        if n == None : n = self.currentRow()
        for m, colName in enumerate(self.columns):
            dic[colName] = self.getCellObject(n,m).text()
        return dic

    def getCellObject(self,n,m):
        cw = self.cellWidget(n, m)
        if cw == None: return self.item(n,m)
        else: return cw

    def removeAll(self):
        self.removeAllRows()
        self.setDic = {}

    def removeAllRows(self):
        model = self.model()
        model.removeRow(0)
        for i in range(0,self.rowCount()):
            self.removeRow(0)


    def mergeRow(self,n=None):
        if n == None: n = self.currentRow()
        self.setRowValues(n)
        merge(self.getRowTable(n))
        self.setTWRowColor(n)
        return True

    def mergeList(self):
        self.setAllValues()
        mergeList(self.listTable)
        self.setTWColor()
        return True

    def insertRowDB(self,n=None):
        if n == None: n = self.currentRow()
        self.setRowValues(n)
        insert(self.getRowTable(n))
        self.setTWRowColor(n)
        return True

    def insertListDB(self):
        self.setAllValues()
        insertList(self.listTable)
        self.setTWColor()
        return True

    def setRowValues(self,n=None):
        if n == None: n = self.currentRow()
        if self.getRowTable(n) == None:
            kwargs = {}
            for m in range(0, self.columnCount()):
                cw = self.cellWidget(n,m)
                if cw == None:
                    kwargs[self.item(n, m).colName] = self.item(n, m).text()
                else:
                    kwargs[cw.getColName()] = cw.getCurrentCode()
                kwargs = {**self.setDic,**kwargs} #key값이 겹치는 경우 뒤 dicData기준(TableWidget 기준 세팅)
            table = self.tableClass(**kwargs)
            self.listTable.append(table)

            for m in  range(0, self.columnCount()):
                self.getCellObject(n,m).table = table
        else:
            for m in  range(0, self.columnCount()):
                cw = self.cellWidget(n, m)
                if cw == None:
                    setattr(self.item(n,m).table,self.item(n,m).colName,self.item(n,m).text())
                else:
                    setattr(cw.table, cw.colName, cw.getCurrentCode())

    def setAllValues(self):
        for n in range(0,self.rowCount()):
            self.setRowValues(n)

    def getTextByColName(self,n,colName):
        if n == -1: return False
        for m in range(0,self.columnCount()):
            if self.item(n,m).colName == colName:
                return self.item(n,m).text()
        return False

    def setTextByColName(self,n,colName,text):
        if self.isSet:
            for m in range(0,self.columnCount()):
                if self.getCellObject(n,m).colName == colName:
                    if text == None:
                        text = ""
                    else: text = str(text)
                    self.setCellText(n,m,text)
                    break
        else:
            logging.error("미조회 Error.. 조회 후 수행 가능합니다.")


    def setCellText(self,n,m,text):
        cw = self.cellWidget(n, m)
        if cw == None:
            self.item(n,m).setText(text)
        else:
            cw.setCurrentText(text)

    def resize(self):
        table = self
        header = table.horizontalHeader()
        twidth = header.width()
        width = []

        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width.append(header.sectionSize(column))
            wfactor = twidth / sum(width)

        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(column, width[column] * wfactor)

    def getDicBasicData(self):
        dicData = {}
        return  dicData

    def setColumnLower(self,colName):
        r"""
            특정 컬럼을 소문자로 세팅한다
        :param colName: 컬럼명
        :return:
        """
        for n in range(self.rowCount()):
            if isNotNull(self.getTextByColName(n, colName)):
                self.setTextByColName(n, colName, self.getTextByColName(n, colName).lower())


    @classmethod
    def convert_to_TableWidget(cls, obj):
        #print("변경 전 : " + str(obj.__class__))
        obj.__class__ = TableWidget
        #print("변경 후 : " + str(obj.__class__))

###############ComboBox####################
class ComboBox(QComboBox,TableBind):
    tableWidget = None
    com_cd_grp = None
    dicCode = None
    reverseDicCode = None
    #declare QComboBox to Customize ComboBox to use Common Code
    def __init__(self,com_cd_grp=None,tableWidget=None,table=None,colName=None):

        r"""
            공통코드 값으로 QComboBox를 세팅한다.
        :param com_cd_grp: 공통코드그룹ID
        :param tableWidget : 부모테이블위젯
        """
        super().__init__()
        TableBind.__init__(self, table, colName)
        self.tableWidget = tableWidget
        self.com_cd_grp = com_cd_grp
        if com_cd_grp != None:
            self.dicCode = dicCodeList[com_cd_grp]
            self.reverseDicCode = dict(map(reversed,self.dicCode.items()))
            for cd in self.dicCode.keys():
                self.addItem(dicCodeList[com_cd_grp][cd])

        #self.currentTextChanged.connect(self.combobox_select)

    def combobox_select(self):
        if self.tableWidget != None:
            self.tableWidget.item(self.tableWidget.currentRow(),self.tableWidget.currentColumn()).setText(self.reverseDicCode[self.currentText()])

    def getCurrentCode(self):
        return self.reverseDicCode[self.currentText()]

    def text(self):
        r"""
            getCellobejct를 사용하여 ComboBox와 TableWidghetItem의 Text를 동시에 가져올 수 있기 위해 만든 함수
        :return:
        """
        return self.currentText()

if __name__ == "__main__":
    pass

