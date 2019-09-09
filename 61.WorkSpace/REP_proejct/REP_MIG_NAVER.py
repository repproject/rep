# -*- coding:utf-8 -*-
# import REP_DAO
import time
from REP_DAO import *
from REP_URL import *
import REP_COM
import REP_MIG
import REP_URL
import REP_DAO
import json
from REP_TABLE import *
from REP_MIG_MAPP import *

def migNaverComplexList():
    global json
    dicLeglCodeList = fetch("selectLeglLv3Dong", "")
    print(dicLeglCodeList)

    for dicLeglCode in dicLeglCodeList:
        url = NaverComplexListURL + dicLeglCode['LEGL_DONG_CD']
        print(url)

        page = REP_MIG.get_html(url)
        jsonPage = json.loads(page)

        #초기화
        for jsonComplex in jsonPage['complexList']:
            for dicName in dicKMIG_NV_CMPX.keys():
                dicKMIG_NV_CMPX[dicName] = ''
            for col in dicMappNaverComplexList.keys():
                try:
                    dicKMIG_NV_CMPX[dicMappNaverComplexList[col]] = jsonComplex[col]
                except Exception as e:
                    str(e)
                    print("migNaverComplexList json Parsing Error" + str(e) + col)
            dicKMIG_NV_CMPX['GOV_LEGL_DONG_CD']=dicLeglCode['LEGL_DONG_CD']
            print(dicKMIG_NV_CMPX)
            REP_DAO.INSERT_KMIG_NV_CMPX(dicKMIG_NV_CMPX)
        time.sleep(2)

if __name__ == '__main__':
    migNaverComplexList()
