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
# class CrawlingSingleBB(CrawlingBasicSingle):
#     siteCode = 'BB'
#     #[LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
#     def selfMakeURL(self,dicStrdData = None):
#         return "http://test.com"
#
#     #[LV3 구현]Page > 변환 > Parse > DB 반영
#     def selfSaveDB(self,page):
#         pass

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

#Lv4 부동산뱅크 지역코드 LV3
class CrawlingBBCmpxTyp(Crawling):
    #[LV3 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,cPage,dicStrdData = None,url = None):
        soup2 = cPage.find("div", id="divMarketPriceList")
        i=0
        #tableName = 'KMIG_BB_CMPX_TYP'
        for s in soup2.find_all("tr"):
            for a in s.find_all("a"):
                if i == 0:
                    i += 1
                    continue
                i += 1

                dicKMIG_BB_CMPX_TYP = {}
                dicKMIG_BB_CMPX_TYP['bb_cmpx_id'] = dicStrdData['bb_cmpx_id']
                dicKMIG_BB_CMPX_TYP['bb_cmpx_typ_seq'] = int(urllib.parse.parse_qs(urllib.parse.urlparse(a['href']).query)['pyung_cd'][0])
                dicKMIG_BB_CMPX_TYP['cmpx_typ_nm'] = a.text

                kwargs = {**dicKMIG_BB_CMPX_TYP}
                tableBbCmpxTyp = BbCmpxTyp(**kwargs)
                delattr(tableBbCmpxTyp,'reg_dtm')
                merge(tableBbCmpxTyp)

#######################################

#Lv4 부동산뱅크 지역코드 LV1
# class CrawlingBBRegnLv1(CrawlingSingleBB):
#     funcName = "CrawlingBBRegnLv1"
#     sqlReportFetchId = "selectNewBBRegnCdLv1"
#     SVC_ID = "BBRegn"
#
#     # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
#     def selfMakeURL(self, dicStrdData=None,reCnt = None):
#         url = URL.URLMaker(self.SVC_ID)
#         url.add("target","lcode")
#         return url
#
#     #[LV3 구현]Page > 변환 > Parse > DB 반영
#     def selfSaveDB(self,page):
#         soup = BeautifulSoup(page, 'html.parser')
#         te = soup.findAll("n")
#         for t in te:
#             dicKMIG_BB_LV1_REGN = setSoup2TableDic("KMIG_BB_LV1_REGN",t)
#             dicKMIG_BB_LV1_REGN['REG_USER_ID'] = userid
#             dicKMIG_BB_LV1_REGN['CHG_USER_ID'] = userid
#
#             try:
#                 insertBasicByTBLDic('KMIG_BB_LV1_REGN', dicKMIG_BB_LV1_REGN)
#             except pymysql.IntegrityError as err:  # 기존 중복 가능
#                 Log.debug(batchContext.getLogName() + "부동산뱅크 LV1 지역 중복" + dicKMIG_BB_LV1_REGN['BB_LV1_REGN_CD'] + "/" + dicKMIG_BB_LV1_REGN['BB_LV1_REGN_NM'])


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
    #CrawlObject = CrawlingBBRegnLv1(batchContext)
    #CrawlObject.run()
    ##sys.path.append("C:\Users\Ceasar.DESKTOP-AQTREV4\PycharmProjects\rep\61.WorkSpace\Almighty")

    co = CrawlingBBCmpxTyp('BBCmpxTyp','BBPastMarketPrice', batchContext)
    co.run()
