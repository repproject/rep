import gc
from bs4 import BeautifulSoup
from sqlalchemy.engine.row import Row

from common.Batch.Batch import *
from common.common.Telegram import *
from common.common.URL import get_html
from common.common.Table import *
import Server.COM
import Server.MIG
from Server.Basic import *
from common.Batch.Basic import *

from urllib import parse
import urllib.parse
import Server.COM
import time
import copy
import os

#LV1 크롤링 클래스
class Crawling:
    funcName = None         #함수명(Lv4필수)
    batchContext = None     #BatchContect(필수)
    dicPasi = None

    # 인자로드함수명
    fetchSqlId = None

    #[LV3/선택]rowCounter 설정값
    rowCounter = None       #Multi호출시 RowCounter Setting용
    rowCountNumber = 500
    rowCounterInterval = "N"
    MessageInterval = 10
    MessageUnit = "P"
    commitCount = 1

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
    outParam = []
    outMultiParam = []
    outAllTblParam = []
    crawlCdExec = None

    #초기화
    def __init__(self,strPasiId,strSvcId,batchContext = None):
        try:
            #funcName Validation Check
            self.batchContext = batchContext
            self.pasiId = strPasiId
            self.svcId = strSvcId

            rslt = Server.COM.getPasi(self.pasiId, self.svcId)
            if rslt == None:
                blog.error(self.batchContext.getLogName() + 'Pasi is not registered : [pasi_id : ' + self.pasiId + "][svc_id : " + self.svcId + "]")
                raise TypeError('Pasi is not registered : [pasi_id : ' + self.pasiId + "][svc_id : " + self.svcId + "]")
            self.tableSvcPasi = rslt[0]
            self.tableSvc = rslt[1]
            self.tableSite = rslt[2]
            self.tableSvcPasiItemIn = Server.COM.getiItemParm(self.svcId,self.pasiId,'I')
            for tb in self.tableSvcPasiItemIn:
                if isNull(tb[0].tbl_nm) or isNull(tb[0].col_nm):
                    self.dicParam[tb[0].item_nm] = tb[0].item_val
            self.sleepStamp = self.tableSite.slep_sec
        except:
            blog.error(traceback.format_exc())
            sendTelegramMessage("Crawling 초기화 Error : " + str(traceback.format_exc()))

    def run(self):
        try:
            self.startLog() #START Log
            self.ready()    #크롤링 전 사전 Data 준비 작업
            self.crawl()    #URL 호출 후 삽입
        except :
            blog.error(traceback.format_exc())
            sendTelegramMessage("Batch 수행 에러 : " + str(traceback.format_exc()))
        try:
            #self.report()   #report 및 마지막 정의
            pass
        except Exception as e:
            blog.error("Batch Report 출력 에러" + str(traceback.format_exc()))
            sendTelegramMessage("Batch Report 출력 에러" + str(traceback.format_exc()))
        #self.end()      #report 및 마지막 정의

    def startLog(self):
        #기본로그 출력
        global blog
        blog = Logger(LogName=self.batchContext.getLogName(), Level="DEBUG", name = "Batch").logger
        blog.info(self.batchContext.getLogName()+"####################START[" + self.batchContext.getFuncName() + "]####################")
        sendTelegramMessage("START[" + self.batchContext.getFuncName() + "]")

    #Lv2 구현
    def ready(self):
        self.dicPasi = getDicFromListTable(Server.COM.getPasi(self.pasiId,self.svcId))[0]
        if self.dicPasi == None :   #기준값이 없는경우(1번 크롤링)
            blog.error(self.batchContext.getLogName() + "Pasi 정보가 없습니다.")
            raise TypeError
        self.dicStrd = self.getListStrdDataList()
        #rowCounter 세팅
        if isNotNull(self.Strd):    #기준값이 있는경우
            blog.info(self.batchContext.getLogName()+ "총 건수 : " + str(self.Strd.__len__()))
            sendTelegramMessage(self.batchContext.getFuncName() + "총 건수 : " + str(self.Strd.__len__()))
            self.setRowCounter(self.Strd.__len__())
        else:   #기준값이 없는경우
            self.setRowCounter(1) #ROW Counter는 1개

        self.outParam = Server.COM.getiItemParm2(self.svcId, self.pasiId, 'O')
        self.outMultiParam = Server.COM.getiItemParmMulti(self.svcId, self.pasiId, 'O')
        a = copy.deepcopy(self.outParam)
        b = copy.deepcopy(self.outMultiParam)
        self.outAllTblParam = a + b
        #print(self.outAllTblParam)
        for param in self.outAllTblParam:
            if param[0].tbl_nm == 'm' and param[1] == None: #Multi용 테이블 리스트를 제거
                self.outAllTblParam.remove(param)
        self.crawlCdExec = Server.COM.getCrawlCdExec(self.tableSvcPasi.svc_id, self.tableSvcPasi.pasi_id, 0)
        if isNull(self.crawlCdExec):
            blog.error(self.batchContext.getLogName() + "코드실행 정보가 없습니다. 코드실행관리에서 등록하세요")
            raise TypeError

    # Lv2 구현
    def crawl(self):
        if self.dicStrd != None:
            for sd in self.dicStrd:
                #item에 컬럼값이 등록되면 기준Data 세팅
                for tb in self.tableSvcPasiItemIn:
                    if isNotNull(tb[0].tbl_nm) and isNotNull(tb[0].col_nm):
                        self.dicParam[tb[0].item_nm] = sd[tb[0].col_nm]
                reCnt = 0
                while True:
                    reCnt = reCnt + 1
                    self.debugDicStrdData(self.dicStrd)
                    url = self.makeURL(sd,reCnt)
                    blog.info("CALL URL : " + url)
                    page = self.request(url)
                    cPage = self.convertPage(page)
                    self.selfSaveDB(cPage,sd,url)
                    time.sleep(self.sleepStamp)
                    if self.isReCrwal(url,page,self.dicStrd,reCnt) == False:
                        self.rowCounter.Cnt()
                        break
                self.CountCommit()
                gc.collect()
        else:
            #null인경우 1번실행용도
            reCnt = 0
            while True:
                reCnt = reCnt + 1
                url = self.makeURL(None,reCnt)
                blog.info("CALL URL : " + url)
                page = self.request(url)
                cPage = self.convertPage(page)
                self.selfSaveDB(cPage,None,url)
                time.sleep(self.sleepStamp)
                if self.isReCrwal(url,page,self.dicStrd,reCnt) == False:
                    self.rowCounter.Cnt()
                    break
            self.CountCommit()
            gc.collect()

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

    def report(self):
        # Report
        dicNewRowList = REP_DAO.fetch(self.sqlReportFetchId, "")
        blog.info(self.batchContext.getLogName() + "####################Batch Report####################")
        sendTelegramMessage("[Batch Report]")
        blog.info(self.batchContext.getLogName() + "신규 건 수  : " + str(dicNewRowList.__len__()) + " 건")
        sendTelegramMessage("신규 건수 : " + str(dicNewRowList.__len__()) + " 건")
        if dicNewRowList.__len__() > 0:
            blog.info(self.batchContext.getLogName() + str(dicNewRowList))
            sendTelegramMessage(self.batchContext.getLogName() + str(dicNewRowList))

    def end(self):
        commit()
        blog.info(self.batchContext.getLogName() + "####################END[" + self.batchContext.getFuncName() + "]####################")
        sendTelegramMessage("END[" + self.batchContext.getFuncName() + "]")

    #[LV4 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,cPage,dicStrdData = None,url = None):
        blog.debug(" Page : " + str(cPage))
        if len(self.crawlCdExec) > 0:
            self.reCurParse(cPage,self.crawlCdExec[0],dicStrdData)
        pass

    def reCurParse(self,page,cdex,strd):
        #코드실행에 등록된 명령대로 파싱
        if cdex[1].cd_exec_cl_cd == "F": #Function
            strExec = cdex[1].exec_cd_cnts + "(" + '"' + str(cdex[0].exec_parm_val) + '"' + ")"
            pasiPage = eval(strExec)

        for p in pasiPage:
            if self.tableSvcPasi.pasi_way_cd == 'SOUP':
                listTable = self.getTableListByOutMapping(self.svcId, self.pasiId, p,strd)
                for tb in listTable:
                    delattr(tb,'reg_user_id')
                    delattr(tb,'reg_dtm')

                blog.debug(listTable)
                mergeListNC(listTable)
                # for tb in self.getTableListByOutMapping(self.svcId, self.pasiId, p,strd):
                #     try:
                #         try:
                #             insert(tb)
                #         except IntegrityError as ie:
                #             #rollback()
                #             #blog.error(traceback.format_exc())
                #             # delattr(tb,'reg_user_id')
                #             # delattr(tb,'reg_dtm')
                #             merge(tb)
                #             pass
                #     except PendingRollbackError as pre:
                #         pass
                #     print("ok")
        return True

    def convertPage(self,page):
        if self.tableSvcPasi.pasi_way_cd == 'SOUP':
            return BeautifulSoup(page, 'html.parser')
        else:
            print('convertPage error')
            raise Exception

    def getTableListByOutMapping(self,strSvcId,strPasiId,p,strd):
        r"""

        :param strSvcId:
        :param strPasiId:
        :param p:
        :param strd:
        :return: TableList Type
        """
        dicTableList = {}

        #Out Param기준정보를 가져온다
        for tb in self.outAllTblParam:
            #SvcPasiItem,TblCol,Tbl
            #테이블 클래스명을 세팅한다.
            if tb[2].cls_nm not in dicTableList:
                dicTableList[tb[2].cls_nm] = {}

            if tb[0].item_src_cl_cd == 'ST': #기준정보
                # 기준정보의경우 기준정보에서 값을 가져옴.
                dicTableList[tb[2].cls_nm][tb[1].col_nm] = strd[tb[0].item_nm]
            else:
                #기준정보가 아닌 경우 page에서 값을 가져온다.
                dicTableList[tb[2].cls_nm][tb[1].col_nm] = self.getParsetext(tb[0],p)
        return getListTableFromDic(dicTableList)

    def getParsetext(self,t,p):
        r"""
            Parsing한 단위Page에서 값을 가져온다.
        :param item_nm: 아이템명
        :param p: 파싱한 Page
        :return:
        """
        if self.tableSvcPasi.pasi_way_cd == 'SOUP':
            str = p.find(t.item_nm).text
            #BeautifulShop의 경우 아래의 함수로 값을 가져온다.
            if isNotNull(t.excp_str):
                excpList = t.excp_str.split("||")
                for excp in excpList:
                    str = StrReplace(str,excp)
            return str
        else : raise Exception

    def request(self,url):
        page = get_html(url,self.tableSvc.req_way_cd,self.dicParam)
        blog.debug(self.batchContext.getLogName() + " PRINT PAGE : " + str(page))
        return page

    def getFuncName(self):
        return self.funcName

    def setRowCounter(self,totalRowCount = None):
        if totalRowCount == None:
            blog.Info(self.batchContext.getLogName() + "totalRowCount 미정의 Error")
            return None
        else:
            self.rowCounter = BatchRowCounter(self.batchContext.getLogName(), totalRowCount,self.rowCountNumber,self.rowCounterInterval,self.MessageInterval,self.MessageUnit)

    def getListStrdDataList(self):
        r"""
            등록된 함수를 실해하여
        :return:
        """
        if isNotNull(self.dicPasi.get('parm_load_func_nm',None)):
            if self.dicPasi.get('parm_load_func_nm',None) != 'null':
                self.Strd = eval(self.dicPasi.get('parm_load_func_nm', ''))
                return getDicFromListTable(self.Strd)
            else :
                blog.info(self.batchContext.getLogName() + "parm_load_func_nm is null ==> dicPasi : " + str(self.dicPasi))
                return None
        else :
            blog.error(self.batchContext.getLogName() + "parm_load_func_nm is empty ==> dicPasi : " + str(self.dicPasi))
            raise ValueError

    def isReCrwal(self,url,page,dicStrdData,reCnt):
        return False

    def debugDicStrdData(self,dicStrdData = None):
        blog.debug(self.batchContext.getLogName() + "DicStrdData : " + str(dicStrdData))
        pass

    def CountCommit(self):
        cnt = self.rowCounter.getCount()
        if cnt % self.commitCount == 0:
            commit()

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
    batchContext = simpleBatchContext("CrawlingBBCmpxTypPrice")
    CrawlObject = Crawling('BBRegnLv1','BBRegn',batchContext)
    #CrawlObject = Crawling('BBMarketPrice', 'BBMarketPrice', batchContext)
    CrawlObject.run()