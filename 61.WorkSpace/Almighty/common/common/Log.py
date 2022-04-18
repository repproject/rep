import logging.handlers
import logging
from common.common.Telegram import *
from datetime import date, timedelta, datetime
import sys, traceback

class Logger:
    def __init__(self, LogName="", Level="INFO", name = "Batch"):
        # 1. 시간 설정 (오늘 날짜)
        dt = datetime.now()
        access_day = dt.strftime('%Y%m%d')
        # 2. logger 생성.
        logger = logging.getLogger(name)
        self.logger = logger

        #Handler 삭제
        self.removeHandler()

        # 3. log의 포맷 설정
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

        # 4. handler 생성
        streamHandler = logging.StreamHandler(sys.stderr)

        #FullLogName = './logs/LOGNAME_'
        FullLogName = 'D:/Log/LOGNAME_'

        # 전달받은 LogName이 존재하면 붙여준다.
        if (len(LogName) > 0):
            FullLogName += LogName + '_'

        FullLogName += access_day + '.log'

        fileHandler = logging.FileHandler(FullLogName)

        streamHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)

        # 5. logger instance에 formatter 생성

        if (logger.hasHandlers()):
            logger.handlers.clear()

        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)
        if Level == "INFO":
            logger.setLevel(level=logging.INFO)
        elif Level == "DEBUG":
            logger.setLevel(level=logging.DEBUG)
        elif Level == "ERROR":
            logger.setLevel(level=logging.ERROR)
        else:
            logger.setLevel(level=logging.INFO)
        self.logger = logger

    def removeHandler(self):
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

class childLogger(Logger):
    def __init__(self, LogName="", Level="INFO", name = None):
        super().__init__(LogName,Level,name)

    def error(msg,*args):
        sendTelegramMessage(msg)
        super().error(msg,*args)

    def info(msg,*args):
        sendTelegramMessage(msg)
        super().info(msg,*args)

    def debug(msg, *args):
        super().debug(msg, *args)

#LogObject = childLogger()
blog = childLogger(name = "Batch").logger
#blog = LogObject.logger
#blog = logging.getLogger('Batch')
blog.propagate=False

# def error():
#     Log.error(traceback.format_exc())
#     sendTelegramMessage(traceback.format_exc())





