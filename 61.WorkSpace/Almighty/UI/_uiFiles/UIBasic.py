from PyQt5.QtWidgets import *

def MessageBox():
    message = QMessageBox()
    return message

def alert(text):
    message = MessageBox()
    message.setText(text)
    rtn = message.exec_()
    return rtn