from bs4 import BeautifulSoup
from common.Batch.Basic import *

from urllib import parse
import urllib.parse
import json

import common.Batch.Crawling

#LV1 크롤링 클래스
class CrawlingmNVAtcl(common.Batch.Crawling.Crawling):
    def isReCrwal(self,url,page,cPage,dicStrdData,reCnt):
        #print(cPage['result']['moreDataYn'])
        if cPage['result']['moreDataYn'] == 'Y':
            return True
        else:
            return False

if __name__ == '__main__':
    batchContext = simpleBatchContext("NVCmpxArticle")
    CrawlObject = CrawlingmNVAtcl('NVCmpxArticle','NVCmpxArticle',batchContext)
    CrawlObject.run()