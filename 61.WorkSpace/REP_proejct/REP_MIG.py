from requests import get
from bs4 import BeautifulSoup
import urllib.request
import REP_DAO                  #DB 전문 CLASS
import hyeogyu
import jiil_sample
import REP_URL
import requests
from urllib import *
import json
#from pandas.io.json import json_normalize
import time
import REP_COM
import REP_TLGR_MSG
import REP_Main
import datetime

sleeptime = 1
NVsleeptime = 2

def migRetBigAreaCode():    #박지일
    print("Function migRetBigAreaCode")
    url = REP_URL.KB부동산과거시세조회URL
    print(url)
    soup = getBeautifulShopFromKB(url)

    for child in soup.find("select", id="부동산대지역코드"):
        if len(child) == 1 and len(child['value']) > 0:    #쓰레기값 제외
            dicRetBigArea = {'KB_REGN_CD' : child['value']
                           , 'KB_REGN_NM' : child.text
                           , 'UP_KB_REGN_CD' : 'null'}
            REP_DAO.INSERT_KMIG_KB_BIG_REGN(dicRetBigArea)

def migRetMidAreaCode():
    print("Function migRetMidAreaCode")
    tupBigArea = REP_DAO.SELECT_RET_BIG_AREA_CD2tup();
    for BigArea in tupBigArea:
        url = REP_URL.getJsonKBRealEstatePastPriceInquery('S','01',REP_COM.tuple2Str(BigArea),'','','','','','','','')
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        l = str(soup)
        print(l)
        jSonMidArea = json.loads(l)
        for midRegn in jSonMidArea['msg']['servicedata']['중지역목록ARRAY'] :
            print(midRegn['부동산중지역코드'],midRegn['부동산중지역명'])
            dicRetMidArea = {'KB_REGN_CD': midRegn['부동산중지역코드'], 'KB_REGN_NM': midRegn['부동산중지역명'], 'UP_KB_REGN_CD': REP_COM.tuple2Str(BigArea)}
            REP_DAO.INSERT_KMIG_KB_MID_REGN(dicRetMidArea)
        time.sleep(sleeptime)

def migRetSmallAreaCode():
    print("Function migRetSmallAreaCode")
    tupMidArea = REP_DAO.SELECT_RET_MID_AREA_CD2tup();
    for MidArea in tupMidArea:
        url = REP_URL.getJsonKBRealEstatePastPriceInquery('S','01','',REP_COM.tuple2Str(MidArea),'','','','','','','')
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        l = str(soup)
        jSonMidArea = json.loads(l)
        for midRegn in jSonMidArea['msg']['servicedata']['소지역목록ARRAY'] :
            print(midRegn['부동산소지역코드'],midRegn['부동산소지역명'])
            dicRetSmallArea = {'KB_REGN_CD': midRegn['부동산소지역코드'], 'KB_REGN_NM': midRegn['부동산소지역명'], 'UP_KB_REGN_CD': REP_COM.tuple2Str(MidArea)}
            REP_DAO.INSERT_KMIG_KB_SMALL_REGN(dicRetSmallArea)
        time.sleep(sleeptime)

def migComplex():
    print("Function migComplex")
    #지금 소스보니 문제가 있는듯
    tupSmallArea = REP_DAO.SELECT_RET_SMALL_AREA_CD2tup();
    for SmallArea in tupSmallArea:
        url = REP_URL.getJsonKBRealEstatePastPriceInquery('S','01','','',REP_COM.tuple2Str(SmallArea),'','','','','','')
        print(url)
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        l = str(soup)
        jSonSmallArea = json.loads(l)
        for smallRegn in jSonSmallArea['msg']['servicedata']['ARRAY수4'] :
            print(smallRegn['물건식별자'],smallRegn['아파트명'],smallRegn['X좌표값'],smallRegn['Y좌표값'])
            dicRetComplex = {'CMPX_IDF_ID': smallRegn['물건식별자'], 'CMPX_IDF_NM': smallRegn['아파트명'], 'KB_REGN_CD': REP_COM.tuple2Str(SmallArea), 'X_COOR_VAL' : smallRegn['X좌표값'], 'Y_COOR_VAL' : smallRegn['Y좌표값']}
            REP_DAO.INSERT_KMIG_KB_CMPX(dicRetComplex)
        time.sleep(sleeptime)

def migComplexTyp():
    print("Function migComplexTyp")
    dicComplex = REP_DAO.SELECT_RET_CMPX_CD2dic();
    for Complex in dicComplex:
        url = REP_URL.getJsonKBRealEstatePastPriceInquery('S','01','','',Complex['SMALL_KB_REGN_CD'],Complex['CMPX_IDF_ID'],'','','','','')
        print(url)
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        l = str(soup)
        jSon = json.loads(l)
        for sJSon in jSon['msg']['servicedata']['ARRAY수5'] :
            print(sJSon['주택형일련번호'],sJSon['주택형'])
            dicRetComplex = {'CMPX_IDF_ID': Complex['CMPX_IDF_ID'],'HOUSE_TYP_SEQ': sJSon['주택형일련번호'], 'HOUSE_TYP_NM': sJSon['주택형']}
            REP_DAO.INSERT_KMIG_KB_CMPX_TYP(dicRetComplex)
        time.sleep(sleeptime)

def migMontlyPrice():
    print("Function migMontlyPrice")
    dicComplexTyp = REP_DAO.SELECT_RET_CMPX_TYP_CD2dic();
    for ComplexTyp in dicComplexTyp:
        MonthPriceList = []
        url = REP_URL.getURLKBRealEstatePastPriceInquery('S','01','','',ComplexTyp['SMALL_KB_REGN_CD'],ComplexTyp['CMPX_IDF_ID'],ComplexTyp['HOUSE_TYP_SEQ'],'190001','210012','','')
        print(url)
        soup = getBeautifulShopFromKB(url)
        for child in soup.find("tbody").find_all("td", {"class", "t_r"}):
            MonthPriceList.append(child.text.replace(",","").replace("-","0"))

        seq = 0;
        conn = REP_DAO.repDBConnect()
        curs = conn.cursor()            #Connection의 반복을 줄여 속도 향상을 위해 부득이하게 REP_MIG로 이관 시간당단지수 (468->1039개로 성능향상)
        for child in soup.find_all("th", scope="row"):
            dicMonthPrice = {'CMPX_IDF_ID': ComplexTyp['CMPX_IDF_ID']
                , 'HOUSE_TYP_SEQ': ComplexTyp['HOUSE_TYP_SEQ']
                ,'STD_YYMM': child.text.replace(".","")
                ,'UP_AVG_PRC' :  MonthPriceList[seq*6+2]
                ,'GNRL_AVG_PRC' : MonthPriceList[seq*6+1]
                ,'DOWN_AVG_PRC' : MonthPriceList[seq*6+0]
                ,'UP_JS_AVG_PRC' : MonthPriceList[seq*6+5]
                ,'GNRL_JS_AVG_PRC' : MonthPriceList[seq*6+4]
                ,'DOWN_JS_AVG_PRC' : MonthPriceList[seq*6+3]
            }
            seq = seq + 1
            REP_DAO.INSERT_KMIG_KB_CMPX_TYP_MON_PRC(curs,dicMonthPrice)
        conn.commit()
        conn.close()
    #time.sleep(sleeptime) #성능이슈로 sleep이 필요없음.

def updateNVComplex():
    print("updateNVComplex")
    #단지(물건)ID를 가져온다.
    tupNVComplex = REP_DAO.SELECT_KMIG_NV_CMPXtup()

    dicSchema = {
        '네이버물건ID': 'NV_CMPX_ID',
        '네이버물건명': 'NV_CMPX_NM',
        '단지카테고리': 'CMPX_CTGR',
        '단지종류': 'CMPX_KND',
        '정부법정동코드': 'GOV_LEGL_DONG_CD',
        '총세대수': 'TOT_HSHL_CNT',
        '총동수': 'TOT_DONG_CNT',
        '준공년월': 'CMPL_YYMM',
        '건설사명': 'BLD_CO_NM',
        '총주차대수': 'TOT_PARK_CNT',
        '세대당주차대수': 'HSHL_PER_PARK_CNT',
        '난방방식': 'HEAT_WAY',
        '난방연료': 'HEAT_FUEL',
        '용적률': 'FAR',
        '건폐율': 'BTLR',
        '최고층': 'MAX_FLR',
        '최저층': 'MIN_FLR',
        '면적': 'AERA_LST', #변경
        '관리사무소 Tel' : 'MGMT_CO_TEL', #변경
        '지하철정보': 'SBWY_INFO',
        '사업단계': 'BIZ_STEP',
        '선정시공사': 'CHC_BLD_CO',
        '예상세대수': 'EXP_HSHL_CNT',
        '예상배정면적': 'EXP_ASGN_AERA',
        '예상용적률': 'EXP_FAR',
        '조합전화번호': 'GULD_TEL',
        '추진회/조합 전화' : 'GULD_TEL',
        '수도배관교체' : 'WASP_PIPE_RPLC',
        '등록자ID': 'REG_USER_ID',
        '등록일시': 'REG_DTM',
        '수정자ID': 'CHG_USER_ID',
        '수정일시': 'CHG_DTM',
    }

    for NVComplex in tupNVComplex:

        listComplexInfoHead = []
        listComplexInfoValue = []
        dicComplexInfo = {}
        dicNVComplex = {}

        dicGetParam = {'rletNo': REP_COM.tuple2Str(NVComplex)}
        url = REP_URL.makeGetURL("NV","article","complexInfo",dicGetParam)  #url을 만든다.
        print(url)
        soup = getBeautifulShopFromKB(url)
        strSoup = str(soup)
        dicNVComplex['CMPX_KND'] = strSoup[strSoup.find("hscp_type_cd")+15:strSoup.find("hscp_type_cd")+18]
        print("CMPX_KND : " + dicNVComplex['CMPX_KND'] + " NV_CMPX_ID : " + REP_COM.tuple2Str(NVComplex))

        soup2 = soup.find("div", {"class", "tab_article"})

        #tr에 th가 없는경우 합쳐 넣으려고 마지막th정보를 별도 보관
        lastthtext = ""

        for trsoup in soup2.find_all("tr"):
            thtext = ""
            tdtext = ""
            try :
                thtext = trsoup.find("th").text
            except :
                thtext = ""

            if thtext != "":
                lastthtext = thtext

            tdsoup = trsoup.find("td")
            tdtext = tdsoup.text

            #tdtext 정보를 붙여넣음
            try :
                dicNVComplex[dicSchema[lastthtext]] = dicNVComplex[dicSchema[lastthtext]] + tdtext.replace('\t', '').replace('\n', '')
            except :
                dicNVComplex[dicSchema[lastthtext]] = tdtext.replace('\t', '').replace('\n', '')


        dicNVComplex['NV_CMPX_ID'] = REP_COM.tuple2Str(NVComplex)


        #해운대아이파크가 너무 사이즈가 커서 임시로.
        #print(dicNVComplex['AERA_LST'].replace('\n','').replace('㎡','').replace(' ',''))

        listddSoup = soup2.find_all("dd")
        dicNVComplex['CMPX_CTGR'] = 'A01'
        dicNVComplex['SBWY_INFO'] = listddSoup[0].text
        dicNVComplex['CHG_USER_ID'] = str(REP_Main.userid)

        REP_DAO.UPDATE_KMIG_NV_CMPX(dicNVComplex)

        for ddaSoup in listddSoup[1].find_all("a"):#버스정보
            dicNvCmplexBus={}
            dicNvCmplexBus['NV_CMPX_ID'] = REP_COM.tuple2Str(NVComplex)
            dicNvCmplexBus['BUS_NUM'] =  ddaSoup.text
            REP_DAO.INSERT_KMIG_NV_CMPX_BUS(dicNvCmplexBus)

        time.sleep(NVsleeptime)

def mig_UPD_ST_001():

    for i in range(51,300):
        startNum = i*100+1
        EndNum = i*100+100
        KBstr = "KBA0"
        KBparam = KBstr
        if startNum < 10000: #네자리
            KBparam += "0"
        print(KBparam+str(startNum) + " " + KBparam+str(EndNum))
        REP_DAO.UPDATE_KMIG_KB_PRC_STAT_001(KBparam+str(startNum),KBparam+str(EndNum))

def getBeautifulShopFromKB(url):    #BeautifulShop Class로 특정 Page를 Return한다.
    soup = ''
    continue_flag = 0;
    while soup == '':
        try:
            if continue_flag == 1:
                continue_flag = 0;
                REP_COM.log("getBeautifulShopFromKB Restart","ERROR")

            r = get(url)
            print(r)
            soup = BeautifulSoup(r.content.decode('utf-8', 'replace'),"html5lib")
            return soup
        except Exception as e:
            REP_COM.log("getBeautifulShopFromKB Exception 발생" + str(e),"ERROR")
            print(url)
            print("Connection refused by the server..")
            print("Let me sleep for 10 seconds")
            print("ZZzzzz...")
            time.sleep(10)
            print("Was a nice sleep, now let me continue...")
            continue_flag = 1
            continue


def get_html(url):
    _html = ""
    resp = ''
    while resp == '':
        try:
            #resp = get(url)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            resp = requests.get(url, headers=headers)

            if resp.status_code == 200:
                _html = resp.text
            return _html
        except Exception as e:
            print(e)
            print("Connection refused by the server..")
            print("Let me sleep for 10 seconds")
            print("ZZzzzz...")
            time.sleep(10)
            print("Was a nice sleep, now let me continue...")
            continue

def migNVComplexType():
    #장원영 작업완료 만세
    print("Function migNVComplexType")
    # 단지정보 파라미터 SELECT
    dicNVComplexId = REP_DAO.SELECT_NV_CMPX_ID_CDdic();

    dicSchema = {
        '네이버물건ID': 'NV_CMPX_ID',
        '네이버물건형일련번호': 'NV_CMPX_TYP_SEQ',
        '물건타입명': 'CMPX_TYP_NM',
        '공급면적': 'SPLY_AERA',
        '전용면적': 'ONLY_AERA',
        '현관구조': 'DOOR_STRC',
        '방수': 'ROOM_CNT',
        '욕실수': 'BATH_CNT',
        '분양세대수': 'SOH_HSHL_CNT',
        '이미지URL': 'IMG_URL',
        '등록자ID': 'REG_USER_ID',
        '등록일시': 'REG_DTM',
        '수정자ID': 'CHG_USER_ID',
        '수정일시': 'CHG_DTM',
    }

    for NVComplexId in dicNVComplexId:
        listComplexTypeInfoHead = []
        listComplexTypeInfoValue = []
        dicComplexTypeInfo = {}
        dicNVComplexType = {}

        url = REP_URL.getURLNVComplexTypeInquery(NVComplexId['CMPX_CTGR'],NVComplexId['NV_CMPX_ID'])
        # print(NVComplexId)
        print(url)
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        soup2 = soup.find("div", {"class", "tab_article"})
        # print(soup2)

        i = 0

        listDicNVComplexType = []

        conn = REP_DAO.repDBConnect()
        curs = conn.cursor()

        for test2 in soup2.find_all('li'):
            i = i+1
            # print(test2)
            listComplexTypeInfoHead.append(test2.text)
            # print(listComplexTypeInfoHead)

            trtdsouplist = test2.find_all("dd")
            # print(trtdsouplist)
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # print(trtdsouplist[0].text)
            # print(trtdsouplist[1].text)

            trtdsouplist2 = test2.find_all("h4")
            # print(trtdsouplist2[0].text)

            nvCmpxID = NVComplexId['NV_CMPX_ID']
            # print(nvCmpxID)

            dicNVComplexType['NV_CMPX_ID'] = nvCmpxID
            dicNVComplexType['NV_CMPX_TYP_SEQ'] = str(i)
            dicNVComplexType['CMPX_TYP_NM'] = '면적'+ trtdsouplist2[0].text.replace('\n', '')
            dicNVComplexType['SPLY_AERA']   =   trtdsouplist[0].text
            dicNVComplexType['ONLY_AERA']   =   trtdsouplist[1].text
            dicNVComplexType['DOOR_STRC']   =   trtdsouplist[2].text
            dicNVComplexType['ROOM_CNT']    =   trtdsouplist[3].text
            dicNVComplexType['BATH_CNT']    =   trtdsouplist[4].text
            dicNVComplexType['SOH_HSHL_CNT'] =  trtdsouplist[5].text
            dicNVComplexType['IMG_URL']     =   'http://land.naver.com/info/groundPlanGallery.nhn?rletNo='+nvCmpxID+'&ptpId='+str(i)

            REP_DAO.INSERT_KMIG_NV_CMPX_TYP(dicNVComplexType,conn,curs)

        conn.commit()
        conn.close()

        time.sleep(2)

def mig_UPDATE_KMIG_KB_CMPX_TYP_MON_PRC(FUNC_ID):
    print("Function mig_UPDATE_KMIG_KB_CMPX_TYP_MON_PRC")
    dicFinalChg = chkFinalChg(FUNC_ID,'KMIG_KB_CMPX_TYP_MON_PRC')
    if dicFinalChg == 0:
        REP_COM.log("UPDATE_KMIG_KB_PRC_STAT이 최근 갱신입니다")
    else:
         dicComplexTyp = REP_DAO.SELECT_RET_CMPX_TYP_CD2dic()
         for ComplexTyp in dicComplexTyp:
             MonthPriceList = []
             url = REP_URL.getURLKBRealEstatePastPriceInquery('S','01','','',ComplexTyp['SMALL_KB_REGN_CD'],ComplexTyp['CMPX_IDF_ID'],ComplexTyp['HOUSE_TYP_SEQ'],dicFinalChg[0]['FINL_CHG_YYMM'],'210012','','')
             print(url)
             print(ComplexTyp)
             while 1:
                 try:
                     soup = getBeautifulShopFromKB(url)
                     #print(soup)
                     #time.sleep(1)
                     for child in soup.find("tbody").find_all("td", {"class", "t_r"}):
                         MonthPriceList.append(child.text.replace(",","").replace("-","0"))

                     seq = 0;
                     conn = REP_DAO.repDBConnect()
                     curs = conn.cursor()            #Connection의 반복을 줄여 속도 향상을 위해 부득이하게 REP_MIG로 이관 시간당단지수 (468->1039개로 성능향상)
                     for child in soup.find_all("th", scope="row"):
                        dicMonthPrice = {'CMPX_IDF_ID': ComplexTyp['CMPX_IDF_ID']
                            , 'HOUSE_TYP_SEQ': ComplexTyp['HOUSE_TYP_SEQ']
                            ,'STD_YYMM': child.text.replace(".","")
                            ,'UP_AVG_PRC' :  MonthPriceList[seq*6+2]
                            ,'GNRL_AVG_PRC' : MonthPriceList[seq*6+1]
                            ,'DOWN_AVG_PRC' : MonthPriceList[seq*6+0]
                            ,'UP_JS_AVG_PRC' : MonthPriceList[seq*6+5]
                            ,'GNRL_JS_AVG_PRC' : MonthPriceList[seq*6+4]
                            ,'DOWN_JS_AVG_PRC' : MonthPriceList[seq*6+3]
                        }
                        seq = seq + 1
                        if dicFinalChg[0]['FINL_CHG_YYMM'] < dicMonthPrice['STD_YYMM']:
                            print("I")
                            REP_DAO.INSERT_KMIG_KB_CMPX_TYP_MON_PRC(curs,dicMonthPrice)
                        elif dicFinalChg[0]['FINL_CHG_YYMM'] == dicMonthPrice['STD_YYMM']:
                            print("U")
                            REP_DAO.UPDATE_KMIG_KB_CMPX_TYP_MON_PRC(curs,dicMonthPrice)
                        conn.commit()
                        conn.close()
                        break;
                 except Exception as e:
                     #REP_COM.log("크롤링 도중 에러" + ComplexTyp['CMPX_IDF_ID'] + str(ComplexTyp['HOUSE_TYP_SEQ']) + str(e) ,"ERROR")
                     continue;
                 print("여긴오나?")
                 break;
                 #time.sleep(1)

def chkFinalChg(FUNC_ID,TBL_NM):
    dicFuncTbl = {
        'FUNC_ID': FUNC_ID,
        'TBL_NM': 'KMIG_KB_CMPX_TYP_MON_PRC',
    }

    dicFinalChg = REP_DAO.SELECT_KADM_FUNC_TGT_TBL2dic(dicFuncTbl)

    now = datetime.datetime.now()
    nowDay = now.strftime('%Y%m%d')

    if nowDay > dicFinalChg[0]['FINL_CHG_YMD']:
        return dicFinalChg
    else:
        return 0



def migNVSale():
    #장원영 작업중 20180515
    print("Function migNVSale")
    # 단지정보 파라미터 SELECT
    dicNVComplexId = REP_DAO.SELECT_NV_CMPX_ID_CDdic();

    for NVComplexId in dicNVComplexId:
        listComplexTypeInfoHead = []
        listComplexTypeInfoValue = []
        dicComplexTypeInfo = {}
        dicNVComplexType = {}

        #url = REP_URL.getURLNVSaleInquery(NVComplexId['CMPX_CTGR'],NVComplexId['NV_CMPX_ID'])
        url = REP_URL.getURLNVSaleInquery('A01', '8409')

        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        soup2 = soup.find('tbody')
        # print(soup2)

        i = 0

        for test2 in soup2.find_all('tr'):
            i = i+1
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(i)

            # print(test2)
            listComplexTypeInfoHead.append(test2.text)
            print(listComplexTypeInfoHead)

            trtdsouplist = test2.find_all("div")
            # print(trtdsouplist)

            print(trtdsouplist[0].text)
            #print(trtdsouplist[1].text)
            #print(trtdsouplist[2].text)
            # print(trtdsouplist[3].text)
            # print(trtdsouplist[4].text)
            # print(trtdsouplist[5].text)
            # print(trtdsouplist[6].text)
            # print(trtdsouplist[7].text)
            # print(trtdsouplist[8].text)
            # print(trtdsouplist[9].text)
            #print(trtdsouplist[10].text)
            #print(trtdsouplist[11].text)

            trtdsouplist2 = test2.find_all("a")
            print(trtdsouplist2[0].text)
            print("###############################")
            nvCmpxID = NVComplexId['NV_CMPX_ID']
            # print(nvCmpxID)

            # dicNVComplexType['NV_CMPX_ID'] = nvCmpxID
            # dicNVComplexType['NV_CMPX_TYP_SEQ'] = str(i)
            # dicNVComplexType['CMPX_TYP_NM'] = '면적'+ trtdsouplist2[0].text.replace('\n', '')
            # dicNVComplexType['SPLY_AERA']   =   trtdsouplist[0].text
            # dicNVComplexType['ONLY_AERA']   =   trtdsouplist[1].text
            # dicNVComplexType['DOOR_STRC']   =   trtdsouplist[2].text
            # dicNVComplexType['ROOM_CNT']    =   trtdsouplist[3].text
            # dicNVComplexType['BATH_CNT']    =   trtdsouplist[4].text
            # dicNVComplexType['SOH_HSHL_CNT'] =  trtdsouplist[5].text
            # dicNVComplexType['IMG_URL']     =   'http://land.naver.com/info/groundPlanGallery.nhn?rletNo='+nvCmpxID+'&ptpId='+str(i)

            # print(dicNVComplexType)

            # REP_DAO.INSERT_KMIG_NV_CMPX_TYP(dicNVComplexType)

        time.sleep(2)

