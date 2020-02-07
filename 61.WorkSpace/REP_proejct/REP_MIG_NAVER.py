# -*- coding:utf-8 -*-
import time
from REP_DAO import *
from REP_URL import *
from REP_COM import *
from REP_TABLE import *
from REP_MIG_MAPP import *
import REP_URL
import REP_MIG
from REP_TLGR_MSG import *
import json
import schedule
import time

userid = 1000000011

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
            page = REP_MIG.get_html(url)
            Log.debug(batchContext.getLogName() + page)
            jsonPage = json.loads(page)

            for jsonComplex in jsonPage['complexList']:
                #json To tableDic
                dicKMIG_NV_CMPX = setJson2TableDic('KMIG_NV_CMPX', jsonComplex)
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
    dicCmpxIdList = fetch("selectNotUpdateNVCmpxList", "")
    # 네이버 단지 전체 건수를 기준으로 출력
    rowCounter = BatchRowCounter(batchContext.getLogName(), dicCmpxIdList.__len__(),1,"N",10,"N")

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
            dicKMIG_NV_CMPX_IMG = setJson2TableDic('KMIG_NV_CMPX_IMG', jsonPage1)
            dicKMIG_NV_CMPX_IMG['NV_CMPX_ID']=dicCmpxId['NV_CMPX_ID']
            dicKMIG_NV_CMPX_IMG['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX_IMG['CHG_USER_ID'] = userid

            try:
                insertBasicByTBLDic('KMIG_NV_CMPX_IMG', dicKMIG_NV_CMPX_IMG)
                dicKMIG_NV_CMPX_IMG = None;
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                Log.debug(batchContext.getLogName() + "네이버물건이미지 중복" + 'NV_CMPX_ID : ')

        #네이버물건상세갱신
        dicKMIG_NV_CMPX = setJson2TableDic('KMIG_NV_CMPX', jsonPage['complexDetail'])
        dicKMIG_NV_CMPX['REG_USER_ID'] = userid
        dicKMIG_NV_CMPX['CHG_USER_ID'] = userid

        dicBasicCond = {}
        dicBasicCond['NV_CMPX_ID'] =  dicCmpxId['NV_CMPX_ID']

        updateBaiscByTBLDic('KMIG_NV_CMPX',dicKMIG_NV_CMPX,dicBasicCond)

        #네이버물건재건축 INSERT
        if jsonPage.get('complexRebuilding',False):
            dicKMIG_NV_CMPX_RBLD = setJson2TableDic('KMIG_NV_CMPX_RBLD', jsonPage['complexRebuilding'])
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
            dicKMIG_NV_CMPX_TYP = setJson2TableDic('KMIG_NV_CMPX_TYP', jsonPageNvCmpxTyp)
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
                    dicKMIG_NV_CMPX_TYP_IMG = setJson2TableDic('KMIG_NV_CMPX_TYP_IMG', jsonPageNvCmpxTypImg)
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
                dicKMIG_NV_CMPX_TYP_STAT = setJson2TableDic('KMIG_NV_CMPX_TYP_STAT', jsonPageNvCmpxTyp['articleStatistics'])
                dicKMIG_NV_CMPX_TYP_STAT['NV_CMPX_ID'] = dicCmpxId['NV_CMPX_ID']
                dicKMIG_NV_CMPX_TYP_STAT['NV_CMPX_TYP_SEQ'] = dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ']
                dicKMIG_NV_CMPX_TYP_STAT['REG_USER_ID'] = userid
                dicKMIG_NV_CMPX_TYP_STAT['CHG_USER_ID'] = userid

                try:
                    insertBasicByTBLDic('KMIG_NV_CMPX_TYP_STAT', dicKMIG_NV_CMPX_TYP_STAT)
                    dicKMIG_NV_CMPX_TYP_STAT = None;
                except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                    Log.debug(batchContext.getLogName() + "네이버물건형통계 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'] + "/" + dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ'])

        rowCounter.Cnt()

        #네이버물건상세UPDATE
        time.sleep(NaverTimeStamp)

if __name__ == '__main__':
    updNaverComplexDtl()

