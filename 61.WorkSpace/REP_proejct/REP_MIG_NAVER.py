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
        jsonPage = json.loads(page)

        for jsonComplex in jsonPage['complexList']:
            #json To tableDic
            dicKMIG_NV_CMPX = setJson2TableDic('KMIG_NV_CMPX', jsonComplex)
            dicKMIG_NV_CMPX['GOV_LEGL_DONG_CD']=dicLeglCode['LEGL_DONG_CD']
            dicKMIG_NV_CMPX['REG_USER_ID'] = userid
            dicKMIG_NV_CMPX['CHG_USER_ID'] = userid

            try:
                insertByDic('KMIG_NV_CMPX',dicKMIG_NV_CMPX)
            except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
                log("네이버물건 중복" + 'NV_CMPX_ID : ' + dicKMIG_NV_CMPX['NV_CMPX_ID'],"D")
        time.sleep(NaverTimeStamp)

if __name__ == '__main__':
    migNaverComplexList()
