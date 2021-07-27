from urllib import parse
import urllib.parse

KB부동산과거시세조회URL = "http://nland.kbstar.com/quics?page=B047172&cc=b028364:b057487"
KB부동산과거시세조회Json = "http://nland.kbstar.com/quics?page=&QAction=763359&RType=json"
KB부동산지도조회Json = "http://nland.kbstar.com/quics?page=B046949&QAction=766912&RType=json&B_CLEAR=1"
네이버부동산동별아파트리스트 = "http://land.naver.com/article/articleList.nhn?"
#네이버부동산 = "http://land.naver.com/article/"
네이버부동산 = "http://land.naver.com"

#신규
NaverTimeStamp = 1.1
NaverComplexListURL = "https://new.land.naver.com/api/regions/complexes?cortarNo="
NaverComplexDtlURL = "https://new.land.naver.com/api/complexes/"

#dicSiteBasic = {
#    'BB' : {
#        'SLEP_TIME' : 0.1,
#        'BAS_URL' : "www.neonet.co.kr",
#        'BAS_PRTC' : "http",
#        'ENCD' : 'euckr'
#    },
#    'AP': {
#        'SLEP_TIME': 0.1,
#        'BAS_URL': "www.applyhome.co.kr",
#        'BAS_PRTC': "https",
#        'ENCD': 'euckr'
#    },
#    'NV':  {
#        'SLEP_TIME': 0.5,
#        'BAS_URL': "new.land.naver.com",
#        'BAS_PRTC': "https",
#        'ENCD': 'euckr'
#    },
#    'GO': {
#        'SLEP_TIME': 0.1,
#        'BAS_URL': "openapi.molit.go.kr",
#        'BAS_PRTC': "http",
#        'ENCD': 'euckr'
#    },
#}

dicSiteDetailMapp= {
    'BBRegn':'BB',
    'BBPastMarketPrice' : 'BB',
    'BBMarketPrice' : 'BB',
    'ApplyAPTList': 'AP',
    'NVAtcl': 'NV',
    'APTTrade' : 'GO'
}

dicService = {
    'BBRegn' : {
        'BAS_SVC_ID' : "/novo-rebank/view/market_price/RegionData.neo",
        'BAS_PARM' : {
            'offerings_gbn' : 'AT',
            'update' : '140228'
            # LV1 http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&update=140228&target=lcode
            # LV2 http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&lcode=01&mcode=&target=mcode&update=140228
            # LV3 http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&lcode=01&mcode=130&target=sname&update=140228
            # 단지목록 http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&lcode=01&mcode=100&target=complex_cd&update=140228&sname=%B8%B8%B8%AE%B5%BF
            # http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&update=140228&target=complex_cd&lcode=01&mcode=100&sname=만리동
        },
        'MTHD' : "GET"
    },
    'BBPastMarketPrice' : {
        'BAS_SVC_ID' : "/novo-rebank/view/market_price/PastMarketPriceList.neo",
        'BAS_PARM': {
            # 물건형 http://www.neonet.co.kr/novo-rebank/view/market_price/PastMarketPriceList.neo?complex_cd=A0024201
        },
        'MTHD': "GET"
    },
    'BBMarketPrice' :{
        'BAS_SVC_ID' : "/novo-rebank/view/market_price/MarketPriceData.neo",
        'BAS_PARM' : {
            'action' : 'COMPLEX_PERIOD_DATA'
        },
        'MTHD': "GET"
        #http://www.neonet.co.kr/novo-rebank/view/market_price/MarketPriceData.neo?action=COMPLEX_PERIOD_DATA&complex_cd=A0024201&pyung_cd=1&period_gbn=month&start_sdate=198001&end_sdate=202001
    },
    'ApplyAPTList': {
        'BAS_SVC_ID': "/ai/aia/selectAPTLttotPblancListView.do",
        'BAS_PARM': {
        },
        'MTHD': "POST"
        #https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do
    },
    'NVAtcl': {
        'BAS_SVC_ID': "/api/articles/complex/",
        'BAS_PARM': {
            'realEstateType' : 'APT:ABYG:JGC:OPST:OBYG:JGB',
            'tradeType':'',
            'tag':'::::::::',
            'rentPriceMin' : '0',
            'rentPriceMax' : '900000000',
            'priceMin' : '0',
            'priceMax' : '900000000',
            'areaMin' : '0',
            'areaMax' : '900000000',
            'oldBuildYears' : '',
            'recentlyBuildYears' : '',
            'minHouseHoldCount' : '',
            'maxHouseHoldCount' : '',
            'showArticle' : 'false',
            'sameAddressGroup' : 'false',
            'minMaintenanceCost' : '',
            'maxMaintenanceCost' : '',
            'priceType' : 'RETAIL',
            'type' : 'list',
            'order' : 'dateDesc'
        },
        'MTHD': "GET"
        #https://new.land.naver.com/api/articles/complex/24206?realEstateType=APT%3AABYG%3AJGC&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page=1&complexNo=24206&buildingNos=&areaNos=&type=list&order=dateDesc
    },
    'APTTrade': {
        'BAS_SVC_ID': "/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev",
        'BAS_PARM': {
            # 서비스키	ServiceKey	20	필수	-	공공데이터포털에서 받은 인증키
            # 페이지 번호	pageNo	4	옵션	1	페이지번호
            # 한 페이지 결과 수	numOfRows	4	옵션	10	한 페이지 결과 수
            # 지역코드	LAWD_CD	5	필수	11110	지역코드
            # 계약월	DEAL_YMD	6	필수	201512	계약월

            'ServiceKey': 'n%2Bx3ws990OxspyqgFNBV0oppRCCskpT5taMq4aQx7VyV%2B7JQrn5snqBWdlWuL%2F8IScN0Jbo62Z6Grm7BjBP1%2BQ%3D%3D',
            'update': '140228'
            # LV1 http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&update=140228&target=lcode
            # LV2 http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&lcode=01&mcode=&target=mcode&update=140228
            # LV3 http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&lcode=01&mcode=130&target=sname&update=140228
            # 단지목록 http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&lcode=01&mcode=100&target=complex_cd&update=140228&sname=%B8%B8%B8%AE%B5%BF
            # http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&update=140228&target=complex_cd&lcode=01&mcode=100&sname=만리동
        },
        'MTHD': "GET"
    },


}

class URLMaker:
    url = None
    URLkey = None
    dicParam = {}
    siteCode = None
    dicSite = None
    dicService = None
    mthd = None
    postData = None
    addStr = ""

    def __init__(self,URLkey):
        self.URLkey = URLkey
        self.siteCode = dicSiteDetailMapp[URLkey]
        self.dicSite = dicSiteBasic[self.siteCode]
        self.dicService = dicService[URLkey]
        self.dicParam = self.dicService['BAS_PARM']
        self.mthd = self.dicService['MTHD']
        self.url = self.getURL()

    def add(self,key,value):
        self.dicParam[key]=value

    def deleteParam(self,key):
        try:
            del(self.dicParam[key])
        except KeyError as e:
            pass

    def addString(self,str):
        self.addStr = str

    def getURL(self):
        self.url = self.dicSite['BAS_PRTC'] + "://" #프로토콜 http
        self.url += urllib.parse.quote(self.dicSite['BAS_URL'] + self.dicService['BAS_SVC_ID'] + self.addStr,encoding=self.dicSite['ENCD'])
        if self.mthd == "GET":
            self.url += "?" + urllib.parse.urlencode(self.dicParam, encoding=self.dicSite['ENCD'])
        elif self.mthd == "POST":
            pass

        return self.url

    def printURL(self):
        url = self.getURL()
        if self.mthd == "POST" :
             url += str(self.dicParam)
        rtn = "[" + self.mthd + "]" + url
        return rtn

    def getMethod(self):
        return self.mthd

    def getDicParam(self):
        return self.dicParam

def getURLQuote(url,type="utf-8"):
    return urllib.urlretrieve(urllib.quote(url.encode(type), '/:'))


def makeGetURL(JOB_CL,SITE_CL,TR_ID,dicGetParam):
    #작업분류 (JOB_CL - NV-Naver부동산 KB-KB부동산)
    #사이트구분 1-매물

    if JOB_CL == "NV":
        URL = 네이버부동산 + "/" + SITE_CL + "/" + TR_ID + ".nhn" + makeGetParam(dicGetParam,'?')
    return URL

NAVER부동산URL = "http://land.naver.com/article/groundPlan.nhn?"

def makeURLParse(url):
    ParseResult = urllib.parse.urlparse(url)
    print(urllib.parse.splitquery(url))
    return ParseResult

def makeGetParam(Dic,Igubun):
    count = 0
    param = ""
    for key, value in Dic.items():
        if count == 0 :
            param += Igubun
        else:
            param += '&'
        param += urllib.parse.quote(key)
        param += '='
        param += str(value)
        count = count + 1
    return param

def makeGetRealParam(Dic):
    param = ""
    for key, value in Dic.items():
        param += '&'
        param += key
        param += '='
        param += value
    return param

def makeURL():
    testDic = {'메뉴타입' : 'S'
        , '물건종별구분' : '01'
        , '부동산대지역코드' : '010000'
        , '부동산중지역코드' : '010200'
        ,'부동산소지역코드' : '010201'
        , '물건식별자' : 'KBA007445'
        , '주택형일련번호' : '1'
        , '조회시작년도' : '2011'
        , '조회시작월': '01'
        , '조회종료년도': '2017'
        , '조회종료월': '01'
        }

def getJsonKBRealEstatePastPriceInquery(메뉴타입,물건종별구분,부동산대지역코드,부동산중지역코드,부동산소지역코드,물건식별자,주택형일련번호,조회시작년도,조회시작월,조회종료년도,조회종료월):
    Dic = {'메뉴타입' : 메뉴타입
        , '물건종별구분' : 물건종별구분
        , '부동산대지역코드' : 부동산대지역코드
        , '부동산중지역코드' : 부동산중지역코드
        ,'부동산소지역코드' : 부동산소지역코드
        , '물건식별자' : 물건식별자
        , '주택형일련번호' : 주택형일련번호
        , '조회시작년도' : 조회시작년도
        , '조회시작월': 조회시작월
        , '조회종료년도': 조회종료년도
        , '조회종료월': 조회종료월
        }
    #print(KB부동산과거시세조회Json + makeGetRealParam(Dic))
    return KB부동산과거시세조회Json + makeGetParam(Dic,'?')

def getURLKBRealEstatePastPriceInquery(메뉴타입,물건종별구분,부동산대지역코드,부동산중지역코드,부동산소지역코드,물건식별자,주택형일련번호,조회시작년도,조회시작월,조회종료년도,조회종료월):
    Dic = {'메뉴타입' : 메뉴타입
        , '물건종별구분' : 물건종별구분
        , '부동산대지역코드' : 부동산대지역코드
        , '부동산중지역코드' : 부동산중지역코드
        ,'부동산소지역코드' : 부동산소지역코드
        , '물건식별자' : 물건식별자
        , '주택형일련번호' : 주택형일련번호
        , '조회시작년도' : 조회시작년도
        , '조회시작월': 조회시작월
        , '조회종료년도': 조회종료년도
        , '조회종료월': 조회종료월
        }
    return KB부동산과거시세조회URL + makeGetParam(Dic,'&')

#KB부동산 지도 가져오기
def getURLKBRealEstateKBCmpxSearch(물건종별구분,물건식별자,부동산대지역코드,부동산중지역코드,부동산소지역코드,부동산대지역명,부동산중지역명,부동산소지역명,매물거래구분,조회구분):
    Dic = {'물건종별구분' : 물건종별구분
        , '물건식별자': 물건식별자
        , '부동산대지역코드' : 부동산대지역코드
        , '부동산중지역코드' : 부동산중지역코드
        , '부동산소지역코드' : 부동산소지역코드
        , '부동산대지역명': 부동산대지역명
        , '부동산중지역명': 부동산중지역명
        , '부동산소지역명': 부동산소지역명
        , '매물거래구분' : 매물거래구분
        , '조회구분': 조회구분
        }

    return KB부동산지도조회Json + makeGetParam(Dic,'?')

def getURLNaverAptcode(rletTypeCd,tradeTypeCd,cortarNo):
    Dic = {'rletTypeCd': rletTypeCd
        , 'tradeTypeCd': tradeTypeCd
        , 'cortarNo': cortarNo
           }

    return 네이버부동산동별아파트리스트 + makeGetRealParam(Dic,'?')

def getNVComplexInfo(rletNo):
    Dic = {'rletNo': rletNo}
    #http://land.naver.com/article/complexInfo.nhn?rletTypeCd=A01&tradeTypeCd=A1&rletNo=107024&cortarNo=4145010900&hscpTypeCd=A01%3AA03%3AA04&mapX=127.183042&mapY=37.5614682&mapLevel=13&page=&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=0&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=&exclsSpc=&splySpcR=&cmplYn=
    #단순화 : http://land.naver.com/article/complexInfo.nhn?rletNo=107024

    return


def getURLNVComplexTypeInquery(CMPX_CTGR, NV_CMPX_ID):
    Dic = {'rletTypeCd': CMPX_CTGR
        , 'rletNo': NV_CMPX_ID
           }
    return NAVER부동산URL + makeGetRealParam(Dic,'?')

def getURLNVComplexTypeInquery(CMPX_CTGR, NV_CMPX_ID):
    Dic = {'rletTypeCd': CMPX_CTGR
        , 'rletNo': NV_CMPX_ID
           }
    return NAVER부동산URL + makeGetRealParam(Dic)

def getURLNVSaleInquery(CMPX_CTGR, NV_CMPX_ID):
    Dic = {'rletTypeCd': CMPX_CTGR
        , 'rletNo': NV_CMPX_ID
           }
    return 네이버부동산동별아파트리스트 + makeGetRealParam(Dic)


if __name__ == '__main__':
    #http://www.neonet.co.kr/novo-rebank/view/market_price/RegionData.neo?offerings_gbn=AT&update=140228&target=complex_cd&lcode=11&mcode=712&sname=%BE%D0%B7%AE%B8%E9

    #%BE%D0%B7%AE%B8%E9
    #%BE%D0%B7%AE%B8%E9
    query = {
        'target': 'complex_cd',
        'lcode': '01',
        'mcode': '100',
        'sname': '압량면'
    }
    #target=complex_cd&lcode=01&mcode=100&sname=만리동
    print(urllib.parse.urlencode(query, encoding='euckr'))
