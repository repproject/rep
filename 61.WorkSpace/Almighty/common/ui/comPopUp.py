from UI._uiFiles.COM.KCOMCOM010 import KCOMCOM010

def finderPop(parent,dicParam):
    #app = QApplication([])
    lb = KCOMCOM010(parent,dicParam)
    #lb.show()
    lb.exec_()
    result = lb.getResult()
    return result