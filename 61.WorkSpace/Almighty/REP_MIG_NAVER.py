# -*- coding:utf-8 -*-
from REP_DAO import *
from common.common.URL import *
from REP_COM import *
from REP_TABLE import *
from common.common import URL
import REP_MIG
from common.common.Telegram import *
import json
import time

userid = 1000000011

#Lv4 네이버 매물
class CrawlingNVAtcl(CrawlingMultiNaver):
    funcName = "CrawlingNVAtcl"
    fetchSqlId =  "selectNVCmpxListforActl"
    #sqlReportFetchId = "selectNewBBRegnCdLv2"
    SVC_ID = "NVAtcl"

    MessageInterval = 10
    MessageUnit = "P"

    # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
    def selfMakeURL(self, dicStrdData=None, reCnt=None):
        seq = 0
        url = URL.URLMaker(self.SVC_ID)
        Log.debug(str(dicStrdData))
        url.addString(dicStrdData['NV_CMPX_ID'])
        url.add("page",str(reCnt))
        url.add("complexNo", dicStrdData['NV_CMPX_ID'])
        seq = int(dicStrdData['NV_CMPX_TYP_SEQ'])
        if seq > 0:
            Log.debug("DEBUG : if seq > 0: is True " + str(seq))
            url.add("areaNos", seq)
        else:
            url.deleteParam("areaNos")
        return url

    #[LV3 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,page,dicStrdData,url=None):
        try:
            jsonPage = json.loads(page)
        except Exception as e:
            Log.error(batchContext.getLogName() + "Json load Error : " + str(dicStrdData['NV_CMPX_ID']) + traceback.format_exc())
            sendMessage(batchContext.getLogName() + "Json load Error" + str(dicStrdData['NV_CMPX_ID']) + traceback.format_exc())
        tableName = "KMIG_NV_CMPX_ATCL"
        listdicTable = list()
        tableName2 = "KMIG_NV_CMPX_ATCL_TAG"
        listdicTable2 = list()

        dicTypNmSeq = {}

        if dicStrdData['NV_CMPX_TYP_SEQ'] == 0: #주택형일련번호 없이 호출한 경우
            dicParam = {}
            dicParam['NV_CMPX_ID'] = dicStrdData['NV_CMPX_ID']
            listDicNV_CMPX_TYP = fetch('selectNVCmxTypForActl',dicParam)
            for dicNV_CMPX_TYP in listDicNV_CMPX_TYP:
                dicTypNmSeq[dicNV_CMPX_TYP['CMPX_TYP_NM']] = dicNV_CMPX_TYP['NV_CMPX_TYP_SEQ']

        if len(jsonPage['articleList']) == 0 and int(dicStrdData['TOT_HSHL_CNT']) > 500 :
            Log.info(batchContext.getLogName() + "500세대 이상 매물 없음 : " + str(dicStrdData['NV_CMPX_ID'] + " ") + url.printURL())
            sendMessage(batchContext.getLogName() + "500세대 이상 매물 없음 : " + str(dicStrdData['NV_CMPX_ID'] + " ") + url.printURL())

        for jsonActl in jsonPage['articleList']:
            #print(jsonActl)
            # json To tableDic
            dicKMIG_NV_CMPX_ATCL = setJson2TableDic('KMIG_NV_CMPX_ATCL', jsonActl,url,page,batchContext)
            dicKMIG_NV_CMPX_ATCL['NV_CMPX_ID'] = dicStrdData['NV_CMPX_ID']
            if dicStrdData['NV_CMPX_TYP_SEQ'] == 0:
                try:
                    dicKMIG_NV_CMPX_ATCL['NV_CMPX_TYP_SEQ'] = dicTypNmSeq[dicKMIG_NV_CMPX_ATCL['CMPX_TYP_NM']]
                except KeyError as key:
                    dicKMIG_NV_CMPX_ATCL['NV_CMPX_TYP_SEQ'] = 0
            else:
                dicKMIG_NV_CMPX_ATCL['NV_CMPX_TYP_SEQ'] = dicStrdData['NV_CMPX_TYP_SEQ']
            dicKMIG_NV_CMPX_ATCL['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX_ATCL['CHG_USER_ID'] = userid
            listdicTable.append(dict(dicKMIG_NV_CMPX_ATCL))

            # isupdate = False
            #             #
            #             # try:
            #             #     insertBasicByTBLDic('KMIG_NV_CMPX_ATCL', dicKMIG_NV_CMPX_ATCL)
            #             # except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
            #             #     Log.debug(batchContext.getLogName() + "네이버매물 중복" + 'ATCL_NUM : ' + dicKMIG_NV_CMPX_ATCL['ATCL_NUM'])
            #             #     isupdate = True

            # if isupdate:
            #     dicBasicCond = {}
            #     dicBasicCond['ATCL_NUM'] = dicKMIG_NV_CMPX_ATCL['ATCL_NUM']
            #     updateBaiscByTBLDic('KMIG_NV_CMPX_ATCL', dicKMIG_NV_CMPX_ATCL, dicBasicCond)

            for strActlTag in jsonActl['tagList']:
                dicKMIG_NV_CMPX_ACTCL_TAG = dicTable['KMIG_NV_CMPX_ATCL_TAG']
                dicKMIG_NV_CMPX_ACTCL_TAG['ATCL_NUM'] = dicKMIG_NV_CMPX_ATCL['ATCL_NUM']
                dicKMIG_NV_CMPX_ACTCL_TAG['TAG_NM'] = strActlTag
                dicKMIG_NV_CMPX_ACTCL_TAG['REG_USER_ID'] = userid
                dicKMIG_NV_CMPX_ACTCL_TAG['CHG_USER_ID'] = userid

                listdicTable2.append(dict(dicKMIG_NV_CMPX_ACTCL_TAG))

                # try:
                #     insertBasicByTBLDic('KMIG_NV_CMPX_ATCL_TAG', dicKMIG_NV_CMPX_ACTCL_TAG)
                # except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                #     Log.debug(batchContext.getLogName() + "네이버매물태그 중복" + 'ATCL_NUM : ' + dicKMIG_NV_CMPX_ACTCL_TAG['ATCL_NUM'] + ' TAG_NM : ' + dicKMIG_NV_CMPX_ACTCL_TAG['TAG_NM'])
                # except Exception as e:
                #     Log.error(batchContext.getLogName() + str(e))

        try:
            insertBasicByTBLDicList(tableName, listdicTable)
        except pymysql.IntegrityError as e:  # 기존 중복 가능
            Log.debug(batchContext.getLogName() + str(e))
            Log.debug(batchContext.getLogName() + "네이버매물 중복 : " + str(dicStrdData['NV_CMPX_ID']) + "/" + str(dicStrdData['NV_CMPX_TYP_SEQ']))

        try:
            insertBasicByTBLDicList(tableName2, listdicTable2)
        except pymysql.IntegrityError as e:  # 기존 중복 가능
            Log.debug(batchContext.getLogName() + str(e))
            Log.debug(batchContext.getLogName() + "네이버매물태그 중복 : " + str(dicStrdData['NV_CMPX_ID']) + "/" + str(dicStrdData['NV_CMPX_TYP_SEQ']))

    def isReCrwal(self, url, page, dicStrdData, reCnt):
        jsonPage = json.loads(page)
        return jsonPage['isMoreData']

def migNaverComplexList(batchContext = None):
    #초기세팅 Log
    global Log
    try:
#        global LogObejct
        batchContext.setFuncName("migNaverComplexList")
#        LogObejct = Logger(batchContext.getLogName())
        Log.info(batchContext.getLogName()+"####################START[" + batchContext.getFuncName() + "]####################")
        sendMessage("START[" + batchContext.getFuncName() + "]")

        # 법정동 전체가져오기
        dicLeglCodeList = fetch("selectLeglLv3Dong", "")

        # rowCounter 설정
        rowCounter = BatchRowCounter(batchContext.getLogName(), dicLeglCodeList.__len__(), 1, "N", 10, "P")

        for dicLeglCode in dicLeglCodeList:

            #url호출
            url = NaverComplexListURL + dicLeglCode['LEGL_DONG_CD']
            Log.info(batchContext.getLogName() + url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }

            page = REP_MIG.get_html(url)
            Log.debug(batchContext.getLogName() + str(page))
            jsonPage = json.loads(page)

            for jsonComplex in jsonPage['complexList']:
                #json To tableDic
                dicKMIG_NV_CMPX = setJson2TableDic('KMIG_NV_CMPX',jsonComplex,url,page)
                dicKMIG_NV_CMPX['GOV_LEGL_DONG_CD']=dicLeglCode['LEGL_DONG_CD']
                dicKMIG_NV_CMPX['REG_USER_ID'] = userid
                dicKMIG_NV_CMPX['CHG_USER_ID'] = userid

                try:
                    insertBasicByTBLDic('KMIG_NV_CMPX',dicKMIG_NV_CMPX)
                except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                    Log.debug(batchContext.getLogName() + "네이버물건 중복" + 'NV_CMPX_ID : ' + dicKMIG_NV_CMPX['NV_CMPX_ID'])
            rowCounter.Cnt()
            time.sleep(NaverTimeStamp)
    except Exception as e:
        Log.error(batchContext.getLogName() + "####################ERROR[" + batchContext.getFuncName() + "]####################")
        Log.error(str(e))
        sendMessage("ERROR[" + batchContext.getFuncName() + "]")
        sendMessage(str(e))

    #Report
    dicNewNVCmpxeList = fetch("selectNewNVCmpxList", "")
    Log.info(batchContext.getLogName() + "####################Batch Report####################")
    sendMessage("[Batch Report]")
    Log.info(batchContext.getLogName() + "신규 네이버 단지 : " + str(dicNewNVCmpxeList.__len__()) + " 건")
    sendMessage("신규 네이버 단지 : " + str(dicNewNVCmpxeList.__len__()) + " 건")
    if dicNewNVCmpxeList.__len__() > 0 :
        Log.info(batchContext.getLogName() + str(dicNewNVCmpxeList))
        sendMessage(batchContext.getLogName() + str(dicNewNVCmpxeList))

    Log.info(batchContext.getLogName()+"####################END[" + batchContext.getFuncName() + "]####################")
    sendMessage("END[" + batchContext.getFuncName() + "]")

def updNaverComplexDtl(batchContext = None):
    #초기 세팅 - 로그

    global LogObejct
    batchContext.setFuncName("updNaverComplexDtl")
    LogObejct = Logger(batchContext.getLogName())
    Log.info(batchContext.getLogName()  + "####################START[updNaverComplexDtl]####################")
    sendMessage(batchContext.getLogName() + "START[updNaverComplexDtl]")

    # 네이버 단지 전체가져오기
    dicCmpxIdList = fetch("selectCmpxIdAll", "")
    #dicCmpxIdList = fetch("selectNotUpdateNVCmpxList", "")
    # 네이버 단지 전체 건수를 기준으로 출력
    rowCounter = BatchRowCounter(batchContext.getLogName(), dicCmpxIdList.__len__(),1,"N",10,"P")

    for dicCmpxId in dicCmpxIdList:
        Log.info(batchContext.getLogName() + str(dicCmpxId))

         #url호출
        url = NaverComplexDtlURL + dicCmpxId['NV_CMPX_ID']
        Log.info(batchContext.getLogName() + url)
        page = REP_MIG.get_html(url)
        jsonPage = json.loads(page)
        Log.debug(batchContext.getLogName() + str(jsonPage))

        #네이버물건이미지 삽입
        for jsonPage1 in jsonPage['photos']:
            #json To tableDic
            dicKMIG_NV_CMPX_IMG = setJson2TableDic('KMIG_NV_CMPX_IMG', jsonPage1,url,page,batchContext)
            dicKMIG_NV_CMPX_IMG['NV_CMPX_ID']=dicCmpxId['NV_CMPX_ID']
            dicKMIG_NV_CMPX_IMG['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX_IMG['CHG_USER_ID'] = userid

            try:
                insertBasicByTBLDic('KMIG_NV_CMPX_IMG', dicKMIG_NV_CMPX_IMG)
                dicKMIG_NV_CMPX_IMG = None;
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                Log.debug(batchContext.getLogName() + "네이버물건이미지 중복" + 'NV_CMPX_ID : ')

        #네이버물건상세갱신
        dicKMIG_NV_CMPX = setJson2TableDic('KMIG_NV_CMPX', jsonPage['complexDetail'],url,page,batchContext)
        dicKMIG_NV_CMPX['REG_USER_ID'] = userid
        dicKMIG_NV_CMPX['CHG_USER_ID'] = userid

        dicBasicCond = {}
        dicBasicCond['NV_CMPX_ID'] =  dicCmpxId['NV_CMPX_ID']

        updateBaiscByTBLDic('KMIG_NV_CMPX',dicKMIG_NV_CMPX,dicBasicCond)

        #네이버물건재건축 INSERT
        if jsonPage.get('complexRebuilding',False):
            dicKMIG_NV_CMPX_RBLD = setJson2TableDic('KMIG_NV_CMPX_RBLD', jsonPage['complexRebuilding'],url,page,batchContext)
            dicKMIG_NV_CMPX_RBLD['NV_CMPX_ID']=dicCmpxId['NV_CMPX_ID']
            dicKMIG_NV_CMPX_RBLD['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX_RBLD['CHG_USER_ID'] = userid

            try:
                insertBasicByTBLDic('KMIG_NV_CMPX_RBLD', dicKMIG_NV_CMPX_RBLD)
                dicKMIG_NV_CMPX_RBLD = None;
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                Log.debug(batchContext.getLogName() + "네이버물건재건축 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'])

        # 네이버물건형 INSERT
        for jsonPageNvCmpxTyp in jsonPage['complexPyeongDetailList']:
            dicKMIG_NV_CMPX_TYP = setJson2TableDic('KMIG_NV_CMPX_TYP', jsonPageNvCmpxTyp,url,page,batchContext)
            if jsonPageNvCmpxTyp.get('averageMaintenanceCost', False):
                dicKMIG_NV_CMPX_TYP['AVG_MNTN_AMT']  = jsonPageNvCmpxTyp['averageMaintenanceCost']['averageTotalPrice']
                dicKMIG_NV_CMPX_TYP['SMMR_MNTN_AMT'] = jsonPageNvCmpxTyp['averageMaintenanceCost']['summerTotalPrice']
                dicKMIG_NV_CMPX_TYP['WNTR_MNTN_AMT'] = jsonPageNvCmpxTyp['averageMaintenanceCost']['winterTotalPrice']

            dicKMIG_NV_CMPX_TYP['NV_CMPX_ID'] = dicCmpxId['NV_CMPX_ID']
            dicKMIG_NV_CMPX_TYP['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX_TYP['CHG_USER_ID'] = userid

            try:
                insertBasicByTBLDic('KMIG_NV_CMPX_TYP', dicKMIG_NV_CMPX_TYP)
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                Log.debug(batchContext.getLogName() + "네이버물건형 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'] + ' NV_CMPX_TYP_SEQ : ' + dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ'])

            if jsonPageNvCmpxTyp.get('grandPlanList', False):
                #네이버물건형이미지 INSERT
                for jsonPageNvCmpxTypImg in jsonPageNvCmpxTyp['grandPlanList']:
                    dicKMIG_NV_CMPX_TYP_IMG = setJson2TableDic('KMIG_NV_CMPX_TYP_IMG', jsonPageNvCmpxTypImg,url,page,batchContext)
                    dicKMIG_NV_CMPX_TYP_IMG['NV_CMPX_ID'] = dicCmpxId['NV_CMPX_ID']
                    dicKMIG_NV_CMPX_TYP_IMG['NV_CMPX_TYP_SEQ'] = dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ']
                    dicKMIG_NV_CMPX_TYP_IMG['REG_USER_ID'] = userid
                    dicKMIG_NV_CMPX_TYP_IMG['CHG_USER_ID'] = userid

                    try:
                        insertBasicByTBLDic('KMIG_NV_CMPX_TYP_IMG', dicKMIG_NV_CMPX_TYP_IMG)
                        dicKMIG_NV_CMPX_TYP_IMG = None
                    except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                        Log.debug(batchContext.getLogName() + "네이버물건형이미지 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'] + "/" + dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ'])

            if jsonPageNvCmpxTyp.get('articleStatistics', False):
                dicKMIG_NV_CMPX_TYP_STAT = setJson2TableDic('KMIG_NV_CMPX_TYP_STAT', jsonPageNvCmpxTyp['articleStatistics'],url,page,batchContext)
                dicKMIG_NV_CMPX_TYP_STAT['NV_CMPX_ID'] = dicCmpxId['NV_CMPX_ID']
                dicKMIG_NV_CMPX_TYP_STAT['NV_CMPX_TYP_SEQ'] = dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ']
                dicKMIG_NV_CMPX_TYP_STAT['REG_USER_ID'] = userid
                dicKMIG_NV_CMPX_TYP_STAT['CHG_USER_ID'] = userid

                try:
                    insertBasicByTBLDic('KMIG_NV_CMPX_TYP_STAT', dicKMIG_NV_CMPX_TYP_STAT)
                except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                    Log.debug(batchContext.getLogName() + "네이버물건형통계 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'] + "/" + dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ'])

                dicBasicCond2 = {}
                dicBasicCond2['NV_CMPX_ID'] = dicKMIG_NV_CMPX_TYP['NV_CMPX_ID']
                dicBasicCond2['NV_CMPX_TYP_SEQ'] = dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ']
                updateBaiscByTBLDic('KMIG_NV_CMPX_TYP_STAT', dicKMIG_NV_CMPX_TYP_STAT, dicBasicCond2)

                dicKMIG_NV_CMPX_TYP_STAT = None;


            if jsonPageNvCmpxTyp.get('maintenanceCostList', False):
                for json2 in jsonPageNvCmpxTyp['maintenanceCostList']:
                    dicKMIG_NV_CMPX_TYP_MNTN_PRC = setJson2TableDic('KMIG_NV_CMPX_TYP_MNTN_PRC', json2,url,page,batchContext)
                    dicKMIG_NV_CMPX_TYP_MNTN_PRC['NV_CMPX_ID'] = dicCmpxId['NV_CMPX_ID']
                    dicKMIG_NV_CMPX_TYP_MNTN_PRC['NV_CMPX_TYP_SEQ'] = dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ']
                    dicKMIG_NV_CMPX_TYP_MNTN_PRC['REG_USER_ID'] = userid
                    dicKMIG_NV_CMPX_TYP_MNTN_PRC['CHG_USER_ID'] = userid

                    try:
                        insertBasicByTBLDic('KMIG_NV_CMPX_TYP_MNTN_PRC', dicKMIG_NV_CMPX_TYP_MNTN_PRC)
                    except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                        Log.debug(batchContext.getLogName() + "네이버물건형유지비용 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'] + "/" + dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ'] + "/" + dicKMIG_NV_CMPX_TYP_MNTN_PRC['STD_YYMM'])

        rowCounter.Cnt()

        #네이버물건상세UPDATE
        time.sleep(NaverTimeStamp)

if __name__ == '__main__':

    dicFunc = {}
    dicFunc['JOB_ID'] = 'TESTJOB'
    dicFunc['JOB_NM'] = 'TESTJOB'
    dicFunc['ACT_ID'] = 'TESTJOB'
    dicFunc['ACT_NM'] = 'TESTJOB'
    dicFunc['FUNC_ID'] = 'TESTJOB'
    dicFunc['FUNC_NM'] = 'TESTJOB'

    now = datetime.now()

    batchContext = BatchContext(dicFunc,"test2",0000000000,now.strftime("%Y%m%d%H%M%S"))
    #updNaverComplexDtl(batchContext)
    CrawlObject = CrawlingNVAtcl(batchContext)
    CrawlObject.run()

