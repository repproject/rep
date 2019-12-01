# import REP_TLGR_MSG
import logging.handlers
from datetime import date, timedelta, datetime

userid = 1000000001


def tuple2Str(tuple):
    return "%s" % tuple


def log(Message, Level):  # ERROR INFO Debug
    try:
        if Level == "E":
            Message = "[E]" + Message
            print(str(Message))
            # REP_TLGR_MSG.sendMessage(str(Message))
        elif Level == "D":
            Message = "[D]" + Message
            print(str(Message))
        elif Level == "I":
            Message = "[I]" + Message
            print(str(Message))
    except Exception as e:
        print("텔레그램 Exception 발생")


class Logger:
    streamHandler = logging.StreamHandler()

    def __init__(self, LogName=""):
        # 1. 시간 설정 (오늘 날짜)
        dt = datetime.now()
        access_day = dt.strftime('%Y%m%d')
        # 2. logger 생성.
        # print(__name__)
        logger = logging.getLogger(__name__)
        self.logger = logger

        #Handler 삭제
        self.removeHandler()

        # 3. log의 포맷 설정
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

        # 4. handler 생성
        streamHandler = logging.StreamHandler()

        FullLogName = './logs/LOGNAME_'

        # 전달받은 LogName이 존재하면 붙여준다.
        if (len(LogName) > 0):
            FullLogName += LogName + '_'

        FullLogName += access_day + '.log'

        fileHandler = logging.FileHandler(FullLogName)

        streamHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)

        # 5. logger instance에 formatter 생성
        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)
        logger.setLevel(level=logging.DEBUG)
        self.logger = logger

        # 전역 로그 세팅
        global Log
        Log = logger

    def removeHandler(self):
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

LogObject = Logger()
Log = LogObject.logger


class BatchContext:
    userId = 0000000000
    dicFunc = {}
    funcName = ""
    LogName = ""

    def __init__(self, dicFunc, funcName="", userId=0000000000):
        self.dicFunc = dicFunc
        self.funcName = funcName
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

class BatchRowCounter:
    totalRowCount = 0   #총 건수
    interval = 0        #출력 단위
    unit = None         #단위 : 숫자,갯수
    count = 0           #현재 건수
    beforeCount = 0     #이전 건수
    printCount = 0      #이전 출력 건수

    def __init__(self, totalRowCount, interval, unit = "Number"):
        self.count = 0
        self.beforeCount = 0
        self.printCount = 0
        self.totalRowCount = totalRowCount
        self.interval = interval
        self.unit = unit

    def Cnt(self,count = 1):
        self.BeforeCount = self.count
        self.count += count
        if(self.unit == "Number"):
            if((self.printCount + self.interval <= self.count)): #기출력 값보다
                self.printCount += self.interval
                global Log
                Log.info("BatchRowCounter : [" + str(self.printCount) + "/" + str(self.totalRowCount) + "]")

def LogFunction_TEST(self, index_no, package_name, name):
    log_message_list = index_no, package_name, name
    try:
        log_message = ", ".join(log_message_list)
        self.logger.debug(log_message)
    except:
        try:
            log_message = ", ".join(str(v) for v in log_message_list)
            self.logger.debug(log_message)
        except:
            log_message = ','.join([None])
            self.logger.debug(log_message)


if __name__ == '__main__':
    batchContext = BatchContext()
    # LogFunction_TEST(logger,1,"TEST","Name")
