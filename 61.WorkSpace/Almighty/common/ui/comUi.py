from PyQt5.QtWidgets import *

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

if __name__ == "__main__" :

    pass