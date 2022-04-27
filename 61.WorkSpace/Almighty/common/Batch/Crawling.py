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
from common.common.UserException import *

from urllib import parse
import urllib.parse
import Server.COM
import time
import copy
import os
import json
from datetime import datetime

#Multi Proccessing 용 import [출처] Python Multiprocessing(Pool)을 사용한 데이터 처리 속도 개선|작성자 SungWook Kang
import multiprocessing as mp
from multiprocessing import Pool
import threading

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
    MessageInterval = 100
    MessageUnit = "P"
    commitCount = 100

    #Multi Processing Thread
    MultiProcessCnt = 1000
    MultiThreadCuttingCnt = 1000
    num_cores = 0
    num_threads = 0

    #URL Making 기준정보
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
    jobId = None
    execDtm = None
    JobExec = None
    job = None
    act = None
    function = None
    process_number = 0

    tbJobFuncExecStrd = None #작업기능실행기준의 종료 상태를 update하기 위한 변수

    #초기화
    def __init__(self,strPasiId,strSvcId,batchContext = None,JobExec = None, job = None, act = None, function = None, process_number = 0):
        try:
            #funcName Validation Check
            self.batchContext = batchContext
            self.pasiId = strPasiId
            self.svcId = strSvcId
            self.job = job
            self.act = act
            self.function = function
            self.process_number = process_number

            if JobExec == None:
                self.jobId = 'NOJOB'
                self.execDtm = datetime.now().strftime("%Y%m%d%H%M%S")
            else:
                self.jobId = JobExec.job_id
                self.execDtm = JobExec.exec_dtm
                self.jobExec = JobExec
                if self.jobExec.exec_parm6 != None and self.jobExec.exec_parm6 != '' and len(self.jobExec.exec_parm6) > 0:
                    self.num_cores = int(self.jobExec.exec_parm6)
                    if self.jobExec.exec_parm7 != None and self.jobExec.exec_parm6 != '' and len(self.jobExec.exec_parm7) > 0:
                        self.num_threads = int(self.jobExec.exec_parm7)

            #입력받은 pasi_id로 Pasing 정보를 가져옴
            rslt = Server.COM.getPasi(self.pasiId, self.svcId)
            if rslt == None:
                blog.error(self.batchContext.getLogName() + 'Pasi is not registered : [pasi_id : ' + self.pasiId + "][svc_id : " + self.svcId + "]")
                raise TypeError('Pasi is not registered : [pasi_id : ' + self.pasiId + "][svc_id : " + self.svcId + "]")
            self.tableSvcPasi = rslt[0]
            self.tableSvc = rslt[1]
            self.tableSite = rslt[2]
            self.tableSvcPasiItemIn = Server.COM.getiItemParm2(self.svcId,self.pasiId,'I')
            for tb in self.tableSvcPasiItemIn:
                if (isNull(tb[0].tbl_nm) or isNull(tb[0].col_nm)) and tb[0].dlmi_str == "GET":
                    self.dicParam[tb[0].item_nm] = tb[0].item_val
            self.sleepStamp = self.tableSite.slep_sec

            self.dicPasi = getDicFromListTable(Server.COM.getPasi(self.pasiId, self.svcId))[0]
            if self.dicPasi == None:  # 기준값이 없는경우(1번 크롤링)
                blog.error(self.batchContext.getLogName() + "Pasi 정보가 없습니다.")
                raise TypeError

            self.outParam = Server.COM.getiItemParm2(self.svcId, self.pasiId, 'O')
            self.outMultiParam = Server.COM.getiItemParmMulti(self.svcId, self.pasiId, 'O')
            a = copy.deepcopy(self.outParam)
            b = copy.deepcopy(self.outMultiParam)
            self.outAllTblParam = a + b
            for param in self.outAllTblParam:
                if param[0].tbl_nm == 'm' and param[1] == None:  # Multi용 테이블 리스트를 제거
                    self.outAllTblParam.remove(param)
            self.crawlCdExec = Server.COM.getCrawlCdExec(self.tableSvcPasi.svc_id, self.tableSvcPasi.pasi_id, 0)
            if isNull(self.crawlCdExec):
                blog.info(self.batchContext.getLogName() + "코드실행 정보가 없습니다. 코드실행관리에서 등록하세요")
                sendTelegramMessage(self.batchContext.getFuncName() + "코드실행 정보가 없습니다. 코드실행관리에서 등록하세요")
                # raise TypeError
        except:
            sendTelegramMessage("Crawling 초기화 Error : " + str(traceback.format_exc()))
            blog.error(traceback.format_exc())

    #Lv2 구현
    def ready(self):
        """
            기준정보를 세팅함.
        :return:
        """
        self.dicStrd = self.getListStrdDataList()
        if self.dicStrd == None:
            return False

        #rowCounter 세팅
        if isNotNull(self.Strd):    #기준값이 있는경우
            blog.info(self.batchContext.getLogName()+ "배치 수행전 예상 호출 총 건수 : " + str(self.Strd.__len__()))
            sendTelegramMessage(self.batchContext.getFuncName() + "배치 수행전 예상 호출 총 건수 : " + str(self.Strd.__len__()))
            self.setRowCounter(self.Strd.__len__())
            return True
        else:   #기준값이 없는경우
            self.setRowCounter(1) #ROW Counter는 1개
            return False

    def run(self):
        try:
            self.startLog() #START Log
            while self.ready():    #실행기준Data가 존재할때까지 실행
                dicSingleProcessParam = {}
                dicSingleProcessParam['listDicStrd'] = copy.deepcopy(self.dicStrd)
                dicSingleProcessParam['dicParam'] = copy.deepcopy(self.dicParam)
                self.crawl(dicSingleProcessParam)    #URL 호출 후 삽입
                dicSingleProcessParam = {}
            blog.info(self.batchContext.getLogName() + "대기열 실행 기준 Data 없음")
        except CrawlingEndException as e:
            message = self.batchContext.getLogName() + "대기열 실행 기준 Data가 없습니다. 프로세스를 종료합니다.["+ str(self.process_number) + "]"
            blog.info(message)
            sendTelegramMessage(message)
        except Exception as e :
            blog.error(self.batchContext.getLogName() + traceback.format_exc())
            sendTelegramMessage("Batch 수행 에러 : " + str(traceback.format_exc()))
            raise
        try:
            #self.report()   #report 및 마지막 정의
            pass
        except Exception as e:
            blog.error("Batch Report 출력 에러" + str(traceback.format_exc()))
            sendTelegramMessage("Batch Report 출력 에러" + str(traceback.format_exc()))
        #self.end()      #report 및 마지막 정의

    def threadCrwal(self,listparm):
        for i in range(0,len(listparm)):
            p = threading.Thread(target=self.crawl,args=(listparm[i],))
            p.start()

    def startLog(self):
        #기본로그 출력
        global blog
        blog = Logger(LogName=self.batchContext.getLogFileName(), Level="INFO", name = "Batch").logger
        blog.info(self.batchContext.getLogName()+"####################START[" + self.batchContext.getFuncName() + "]####################")
        sendTelegramMessage("START[" + self.batchContext.getFuncName() + "]")

    # Lv2 구현
    def crawl(self,dicparm):
        """
        1. 기준 정보를 Inparam 매핑정보를 사용해 url를 조합한다.
        2. 조합한 url을 호출한다.
        :return:
        """
        blog = logging.getLogger('Batch')
        dicStrd = dicparm['listDicStrd']
        dicParam = dicparm['dicParam']
        ss = createSession()

        if dicStrd != None:
            for sd in dicStrd:
                blog.debug(self.batchContext.getLogName() + "========================단위 CRAWL START !!!==========================")
                #item에 컬럼값이 등록되면 기준Data 세팅
                for tb in self.tableSvcPasiItemIn:
                    if isNotNull(tb[0].tbl_nm) and isNotNull(tb[0].col_nm) and tb[0].dlmi_str == "GET":
                        self.dicParam[tb[0].item_nm] = sd[tb[0].col_nm]
                reCnt = 0
                blog.debug(self.batchContext.getLogName() + "dicParam Setting 완료")
                while True:
                    reCnt = reCnt + 1
                    blog.debug(self.batchContext.getLogName() + "make URL 이전")
                    url = self.makeURL(sd,reCnt,dicParam = dicParam)
                    blog.info(self.batchContext.getLogName() + "CALL URL : " + url)
                    page = self.request(url)
                    cPage = self.convertPage(page)  #page를 객체화(BeutifulShop)형태로 변경
                    self.selfSaveDB(cPage,sd,url,session = ss)
                    blog.debug(self.batchContext.getLogName() + "SLEEP 전 ")
                    time.sleep(self.sleepStamp)
                    blog.debug(self.batchContext.getLogName() + "SLEEP 후 ")
                    if self.isReCrwal(url,page,cPage,dicStrd,reCnt) == False:
                        blog.debug(self.batchContext.getLogName() + "Cnt 전 ")
                        self.rowCounter.Cnt()
                        blog.debug(self.batchContext.getLogName() + "Cnt 후 ")
                        break

                blog.debug(self.batchContext.getLogName() + "COMMIT전 ")
                self.CountCommit(session = ss)
                blog.debug(self.batchContext.getLogName() + "COMMIT후 ")
                blog.debug(self.batchContext.getLogName() + "단위 CRAWL END !!!")
        else:
            #null인경우 1번실행용도
            reCnt = 0
            while True:
                reCnt = reCnt + 1
                url = self.makeURL(None,reCnt)
                blog.info("CALL URL : " + url)
                page = self.request(url)
                blog.debug("PAGE : " + page)
                cPage = self.convertPage(page)
                blog.debug("convert Page : " + cPage)
                self.selfSaveDB(cPage,None,url,session = ss)
                time.sleep(self.sleepStamp)
                if self.isReCrwal(url,page,dicStrd,reCnt) == False:
                    self.rowCounter.Cnt()
                    break
            self.CountCommit(ss)
            #gc.collect()

        self.tbJobFuncExecStrd.std_exec_stat_cd = 'T'
        self.tbJobFuncExecStrd.updateChg()
        ss.add(self.tbJobFuncExecStrd)
        ss.commit()
        ss.close()
        gc.collect()

    def makeURL(self, dicStrdData=None, reCnt=None, dicParam = None):
        """
        self,dicParam = url get방식의 파라미터를 가지고 있는 Dictionary
        :param dicStrdData: url기준정보를 가지고 있는 dictionary
        :param reCnt: 같은 url을 여러번 크롤링 하는 경우 (page가 있는 경우)
        :return:
        """
        sub_url = ""

        if dicParam == None:
            dicParam = self.dicParam

        for tb in self.tableSvcPasiItemIn: #debug 이상함
            #값이 'reCnt'인경우에 page정보를 url에 삽입한다.(추후 별도 함수로 변경 필요)
            if tb[0].item_val == 'reCnt':
                dicParam[tb[0].item_nm] = reCnt
            if tb[0].dlmi_str == "GET" and isNotNull(tb[0].tbl_nm) and isNotNull(tb[0].col_nm):
                dicParam[tb[0].item_nm]=dicStrdData[tb[0].col_nm]
#            elif tb[0].dlmi_str == "GET":
#                self.dicParam[tb[0].item_nm]=tb[0].item_val
            elif tb[0].dlmi_str != "GET":
                sub_url += tb[0].dlmi_str + dicStrdData[tb[0].col_nm]
        self.url = self.tableSite.bas_prtc + "://"  # 프로토콜 http
        if self.tableSite.han_enc_yn == "Y":
            self.url += urllib.parse.quote(self.tableSite.bas_url + self.tableSvc.bas_svc_url,
                                           encoding=self.tableSite.enc_cd)
        else:
            self.url += self.tableSite.bas_url + self.tableSvc.bas_svc_url
        self.url += sub_url

        if self.tableSvc.req_way_cd == "GET":
            if self.tableSite.han_enc_yn == "Y":
                self.url += "?" + urllib.parse.urlencode(dicParam, encoding=self.tableSite.enc_cd)
            else:
                self.url += "?" + urllib.parse.urlencode(dicParam)
        elif self.tableSvc.req_way_cd == "POST":
            pass
        return self.url

    def report(self):
        # Report
        #dicNewRowList = REP_DAO.fetch(self.sqlReportFetchId, "")
        #blog.info(self.batchContext.getLogName() + "####################Batch Report####################")
        #sendTelegramMessage("[Batch Report]")
        #blog.info(self.batchContext.getLogName() + "신규 건 수  : " + str(dicNewRowList.__len__()) + " 건")
        #sendTelegramMessage("신규 건수 : " + str(dicNewRowList.__len__()) + " 건")
        #if dicNewRowList.__len__() > 0:
        #    blog.info(self.batchContext.getLogName() + str(dicNewRowList))
        #    sendTelegramMessage(self.batchContext.getLogName() + str(dicNewRowList))
        pass

    def end(self):
        commit()
        blog.info(self.batchContext.getLogName() + "####################END[" + self.batchContext.getFuncName() + "]####################")
        sendTelegramMessage("END[" + self.batchContext.getFuncName() + "]")

    #[LV4 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,cPage,dicStrdData = None,url = None, session = None):
        blog.debug(" Page : " + str(cPage))
        if len(self.crawlCdExec) > 0:
            self.reCurParse(cPage,self.crawlCdExec[0],dicStrdData, session = session)
        pass

    def reCurParse(self,page,cdex,strd,session = None):
        ss = session
        #코드실행에 등록된 명령대로 1차 파싱
        if cdex[1].cd_exec_cl_cd == "F": #Function
            strExec = cdex[1].exec_cd_cnts + "(" + '"' + str(cdex[0].exec_parm_val) + '"' + ")"
            pasiPage = eval(strExec)
        elif cdex[1].cd_exec_cl_cd == "L":  # list
            strExec = cdex[1].exec_cd_cnts + str(cdex[0].exec_parm_val)
            pasiPage = eval(strExec)

        if pasiPage != None:
            #단위 페이지를 파싱하여 INSERT
            for p in pasiPage:
                #if self.tableSvcPasi.pasi_way_cd == 'SOUP':
                listTable = self.getTableListByOutMapping(self.svcId, self.pasiId, p, strd)
                for tb in listTable:
                    delattr(tb,'reg_user_id')
                    delattr(tb,'reg_dtm')
                    tb.updateChg()
                    try:
                        ss.add(tb)
                        blog.debug("merge 이후 : " + str(tb))
                    except Exception as e:
                        blog.error(traceback.format_exc())
                listTable = None
        return True

    def convertPage(self,page):
        """
        Page를 객체화된 형태로 변경한다.
        :param page: page정보(String)
        :return: BeautifulShop 객체
        """
        if self.tableSvcPasi.pasi_way_cd == 'SOUP':
            #return BeautifulSoup(page, 'html.parser')
            return BeautifulSoup(page, 'lxml-xml')
        elif self.tableSvcPasi.pasi_way_cd == 'JSON':
            soup = BeautifulSoup(page, 'html.parser')  # 파싱을 위한 객체화
            l = str(soup)
            j = json.loads(l)  # json 객체로 로딩
            return j
        else:
            raise Exception

    def getTableListByOutMapping(self,strSvcId,strPasiId,p,strd):
        r"""
            단위 페이지를 파싱한다.
        :param strSvcId: 서비스ID
        :param strPasiId: 파싱ID
        :param p: page
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
                str = self.getParsetext(tb[0],p)
                dicTableList[tb[2].cls_nm][tb[1].col_nm] = str

        for key in dicTableList.keys():
            dicTableList[key]['job_id'] = self.jobId
            dicTableList[key]['exec_dtm'] = self.execDtm

        rslt = getListTableFromDic(dicTableList)
        return rslt

    def getParsetext(self,t,p):
        r"""
            Parsing한 단위Page에서 값을 가져온다.
        :param item_nm: 아이템명
        :param p: 파싱한 Page
        :return:
        """

        try:
            if self.tableSvcPasi.pasi_way_cd == 'SOUP':
                str = p.find(t.item_nm).text
            elif self.tableSvcPasi.pasi_way_cd == 'JSON':
                try:
                    str = p[t.item_nm]
                except KeyError:
                    blog.debug("getParsetext >> 정의된 값이 존재하지 않음 : " + t.item_nm )
                    str = ""
            else:
                raise Exception
        except AttributeError as e:
            str = None
            blog.debug("Attribute Not found : item :[" + t.item_nm + "]")
        #BeautifulShop의 경우 아래의 함수로 값을 가져온다.
        if isNotNull(t.excp_str):
            excpList = t.excp_str.split("||")
            for excp in excpList:
                str = StrReplace(str,excp)
        return str

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
                execStrd = self.dicPasi.get('parm_load_func_nm', '')
                execStrd = execStrd[:-1] + "2,'" + self.job.job_id +"','"+ self.act.act_id + "','" + self.function.func_id + "','" + self.execDtm + "'," + str(self.process_number) +")"  # Crawling Object에서 수행하는 경우 2번으로 호출
                rslt = eval(execStrd)
                if len(rslt) != 2:
                    message = self.batchContext.getLogName()+"정의된 함수의 인자가 일치하지 않습니다.(2개 필요)"
                    blog.error(message)
                    sendTelegramMessage(message)
                    raise Exception(message)
                self.Strd = copy.deepcopy(rslt[0])
                self.tbJobFuncExecStrd = copy.deepcopy(rslt[1])

                if self.Strd != None and self.Strd != False:
                    return getDicFromListTable(self.Strd)
                else : raise CrawlingEndException #기준정보가 없으면 배치가 종료된 것 이므로
            else :
                blog.info(self.batchContext.getLogName() + "parm_load_func_nm is null ==> dicPasi : " + str(self.dicPasi))
                return None
        else :
            blog.error(self.batchContext.getLogName() + "parm_load_func_nm is empty ==> dicPasi : " + str(self.dicPasi))
            raise ValueError

    def isReCrwal(self,url,page,cPage,dicStrdData,reCnt):
        return False

    def debugDicStrdData(self,dicStrdData = None):
        blog.debug(self.batchContext.getLogName() + "DicStrdData : " + str(dicStrdData))
        pass

    def CountCommit(self,session = None):
        ss = session
        cnt = self.rowCounter.getCount()
        if cnt % self.commitCount == 0:
            ss.commit()
            gc.collect()

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
    #num_cores = mp.cpu_count()
    #print(num_cores)
    pass
    #print(num_cores)
    #batchContext = simpleBatchContext("NVCmpxTyp")
    #CrawlObject = Crawling('NVCmpxTyp','NVComplexTyp',batchContext)
    #CrawlObject.run()