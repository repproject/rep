from Batch.COM_LOG import *

class Crawling:
    #global Log
    funcName = None         #함수명(Lv4필수)
    batchContext = None     #BatchContect(필수)

    #초기화
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
            self.ready()    #크롤링 전 사전 Data 준비 작업
            self.crawl()    #URL 호출 후 삽입
        except Exception as e:
            Log.error("Crawling run Error : " + traceback.format_exc())
            sendMessage("Crawling run Error : " +traceback.format_exc())
        try:
            self.report()   #report 및 마지막 정의
        except Exception as e:
            Log.error("Batch Report 출력 에러" + str(e))
            sendMessage("Batch Report 출력 에러" + str(e))
        self.end()      #report 및 마지막 정의

    def startLog(self):
        #기본로그 출력
        Log.info(self.batchContext.getLogName()+"####################START[" + self.batchContext.getFuncName() + "]####################")
        sendMessage("START[" + self.batchContext.getFuncName() + "]")

    #Lv2 구현
    def ready(self):
        pass

    # Lv2 구현
    def crawl(self):
       pass

    def report(self):
        # Report
        dicNewRowList = REP_DAO.fetch(self.sqlReportFetchId, "")
        Log.info(self.batchContext.getLogName() + "####################Batch Report####################")
        sendMessage("[Batch Report]")
        Log.info(self.batchContext.getLogName() + "신규 건 수  : " + str(dicNewRowList.__len__()) + " 건")
        sendMessage("신규 건수 : " + str(dicNewRowList.__len__()) + " 건")
        if dicNewRowList.__len__() > 0:
            Log.info(self.batchContext.getLogName() + str(dicNewRowList))
            sendMessage(self.batchContext.getLogName() + str(dicNewRowList))

    def end(self):
        Log.info(self.batchContext.getLogName() + "####################END[" + self.batchContext.getFuncName() + "]####################")
        sendMessage("END[" + self.batchContext.getFuncName() + "]")

    def makeURL(self,dicStrdData = None,reCnt = None):
        url = self.selfMakeURL(dicStrdData,reCnt)
        Log.info(self.batchContext.getLogName() + " ReCnt : " + str(reCnt) + url.printURL())
        return url