# -*- coding:utf-8 -*-
# import REP_DAO
import time
from REP_DAO import *
from REP_URL import *
from REP_COM import *
import REP_MIG
import REP_URL
import REP_DAO
import json
from REP_TABLE import *
from REP_MIG_MAPP import *

def migNaverComplexList():
    # 법정동 전체가져오기
    dicLeglCodeList = fetch("selectLeglLv3Dong", "")

    for dicLeglCode in dicLeglCodeList:
        #url호출
        url = NaverComplexListURL + dicLeglCode['LEGL_DONG_CD']
        log(url,"I")

        page = REP_MIG.get_html(url)
        print(page)
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
                log("네이버물건 중복" + 'NV_CMPX_ID : ' + dicKMIG_NV_CMPX['NV_CMPX_ID'],"D")
        time.sleep(NaverTimeStamp)
        
def updNaverComplexDtl():
    # 법정동 전체가져오기
    dicCmpxIdList = fetch("selectCmpxIdAll", "")

    for dicCmpxId in dicCmpxIdList:
         #url호출
        url = NaverComplexDtlURL + dicCmpxId['NV_CMPX_ID']
        log(url,"I")

        page = REP_MIG.get_html(url)
        print(page)
        jsonPage = json.loads(page)
        print(jsonPage)

        #네이버물건이미지 삽입
        for jsonPage1 in jsonPage['photos']:
            #json To tableDic
            dicKMIG_NV_CMPX_IMG = setJson2TableDic('KMIG_NV_CMPX_IMG', jsonPage1)
            dicKMIG_NV_CMPX_IMG['NV_CMPX_ID']=dicCmpxId['NV_CMPX_ID']
            dicKMIG_NV_CMPX_IMG['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX_IMG['CHG_USER_ID'] = userid

            try:
                insertBasicByTBLDic('KMIG_NV_CMPX_IMG', dicKMIG_NV_CMPX_IMG)
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                log("네이버물건이미지 중복" + 'NV_CMPX_ID : ', "D")

        #네이버물건상세갱신
        print(jsonPage['complexDetail'])
        dicKMIG_NV_CMPX = setJson2TableDic('KMIG_NV_CMPX', jsonPage['complexDetail'])
        dicKMIG_NV_CMPX['REG_USER_ID'] = userid
        dicKMIG_NV_CMPX['CHG_USER_ID'] = userid
        print(dicKMIG_NV_CMPX)

        dicBasicCond = {}
        dicBasicCond['NV_CMPX_ID'] =  dicCmpxId['NV_CMPX_ID']

        updateBaiscByTBLDic('KMIG_NV_CMPX',dicKMIG_NV_CMPX,dicBasicCond)

        #네이버물건재건축 INSERT
        if jsonPage.get('complexRebuilding',False):
            print("재건축단지 INSERT")
            print(jsonPage['complexRebuilding'])
            dicKMIG_NV_CMPX_RBLD = setJson2TableDic('KMIG_NV_CMPX_RBLD', jsonPage['complexRebuilding'])
            dicKMIG_NV_CMPX_RBLD['NV_CMPX_ID']=dicCmpxId['NV_CMPX_ID']
            dicKMIG_NV_CMPX_RBLD['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX_RBLD['CHG_USER_ID'] = userid
            print(dicKMIG_NV_CMPX)

            try:
                insertBasicByTBLDic('KMIG_NV_CMPX_RBLD', dicKMIG_NV_CMPX_IMG)
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                log("네이버물건재건축 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'] , "D")

        # 네이버물건형 INSERT
        for jsonPageNvCmpxTyp in jsonPage['complexPyeongDetailList']:
            print("네이버물건형 INSERT")
            print(jsonPageNvCmpxTyp)
            dicKMIG_NV_CMPX_TYP = setJson2TableDic('KMIG_NV_CMPX_TYP', jsonPageNvCmpxTyp)
            dicKMIG_NV_CMPX_TYP['NV_CMPX_ID'] = dicCmpxId['NV_CMPX_ID']
            dicKMIG_NV_CMPX_TYP['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX_TYP['CHG_USER_ID'] = userid
            print(dicKMIG_NV_CMPX_TYP)

            try:
                insertBasicByTBLDic('KMIG_NV_CMPX_TYP', dicKMIG_NV_CMPX_TYP)
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                log("네이버물건형 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'], "D")

            if jsonPageNvCmpxTyp.get('grandPlanList', False):
                #네이버물건형이미지 INSERT
                for jsonPageNvCmpxTypImg in jsonPageNvCmpxTyp['grandPlanList']:
                    print("네이버물건형이미지 INSERT")
                    print(jsonPageNvCmpxTypImg)
                    dicKMIG_NV_CMPX_TYP_IMG = setJson2TableDic('KMIG_NV_CMPX_TYP_IMG', jsonPageNvCmpxTypImg)
                    dicKMIG_NV_CMPX_TYP_IMG['NV_CMPX_ID'] = dicCmpxId['NV_CMPX_ID']
                    dicKMIG_NV_CMPX_TYP_IMG['NV_CMPX_TYP_SEQ'] = dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ']
                    dicKMIG_NV_CMPX_TYP_IMG['REG_USER_ID'] = userid
                    dicKMIG_NV_CMPX_TYP_IMG['CHG_USER_ID'] = userid
                    print(dicKMIG_NV_CMPX_TYP_IMG)

                    try:
                        insertBasicByTBLDic('KMIG_NV_CMPX_TYP_IMG', dicKMIG_NV_CMPX_TYP_IMG)
                    except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                        log("네이버물건형이미지 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'] + "/" + dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ'], "D")

            if jsonPageNvCmpxTyp.get('articleStatistics', False):
                print("네이버물건형통계 INSERT")
                print(jsonPageNvCmpxTyp['articleStatistics'])
                dicKMIG_NV_CMPX_TYP_STAT = setJson2TableDic('KMIG_NV_CMPX_TYP_STAT', jsonPageNvCmpxTyp['articleStatistics'])
                dicKMIG_NV_CMPX_TYP_STAT['NV_CMPX_ID'] = dicCmpxId['NV_CMPX_ID']
                dicKMIG_NV_CMPX_TYP_STAT['NV_CMPX_TYP_SEQ'] = dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ']
                dicKMIG_NV_CMPX_TYP_STAT['MSML_PYNG_PER_AMT'] = dicKMIG_NV_CMPX_TYP_STAT['MSML_PYNG_PER_AMT'].replace(",", "")
                dicKMIG_NV_CMPX_TYP_STAT['MBIG_PYNG_PER_AMT'] = dicKMIG_NV_CMPX_TYP_STAT['MBIG_PYNG_PER_AMT'].replace(",", "")
                dicKMIG_NV_CMPX_TYP_STAT['REG_USER_ID'] = userid
                dicKMIG_NV_CMPX_TYP_STAT['CHG_USER_ID'] = userid
                print(dicKMIG_NV_CMPX_TYP_STAT)

            try:
                insertBasicByTBLDic('KMIG_NV_CMPX_TYP_STAT', dicKMIG_NV_CMPX_TYP_STAT)
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                log("네이버물건형통계 중복" + 'NV_CMPX_ID : ' + dicCmpxId['NV_CMPX_ID'] + "/" + dicKMIG_NV_CMPX_TYP['NV_CMPX_TYP_SEQ'], "D")

        #네이버물건상세UPDATE
        time.sleep(NaverTimeStamp)
if __name__ == '__main__':
    updNaverComplexDtl()
