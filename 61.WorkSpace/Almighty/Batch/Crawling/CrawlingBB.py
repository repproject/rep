# -*- coding:utf-8 -*-
#from REP_DAO import *
from common.common.URL import *
#from REP_COM import *
#from REP_TABLE import *
from common.common import URL
from bs4 import BeautifulSoup
import urllib
from common.Batch.Crawling import *
from common.common.Log import *

userid = 1000000011

#Lv3
class CrawlingSingleBB(CrawlingBasicSingle):
    siteCode = 'BB'
    #[LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
    def selfMakeURL(self,dicStrdData = None):
        return "http://test.com"

    #[LV3 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,page):
        pass

#Lv3
# class CrawlingMultiBB(CrawlingBasicMulti):
#     siteCode = 'BB'
#
#     def __init__(self):
#         super.__init__()
#
#     #[LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
#     def selfMakeURL(self,dicStrdData = None):
#         url = URL.URLMaker("BBRegn")
#         url.add("target","lcode")
#         return url.getURL()
#
#     #[LV3 구현]Page > 변환 > Parse > DB 반영
#     def selfSaveDB(self,page):
#         pass

#Lv4 부동산뱅크 지역코드 LV1
class CrawlingBBRegnLv1(CrawlingSingleBB):
    funcName = "CrawlingBBRegnLv1"
    sqlReportFetchId = "selectNewBBRegnCdLv1"
    SVC_ID = "BBRegn"

    # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
    def selfMakeURL(self, dicStrdData=None,reCnt = None):
        url = URL.URLMaker(self.SVC_ID)
        url.add("target","lcode")
        return url.getURL()

    #[LV3 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,page):
        soup = BeautifulSoup(page, 'html.parser')
        te = soup.findAll("n")
        for t in te:
            dicKMIG_BB_LV1_REGN = setSoup2TableDic("KMIG_BB_LV1_REGN",t)
            dicKMIG_BB_LV1_REGN['REG_USER_ID'] = userid
            dicKMIG_BB_LV1_REGN['CHG_USER_ID'] = userid

            try:
                insertBasicByTBLDic('KMIG_BB_LV1_REGN', dicKMIG_BB_LV1_REGN)
            except pymysql.IntegrityError as err:  # 기존 중복 가능
                Log.debug(batchContext.getLogName() + "부동산뱅크 LV1 지역 중복" + dicKMIG_BB_LV1_REGN['BB_LV1_REGN_CD'] + "/" + dicKMIG_BB_LV1_REGN['BB_LV1_REGN_NM'])

#Lv4 부동산뱅크 지역코드 LV2
# class CrawlingBBRegnLv2(CrawlingMultiBB):
#     funcName = "CrawlingBBRegnLv2"
#     fetchSqlId =  "selectBBRegnCdLv1"
#     sqlReportFetchId = "selectNewBBRegnCdLv2"
#     SVC_ID = "BBRegn"
#
#     MessageInterval = 50
#     MessageUnit = "P"
#
#     # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
#     def selfMakeURL(self, dicStrdData=None,reCnt = None):
#         url = URL.URLMaker(self.SVC_ID)
#         url.add("target","mcode")
#         url.add("lcode",dicStrdData['BB_LV1_REGN_CD'])
#         return url.getURL()
#
#     #[LV3 구현]Page > 변환 > Parse > DB 반영
#     def selfSaveDB(self,page,dicStrdData):
#         soup = BeautifulSoup(page, 'html.parser')
#         te = soup.findAll("n")
#         tableName = "KMIG_BB_LV3_REGN"
#         for t in te:
#             dicKMIG_BB_LV2_REGN = setSoup2TableDic(tableName,t)
#             dicKMIG_BB_LV2_REGN['BB_LV1_REGN_CD'] = dicStrdData['BB_LV1_REGN_CD']
#             dicKMIG_BB_LV2_REGN['BB_LV1_REGN_NM'] = dicStrdData['BB_LV1_REGN_NM']
#             dicKMIG_BB_LV2_REGN['REG_USER_ID'] = userid
#             dicKMIG_BB_LV2_REGN['CHG_USER_ID'] = userid
#
#             try:
#                 insertBasicByTBLDic(tableName, dicKMIG_BB_LV2_REGN)
#             except pymysql.IntegrityError as err:  # 기존 중복 가능
#                 Log.debug(batchContext.getLogName() + "부동산뱅크 LV2 지역 중복" + dicKMIG_BB_LV2_REGN['BB_LV2_REGN_CD'] +
#                           "/" + dicKMIG_BB_LV2_REGN['BB_LV2_REGN_NM'] + "/" + + dicKMIG_BB_LV2_REGN['BB_LV1_REGN_CD'] + "/" + dicKMIG_BB_LV2_REGN['BB_LV1_REGN_NM'])
#
# #Lv4 부동산뱅크 지역코드 LV3
# class CrawlingBBRegnLv3(CrawlingMultiBB):
#     funcName = "CrawlingBBRegnLv3"
#     fetchSqlId =  "selectBBRegnCdLv2"
#     sqlReportFetchId = "selectNewBBRegnCdLv3"
#     SVC_ID = "BBRegn"
#
#     # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
#     def selfMakeURL(self, dicStrdData=None,reCnt = None):
#         url = URL.URLMaker(self.SVC_ID)
#         url.add("target","sname")
#         url.add("lcode",dicStrdData['BB_LV1_REGN_CD'])
#         url.add("mcode",dicStrdData['BB_LV2_REGN_CD'])
#         return url.getURL()
#
#     #[LV3 구현]Page > 변환 > Parse > DB 반영
#     def selfSaveDB(self,page,dicStrdData):
#         soup = BeautifulSoup(page, 'html.parser')
#         te = soup.findAll("n")
#         tableName = "KMIG_BB_LV3_REGN"
#         for t in te:
#             dicKMIG_BB_LV3_REGN = setSoup2TableDic(tableName,t)
#             dicKMIG_BB_LV3_REGN['BB_LV1_REGN_CD'] = dicStrdData['BB_LV1_REGN_CD']
#             dicKMIG_BB_LV3_REGN['BB_LV1_REGN_NM'] = dicStrdData['BB_LV1_REGN_NM']
#             dicKMIG_BB_LV3_REGN['BB_LV2_REGN_CD'] = dicStrdData['BB_LV2_REGN_CD']
#             dicKMIG_BB_LV3_REGN['BB_LV2_REGN_NM'] = dicStrdData['BB_LV2_REGN_NM']
#             dicKMIG_BB_LV3_REGN['REG_USER_ID'] = userid
#             dicKMIG_BB_LV3_REGN['CHG_USER_ID'] = userid
#
#             try:
#                 insertBasicByTBLDic(tableName, dicKMIG_BB_LV3_REGN)
#             except pymysql.IntegrityError as err:  # 기존 중복 가능
#                 Log.debug(batchContext.getLogName() + "부동산뱅크 LV3 지역 중복" + dicKMIG_BB_LV3_REGN['BB_LV3_REGN_CD'] + "/" + dicKMIG_BB_LV3_REGN['BB_LV2_REGN_NM']
#                           + "/" + dicKMIG_BB_LV3_REGN['BB_LV2_REGN_CD'] + "/" + dicKMIG_BB_LV3_REGN['BB_LV2_REGN_NM']
#                           + "/" +dicKMIG_BB_LV3_REGN['BB_LV1_REGN_CD'] + "/" + dicKMIG_BB_LV3_REGN['BB_LV1_REGN_NM'])
#
# #Lv4 부동산뱅크단지
# class CrawlingBBCmpx(CrawlingMultiBB):
#     funcName = "CrawlingBBCmpx"
#     fetchSqlId =  "selectBBRegnCdLv3"
#     sqlReportFetchId = "selectNewBBCmpx"
#     SVC_ID = "BBRegn"
#
#     # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
#     def selfMakeURL(self, dicStrdData=None,reCnt = None):
#         url = URL.URLMaker(self.SVC_ID)
#         url.add("target","complex_cd")
#         url.add("lcode",dicStrdData['BB_LV1_REGN_CD'])
#         url.add("mcode",dicStrdData['BB_LV2_REGN_CD'])
#         url.add("sname",dicStrdData['BB_LV3_REGN_CD'])
#         return url.getURL()
#
#     #[LV3 구현]Page > 변환 > Parse > DB 반영
#     def selfSaveDB(self,page,dicStrdData):
#         soup = BeautifulSoup(page, 'html.parser')
#         te = soup.findAll("n")
#         tableName = "KMIG_BB_CMPX"
#         tableName2 = "KMIG_BB_REGN_CMPX_REL"
#
#         for t in te:
#             dicKMIG_BB_CMPX = setSoup2TableDic(tableName,t)
#             dicKMIG_BB_CMPX['REG_USER_ID'] = userid
#             dicKMIG_BB_CMPX['CHG_USER_ID'] = userid
#
#             try:
#                 insertBasicByTBLDic(tableName, dicKMIG_BB_CMPX)
#             except pymysql.IntegrityError as err:  # 기존 중복 가능
#                 Log.debug(batchContext.getLogName() + "부동산뱅크 물건 중복" + dicKMIG_BB_CMPX['BB_CMPX_ID'] + "/" + dicKMIG_BB_CMPX['BB_CMPX_NM']
#                           + "/" + dicStrdData['BB_LV3_REGN_CD'] + "/" + dicStrdData['BB_LV2_REGN_NM']
#                           + "/" + dicStrdData['BB_LV2_REGN_CD'] + "/" + dicStrdData['BB_LV2_REGN_NM']
#                           + "/" + dicStrdData['BB_LV1_REGN_CD'] + "/" + dicStrdData['BB_LV1_REGN_NM'])
#
#             dicKMIG_BB_REGN_CMPX_REL = dicTable[tableName2]
#             dicKMIG_BB_REGN_CMPX_REL['BB_LV1_REGN_CD'] = dicStrdData['BB_LV1_REGN_CD']
#             dicKMIG_BB_REGN_CMPX_REL['BB_LV2_REGN_CD'] = dicStrdData['BB_LV2_REGN_CD']
#             dicKMIG_BB_REGN_CMPX_REL['BB_LV3_REGN_CD'] = dicStrdData['BB_LV3_REGN_CD']
#             dicKMIG_BB_REGN_CMPX_REL['BB_CMPX_ID'] = dicKMIG_BB_CMPX['BB_CMPX_ID']
#             dicKMIG_BB_REGN_CMPX_REL['REG_USER_ID'] = userid
#             dicKMIG_BB_REGN_CMPX_REL['CHG_USER_ID'] = userid
#
#             try:
#                 insertBasicByTBLDic(tableName2, dicKMIG_BB_REGN_CMPX_REL)
#             except pymysql.IntegrityError as err:  # 기존 중복 가능
#                 Log.debug(batchContext.getLogName() + "부동산뱅크 지역 물건 관계 중복" + dicKMIG_BB_CMPX['BB_CMPX_ID'] + "/" + dicKMIG_BB_CMPX['BB_CMPX_NM']
#                           + dicStrdData['BB_LV3_REGN_CD'] + "/" + dicStrdData['BB_LV2_REGN_NM']
#                           + "/" + dicStrdData['BB_LV2_REGN_CD'] + "/" + dicStrdData['BB_LV2_REGN_NM']
#                           + "/" +dicStrdData['BB_LV1_REGN_CD'] + "/" + dicStrdData['BB_LV1_REGN_NM'])
#
# #Lv4 부동산뱅크 지역코드 LV3
# class CrawlingBBCmpxTyp(CrawlingMultiBB):
#     funcName = "CrawlingBBCmpxTyp"
#     fetchSqlId =  "selectBBCmpx"
#     sqlReportFetchId = "selectNewBBCmpxTyp"
#     SVC_ID = "BBPastMarketPrice"
#
#     # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
#     def selfMakeURL(self, dicStrdData=None,reCnt = None):
#         url = URL.URLMaker(self.SVC_ID)
#         url.add("complex_cd",dicStrdData['BB_CMPX_ID'])
#         return url.getURL()
#
#     #[LV3 구현]Page > 변환 > Parse > DB 반영
#     def selfSaveDB(self,page,dicStrdData):
#         soup = BeautifulSoup(page, 'html.parser')
#         soup2 = soup.find("div", id="divMarketPriceList")
#         i=0
#         tableName = 'KMIG_BB_CMPX_TYP'
#         for s in soup2.find_all("tr"):
#             for a in s.find_all("a"):
#                 if i == 0:
#                     i += 1
#                     continue
#                 i += 1
#                 dicKMIG_BB_CMPX_TYP = dicTable[tableName]
#                 dicKMIG_BB_CMPX_TYP['BB_CMPX_ID'] = dicStrdData['BB_CMPX_ID']
#                 dicKMIG_BB_CMPX_TYP['BB_CMPX_TYP_SEQ'] = int(urllib.parse.parse_qs(urllib.parse.urlparse(a['href']).query)['pyung_cd'][0])
#                 dicKMIG_BB_CMPX_TYP['SPLY_AREA'] = a.text
#                 dicKMIG_BB_CMPX_TYP['REG_USER_ID'] = userid
#                 dicKMIG_BB_CMPX_TYP['CHG_USER_ID'] = userid
#
#                 try:
#                     insertBasicByTBLDic(tableName, dicKMIG_BB_CMPX_TYP)
#                 except pymysql.IntegrityError as err:  # 기존 중복 가능
#                     Log.debug(batchContext.getLogName() + "부동산뱅크 물건형 중복" + dicKMIG_BB_CMPX_TYP['BB_CMPX_ID'] + "/" +
#                               dicKMIG_BB_CMPX_TYP['BB_CMPX_TYP_SEQ'] + "/" + dicKMIG_BB_CMPX_TYP['SPLY_AREA'])
#
#
# #Lv4 부동산뱅크 물건형별월별시세
# class CrawlingBBCmpxTypMarketPrice(CrawlingMultiBB):
#     funcName = "CrawlingBBCmpxTypMarketPrice"
#     fetchSqlId =  "selectBBCmpxTyp"
#     sqlReportFetchId = "selectNewBBCmpxTypMonthPrc"
#     SVC_ID = "BBMarketPrice"
#
#     # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
#     def selfMakeURL(self, dicStrdData=None,reCnt = None):
#         url = URL.URLMaker(self.SVC_ID)
#         url.add("complex_cd",dicStrdData['BB_CMPX_ID'])
#         url.add("pyung_cd", dicStrdData['BB_CMPX_TYP_SEQ'])
#         url.add("period_gbn", "month")
#         url.add("start_sdate", "198001")
#         url.add("end_sdate", "203001")
#         return url.getURL()
#
#     #[LV3 구현]Page > 변환 > Parse > DB 반영
#     def selfSaveDB(self,page,dicStrdData):
#         soup = BeautifulSoup(page, 'html.parser')
#         te = soup.findAll("market_price")
#         tableName = "KMIG_BB_CMPX_TYP_MON_PRC"
#         listdicTable = list()
#         for t in te:
#             dicKMIG_BB_CMPX_TYP_MON_PRC = setSoup2TableDic(tableName,t)
#             dicKMIG_BB_CMPX_TYP_MON_PRC['BB_CMPX_ID'] = dicStrdData['BB_CMPX_ID']
#             dicKMIG_BB_CMPX_TYP_MON_PRC['BB_CMPX_TYP_SEQ'] = dicStrdData['BB_CMPX_TYP_SEQ']
#             dicKMIG_BB_CMPX_TYP_MON_PRC['STD_YYMM'] = dicKMIG_BB_CMPX_TYP_MON_PRC['STD_YYMM'].replace(".","").replace(",","")
#             dicKMIG_BB_CMPX_TYP_MON_PRC['STD_YMD'] = dicKMIG_BB_CMPX_TYP_MON_PRC['STD_YMD'].replace(".", "").replace(",","")
#             dicKMIG_BB_CMPX_TYP_MON_PRC['DOWN_PRC'] = dicKMIG_BB_CMPX_TYP_MON_PRC['DOWN_PRC'].replace(".", "").replace(",","")
#             dicKMIG_BB_CMPX_TYP_MON_PRC['UP_PRC'] = dicKMIG_BB_CMPX_TYP_MON_PRC['UP_PRC'].replace(".", "").replace(",","")
#             dicKMIG_BB_CMPX_TYP_MON_PRC['CHG_PRC'] = dicKMIG_BB_CMPX_TYP_MON_PRC['CHG_PRC'].replace(".", "").replace(",","")
#             dicKMIG_BB_CMPX_TYP_MON_PRC['DOWN_JS_PRC'] = dicKMIG_BB_CMPX_TYP_MON_PRC['DOWN_JS_PRC'].replace(".", "").replace(",","")
#             dicKMIG_BB_CMPX_TYP_MON_PRC['UP_JS_PRC'] = dicKMIG_BB_CMPX_TYP_MON_PRC['UP_JS_PRC'].replace(".", "").replace(",","")
#             dicKMIG_BB_CMPX_TYP_MON_PRC['CHG_JS_PRC'] = dicKMIG_BB_CMPX_TYP_MON_PRC['CHG_JS_PRC'].replace(".", "").replace(",","")
#             dicKMIG_BB_CMPX_TYP_MON_PRC['REG_USER_ID'] = userid
#             dicKMIG_BB_CMPX_TYP_MON_PRC['CHG_USER_ID'] = userid
#             listdicTable.append(dict(dicKMIG_BB_CMPX_TYP_MON_PRC))
#
#         try:
#             insertBasicByTBLDicList(tableName, listdicTable)
#         except pymysql.IntegrityError as e:  # 기존 중복 가능
#             Log.debug(batchContext.getLogName() + str(e))
#             Log.debug(batchContext.getLogName() + "부동산뱅크 물건형별 월별시세 중복" + dicStrdData['BB_CMPX_ID'] + "/" + str(dicStrdData['BB_CMPX_TYP_SEQ']))


if __name__ == '__main__':
    batchContext = simpleBatchContext("CrawlingBBCmpxTyp")
    CrawlObject = CrawlingBBRegnLv1(batchContext)
    CrawlObject.run()
    #migBBRegnLv1Code(batchContext)