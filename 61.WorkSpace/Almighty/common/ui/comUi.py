from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
from Server.Basic import *
import copy

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
        except Exception as e:
            print("set Table to Edit Text Failure... : [" + colname + "]")
            print(e)
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

############### Code ################
def getCode(grp):
    r"""
        공통코드그룹ID로 코드값을 dictionary로 return 한다.
    :param grp : 공통코드그룹ID
    :return: dictionary {com_cd:com_cd_nm}
    """
    #이미 코드가 존재하면 존재하는 리스트값으로 return
    if grp in dicCodeList:
        return dicCodeList[grp]
    result = getCode(grp)
    code = {}
    for cd in result:
        code[cd.com_cd] = cd.com_cd_nm
    dicCodeList[grp] = code
    return code

def setCode(grp):   #코드세팅
    r"""
        공통코드그룹ID를 받아 공통코드 공통리스트 전역변수에 반영한다.
    :param grp : 공통코드그룹ID
    :return: True/False
    """
    if grp not in dicCodeList:
        result = getCode(grp)
        code = {}
        for cd in result:
            code[cd.com_cd] = cd.com_cd_nm
        dicCodeList[grp] = code
        return True
    else : return False

############Table############
class TableListBind():
    listTable = None
    columns = None
    table = None

    def __init__(self, listTable=None, columns=None):
        try:
            self.setlistTable(listTable)
            self.setColumns(columns)
        except Exception as e:
            print("class TableBind Exception : " + str(e))

    def setListTable(self, listTable): self.listTable = listTable
    def setColumns(self, columns):     self.columns = columns
    def setTable(self, table):         self.table = table
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
    def setColumnValue(self,text):
        setattr(self.table,self.colName,text)

############TableWidget##############
class TableWidgetItem(QTableWidgetItem,TableBind):
    def __init__(self,text=None,table=None,colName=None):
        try:
            QTableWidgetItem.__init__(self,text)
            TableBind.__init__(self,table,colName)
        except Exception as e:
            print("class TableWidgetItem : " + str(e))

    def setColumnValue(self):
        super().setColumnValue(self.text())

class TableWidget(QTableWidget,TableListBind):
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

    def setByTableList(self):
        try:
            self.setRowCount(len(self.listTable))
            for n, row in enumerate(self.listTable): self.setTableWidgetRow(n,self.listTable[n])
            return True
        except Exception as e:
            print('TableWidget.setByTableList : ' + str(e))
            return False

    def setTableWidgetRow(self,n,table=None):
        try:
            for m, col in enumerate(self.columns):
                colClass = getattr(self.table, col)
                if colClass.kcom_cd_domain:  # com_cd  도메인인경우
                    combobox = ComboBox(colClass.kcom_cd_grp)
                    try:
                        if table != None : combobox.setCurrentText(dicCodeList[colClass.kcom_cd_grp][getattr(table, col)])
                    except KeyError as ke:
                        if table != None: print("공통코드 미등록 >> " + colClass.kcom_cd_grp + " : " + getattr(table, col))
                        else: print("공통코드 미등록 >> " + colClass.kcom_cd_grp + " : table is None ")
                    self.setCellWidget(n, m, combobox)
                else:
                    if table == None : text = None
                    else : text = getattr(table, col)
                    newitem = TableWidgetItem(text, table, col)
                    self.setItem(n, m, newitem)
        except Exception as e:
            print('comUI.setTableWidgetRow : ' + str(e))

    def insertTableWidgetRow(self,n):
        self.insertRow(n)
        #table = self.table()
        #self.listTable.insert(n,table)
        self.setTableWidgetRow(n)

    def addTableWidgetRow(self):
        n = self.rowCount()
        self.insertTableWidgetRow(n)

    def removeAll(self):
        model = self.model()
        model.removeRow(0)
        for i in range(0,self.rowCount()):
            self.removeRow(0)

    def mergeRow(self,n=None):
        if n == None: n = self.currentRow()
        self.setRowValues(n)
        merge(self.item(n,0).table)

    def setRowValues(self,n=None):
        if n == None: n = self.currentRow()
        for m in range(0, self.columnCount()):
            self.item(n, m).setColumnValue()

    def setAllValues(self):
        for n in range(0,self.rowCount()):
            self.setRowValues(n)

    def mergeList(self):
        self.setAllValues()
        mergeList(self.listTable)

    @pyqtSlot(int, int)
    def onCellChanged(self, row, column): self.item(row,column).setColumnValue()

    @classmethod
    def convert_to_TableWidget(cls, obj):
        obj.__class__ = TableWidget

###############ComboBox####################
class ComboBox(QComboBox):
    #declare QComboBox to Customize ComboBox to use Common Code
    def __init__(self,com_cd_grp=None):
        r"""
            공통코드 값으로 QComboBox를 세팅한다.
        :param com_cd_grp: 공통코드그룹ID
        """
        super().__init__()
        if com_cd_grp != None:
            for cd in dicCodeList[com_cd_grp].keys():
                self.addItem(dicCodeList[com_cd_grp][cd])

    if __name__ == "__main__":
        pass

