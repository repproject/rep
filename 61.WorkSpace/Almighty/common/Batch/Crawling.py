from common.common.Log import *
from common.Batch.Batch import *
from common.common.Telegram import *
from common.common.URL import get_html
import Server.COM

sleeptime = 1
NVsleeptime = 2

#LV1 크롤링 클래스
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
        except : error()
        try:
            self.report()   #report 및 마지막 정의
        except Exception as e:
            Log.error("Batch Report 출력 에러" + str(e))
            sendTelegramMessage("Batch Report 출력 에러" + str(e))
        self.end()      #report 및 마지막 정의

    def startLog(self):
        #기본로그 출력
        Log.info(self.batchContext.getLogName()+"####################START[" + self.batchContext.getFuncName() + "]####################")
        sendTelegramMessage("START[" + self.batchContext.getFuncName() + "]")

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
        sendTelegramMessage("[Batch Report]")
        Log.info(self.batchContext.getLogName() + "신규 건 수  : " + str(dicNewRowList.__len__()) + " 건")
        sendTelegramMessage("신규 건수 : " + str(dicNewRowList.__len__()) + " 건")
        if dicNewRowList.__len__() > 0:
            Log.info(self.batchContext.getLogName() + str(dicNewRowList))
            sendTelegramMessage(self.batchContext.getLogName() + str(dicNewRowList))

    def end(self):
        Log.info(self.batchContext.getLogName() + "####################END[" + self.batchContext.getFuncName() + "]####################")
        sendTelegramMessage("END[" + self.batchContext.getFuncName() + "]")

    def makeURL(self,dicStrdData = None,reCnt = None):
        url = self.selfMakeURL(dicStrdData,reCnt)
        Log.info(self.batchContext.getLogName() + " ReCnt : " + str(reCnt) + url.printURL())
        return url

    #[LV4 구현]각 Lv4 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
    def selfMakeURL(self,dicStrdData = None):
        return "http://test.com"

    #[LV4 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,page,dicStrdData = None,url = None):
        pass

    def request(self,url):
        page = get_html(url.getURL(),url.getMethod(),url.getDicParam())
        Log.debug(self.batchContext.getLogName() + str(page))
        return page

    def getFuncName(self):
        return self.funcName

class DataStrd:
    #Crawling의 기준 data list
    listStrdData = None
    #현재 참조중인 index
    index = 0

    def __init__(self,listStrdData):
        #리스트 자료형을 객체에 세팅한다.
        self.listStrdData = listStrdData
        self.index = 0

    #현재 자료를 가져온다.
    def getCurrentData(self):
        return self.listStrdData[self.index]

#LV2 Craling Class 기본 멀티
class CrawlingBasicMulti(Crawling):
    # [LV4/필수]URL Multi호출시 값 기준정보 세팅 SQLID
    fetchSqlId = None

    #[LV3/선택]rowCounter 설정값
    rowCounter = None       #Multi호출시 RowCounter Setting용
    rowCountNumber = 1
    rowCounterInterval = "N"
    MessageInterval = 10
    MessageUnit = "P"

    #URL Making 기준정보
    dicStrdDataList = None

    #[LV3]
    sleepStamp = 0.1

    def __init__(self):
        self.sleepStamp = Server.COM.getSite(self.siteCode)[0].slep_sec

    def ready(self):
        # super().ready()
        # self.dicStrdDataList = self.getListStrdDataList()
        # #rowCounter 세팅
        # self.setRowCounter(self.dicStrdDataList.__len__())
        pass

    def crawl(self):
        # for dicStrdData in self.dicStrdDataList:
        #     try:
        #         reCnt = 0
        #
        #         while True:
        #             reCnt = reCnt + 1
        #             self.debugDicStrdData(dicStrdData)
        #             url = self.makeURL(dicStrdData,reCnt)
        #             page = self.request(url)
        #             self.selfSaveDB(page,dicStrdData,url)
        #             time.sleep(self.sleepStamp)
        #             if self.isReCrwal(url,page,dicStrdData,reCnt) == False:
        #                 self.rowCounter.Cnt()
        #                 break
        #         gc.collect()
        #     except Exception as e:
        #         Log.error(self.batchContext.getLogName() + traceback.format_exc())
        #         sendTelegramMessage(traceback.format_exc())
        pass

    def getListStrdDataList(self):
        return REP_DAO.fetch(self.fetchSqlId, "")

    def isReCrwal(self,url,page,dicStrdData,reCnt):
        return False

    def debugDicStrdData(self,dicStrdData = None):
        Log.debug(self.batchContext.getLogName() + "DicStrdData : " + str(dicStrdData))

    def setRowCounter(self,totalRowCount = None):
        if totalRowCount == None:
            Log.Info("totalRowCount 미정의 Error")
            return None
        else:
            self.rowCounter = BatchRowCounter(self.batchContext.getLogName(), totalRowCount,self.rowCountNumber,self.rowCounterInterval,self.MessageInterval,self.MessageUnit)

class CrawlingBasicSingle(Crawling):
     def crawl(self):
         url = self.makeURL()
         page = self.request(url)
         self.selfSaveDB(page)

    #BatchContect 세팅
    #self.batchContext = batchContext
    #self.batchContext.setFuncName(self.funcName)