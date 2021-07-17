from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys

def setTable2Edit(form,table):
    for col in table.__table__.c:
        colname = str(col).split('.')[1]
        try:
            text = str(getattr(table,colname))
            form.findChild(QLineEdit, 'edit_' + colname).setText(text)
        except Exception as e:
            print("set Table to Edit Text Failure... : [" + colname + "]")
            print(e)

def setEdit2Table(form,table):
    for col in table.__table__.c:
        colname = str(col).split('.')[1]
        try:
            text = form.findChild(QLineEdit, 'edit_' + colname).text()
            setattr(table,colname,text)
        except Exception as e:
            print("set Edit to Table Text Failure... : [" + colname + "]")
            print(e)

#def setRow2Edit(form,table):
    # for col in dict(table).keys():
    #     try:
    #         text = str(dict(table)[col])
    #         form.findChild(QLineEdit, 'edit_' + col).setText(text)
    #     except Exception as e:
    #         print("set Column to Edit Text Failure... : [" + col + "]")
    #         print(e)

data = {'col1': ['1', '2', '3', '4'],
        'col2': ['1', '2', '1', '3'],
        'col3': ['1', '1', '2', '1']}

list = []
dict = {}

class TableView(QTableWidget):
    def __init__(self,qtableWidget, data, *args):
        QTableWidget.__init__(self, *args)
        if qtableWidget != None:
            self.setParent(qtableWidget)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.show()

    def setData(self):
        print('setdata')
        print(self.data.__class__)
        # print(self.data.__bases__)
        if str(self.data.__class__) == "<class 'list'>":
            print(self.data.__bases__)
            print('list list')
        elif str(self.data.__class__) == "<class 'dict'>":
            print("dict dict ")
            horHeaders = []
            print(data)
            for n, key in enumerate(sorted(self.data.keys())):
                print(key)
                print(n)
                horHeaders.append(key)
                for m, item in enumerate(self.data[key]):
                    newitem = QTableWidgetItem(item)
                    self.setItem(m, n, newitem)
            self.setHorizontalHeaderLabels(horHeaders)

def main(args):
    app = QApplication(args)
    table = TableView(None,data, 4, 3)
    table.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)

