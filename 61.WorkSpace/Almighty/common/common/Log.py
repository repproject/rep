import logging.handlers
import logging
from common.common.Telegram import *
from datetime import date, timedelta, datetime
import sys, traceback

# logging.basicConfig(level=logging.DEBUG
# #                    ,filename=os.path.dirname(__file__) + "/Almighty.log"
#                     )
#
# class Logger:
#     streamHandler = logging.StreamHandler()
#
#     def __init__(self, LogName="", Level="DEBUG"):
#         # 1. 시간 설정 (오늘 날짜)
#         dt = datetime.now()
#         access_day = dt.strftime('%Y%m%d')
#         # 2. logger 생성.
#         # print(__name__)
#         logger = logging.getLogger(__name__)
#         self.logger = logger
#
#         #Handler 삭제
#         self.removeHandler()
#
#         # 3. log의 포맷 설정
#         formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
#
#         # 4. handler 생성
#         streamHandler = logging.StreamHandler()
#
#         #FullLogName = './logs/LOGNAME_'
#         FullLogName = 'D:/Log/LOGNAME_'
#
#         # 전달받은 LogName이 존재하면 붙여준다.
#         if (len(LogName) > 0):
#             FullLogName += LogName + '_'
#
#         FullLogName += access_day + '.log'
#
#         fileHandler = logging.FileHandler(FullLogName)
#
#         streamHandler.setFormatter(formatter)
#         fileHandler.setFormatter(formatter)
#
#         # 5. logger instance에 formatter 생성
#         logger.addHandler(streamHandler)
#         logger.addHandler(fileHandler)
#         if Level == "INFO":
#             logger.setLevel(level=logging.INFO)
#         elif Level == "DEBUG":
#             logger.setLevel(level=logging.DEBUG)
#         elif Level == "ERROR":
#             logger.setLevel(level=logging.ERROR)
#         else:
#             logger.setLevel(level=logging.INFO)
#         self.logger = logger
#
#         # 전역 로그 세팅
#         # global Log
#         # Log = logger
#
#     def removeHandler(self):
#         for handler in self.logger.handlers[:]:
#             self.logger.removeHandler(handler)
#
# class childLogger(Logger):
#     def __init__(self, LogName="", Level="DEBUG"):
#         super().__init__()
#
#     def error(msg,*args):
#         super().error(msg,*args)
#
#     def info(msg,*args):
#         super().info(msg,*args)
#
#     def debug(msg, *args):
#         super().debug(msg, *args)
#
# LogObject = childLogger()
# Log = LogObject.logger

# def error():
#     Log.error(traceback.format_exc())
#     sendTelegramMessage(traceback.format_exc())




