from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import Server.COM
from common.ui.comPopUp import *
from common.ui.comUi import *
from Server.Basic import *


def MessageBox():
    message = QMessageBox()
    return message

def alert(text):
    message = MessageBox()
    message.setText(text)
    rtn = message.exec_()
    return rtn