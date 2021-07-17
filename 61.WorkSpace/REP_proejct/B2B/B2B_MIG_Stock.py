import win32com.client
from B2B import B2B_DAO
from B2B import B2B_COM
import ctypes
from datetime import date

################################################StockDashinConnect
# PLUS 공통 OBJECT
g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
g_objCpTrade = win32com.client.Dispatch('CpTrade.CpTdUtil')
objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

def InitPlusCheck():
    global Log

    # 프로세스가 관리자 권한으로 실행 여부
    if ctypes.windll.shell32.IsUserAnAdmin():
        Log.info('정상: 관리자권한으로 실행된 프로세스입니다.')
    else:
        Log.error('오류: 일반권한으로 실행됨. 관리자 권한으로 실행해 주세요')
        return False

    # 연결 여부 체크
    if (g_objCpStatus.IsConnect == 0):
        Log.error("PLUS가 정상적으로 연결되지 않음. ","ERROR")
        return False

    # # 주문 관련 초기화
    # if (g_objCpTrade.TradeInit(0) != 0):
    #     print("주문 초기화 실패")
    #     return False

    return True

def StockDashinConnect():
    global Log

    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect
    if (bConnect == 0):
        Log.error("PLUS가 정상적으로 연결되지 않음.")
        exit()
    Log.info("PLUS Connection Completed.")
    return objCpCybos

def connectCodeMgr(apiName):
    objCpCybos = StockDashinConnect()
    return win32com.client.Dispatch(apiName)

# [기준정보MIG] 거래원코드(회원사)의 코드 리스트를 반환한다.
def migMemberList():
    global Log

    g_objCodeMgr = connectCodeMgr('CpUtil.CpCodeMgr')
    listMember = g_objCodeMgr.GetMemberList()

    count = 1
    for member in listMember:
        memberNm = g_objCodeMgr.GetMemberName(member)
        dicinds = {'COM_CD_ID': 'DELR', 'COM_CD': member, 'COM_CD_NM': memberNm, 'COM_CD_DESC': memberNm,
                   'PRNT_SEQ': count, 'EFF_OPEN_YMD': '20180416', 'EFF_END_YMD': '99991231',
                   'REG_USER_ID': '1000000001', 'CHG_USER_ID': '100000001'}
        B2B_DAO.InsertSTDdic(dicinds, "JADM_COM_CD_DTL")
        count = count + 1

# [DSIN003_기준정보MIG] 주식의 전 산업 업종코드를 가져온다.
def migIndustryList(argv):
    Log.info("[FUNCTION]START migIndustryList")

    for i in range(1,4):
        g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        if(i == 1): IndsCodeList = g_objCodeMgr.GetIndustryList()
        elif(i == 2): IndsCodeList = g_objCodeMgr.GetKosdaqIndustry1List()
        elif(i == 3): IndsCodeList = g_objCodeMgr.GetKosdaqIndustry2List()
        elif (i == 4): IndsCodeList = g_objCodeMgr.GetKosdaqIndustry3List()

        count = 1
        for indsCode in IndsCodeList:
            indsNm = g_objCodeMgr.GetIndustryName(indsCode)
            dicinds = {'COM_CD_ID': 'STK_INDS', 'COM_CD': indsCode, 'COM_CD_NM': indsNm, 'COM_CD_DESC': indsNm,
                       'PRNT_SEQ': count, 'EFF_OPEN_YMD': '20180416', 'EFF_END_YMD': '99991231',
                       'REG_USER_ID': '1000000001', 'CHG_USER_ID': '100000001'}
            B2B_DAO.InsertSTDdic(dicinds, "JADM_COM_CD_DTL")
            count = count + 1

    #추가되지 않은 업종을 카테고리로 삽입한다.
    B2B_DAO.insertStockProdCtgrFromIndustryCode();
    Log.info("[FUNCTION]END migIndustryList")

#[DSUP002]주식 목록 및 속성을 가져온다.
def migStockList():
    global Log

    Log.info("[FUNCTION]START migStockList")
    objCpCybos = StockDashinConnect()

    count = 0
    for i in range(1, 4):   #I = 주식소속/STK_ASGN
        codeList = g_objCodeMgr.GetStockListByMarket(i)  # 거래소
        for code in codeList:
            count = count + 1
            codeName = g_objCodeMgr.CodeToName(code)
            prod_id = 'S' + str(count).zfill(9)
            dicProd = {'PROD_ID': prod_id
                    ,'PROD_NM' : codeName
                    ,'PROD_ST_CD' : 'OP'
                    ,'PROD_DESC' : codeName
                    ,'FINL_CHG_DTM' : ''
                    ,'CRWL_PROD_ID' : code
                    ,'CRWL_PROD_NM' : codeName
                    ,'UNIT_CD' : 'KRW_STK'                                          #단위 : 주당 원화
                    ,'EXMK_CD' : 'KRX'                                                  #거래소 : KRX(한국거래소)
                    ,'PROD_CTGR_ID' : 'S0' + g_objCodeMgr.GetStockIndustryCode(code)    #카테고리 코드
                    ,'REG_USER_ID' : '1000000001'
                    ,'CHG_USER_ID' : '1000000001'}

            dicStockProd = {'PROD_ID' : prod_id
                            ,'EVDC_MONY_RATE' : g_objCodeMgr.GetStockMarginRate(code) #증거금율
                            ,'DEAL_UNIT_STK_CNT' : g_objCodeMgr.GetStockMemeMin(code) #거래단위주식수
                            ,'STK_INDS_CD' : g_objCodeMgr.GetStockIndustryCode(code) #주식업종코드
                            ,'STK_ASGN_CD' : g_objCodeMgr.GetStockMarketKind(code) #주식소속코드
                            ,'SPV_CL_CD' : g_objCodeMgr.GetStockControlKind(code) #감리구분코드
                            ,'STK_MGMT_CL_CD' : g_objCodeMgr.GetStockSupervisionKind(code) #주식관리구분코드
                            ,'STK_ST_CD' : g_objCodeMgr.GetStockStatusKind(code) #주식상태코드
                            ,'CPTL_SCAL_CL_CD' : g_objCodeMgr.GetStockCapital(code) #자본금규모구분코드
                            ,'STAC_MM' : g_objCodeMgr.GetStockFiscalMonth(code) #결산월
                            ,'GRPC_CD' : g_objCodeMgr.GetStockGroupCode(code) #그룹사코드
                            ,'KOSPI_200_INDS_CD' : g_objCodeMgr.GetStockKospi200Kind(code) #코스피200업종코드
                            ,'STK_SECT_CD' : g_objCodeMgr.GetStockSectionKind(code) #주식섹션코드
                            ,'FALL_CL_CD' : g_objCodeMgr.GetStockLacKind(code) #락구분코드
                            ,'LSTD_YMD' : g_objCodeMgr.GetStockListedDate(code) #상장일자
                            ,'FACE_PRC' : g_objCodeMgr.GetStockParPrice(code) #액면가
                            ,'STD_PRC' : g_objCodeMgr.GetStockStdPrice(code) #기준가
                            ,'CRDT_PSBL_LST_YN' : B2B_COM.convert10toYN(g_objCodeMgr.IsStockCreditEnable(code)) #신용가능종목여부
                            ,'FACE_INFO_CD' : g_objCodeMgr.GetStockParPriceChageType(code) #액면정보코드
                            ,'SPAC_YN' : B2B_COM.convert10toYN(g_objCodeMgr.IsSPAC(code)) #스팩여부
                            ,'REG_USER_ID' : '1000000001'
                            ,'CHG_USER_ID' : '1000000001'}

            B2B_DAO.MergeSTDdic(dicProd, "JMIG_PROD")
            B2B_DAO.MergeSTDdic(dicStockProd, "JMIG_STK_PROD")

#[DSIN001]주식 가격 갱신
def migStockDayPrice(argv):
    global Log

    Log.info("[FUNCTION]START migStockDayPrice")
    #argv[2] : 시작일자
    #argv[3] : 종료일자
    startDay = 0;
    endDay = 0;
    maxStdYmd = 0;

    try:
        if(argv[2] is None):
            # 주식카테코리(S) 의 최대일자를 가져온다
            dicparam = {'UP_PROD_CTGR_ID': 'S'}
            maxStdYmd = B2B_DAO.selecMaxStdYmdFromDayProdPrc(dicparam)
            if (maxStdYmd is None):
                maxStdYmd = '19800101'

            # 주식카테코리(S) 의 최대일자에 해당 하는 가격정보를 삭제한다( 갱신되었을 수가 있음)
            dicparam = {'UP_PROD_CTGR_ID': 'S', 'STD_YMD': maxStdYmd}
            B2B_DAO.deleteJMIG_PROD_PRCStock(dicparam)
            startDay = int(maxStdYmd)
        else:
            startDay = int(argv[2])


    except Exception as err:
        print(err)
        starDay = 0
        # 주식카테코리(S) 의 최대일자를 가져온다
        dicparam = {'UP_PROD_CTGR_ID': 'S'}
        maxStdYmd = B2B_DAO.selecMaxStdYmdFromDayProdPrc(dicparam)
        if(maxStdYmd is None):
            maxStdYmd = '19800101'
        Log.info("maxStdYmd : " + maxStdYmd)

        # 주식카테코리(S) 의 최대일자에 해당 하는 가격정보를 삭제한다( 갱신되었을 수가 있음)
        dicparam = {'UP_PROD_CTGR_ID': 'S', 'STD_YMD' : maxStdYmd}
        B2B_DAO.deleteJMIG_PROD_PRCStock(dicparam)

        startDay = int(maxStdYmd)

    try:
        if(argv[3] is None):
            endDay = int(B2B_COM.nowDay())
        else:
            endDay = int(argv[3])
    except Exception as err:
        print(err)
        endDay = int(B2B_COM.nowDay())

    Log.info("[FUNCTION]migStockDayPrice startDay : " + str(startDay) + "endDay : " + str(endDay))

    #주식카테코리(S), 거래소(KRX)
    dicparam = {'UP_PROD_CTGR_ID' : 'S', 'EXMK_CD' : 'KRX'}

    #1) 파라미터를을 구성할 값을 DB로부터 가져온다.(크롤링상품ID)
    listProd = B2B_DAO.SELECT_CRWL_PROD_IDdic(dicparam)
    for dicProd in listProd:
        if((endDay - startDay) > 100000) : #10년이 넘는 경우
            stdyy = 0
            for i in range(198, 203):  # 1980년도부터 2010년대 까지 반복
                stdyy = i * 10  # 연도 세팅 10년단위로 가져옴
                paramEndDay = stdyy*10000 + 1231
                migStockDayPrice2(startDay, paramEndDay, dicProd,2600);
        else:
            d_1 = date(int(endDay/10000),int((endDay%10000)/100),int(endDay%100))
            d_2 = date(int(startDay/10000),int((startDay%10000)/100),int(startDay%100))
            d_gap = d_1 - d_2
            result = d_gap.days
            migStockDayPrice2(startDay, endDay, dicProd, result);

        dicDayProdPrc2 = {
            'PROD_ID': dicProd['PROD_ID'],
            'CRNC_CD': 'KRW',
            'START_YMD' : str(startDay),
            'END_YMD' : str(endDay),
            'CHG_USER_ID': '1000000001'
        }
        B2B_DAO.updateYmdSeqJMIG_DAY_PROD_PRC(dicDayProdPrc2)
        B2B_DAO.DeleteJMIG_DAY_PROD_ANAL(dicDayProdPrc2)
        B2B_DAO.InsertJMIG_DAY_PROD_ANAL(dicDayProdPrc2)
    Log.info("DSIN001_주식가격MIG가 완료되었습니다.")

def migStockDayPrice2(startDay,endDay,dicProd, getCnt):
    global Log
    Log.info("시작일자 : " + str(startDay) + " 종료일자 : " + str(endDay) + " 종목 : " + str(dicProd) + " START...")

    objStockChart.SetInputValue(0, dicProd['CRWL_PROD_ID'])  # 종목 코드 - 크롤링 상품ID
    objStockChart.SetInputValue(1, '1')  # 기간으로 조회
    # objStockChart.SetInputValue(2, stdyy*10000 + 1231)  # 요청종료일 (0:최근날짜)
    objStockChart.SetInputValue(2, endDay)  # 요청종료일 (0:최근날짜)
    objStockChart.SetInputValue(3, startDay)  # 요청시작일 기간으로 조회
    objStockChart.SetInputValue(4, getCnt)  # 최근 100일치
    objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8, 9, 12, 13, 16, 17, 18, 19, 20, 21,
                                    25])  # 0 - 날짜,2 - 시가,3 - 고가, 4 - 저가, 5 - 종가, 8 - 거래량, 9 - 거래대금, 12 - 상장주식수,13 - 시가총액, 16 - 외국인현보유수량, 17 - 외국인현보유비율. 18 - 수정주가일자, 19 - 수정주가비율, 20 - 기관순매수, 21 - 기관누적순매수, 25 - 주식회전율
    objStockChart.SetInputValue(6, ord('D'))  # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
    objStockChart.BlockRequest()

    length = objStockChart.GetHeaderValue(3)

    # print("날짜", "시가", "고가", "저가", "종가", "거래량", "거래대금", "상장주식수", "시가총액","외국인현보유수량", "외국인현보유비율","수정주가일자","수정주가비율","기관순매수","기관누적순매수","주식회전율")
    dicDayProdPrcList = []



    #일자Seq를 가져온다.
    #YmdSeq = int(B2B_DAO.selectYmdSeqJMIG_DAY_PROD_PRC(dicDayProdPrc2))

    for i in range(length):
        dicDayProdPrc = {
            'PROD_ID': dicProd['PROD_ID'],
            'CRNC_CD': 'KRW',
            'STD_YMD': objStockChart.GetDataValue(0, i),  # 기준일자
            'NOW_PRC': objStockChart.GetDataValue(4, i),  # 현재가(종가)
            'OPEN_PRC': objStockChart.GetDataValue(1, i),  # 시가
            'END_PRC': objStockChart.GetDataValue(4, i),  # 종가
            'HIGH_PRC': objStockChart.GetDataValue(2, i),  # 고가
            'LOW_PRC': objStockChart.GetDataValue(3, i),  # 저가
            'DEAL_CNT': objStockChart.GetDataValue(5, i),  # 거래량
            'DEAL_AMT': objStockChart.GetDataValue(6, i),  # 거래대금
            'LSTD_STK_CNT': objStockChart.GetDataValue(7, i),  # 상장주식수
            'OPEN_PRC_TOT_AMT': objStockChart.GetDataValue(8, i),  # 시가총액
            'FRNR_PSES_CNT': objStockChart.GetDataValue(9, i),  # 외국인보유수량
            'FRNR_PSES_RATE': objStockChart.GetDataValue(10, i),  # 외국인보유율
            'CHG_PRC_YMD': objStockChart.GetDataValue(11, i),  # 수정가격일자
            'CHG_PRC_RATE': objStockChart.GetDataValue(12, i),  # 수정가격율
            'ORGN_PURE_BUY_CNT': objStockChart.GetDataValue(13, i),  # 기관순매수수량
            'ORGN_ACCM_PURE_BUY_CNT': objStockChart.GetDataValue(14, i),  # 기관누적순매수수량
            'STK_ROTE_RATE': objStockChart.GetDataValue(15, i),  # 주식회전율
            'RCV_ST_CD' : 'C', #수신상태코드
            'REG_USER_ID': '1000000001',
            'CHG_USER_ID': '1000000001'
        }
        dicDayProdPrcList.append(dicDayProdPrc)
        #YmdSeq = YmdSeq + 1
    # 배열삽입
    B2B_DAO.MergeSTDdiclist(dicDayProdPrcList, "JMIG_DAY_PROD_PRC")

if __name__ == '__main__':
    migStockList()