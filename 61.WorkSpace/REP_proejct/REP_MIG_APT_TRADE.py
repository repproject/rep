from bs4 import BeautifulSoup
import urllib
import pymysql
from datetime import datetime
from REP_SQL import *
from REP_COM import *
from REP_DAO import *

dicTable = { "GOV_LEGL_DONG_CD" : "",
          "REAL_DEAL_CMPX_KND" : "",
          "DEAL_AMT": '',
           "CMPL_YY": '',
           "DEAL_YYMM" : '',
           "DEAL_YMD": '',
           "ROAD_NM": '',
           "ROAD_NM_CMPX_ORGL_NUM_CD": '',
           "ROAD_NM_CMPX_VICE_NUM_CD": '',
           "ROAD_NM_SGG_CD": '',
           "ROAD_NM_SEQ_CD": '',
           "ROAD_NM_ONG_UNG_CD": '',
           "ROAD_NM_CD": '',
           "LEGL_DONG_NM": '',
           "LEGL_DONG_ORGL_NUM_CD": '',
            "LEGL_DONG_VICE_NUM_CD": '',
            "LEGL_DONG_SGG_CD": '',
            "LEGL_DONG_UMD_CD": '',
            "LEGL_DONG_HNUM_CD": '',
            "REAL_DEAL_CMPX_NM": '',
            "ONLY_AREA": '',
            "HNUM": '',
            "FLR": '',
            "REG_USER_ID" : "",
            "REG_DTM"  : "",
            "CHG_USER_ID" : "",
            "CHG_DTM" : ""

}

dicMapp= {"지역코드" : "GOV_LEGL_DONG_CD",
          "실거래물건종류" : "REAL_DEAL_CMPX_KND",
          "거래금액": 'DEAL_AMT',
           "건축년도": 'CMPL_YY',
           "거래년월" : 'DEAL_YYMM',
           "일": 'DEAL_YMD',     #일자만
           "도로명": 'ROAD_NM',
           "도로명건물본번호코드": 'ROAD_NM_CMPX_ORGL_NUM_CD',
           "도로명건물부번호코드": 'ROAD_NM_CMPX_VICE_NUM_CD',
           "도로명시군구코드": 'ROAD_NM_SGG_CD',
           "도로명일련번호코드": 'ROAD_NM_SEQ_CD',
           "도로명지상지하코드": 'ROAD_NM_ONG_UNG_CD',
           "도로명코드": 'ROAD_NM_CD',
           "법정동": 'LEGL_DONG_NM',
           "법정동본번코드": 'LEGL_DONG_ORGL_NUM_CD',
            "법정동부번코드": 'LEGL_DONG_VICE_NUM_CD',
            "법정동시군구코드": 'LEGL_DONG_SGG_CD',
            "법정동읍면동코드": 'LEGL_DONG_UMD_CD',
            "법정동지번코드": 'LEGL_DONG_HNUM_CD',
            "아파트": 'REAL_DEAL_CMPX_NM',
            "전용면적": 'ONLY_AREA',
            "지번": 'HNUM',
            "층": 'FLR',
            "등록자ID" : "REG_USER_ID",
            "등록일시"  : "REG_DTM",
            "수정자ID" : "CHG_USER_ID",
            "수정일시" : "CHG_DTM"
         }



def migAptTrade():

    # 법정동, 연월 전체가져오기
    dicLeglCodeList = fetch("selectLeglLv2Dong", "")
    ymList = fetch("selectYYMM", "")

    for dicLeglCode in dicLeglCodeList:

        try:
            for ym in ymList :

                API_KEY = "n%2Bx3ws990OxspyqgFNBV0oppRCCskpT5taMq4aQx7VyV%2B7JQrn5snqBWdlWuL%2F8IScN0Jbo62Z6Grm7BjBP1%2BQ%3D%3D"
                url="http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
                url=url+"?&LAWD_CD="+dicLeglCode['LEGL_DONG_CD']+"&DEAL_YMD="+ym['STD_YYMM']+"&serviceKey="+API_KEY+"&numOfRows=9999"
                #print(url)
                resultXML = urllib.request.urlopen(url)
                result = resultXML.read()
                #print(result)
                xmlsoup = BeautifulSoup(result, 'lxml-xml')
                te = xmlsoup.findAll("item")

                for t in te:
                        for dic1 in dicMapp.keys():

                            try:
                                dicTable[dicMapp[dic1]] = t.find(dic1).text

                            except:
                                dicTable[dicMapp[dic1]] = ""

                        dicTable["DEAL_AMT"] = dicTable["DEAL_AMT"].replace(" ", "").replace(",", "")
                        dicTable['GOV_LEGL_DONG_CD'] = dicLeglCode['LEGL_DONG_CD']
                        dicTable['DEAL_YYMM'] = ym['STD_YYMM']
                        dicTable['REG_USER_ID'] = 1000000002
                        dicTable['CHG_USER_ID'] = 1000000002
                        dicTable['REAL_DEAL_CMPX_KND'] = '아파트'

                        insertBasicByTBLDic('KMIG_DEAL_DTL', dicTable)

        except Exception as e:
            print("error " + dicLeglCode['LEGL_DONG_CD'] + ym['STD_YYMM'])
            print(url)
            print(e)



##item_list = []
## item_list.append(aa)활용방안?
##return(item_list)

# def get_dong_cd(file_nm) :
#     file = pd.read_csv(file_nm, engine='python', sep='\t')
#     file['lawd_cd'] = file['법정동코드'].apply(str).str[:5]
#     return(file)


## 전월세도 같은 형식으로 추가

# def migAptTrade():
#
#
#     # 법정동, 연월 전체가져오기
#     dicLeglCodeList = fetch("selectLeglLv2Dong", "")
#     ymList = fetch("selectYYMM", "")
#     # print(ymList)
#     # print(dicLeglCodeList)
#
#     for dicLeglCode in dicLeglCodeList:
#
#         for ym in ymList :
#
#             dicAPT = collect_trade(ym['STD_YYMM'], dicLeglCode['LEGL_DONG_CD'])
#             # print(dicAPT)
#
#             try :
#                 insertByDic('KMIG_DEAL_DTL', dicAPT)
#             except :
#                 print("error " + dicLeglCode['LEGL_DONG_CD'] + ym['STD_YYMM'] )


if __name__ == '__main__':
    migAptTrade()