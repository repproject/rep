from UI._uiFiles.COM.KCOMCOM010 import KCOMCOM010
from UI._uiFiles.COM.KCOMDEV051 import KCOMDEV051

def finderPop(parent,dicParam):
    #app = QApplication([])
    lb = KCOMCOM010(parent,dicParam)
    #lb.show()
    lb.exec_()
    result = lb.getResult()
    return result

def PopUp(parent,pgm_id,dicParam={}):
    exec = pgm_id+"(parent,dicParam)"
    lb = eval(exec)
    lb.exec_()
    result = lb.getResult()
    return result