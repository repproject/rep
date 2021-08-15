import traceback
import math
from common.common.Log import *
from common.common.Telegram import *

class Batch:
    #global Log
    funcName = None         #함수명(Lv4필수)
    batchContext = None     #BatchContect(필수)

    def __init__(self,batchContext = None):
        #self.Log = Log
        #funcName Validation Check
        if self.funcName == None:
            blog.Error("funcName 미정의 Error")
            return False
        else:
            #BatchContect 세팅
            self.batchContext = batchContext
            self.batchContext.setFuncName(self.funcName)

    def run(self):
        try:
            self.startLog() #START Log
        except Exception as e:
            blog.error("Crawling run Error : " + traceback.format_exc())
            sendTelegramMessage("Crawling run Error : " +traceback.format_exc())
        try:
            self.report()   #report 및 마지막 정의
        except Exception as e:
            blog.error("Batch Report 출력 에러" + str(e))
            sendTelegramMessage("Batch Report 출력 에러" + str(e))
        self.end()      #report 및 마지막 정의

    #하위 Batch구현
    def exec(self):
        pass

    def checkFuncName(self):
        if self.funcName == None:
            blog.error("funcName 미정의 Error")
            return False

class BatchContext:
    userId = 0000000000
    dicFunc = {}
    funcName = ""
    LogName = ""
    ExecDtm = ""

    def __init__(self, dicFunc, funcName="", userId=0000000000, ExecDtm = None):
        self.dicFunc = dicFunc
        self.funcName = funcName
        self.ExecDtm = ExecDtm
        self.setLogName()

    def getJOB_ID(self):
        return self.dicFunc['JOB_ID']

    def getJOB_NM(self):
        return self.dicFunc['JOB_NM']

    def getACT_ID(self):
        return self.dicFunc['ACT_ID']

    def getACT_NM(self):
        return self.dicFunc['ACT_NM']

    def getFUNC_ID(self):
        return self.dicFunc['FUNC_ID']

    def getFUNC_NM(self):
        return self.dicFunc['FUNC_NM']

    def getFuncName(self):
        return self.funcName

    def getUserId(self):
        return self.userId

    def getLogName(self):
        return self.LogName

    def getExecDtm(self):
        return self.ExecDtm

    # def getDicFunc(self):
    #     return self.dicFunc

    def setFuncName(self, funcName):
        self.funcName = funcName
        self.setLogName()

    def setLogName(self):
        self.LogName = "[" + self.getJOB_ID() + "][" + self.getACT_ID() + "][" + self.getFUNC_ID() + "][" + self.getFuncName() + "]"

    # def debug(self,logMessage):
    #     logMessage = str(logMessage)
    #     self.Log.logger.debug(self.LogName + logMessage)
    #
    # def info(self,logMessage):
    #     logMessage = str(logMessage)
    #     self.Log.logger.info(self.LogName + logMessage)
    #
    # def error(self,logMessage):
    #     logMessage = str(logMessage)
    #     self.Log.logger.error(self.LogName + logMessage)

class simpleBatchContext:
    userId = 0000000000
    funcName = ""
    LogName = ""

    def __init__(self, funcName="", userId=0000000000):
        self.funcName = funcName
        self.setLogName()

    def getFuncName(self):
        return self.funcName

    def getUserId(self):
        return self.userId

    def getLogName(self):
        return self.LogName

    def setFuncName(self, funcName):
        self.funcName = funcName
        self.setLogName()

    def setLogName(self):
        self.LogName = "[" + self.getFuncName() + "]"

#def error():logging.error(traceback.format_exc())