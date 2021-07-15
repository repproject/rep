import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import Server.COM
from UI._uiFiles.COM import *
#from UI._uiFiles.COM.KCOMMAN002 import *
import UI._uiFiles.COM.KCOMMAN002
import importlib

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("KCOMMAN001.ui")[0]
basic_ui_route = 'UI._uiFiles.COM'
user_id = 1000000001

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.makeMenu()

    def loadUI(self,dicMenuLv2Action):
        sender = self.sender()
        menu = dicMenuLv2Action[sender]
        print(type(menu))
        print(menu)
        mod = importlib.import_module(basic_ui_route + '.' + menu[0].pgm_id)
        uiClass = getattr(mod, menu[0].pgm_id)()
        self.tabWidget.addTab(uiClass, menu[0].menu_nm)
        return True

    def makeMenu(self):
        menuLv1 = Server.COM.getMenuLv(1)
        menuLv2 = Server.COM.getMenuLv(2)

        #menubar 생성
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menuLv1dict = {}
        for menu1 in menuLv1:
            menuLv1menu = menubar.addMenu('&' + menu1[0].menu_nm)
            menuLv1dict[menu1[0].menu_id] = menuLv1menu

        dicMenuLv2Action = {}

        for menu2 in menuLv2:
            action = QAction(menu2[0].menu_nm, self)
            dicMenuLv2Action[action] = menu2
            #PGM_ID를 로딩하는 함수를 연결
            action.triggered.connect(lambda : self.loadUI(dicMenuLv2Action))
            menuLv1dict[menu2[0].up_menu_id].addAction(action)

        #종료 버튼 추가
        exitAction = QAction('Exit',self)
        exitAction.triggered.connect(qApp.quit)
        menuLv1dict['M100000000'].addAction(exitAction)

        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(0)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
