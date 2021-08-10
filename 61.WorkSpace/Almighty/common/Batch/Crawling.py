import gc

from common.common.Log import *
from common.Batch.Batch import *
from common.common.Telegram import *
from common.common.URL import get_html
from common.ui.comUiFunc import *
from common.common.Table import *
import Server.COM
import Server.MIG

from urllib import parse
import urllib.parse
import Server.COM
import time

#LV1 크롤링 클래스
class Crawling:
    #global Log
    funcName = None         #함수명(Lv4필수)
    batchContext = None     #BatchContect(필수)
    dicPasi = None

    # 인자로드함수명
    fetchSqlId = None

    #[LV3/선택]rowCounter 설정값
    rowCounter = None       #Multi호출시 RowCounter Setting용
    rowCountNumber = 1
    rowCounterInterval = "N"
    MessageInterval = 10
    MessageUnit = "P"

    #URL Making 기준정보
    dicStrdDataList = None
    Strd = None
    dicStrd = None

    #테이블객체
    tableSvcPasi = None
    tableSvc = None
    tableSite = None
    tableSvcPasiItemIn = None

    #[LV3]
    sleepStamp = 0.1

    #기본인자
    pasiId = None
    svcId = None
    url = None
    dicParam = {}

    #초기화
    def __init__(self,strPasiId,strSvcId,batchContext = None):
        #self.Log = logging(batchContext.getLogName())
        #funcName Validation Check
        self.pasiId = strPasiId
        self.svcId = strSvcId

        # if self.funcName == None:
        #     logging.error("funcName 미정의 Error")
        #     return None
        # else:
        #     #BatchContect 세팅
        #     self.batchContext = batchContext
        #     self.batchContext.setFuncName(self.funcName)

        rslt = Server.COM.getPasi(self.pasiId, self.svcId)
        self.tableSvcPasi = rslt[0]
        self.tableSvc = rslt[1]
        self.tableSite = rslt[2]
        self.tableSvcPasiItemIn = Server.COM.getiItemParm(self.svcId,self.pasiId,'I')
        for tb in self.tableSvcPasiItemIn:
            if isNull(tb[0].tbl_nm) or isNull(tb[0].col_nm):
                self.dicParam[tb[0].item_nm] = tb[0].item_val
        self.sleepStamp = self.tableSite.slep_sec

    def run(self):
        try:
#            self.startLog() #START Log
            self.ready()    #크롤링 전 사전 Data 준비 작업
            self.crawl()    #URL 호출 후 삽입
        except : error()
        try:
            #self.report()   #report 및 마지막 정의
            pass
        except Exception as e:
            logging.error("Batch Report 출력 에러" + str(e))
            sendTelegramMessage("Batch Report 출력 에러" + str(e))
        #self.end()      #report 및 마지막 정의

#    def startLog(self):
        #기본로그 출력
#        logging.info(self.batchContext.getLogName()+"####################START[" + self.batchContext.getFuncName() + "]####################")
#        sendTelegramMessage("START[" + self.batchContext.getFuncName() + "]")

    #Lv2 구현
    def ready(self):
        self.dicPasi = getDicFromListTable(Server.COM.getPasi(self.pasiId,self.svcId))[0]
        if isNotNull(self.dicPasi.get('parm_load_func_nm',None)):
            self.Strd = eval(self.dicPasi.get('parm_load_func_nm',''))
            self.dicStrd = getDicFromListTable(self.Strd)
            #self.dicStrdDataList = self.getListStrdDataList()
        #rowCounter 세팅
        #self.setRowCounter(self.Strd.__len__())

    # Lv2 구현
    def crawl(self):
        for sd in self.dicStrd:
            print("########sd##########")
            print(sd)
            #item에 컬럼값이 등록되면 기준Data 세팅
            for tb in self.tableSvcPasiItemIn:
                if isNotNull(tb[0].tbl_nm) and isNotNull(tb[0].col_nm):
                    self.dicParam[tb[0].item_nm] = sd[tb[0].col_nm]
            try:
                reCnt = 0
                while True:
                    reCnt = reCnt + 1
                    self.debugDicStrdData(self.dicStrd)
                    url = self.makeURL(sd,reCnt)
                    print(url)
                    page = self.request(url)
                    print(page)
                    self.selfSaveDB(page,self.dicStrd,url)
                    time.sleep(self.sleepStamp)
                    #if self.isReCrwal(url,page,self.dicStrd,reCnt) == False:
                        #self.rowCounter.Cnt()
                        #break
                gc.collect()
            except Exception as e:
                error()
#                logging.error(self.batchContext.getLogName() + traceback.format_exc())
#                sendTelegramMessage(traceback.format_exc())

    def makeURL(self, dicStrdData=None, reCnt=None):
        for tb in self.tableSvcPasiItemIn:
            if isNotNull(tb[0].tbl_nm) and isNotNull(tb[0].col_nm):
                self.dicParam[tb[0].item_nm]=dicStrdData[tb[0].col_nm]
        self.url = self.tableSite.bas_prtc + "://"  # 프로토콜 http
        self.url += urllib.parse.quote(self.tableSite.bas_url + self.tableSvc.bas_svc_url,
                                       encoding=self.tableSite.enc_cd)
        if self.tableSvc.req_way_cd == "GET":
            self.url += "?" + urllib.parse.urlencode(self.dicParam, encoding=self.tableSite.enc_cd)
        elif self.tableSvc.req_way_cd == "POST":
            pass
        return self.url

        # print('makeURL')
        # url = self.selfMakeURL(dicStrdData,reCnt)
        # logging.info(self.batchContext.getLogName() + " ReCnt : " + str(reCnt) + url.printURL())
        # return url

    def report(self):
        # Report
        dicNewRowList = REP_DAO.fetch(self.sqlReportFetchId, "")
        logging.info(self.batchContext.getLogName() + "####################Batch Report####################")
        sendTelegramMessage("[Batch Report]")
        logging.info(self.batchContext.getLogName() + "신규 건 수  : " + str(dicNewRowList.__len__()) + " 건")
        sendTelegramMessage("신규 건수 : " + str(dicNewRowList.__len__()) + " 건")
        if dicNewRowList.__len__() > 0:
            logging.info(self.batchContext.getLogName() + str(dicNewRowList))
            sendTelegramMessage(self.batchContext.getLogName() + str(dicNewRowList))

#    def end(self):
#       logging.info(self.batchContext.getLogName() + "####################END[" + self.batchContext.getFuncName() + "]####################")
#        sendTelegramMessage("END[" + self.batchContext.getFuncName() + "]")

    #[LV4 구현]각 Lv4 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
    #def selfMakeURL(self,dicStrdData = None):
    #    return "http://test.com"

    #[LV4 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,page,dicStrdData = None,url = None):
        pass

    def request(self,url):
        page = get_html(url,self.tableSvc.req_way_cd,self.dicParam)
#        logging.debug(self.batchContext.getLogName() + str(page))
        return page

    def getFuncName(self):
        return self.funcName

    def setRowCounter(self,totalRowCount = None):
        if totalRowCount == None:
            Log.Info("totalRowCount 미정의 Error")
            return None
        else:
            self.rowCounter = BatchRowCounter(self.batchContext.getLogName(), totalRowCount,self.rowCountNumber,self.rowCounterInterval,self.MessageInterval,self.MessageUnit)

    def getListStrdDataList(self):
        return REP_DAO.fetch(self.fetchSqlId, "")

    def isReCrwal(self,url,page,dicStrdData,reCnt):
        return False

    def debugDicStrdData(self,dicStrdData = None):
#        logging.debug(self.batchContext.getLogName() + "DicStrdData : " + str(dicStrdData))
        pass

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

if __name__ == '__main__':
    batchContext = simpleBatchContext("CrawlingBBCmpxTyp")
    CrawlObject = Crawling('BBRegnLv2','BBRegn',batchContext)
    CrawlObject.run()