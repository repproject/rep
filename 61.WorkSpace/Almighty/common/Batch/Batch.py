import traceback

class Batch:
    #global Log
    funcName = None         #함수명(Lv4필수)
    batchContext = None     #BatchContect(필수)

    def __init__(self,batchContext = None):
        #self.Log = Log
        #funcName Validation Check
        if self.funcName == None:
            Log.Error("funcName 미정의 Error")
            return False
        else:
            #BatchContect 세팅
            self.batchContext = batchContext
            self.batchContext.setFuncName(self.funcName)

    def run(self):
        try:
            self.startLog() #START Log
        except Exception as e:
            Log.error("Crawling run Error : " + traceback.format_exc())
            sendMessage("Crawling run Error : " +traceback.format_exc())
        try:
            self.report()   #report 및 마지막 정의
        except Exception as e:
            Log.error("Batch Report 출력 에러" + str(e))
            sendMessage("Batch Report 출력 에러" + str(e))
        self.end()      #report 및 마지막 정의

    #하위 Batch구현
    def exec(self):
        pass

    def checkFuncName(self):
        if self.funcName == None:
            Log.error("funcName 미정의 Error")
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

class BatchRowCounter:
    totalRowCount = 0   #총 건수
    interval = 0        #출력 단위
    MessageInterval = 0 #메세지 출력 단위
    unit = None         #단위 : 숫자,갯수
    count = 0           #현재 건수
    printCount = 0      #이전 출력 건수
    MessagePrintCount = 0  # 이전 출력 건수
    Name = None         #출력 메시지명

    def __init__(self, Name, totalRowCount, interval, unit = "N", MessageInterval=0, MessageUnit = None):
        self.count = 0
        self.beforeCount = 0
        self.printCount = 0
        self.MessagePrintCount = 0
        self.totalRowCount = totalRowCount
        self.interval = interval
        self.unit = unit
        self.MessageInterval = MessageInterval
        self.MessageUnit = MessageUnit
        self.Name = Name

    def Cnt(self,count = 1):
        self.count += count
        global Log

        #N = Number P = Percent
        if(self.unit == "N"):
            if((self.printCount + self.interval <= self.count)): #기출력 값보다
                self.printCount += self.interval
                Log.info(self.Name + "BatchRowCounter : [" + str(self.printCount) + "/" + str(self.totalRowCount) + "]")

        if (self.MessageUnit == "N"):
            if ((self.MessagePrintCount + self.MessageInterval <= self.count)):  # 기출력 값보다
                self.MessagePrintCount += self.MessageInterval
                REP_TLGR_MSG.sendMessage(self.Name + "BatchRowCounter : [" + str(self.MessagePrintCount) + "/" + str(self.totalRowCount) + "]")

        if(self.unit == "P"):
            if(self.printCount + math.floor(self.totalRowCount*self.interval/100) <= self.count): #기출력 값보다
                self.printCount += math.floor(self.totalRowCount*self.interval/100)
                Log.info(self.Name + "BatchRowCounter : [" + str(self.printCount) + "/" + str(self.totalRowCount) + "]")

        if(self.MessageUnit == "P"):
            if((self.MessagePrintCount + math.floor(self.totalRowCount*self.MessageInterval/100)) <= self.count): #기출력 값보다
                self.MessagePrintCount += math.floor(self.totalRowCount*self.MessageInterval/100)
                REP_TLGR_MSG.sendMessage(self.Name + "BatchRowCounter : [" + str(self.MessagePrintCount) + "/" + str(self.totalRowCount) + "]")

