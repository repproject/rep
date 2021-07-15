#https://www.youtube.com/watch?v=LYu5x339USM&t=478s&ab_channel=%EC%BB%B4%EB%85%B8%EB%8B%88comnoni
# -*- coding: utf-8 -*-
import sys
import UI.comnoni.modules.UIfile


import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

#CalUI = "_uiFiles/calculator.ui"
#UI/comnoni/

#pyuic5 -x UI/comnoni/_uiFiles/calculator.ui -o UI/comnoni/modules/UI.py
#pyinstaller -w -F --icon=icon.ico -p _dllFiles main.py

class MainDialog(QDialog,UI.comnoni.modules.UIfile.Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self, None,Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        #uic.loadUi(CalUI,self)


        self.num_pushButton_1.clicked.connect(lambda state, button=self.num_pushButton_1: self.NumClicked(state, button))
        self.num_pushButton_2.clicked.connect(lambda state, button=self.num_pushButton_2: self.NumClicked(state, button))
        self.num_pushButton_3.clicked.connect(lambda state, button=self.num_pushButton_3: self.NumClicked(state, button))
        self.num_pushButton_4.clicked.connect(lambda state, button=self.num_pushButton_4: self.NumClicked(state, button))
        self.num_pushButton_5.clicked.connect(lambda state, button=self.num_pushButton_5: self.NumClicked(state, button))
        self.num_pushButton_6.clicked.connect(lambda state, button=self.num_pushButton_6: self.NumClicked(state, button))
        self.num_pushButton_7.clicked.connect(lambda state, button=self.num_pushButton_7: self.NumClicked(state, button))
        self.num_pushButton_8.clicked.connect(lambda state, button=self.num_pushButton_8: self.NumClicked(state, button))
        self.num_pushButton_9.clicked.connect(lambda state, button=self.num_pushButton_9: self.NumClicked(state, button))
        self.num_pushButton_0.clicked.connect(lambda state, button=self.num_pushButton_0: self.NumClicked(state, button))

        self.sign_pushButton_1.clicked.connect(lambda state, button=self.sign_pushButton_1: self.NumClicked(state, button))
        self.sign_pushButton_2.clicked.connect(lambda state, button=self.sign_pushButton_2: self.NumClicked(state, button))
        self.sign_pushButton_3.clicked.connect(lambda state, button=self.sign_pushButton_3: self.NumClicked(state, button))
        self.sign_pushButton_4.clicked.connect(lambda state, button=self.sign_pushButton_4: self.NumClicked(state, button))

        self.result_pushButton.clicked.connect(self.MakeResult)
        self.reset_pushButton.clicked.connect(self.Reset)
        self.del_pushButton.clicked.connect(self.Delete)

        #self.del_pushButton.setStyleSheet('image:url(_uiFiles/img/delete.png); border:0px;')
        self.del_pushButton.setStyleSheet(
            '''
            QPushButton{image:url(_uiFiles/img/delete.png); border:0px;}
            QPushButton:hover{image:url(_uiFiles/img/delete_red.png); border:0px;}
            
            ''')

    def NumClicked(self,state,button):
        exist_line_text = self.q_lineEdit.text()
        now_num_text = button.text()

        self.q_lineEdit.setText(exist_line_text + now_num_text)

    def MakeResult(self):
        try:
            result = eval(self.q_lineEdit.text())
            self.a_lineEdit.setText(str(result))
        except Exception as e:
            print(e)
            pass

    def Reset(self):
        print('리셋이야')
        self.q_lineEdit.clear()
        self.a_lineEdit.setText('0')

    def Delete(self):
        exists_line_text = self.q_lineEdit.text()
        exists_line_text = exists_line_text[:-1]
        self.q_lineEdit.setText(exists_line_text)

app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
#main_dialog_2 = MainDialog()
#main_dialog_2.show()
print(main_dialog)
#print(main_dialog_2)
app.exec_()

