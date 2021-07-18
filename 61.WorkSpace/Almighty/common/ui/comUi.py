from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
import Server.Basic

basic_ui_route = 'UI._uiFiles.COM'
basic_ui_dictionary = "C:/Users/Ceasar.DESKTOP-AQTREV4/PycharmProjects/rep/61.WorkSpace/Almighty/UI/_uiFiles/COM/"


###############공통코드################
dicCodeList ={} #코드목록
dicCode = {}

###############Edit#########################
#setTable2Edit: Table객체를 edit으로 세팅
#Edit 명은 edit_으로 시작해야함
def setTable2Edit(form,table):
    for col in table.__table__.c:
        colname = str(col).split('.')[1]
        try:
            text = str(getattr(table,colname))
            getattr(form,'edit_'+colname).setText(text)
        except Exception as e:
            print("set Table to Edit Text Failure... : [" + colname + "]")
            print(e)

#setEdit2Table: edit을 Table객체로 변환
#Edit 명은 edit_으로 시작해야함
def setEdit2Table(form,table):
    for col in table.__table__.c:
        colname = str(col).split('.')[1]
        try:
            text = getattr(form,"edit_"+colname).text()
            setattr(table,colname,text)
        except Exception as e:
            print("set Edit to Table Text Failure... : [" + colname + "]")
            print(e)

#################Qtable##################
def setTableWidgetByTableList(tableWidget,listTable,columns,headers):
    try:
        tableWidget.clear()
        tableWidget.setRowCount(len(listTable))
        tableWidget.setColumnCount(len(columns))
        for n, row in enumerate(listTable):
            for m, col in enumerate(columns):
                colClass = getattr(row.__class__, col)
                if colClass.kcom_cd_domain:  # com_cd  도메인인경우
                    combobox = ComboBox(colClass.kcom_cd_grp)
                    try:
                        combobox.setCurrentText(dicCodeList[colClass.kcom_cd_grp][getattr(row, col)])
                    except KeyError as ke:
                        print("공통코드 미등록 >> " + colClass.kcom_cd_grp + " : " + getattr(row, col))
                    tableWidget.setCellWidget(n, m, combobox)
                else:
                    newitem = QTableWidgetItem(getattr(row, col))
                    tableWidget.setItem(n, m, newitem)
        tableWidget.setHorizontalHeaderLabels(headers)
    except Exception as e:
        print('comUI.setTableWidgetByTableList : ' + str(e))

###############ComboBox####################
class ComboBox(QComboBox):
    def __init__(self,com_cd_grp=None):
        super().__init__()
        #공통코드그룹ID로 QComboBox를 세팅
        if com_cd_grp != None:
            for cd in dicCodeList[com_cd_grp].keys():
                self.addItem(dicCodeList[com_cd_grp][cd])

############### 코드 ################
def getCode(grp):
    #returnType : dictionary {com_cd:com_cd_nm}

    #이미 코드가 존재하면 존재한 리스트를 세팅
    if grp in dicCodeList:
        return dicCodeList[grp]
    result = Server.Basic.getCode(grp)
    code = {}
    for cd in result:
        code[cd.com_cd] = cd.com_cd_nm
    dicCodeList[grp] = code
    return code

#코드세팅
def setCode(grp):
    #input : 공통코드그룹ID
    if grp not in dicCodeList:
        result = Server.Basic.getCode(grp)
        code = {}
        for cd in result:
            code[cd.com_cd] = cd.com_cd_nm
        dicCodeList[grp] = code
        return True
    else : return False

################# 메인 ###############
def main(args):
    app = QApplication(args)
    table = TableView(None,data, 4, 3)
    table.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)

