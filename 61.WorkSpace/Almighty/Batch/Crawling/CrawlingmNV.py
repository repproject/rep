from bs4 import BeautifulSoup
from common.Batch.Basic import *

from urllib import parse
import urllib.parse
import json

import common.Batch.Crawling

#LV1 크롤링 클래스
class CrawlingmNV(common.Batch.Crawling.Crawling):
    """

    """
    #page = 1,2,3 ... customized
    def makeURL(self, dicStrdData=None, reCnt=None):
        for tb in self.tableSvcPasiItemIn:
            if isNotNull(tb[0].tbl_nm) and isNotNull(tb[0].col_nm):
                self.dicParam[tb[0].item_nm]=dicStrdData[tb[0].col_nm]

        #customized page 파라미터 추가
        if reCnt == None:
            self.dicParam['page'] = 1
        else :
            self.dicParam['page'] = reCnt

        self.url = self.tableSite.bas_prtc + "://"  # 프로토콜 http
        self.url += urllib.parse.quote(self.tableSite.bas_url + self.tableSvc.bas_svc_url,
                                       encoding=self.tableSite.enc_cd)
        if self.tableSvc.req_way_cd == "GET":
            self.url += "?" + urllib.parse.urlencode(self.dicParam, encoding=self.tableSite.enc_cd)
        elif self.tableSvc.req_way_cd == "POST":
            pass
        return self.url

    #[LV4 구현]Page > 변환 > Parse > DB 반영
    def selfSaveDB(self,cPage,dicStrdData = None,url = None):
        blog.info(" Page : " + str(cPage))
        if len(self.crawlCdExec) > 0:
            self.reCurParse(cPage,self.crawlCdExec[0],dicStrdData)
        pass

    def isReCrwal(self,url,page,dicStrdData,reCnt):
        soup = BeautifulSoup(page, 'html.parser')  # 파싱을 위한 객체화
        l = str(soup)
        j = json.loads(l)  # json 객체로 로딩
        return j['more']

if __name__ == '__main__':
    batchContext = simpleBatchContext("mNVArticleList")
    CrawlObject = CrawlingmNV('mNVArticleList','NVArticleList',batchContext)
    CrawlObject.run()