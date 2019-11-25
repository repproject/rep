import pandas as pd
from bs4 import BeautifulSoup
import urllib
import pymysql
from datetime import datetime
from REP_SQL import *
from REP_DAO import *

dicTable = { "GOV_LEGL_DONG_CD" : "",
          "REAL_DEAL_CMPX_KND" : "",
          "DPST_AMT": '',
           "WS_AMT": '',
           "CMPL_YY" : '',
           "DEAL_YYMM": '',
           "DEAL_YMD": '',
           "LEGL_DONG_NM": '',
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
          "보증금액": "DPST_AMT",
          "월세금액": "WS_AMT",
          "건축년도": "CMPL_YY",
          "거래년월" : "DEAL_YYMM",
          "일": 'DEAL_YMD', #Day
          "법정동": 'LEGL_DONG_NM',
          "아파트": 'REAL_DEAL_CMPX_NM',
          "전용면적": 'ONLY_AREA',
          "지번": 'HNUM',
          "층": 'FLR',
          "등록자ID" : "REG_USER_ID",
          "등록일시"  : "REG_DTM",
          "수정자ID" : "CHG_USER_ID",
          "수정일시" : "CHG_DTM"}

def migAptRent():

    # 법정동, 연월 전체가져오기
    dicLeglCodeList = fetch("selectLeglLv2Dong", "")
    ymList = fetch("selectYYMM", "")

    for dicLeglCode in dicLeglCodeList:

        for ym in ymList :

            API_KEY = "n%2Bx3ws990OxspyqgFNBV0oppRCCskpT5taMq4aQx7VyV%2B7JQrn5snqBWdlWuL%2F8IScN0Jbo62Z6Grm7BjBP1%2BQ%3D%3D"
            url="http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent"
            url=url+"?&LAWD_CD="+dicLeglCode['LEGL_DONG_CD']+"&DEAL_YMD="+ym['STD_YYMM']+"&serviceKey="+API_KEY+"&numOfRows=9999"
            print(url)
            resultXML = urllib.request.urlopen(url)
            result = resultXML.read().decode('utf-8')
            print(result)
            xmlsoup = BeautifulSoup(result, 'lxml-xml')
            te = xmlsoup.findAll("item")

            for t in te:

                try :
                    for dic1 in dicMapp.keys():

                        try:
                            dicTable[dicMapp[dic1]] = t.find(dic1).text

                        except:
                            dicTable[dicMapp[dic1]] = ""

                    dicTable["DPST_AMT"] = dicTable["DPST_AMT"].replace(" ", "").replace(",", "")
                    dicTable["WS_AMT"] = dicTable["WS_AMT"].replace(" ", "").replace(",", "")
                    dicTable['GOV_LEGL_DONG_CD'] = dicLeglCode['LEGL_DONG_CD']
                    dicTable['DEAL_YYMM'] = ym['STD_YYMM']
                    dicTable['REG_USER_ID'] = 1000000002
                    dicTable['CHG_USER_ID'] = 1000000002
                    dicTable['REAL_DEAL_CMPX_KND'] = '아파트'

                    insertByDic('KMIG_JWS_DEAL', dicTable)

                except:
                    print("error " + dicLeglCode['LEGL_DONG_CD'] + ym['STD_YYMM'])



if __name__ == '__main__':
    migAptRent()