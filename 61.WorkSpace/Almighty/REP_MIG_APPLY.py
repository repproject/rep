from REP_COM import *
from common.common import URL
import REP_MIG


#Lv3
class CrawlingSingleAP(REP_MIG.CrawlingBasicSingle):
    siteCode = 'AP'
    #[LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
    def selfMakeURL(self,dicStrdData = None):
        return "http://test.com"

    #[LV3 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,page):
        pass

#Lv3
class CrawlingMultiAP(REP_MIG.CrawlingBasicMulti):
    siteCode = 'AP'
    sleepStamp = dicSiteBasic[siteCode]['SLEP_TIME']

    #[LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
    def selfMakeURL(self,dicStrdData = None):
        url = URL.URLMaker("ApplyAPTList")
        #url.add("target","lcode")
        return url.getURL()

    #[LV3 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,page):
        pass

#Lv4 청약아파트 목록
class CrawlingAPAptList(CrawlingMultiAP):
    funcName = "CrawlingAPAptList"
    fetchSqlId =  "selectYYYY"
    #sqlReportFetchId = "selectNewBBRegnCdLv2"
    SVC_ID = "ApplyAPTList" #

    MessageInterval = 50
    MessageUnit = "P"

    # [LV3 구현]각 Lv3 Class(웹사이트(url) 별로) URL을 만드는 부분을 정의
    def selfMakeURL(self, dicStrdData=None):
        url = URL.URLMaker(self.SVC_ID)
        url.add("beginPd",dicStrdData['YYYY'] + "01")
        url.add("endPd", dicStrdData['YYYY'] + "12")
        url.add("pageIndex", "1")
        url.add("gvPgmId", "AIA01M01")
        url.getURL()
        #beginPd=201904&endPd=202003&houseDetailSecd=&suplyAreaCode=&houseNm=&pageIndex=1&gvPgmId=AIA01M01

        return url

    #[LV3 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,page,dicStrdData):
        print(page)
        # soup = BeautifulSoup(page, 'html.parser')
        # te = soup.findAll("n")
        # tableName = "KMIG_BB_LV3_REGN"
        # for t in te:
        #     dicKMIG_BB_LV2_REGN = setSoup2TableDic(tableName,t)
        #     dicKMIG_BB_LV2_REGN['BB_LV1_REGN_CD'] = dicStrdData['BB_LV1_REGN_CD']
        #     dicKMIG_BB_LV2_REGN['BB_LV1_REGN_NM'] = dicStrdData['BB_LV1_REGN_NM']
        #     dicKMIG_BB_LV2_REGN['REG_USER_ID'] = userid
        #     dicKMIG_BB_LV2_REGN['CHG_USER_ID'] = userid
        #
        #     try:
        #         insertBasicByTBLDic(tableName, dicKMIG_BB_LV2_REGN)
        #     except pymysql.IntegrityError as err:  # 기존 중복 가능
        #         Log.debug(batchContext.getLogName() + "부동산뱅크 LV2 지역 중복" + dicKMIG_BB_LV2_REGN['BB_LV2_REGN_CD'] +
        #                   "/" + dicKMIG_BB_LV2_REGN['BB_LV2_REGN_NM'] + "/" + + dicKMIG_BB_LV2_REGN['BB_LV1_REGN_CD'] + "/" + dicKMIG_BB_LV2_REGN['BB_LV1_REGN_NM'])

if __name__ == '__main__':
    batchContext = simpleBatchContext("CrawlingAP")
    CrawlObject = CrawlingAPAptList(batchContext)
    CrawlObject.run()