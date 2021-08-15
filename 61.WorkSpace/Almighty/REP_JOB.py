import REP_MIG_NAVER
import REP_COM
from REP_DAO import *
import sys
import schedule
import time
#from REP_TLGR_MSG import *
import REP_TABLE
import traceback

def doJOB(JOB_ID):    #JOB수행
    pass
    # try :
    #     Log.info("####################START[doJOB : " + JOB_ID + "]####################")
    #     sendMessage("START[doJOB : " + JOB_ID + "]")
    #     dicJob = SELECT_FUNCbyJOB_ID2dic(JOB_ID)
    #
    #     for dicFunc in dicJob:
    #         try:
    #             Log.info("####################START[doFunc : " + str(dicFunc) + "]####################")
    #
    #             now = datetime.now()
    #             strNow = now.strftime("%Y%m%d%H%M%S")
    #
    #             batchContext = REP_COM.BatchContext(dicFunc,"",0000000000,strNow)
    #
    #             dicKADM_JOB_FUNC_EXEC = REP_TABLE.dicTable['KADM_JOB_FUNC_EXEC']
    #             dicKADM_JOB_FUNC_EXEC['JOB_ID'] = dicFunc['JOB_ID']
    #             dicKADM_JOB_FUNC_EXEC['ACT_ID'] = dicFunc['ACT_ID']
    #             dicKADM_JOB_FUNC_EXEC['FUNC_ID'] = dicFunc['FUNC_ID']
    #             dicKADM_JOB_FUNC_EXEC['EXEC_DTM'] = strNow
    #             dicKADM_JOB_FUNC_EXEC['EXEC_STAT_CD'] = 'R'
    #             dicKADM_JOB_FUNC_EXEC['STA_DTM'] = strNow
    #             dicKADM_JOB_FUNC_EXEC['REG_USER_ID'] = userid
    #             dicKADM_JOB_FUNC_EXEC['CHG_USER_ID'] = userid
    #
    #             insertBasicByTBLDic('KADM_JOB_FUNC_EXEC', dicKADM_JOB_FUNC_EXEC)
    #
    #             dicBasicCond = {}
    #             dicBasicCond['JOB_ID'] = dicKADM_JOB_FUNC_EXEC['JOB_ID']
    #             dicBasicCond['FUNC_ID'] = dicKADM_JOB_FUNC_EXEC['FUNC_ID']
    #             dicBasicCond['ACT_ID'] = dicKADM_JOB_FUNC_EXEC['ACT_ID']
    #             dicBasicCond['EXEC_DTM'] = dicKADM_JOB_FUNC_EXEC['EXEC_DTM']
    #
    #             UdicKADM_JOB_FUNC_EXEC = {}
    #             UdicKADM_JOB_FUNC_EXEC['JOB_ID'] = dicKADM_JOB_FUNC_EXEC['JOB_ID']
    #             UdicKADM_JOB_FUNC_EXEC['FUNC_ID'] = dicKADM_JOB_FUNC_EXEC['FUNC_ID']
    #             UdicKADM_JOB_FUNC_EXEC['ACT_ID'] = dicKADM_JOB_FUNC_EXEC['ACT_ID']
    #             UdicKADM_JOB_FUNC_EXEC['EXEC_DTM'] = dicKADM_JOB_FUNC_EXEC['EXEC_DTM']
    #
    #             doFunc(dicFunc['FUNC_ID'],batchContext)
    #
    #             # JOB 수행 종료 상태
    #             UdicKADM_JOB_FUNC_EXEC['EXEC_STAT_CD'] = 'T'
    #
    #         except Exception as e:
    #             # JOB 수행 ERROR 상태
    #             now = datetime.now()
    #             UdicKADM_JOB_FUNC_EXEC = {}
    #             UdicKADM_JOB_FUNC_EXEC['JOB_ID'] = dicKADM_JOB_FUNC_EXEC['JOB_ID']
    #             UdicKADM_JOB_FUNC_EXEC['FUNC_ID'] = dicKADM_JOB_FUNC_EXEC['FUNC_ID']
    #             UdicKADM_JOB_FUNC_EXEC['ACT_ID'] = dicKADM_JOB_FUNC_EXEC['ACT_ID']
    #             UdicKADM_JOB_FUNC_EXEC['EXEC_DTM'] = dicKADM_JOB_FUNC_EXEC['EXEC_DTM']
    #             UdicKADM_JOB_FUNC_EXEC['EXEC_STAT_CD'] = 'E'    #Batch Error 종료
    #             UdicKADM_JOB_FUNC_EXEC['END_DTM'] = datetime.now().strftime("%Y%m%d%H%M%S")
    #             updateBaiscByTBLDic('KADM_JOB_FUNC_EXEC', UdicKADM_JOB_FUNC_EXEC, dicBasicCond)
    #         now = datetime.now()
    #         UdicKADM_JOB_FUNC_EXEC['END_DTM'] = datetime.now().strftime("%Y%m%d%H%M%S")
    #         updateBaiscByTBLDic('KADM_JOB_FUNC_EXEC', UdicKADM_JOB_FUNC_EXEC, dicBasicCond)
    #
    #
    # except Exception as e:
    #     Log.error("####################ERROR[doJOB : " + JOB_ID + "]####################")
    #     Log.error(traceback.format_exc())
    #     sendMessage("ERROR[doJOB : " + JOB_ID + "]" + traceback.format_exc())

def doFunc(Func,batchContext):
    pass
    # if 1==0 : print('error')
    # elif REP_COM.tuple2Str(Func) == "DEL_KB_BIG_REGN"  : func_DEL_KB_BIG_REGN()
    # elif REP_COM.tuple2Str(Func) == "INS_KB_BIG_REGN"  : func_INS_KB_BIG_REGN()
    # elif REP_COM.tuple2Str(Func) == "DEL_KB_MID_REGN"  : func_DEL_KB_MID_REGN()
    # elif REP_COM.tuple2Str(Func) == "INS_KB_MID_REGN"  : func_INS_KB_MID_REGN()
    # elif REP_COM.tuple2Str(Func) == "DEL_KB_SMALL_REGN": func_DEL_KB_SMALL_REGN()
    # elif REP_COM.tuple2Str(Func) == "INS_KB_SMALL_REGN": func_INS_KB_SMALL_REGN()
    # elif REP_COM.tuple2Str(Func) == "DEL_KB_CMPX": func_DEL_KB_CMPX()
    # elif REP_COM.tuple2Str(Func) == "INS_KB_CMPX": func_INS_KB_CMPX()
    # elif REP_COM.tuple2Str(Func) == "DEL_KB_CMPX_TYP": func_DEL_KB_CMPX_TYP()
    # elif REP_COM.tuple2Str(Func) == "INS_KB_CMPX_TYP": func_INS_KB_CMPX_TYP()
    # elif REP_COM.tuple2Str(Func) == "DEL_KB_CMPX_TYP_MPRC": func_DEL_KB_CMPX_TYP_MPRC()
    # elif REP_COM.tuple2Str(Func) == "INS_KB_CMPX_TYP_MPRC": func_INS_KB_CMPX_TYP_MPRC()
    # elif REP_COM.tuple2Str(Func) == "DEL_NV_CMPX": func_DEL_NV_CMPX()
    # elif REP_COM.tuple2Str(Func) == "INS_NV_CMPX": func_INS_NV_CMPX(batchContext)
    # elif REP_COM.tuple2Str(Func) == "UPD_NV_CMPX": func_NV_UP_CMPX_INFO(batchContext)
    # elif REP_COM.tuple2Str(Func) == "DEL_NV_CMPX_TYP": func_DEL_NV_CMPX_TYP()
    # elif REP_COM.tuple2Str(Func) == "INS_NV_CMPX_TYP": func_INS_NV_CMPX_TYP()
    # elif REP_COM.tuple2Str(Func) == "UPD_ST_001": func_UPD_ST_001()
    # elif REP_COM.tuple2Str(Func) == "UPD_KB_CMPX_001": func_UPDATE_KMIG_KB_CMPX_TYP_MON_PRC("UPD_KB_CMPX_001")
    # elif REP_COM.tuple2Str(Func) == "INS_NV_SALE": func_INS_KMIG_NV_SALE()

#Func 목록
# def func_DEL_KB_BIG_REGN():REP_DAO.DELETE_KMIG_KB_BIG_REGN()
# def func_INS_KB_BIG_REGN():REP_MIG.migRetBigAreaCode()
# def func_DEL_KB_MID_REGN():REP_DAO.DELETE_KMIG_KB_MID_REGN()
# def func_INS_KB_MID_REGN():REP_MIG.migRetMidAreaCode()
# def func_DEL_KB_SMALL_REGN():REP_DAO.DELETE_KMIG_KB_SMALL_REGN()
# def func_INS_KB_SMALL_REGN():REP_MIG.migRetSmallAreaCode()
# def func_DEL_KB_CMPX():REP_DAO.DELETE_KMIG_KB_CMPX()
# def func_INS_KB_CMPX(): REP_MIG.migComplex()
# def func_DEL_KB_CMPX_TYP():REP_DAO.DELETE_KMIG_KB_CMPX_TYP()
# def func_INS_KB_CMPX_TYP(): REP_MIG.migComplexTyp()
# def func_DEL_KB_CMPX_TYP_MPRC():REP_DAO.DELETE_KMIG_KB_CMPX_TYP_MON_PRC()
# def func_INS_KB_CMPX_TYP_MPRC(): REP_MIG.migMontlyPrice()
# def func_DEL_NV_CMPX(): print("func_DEL_NV_CMPX")
# def func_INS_NV_CMPX(batchContext):REP_MIG_NAVER.migNaverComplexList(batchContext)
# def func_UPD_NV_CMPX():
#     try :
#         REP_MIG.updateNVComplex()
#     except Exception as e:
#         REP_COM.log("updateNVComplex ERROR " + str(e),"ERROR")
# def func_DEL_NV_CMPX_TYP() : print("func_DEL_NV_CMPX_TYP")
# def func_INS_NV_CMPX_TYP() : REP_MIG.migNVComplexType()
# def func_UPD_ST_001() : REP_MIG.mig_UPD_ST_001()
# def func_UPDATE_KMIG_KB_CMPX_TYP_MON_PRC(FUNC_ID) : REP_MIG.mig_UPDATE_KMIG_KB_CMPX_TYP_MON_PRC(FUNC_ID)
# def func_INS_KMIG_NV_SALE() : REP_MIG.migNVSale()
# def func_NV_UP_CMPX_INFO(batchContext): REP_MIG_NAVER.updNaverComplexDtl(batchContext)

def doSchedule():
    

    #Log.info("####################START[doSchedule]####################")
    #sendMessage("START[doSchedule]")

    #Log.info("####################START[setJob]####################")
    #dicJobSchdList = fetch("selectJobSchdUsingAll","")
    #Log.info(dicJobSchdList)

    # for dicJobSchd in dicJobSchdList:
    #     if(dicJobSchd['EXEC_PERD_CD'] == "DD"): #일배치의 경우
    #         schedule.every().day.at(dicJobSchd['EXEC_HH'] + ":" + dicJobSchd['EXEC_MI']).do(doJOB,dicJobSchd['JOB_ID'])
    #     elif(dicJobSchd['EXEC_PERD_CD'] == "CYCL"):
    #         schedule.every(dicJobSchd['CYCL_MI']).minutes.do(doJOB,dicJobSchd['JOB_ID'])
    #     elif(dicJobSchd['EXEC_PERD_CD'] == "DAY"):
    #         if(dicJobSchd['EXEC_DAY_CD'] == "SUN"):
    #             schedule.every().sunday.at(dicJobSchd['EXEC_HH'] + ":" + dicJobSchd['EXEC_MI']).do(doJOB,dicJobSchd['JOB_ID'])
    #         elif(dicJobSchd['EXEC_DAY_CD'] == "MON"):
    #             schedule.every().monday.at(dicJobSchd['EXEC_HH'] + ":" + dicJobSchd['EXEC_MI']).do(doJOB,dicJobSchd['JOB_ID'])
    #         elif(dicJobSchd['EXEC_DAY_CD'] == "TUE"):
    #             schedule.every().tuesday.at(dicJobSchd['EXEC_HH'] + ":" + dicJobSchd['EXEC_MI']).do(doJOB,dicJobSchd['JOB_ID'])
    #         elif(dicJobSchd['EXEC_DAY_CD'] == "WED"):
    #             schedule.every().wednesday.at(dicJobSchd['EXEC_HH'] + ":" + dicJobSchd['EXEC_MI']).do(doJOB,dicJobSchd['JOB_ID'])
    #         elif(dicJobSchd['EXEC_DAY_CD'] == "THU"):
    #             schedule.every().thursday.at(dicJobSchd['EXEC_HH'] + ":" + dicJobSchd['EXEC_MI']).do(doJOB,dicJobSchd['JOB_ID'])
    #         elif(dicJobSchd['EXEC_DAY_CD'] == "FRI"):
    #             schedule.every().friday.at(dicJobSchd['EXEC_HH'] + ":" + dicJobSchd['EXEC_MI']).do(doJOB,dicJobSchd['JOB_ID'])
    #         elif(dicJobSchd['EXEC_DAY_CD'] == "SAT"):
    #             schedule.every().saturday.at(dicJobSchd['EXEC_HH'] + ":" + dicJobSchd['EXEC_MI']).do(doJOB,dicJobSchd['JOB_ID'])
    #     elif(dicJobSchd['EXEC_PERD_CD'] == "MM" | dicJobSchd['EXEC_PERD_CD'] == "HH"):
    #         Log.error("setJob Error undefined EXEC_PERD_CD MM HH")
    #         sendMessage("setJob Error undefined EXEC_PERD_CD MM HH")
    #
    # Log.info("####################END[setJob]####################")

    #JOB 초기화
    while True:
        try:
            #즉시 수행 job 스케쥴을 가져옴
            #Log.info("####################START[doImidiateJOB]####################")
            #dicJobSchdList = fetch("selectJobSchdImdi", "")
            # count = 0
            # for dicJobSchd in dicJobSchdList:
            #     # 수행시간을 기록하기 위하여 현재 시간을 가져옴
            #     strNow = datetime.now().strftime("%Y%m%d%H%M%S")
            #
            #     #JOB 수행정보 세팅
            #     dicKADM_JOB_EXEC = REP_TABLE.dicTable['KADM_JOB_EXEC']
            #     dicKADM_JOB_EXEC['JOB_ID'] = dicJobSchd['JOB_ID']
            #     dicKADM_JOB_EXEC['EXEC_DTM'] = strNow
            #     dicKADM_JOB_EXEC['EXEC_STAT_CD'] = 'R'
            #     dicKADM_JOB_EXEC['STA_DTM'] = strNow
            #     dicKADM_JOB_EXEC['REG_USER_ID'] = userid
            #     dicKADM_JOB_EXEC['CHG_USER_ID'] = userid
            #
            #     insertBasicByTBLDic('KADM_JOB_EXEC', dicKADM_JOB_EXEC)
            #
            #     dicBasicCond = {}
            #     dicBasicCond['JOB_ID'] = dicKADM_JOB_EXEC['JOB_ID']
            #     dicBasicCond['EXEC_DTM'] = dicKADM_JOB_EXEC['EXEC_DTM']
            #
            #     try :
            #         #JOB실행
            #         doJOB(dicJobSchd['JOB_ID'])
            #
            #         # JOB 수행 종료 상태
            #         dicKADM_JOB_EXEC = REP_TABLE.dicTable['KADM_JOB_EXEC']
            #         dicKADM_JOB_EXEC['JOB_ID'] = dicJobSchd['JOB_ID']
            #         dicKADM_JOB_EXEC['EXEC_STAT_CD'] = 'T'
            #         dicKADM_JOB_EXEC['STA_DTM'] = None
            #         dicKADM_JOB_EXEC['END_DTM'] = datetime.now().strftime("%Y%m%d%H%M%S")
            #         dicKADM_JOB_EXEC['REG_USER_ID'] =None
            #         dicKADM_JOB_EXEC['CHG_USER_ID'] = userid
            #
            #         updateBaiscByTBLDic('KADM_JOB_EXEC', dicKADM_JOB_EXEC, dicBasicCond)
            #
            #     except Exception as e:
            #         #Log.Error("Error in doImidiateJOB" + traceback.format_exc())
            #         dicKADM_JOB_EXEC['EXEC_STAT_CD'] = 'E'
            #         dicKADM_JOB_EXEC['END_DTM'] = datetime.now().strftime("%Y%m%d%H%M%S")
            #         updateBaiscByTBLDic('KADM_JOB_EXEC', dicKADM_JOB_EXEC, dicBasicCond)
            #
            #     # 즉시수행여부를 꺾어버림
            #     dicKADM_JOB_SCHD = REP_TABLE.dicTable['KADM_JOB_SCHD']
            #     dicKADM_JOB_SCHD['JOB_ID'] = dicJobSchd['JOB_ID']
            #     dicKADM_JOB_SCHD['JOB_SEQ'] = dicJobSchd['JOB_SEQ']
            #     dicKADM_JOB_SCHD['IMDI_EXEC_YN'] = 'N'  # 즉시수행여부를 N으로 변경
            #     dicKADM_JOB_SCHD['CHG_USER_ID'] = userid
            #
            #     dicBasicCond = {}
            #     dicBasicCond['JOB_ID'] = dicJobSchd['JOB_ID']
            #     dicBasicCond['JOB_SEQ'] = dicJobSchd['JOB_SEQ']
            #
            #     updateBaiscByTBLDic('KADM_JOB_SCHD', dicKADM_JOB_SCHD, dicBasicCond)
            #Log.error("####################END[doImidiateJOB]####################")

            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            #Log.error(traceback.format_exc())
            #sendMessage("doJob Error" + traceback.format_exc())
            pass

if __name__ == '__main__':
    doSchedule()



