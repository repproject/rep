from urllib import parse
import urllib.parse
import Server.COM
import time

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

def setSoup2TableDic(strSvcId,strPasiId,soup):
    dicTBL = getTableDic(tableName)
    for col in dicMigMapp[tableName].keys():
        try:
            dicTBL[dicMigMapp[tableName][col]] = soup.find(col).text
        except Exception as e:
            pass
            Log.debug("migNaverComplexList soup Parsing Error" + str(e) + col)
    return dicTBL

class URLMaker:
    svcId = None
    tableSite = None
    tableSvc = None
    url = None
    dicParam = {} #URL 호출 파라미터
    site_cd = None
    dicSite = None
    dicService = None
    req_way_cd = None
    postData = None
    addStr = ""

    def __init__(self,svcId):
        self.svcId = svcId
        tables = Server.COM.getSvcInfo(self.svcId)[0]
        self.tableSite = tables[0] #table Site
        self.tableSvc = tables[1]  #table Svc
        self.site_cd = self.tableSite.site_cd
        self.req_way_cd = self.tableSvc.req_way_cd
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
        self.url = self.tableSite.bas_prtc + "://" #프로토콜 http
        self.url += urllib.parse.quote(self.tableSite.bas_url + self.tableSvc.bas_svc_url + self.addStr,encoding=self.tableSite.enc_cd)
        if self.req_way_cd == "GET":
            self.url += "?" + urllib.parse.urlencode(self.dicParam, encoding=self.tableSite.enc_cd)
        elif self.req_way_cd == "POST":
            pass
        return self.url

    def printURL(self):
        url = self.getURL()
        if self.req_way_cd == "POST" :
             url += str(self.dicParam)
        rtn = "[" + self.req_way_cd + "]" + url
        return rtn

    def getMethod(self):
        return self.req_way_cd

    def getDicParam(self):
        return self.dicParam

def getURLQuote(url,type="utf-8"):
    return urllib.urlretrieve(urllib.quote(url.encode(type), '/:'))

def get_html(url,method = "GET",data = None):
    _html = ""
    resp = ''
    while resp == '':
        try:
            # resp = get(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; U; Mac OS X 10_6_1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5'}
            if method == "GET":
                preReq = urllib.request.Request(url, headers=headers)
                req = urllib.request.urlopen(preReq)
                resp = req.read()

                #resp = requests.get(url, headers=headers, verify=False)
                #resp = requests.get(url, headers=headers)
            elif method == "POST":
                #resp = requests.get(url, data = data)
                preReq = urllib.request.Request(url, headers=headers)
                req = urllib.request.urlopen(preReq)
                resp = req.read()

#            if resp.status_code == 200:
#                _html = resp
            return resp
        except Exception as e:
            print(e)
            print("Connection refused by the server..")
            print("Let me sleep for 10 seconds")
            print("ZZzzzz...")
            time.sleep(10)
            print("Was a nice sleep, now let me continue...")
            continue




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


#JSON을 TABLE DIC으로 변환한다.
def setSoup2TableDic(tableName,soup):
    global Log
    dicTBL = getTableDic(tableName)
    for col in dicMigMapp[tableName].keys():
        try:
            dicTBL[dicMigMapp[tableName][col]] = soup.find(col).text
        except Exception as e:
            pass
            Log.debug("migNaverComplexList soup Parsing Error" + str(e) + col)
    return dicTBL

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

