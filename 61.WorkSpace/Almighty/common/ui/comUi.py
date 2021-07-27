from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from Server.Basic import *
import sys, traceback
import copy
import Server.COM

basic_ui_route = 'UI._uiFiles.COM'
basic_ui_dictionary = "C:/Users/Ceasar.DESKTOP-AQTREV4/PycharmProjects/rep/61.WorkSpace/Almighty/UI/_uiFiles/COM/"


###############공통코드################
dicCodeList ={} #코드목록
dicCode = {}

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
            "'KCOMMAN020' object has no attribute 'edit_reg_user_id'",
            "'KCOMMAN020' object has no attribute 'edit_reg_dtm'",
            "'KCOMMAN020' object has no attribute 'edit_chg_user_id'",
            "'KCOMMAN020' object has no attribute 'edit_chg_dtm'")
            if str(ae) not in setTable2EditErrorList: error()
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
        except Exception as e:
            print("set Edit to Table Text Failure... : [" + colname + "]")
            print(e)
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
    else : return False

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
    listTable = None
    columns = None
    tableClass = None
    setDic = {}

    def __init__(self, listTable=None, columns=None):
        try:
            self.setlistTable(listTable)
            self.setColumns(columns)
        except Exception as e:
            print("class TableBind Exception : " + str(e))

    def setListTable(self, listTable): self.listTable = listTable
    def setColumns(self, columns):
        self.columns = []
        for col in columns:
            self.columns.append(col.lower())
    def setSetDic(self,setdic):        self.setDic = setdic
    def setTableClass(self, tableClass):
        self.tableClass = tableClass
        Server.COM.setCodeByTable(tableClass)
    def getColumns(self):              return self.columns
    def getlistTable(self):            return self.listTable

class TableBind():
    table = None
    colName = None

    def __init__(self, table=None, colName=None):
        try:
            self.setTable(table)
            self.setColName(colName)
        except Exception as e:
            print("class TableBind Exception : " + str(e))

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
        except Exception as e:
            print("class TableWidgetItem : " + str(e))

class TableWidget(QTableWidget,TableListBind):
    widths = {}
    algins = {}

    def __init__(self,table = None, listTable = None, columns = None):
        try:
            super(TableWidget,self).__init__(listTable,columns)
            self.init()
        except Exception as e:
            print(e)

    def init(self):
        #self.cellChanged.connect(self.onCellChanged)
        pass

    def setListTable(self,listTable):
        self.removeAll()
        super(TableWidget,self).setListTable(listTable)
        self.setByTableList()

    def setBasic(self,*args,**kwargs):
        self.setColumns(kwargs.pop("columns"))
        self.setWidths(kwargs.pop("widths",{}))
        self.setTableClass(kwargs.pop("tableClass",""))
        self.setSetDic(kwargs.pop("setDic", {}))
        self.setAligns(kwargs.pop("aligns", {}))

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
                colClass = getattr(self.tableClass, col)
                if colClass.kcom_cd_domain:  # com_cd  도메인인경우
                    combobox = ComboBox(colClass.kcom_cd_grp,self,table,col.lower())
                    combobox.setFixedWidth(self.widths[self.columns[m]])
                    try:
                        if table != None :
                            combobox.setCurrentText(combobox.dicCode[getattr(table, col)])
                        else : combobox.setCurrentIndex(0)
                    except KeyError as ke:
                        combobox.setCurrentIndex(0)
                        if table != None :
                            print("공통코드 미등록 >> " + colClass.kcom_cd_grp + " : " + str(getattr(table, col)))
                            error()
                        else:
                            print("공통코드 미등록 >> " + colClass.kcom_cd_grp + " : table is None ")
                            error()
                    self.setCellWidget(n, m, combobox)
                if table == None : text = ""
                else :
                    text = getattr(table, col)
                    if text == None :
                        text = ""
                newitem = TableWidgetItem(str(text), table, col.lower())
                if col in self.aligns.keys() : newitem.setTextAlignment(self.aligns[col])
                self.setItem(n, m, newitem)
        except Exception as e: error()

    def insertTWRow(self, n):
        self.insertRow(n)
        self.setTWRow(n)

    def addTWRow(self):
        n = self.rowCount()
        self.insertTWRow(n)
        return n

    def removeAll(self):
        model = self.model()
        model.removeRow(0)
        for i in range(0,self.rowCount()):
            self.removeRow(0)

    def mergeRow(self,n=None):
        if n == None: n = self.currentRow()
        self.setRowValues(n)
        merge(self.item(n,0).table)

    def mergeList(self):
        self.setAllValues()
        mergeList(self.listTable)

    def setRowValues(self,n=None):
        if n == None: n = self.currentRow()

        if self.item(n, 0).table == None:
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
                self.item(n,m).table = table
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
        for m in range(0,self.columnCount()):
            if self.item(n,m).colName == colName:
                return self.item(n,m).text()
        return False

    def setTextByColName(self,n,colName,text):
        for m in range(0,self.columnCount()):
            if self.item(n,m).colName == colName:
                if text == None:
                    text = ""
                else: text = str(text)
                self.item(n,m).setText(text)

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
        pass

    @classmethod
    def convert_to_TableWidget(cls, obj):
        obj.__class__ = TableWidget

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



    if __name__ == "__main__":
        pass

