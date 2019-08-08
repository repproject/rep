from urllib import parse
from urllib.parse import quote

KB부동산과거시세조회URL = "http://nland.kbstar.com/quics?page=B047172&cc=b028364:b057487"
KB부동산과거시세조회Json = "http://nland.kbstar.com/quics?page=&QAction=763359&RType=json"
KB부동산지도조회Json = "http://nland.kbstar.com/quics?page=B046949&QAction=766912&RType=json&B_CLEAR=1"
네이버부동산동별아파트리스트 = "http://land.naver.com/article/articleList.nhn?"
#네이버부동산 = "http://land.naver.com/article/"
네이버부동산 = "http://land.naver.com"


def makeGetURL(JOB_CL,SITE_CL,TR_ID,dicGetParam):
    #작업분류 (JOB_CL - NV-Naver부동산 KB-KB부동산)
    #사이트구분 1-매물

    if JOB_CL == "NV":
        URL = 네이버부동산 + "/" + SITE_CL + "/" + TR_ID + ".nhn" + makeGetParam(dicGetParam,'?')
    return URL

NAVER부동산URL = "http://land.naver.com/article/groundPlan.nhn?"

def makeGetParam(Dic,Igubun):
    count = 0
    param = ""
    for key, value in Dic.items():
        if count == 0 :
            param += Igubun
        else:
            param += '&'
        param += quote(key)
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