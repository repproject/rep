import sys
import Server.COM
import Server.Basic
from PyQt5 import QtCore
from common.ui import comUi
from UI._uiFiles.KWidget import *
from UI._uiFiles.UIBasic import *
from DAO.KADM import *
import datetime


pgm_id = 'KCOMMAN002'
form_class = uic.loadUiType(pgm_id + ".ui")[0]

class KCOMMAN002(QWidget,KWidget,form_class) :
    selectedItem = None
    root = None
    tableMenu = None
    CUDflag = 'U'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        #메뉴목록 가져오기
        self.tableMenu = self.getMenuList()

        #tabWidget Setting
        self.tw.setColumnCount(1)
        self.tw.setHeaderLabels(["메뉴"])

        #lv1 추가를 위해 root TreeWidget Setting
        item = QTreeWidgetItem()
        item.setText(0,"Root")
        self.root2 = self.tw.invisibleRootItem()
        self.root2.addChild(item)
        item.setExpanded(True)
        self.root = item

        dicMenuItem = {}
        #메뉴레벨1 세팅
        for menu1 in self.tableMenu:
            if menu1.menu_lv == 1:
                item = QTreeWidgetItem()
                item.setText(0, menu1.menu_nm)
                self.root.addChild(item)
                item.__setattr__('menu', menu1)
                dicMenuItem[menu1.menu_id] = item

        for menu2 in self.tableMenu:
            if menu2.menu_lv == 2:
                sub_item = QTreeWidgetItem()
                sub_item.setText(0, menu2.menu_nm)
                sub_item.__setattr__('menu',menu2)
                dicMenuItem[menu2.up_menu_id].addChild(sub_item)

        self.tw.itemClicked.connect(self.onItemClicked)
        self.pushButton_Save.clicked.connect(self.save)
        self.pushButton_Add.clicked.connect(self.add)
        self.edit_menu_nm.textChanged.connect(self.edit_menu_nm_Changed)

    def getMenuList(self):
        menu = Server.COM.getMenu()
        return menu

    @QtCore.pyqtSlot(QTreeWidgetItem,int)
    def onItemClicked(self,it,col):
        try:
            self.selectedItem = it
            if self.root != self.selectedItem:  #root가 아닌경우
                menu = it.__getattribute__('menu')
                #테이블객체 컬럼 > edit 자동매핑
                comUi.setTable2Edit(self, menu)
            else:
                self.edit_menu_id.setText(None)
                self.edit_menu_lv.setText(None)
                self.edit_prnt_seq.setText(None)
                self.edit_menu_nm.setText(None)
                self.edit_up_menu_id.setText(None)
                self.edit_fst_reg_ymd.setText(None)
                self.edit_pgm_id.setText(None)
            return True
        except Exception as e:
            print('Function onItemClicked Error..')
            print(e)

    def save(self):
        try:
            if self.selectedItem == None:
                alert("메뉴를 선택 후 저장하세요")
                return False

            menu = self.selectedItem.__getattribute__('menu')
            comUi.setEdit2Table(self,menu)
            Server.Basic.merge(menu)
            return True
        except Exception as e :
            print(e)

    def add(self):
        try:
            if self.selectedItem == None:
                alert("메뉴를 선택 후 추가하세요")
                return False

            menu_lv = 0
            menu_id = None
            up_menu_id = None
            max_menu_id = None

            if self.root != self.selectedItem: #root가 아닌경우
                menu = self.selectedItem.__getattribute__('menu')
                menu_lv = menu.menu_lv
                up_menu_id = menu.menu_id
                max_menu_id = menu.menu_id
                if menu_lv > 1:
                    alert("마지막 메뉴 레벨입니다. 상위메뉴를 선택 후 추가해 주세요")
            else:
                max_menu_id = 'M000000000'


            last_prt_seq = 0
            for smenu in self.tableMenu:
                if smenu.menu_lv == menu_lv + 1 and smenu.up_menu_id == up_menu_id:
                    if max_menu_id < smenu.menu_id:
                        max_menu_id = smenu.menu_id
                        last_prt_seq = smenu.prnt_seq

            seq2 = int(max_menu_id[1:]) + 10**(7-menu_lv*2)
            new_menu_id = 'M' + str(seq2)
            new_menu_lv = menu_lv+1
            new_prt_seq = last_prt_seq + 1
            new_up_menu_id = up_menu_id

            item = QTreeWidgetItem()
            self.selectedItem.addChild(item)
            self.tw.setCurrentItem(item)
            self.selectedItem = item

            new_menu = Menu(new_menu_id, new_menu_lv, new_prt_seq, None, new_up_menu_id, None)
            item.__setattr__('menu', new_menu)

            self.edit_menu_id.setText(new_menu_id)
            self.edit_menu_lv.setText(str(new_menu_lv))
            self.edit_prnt_seq.setText(str(new_prt_seq))
            self.edit_menu_nm.setText(None)
            self.edit_up_menu_id.setText(new_up_menu_id)
            self.edit_fst_reg_ymd.setText(None)
            self.edit_pgm_id.setText(None)
        except Exception as e :
            print(e)

    def edit_menu_nm_Changed(self):
        self.selectedItem.setText(0,self.edit_menu_nm.text())

if __name__ == "__main__":
# QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

# WindowClass의 인스턴스 생성
    myWindow = KCOMMAN002()

#    프로그램 화면을 보여주는 코드
    myWindow.show()

# 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


