import REP_DAO
import REP_MIG
import REP_COM
import REP_MIG_NAVER

def doJOB(JOB_ID):    #JOB수행
    FuncTuple = REP_DAO.SELECT_FUNCbyJOB_ID2tup(JOB_ID)
    print(FuncTuple)
    for Func in FuncTuple:
        doFunc(Func)

def doFunc(Func):
    if 1==0 : print('error')
    elif REP_COM.tuple2Str(Func) == "DEL_KB_BIG_REGN"  : func_DEL_KB_BIG_REGN()
    elif REP_COM.tuple2Str(Func) == "INS_KB_BIG_REGN"  : func_INS_KB_BIG_REGN()
    elif REP_COM.tuple2Str(Func) == "DEL_KB_MID_REGN"  : func_DEL_KB_MID_REGN()
    elif REP_COM.tuple2Str(Func) == "INS_KB_MID_REGN"  : func_INS_KB_MID_REGN()
    elif REP_COM.tuple2Str(Func) == "DEL_KB_SMALL_REGN": func_DEL_KB_SMALL_REGN()
    elif REP_COM.tuple2Str(Func) == "INS_KB_SMALL_REGN": func_INS_KB_SMALL_REGN()
    elif REP_COM.tuple2Str(Func) == "DEL_KB_CMPX": func_DEL_KB_CMPX()
    elif REP_COM.tuple2Str(Func) == "INS_KB_CMPX": func_INS_KB_CMPX()
    elif REP_COM.tuple2Str(Func) == "DEL_KB_CMPX_TYP": func_DEL_KB_CMPX_TYP()
    elif REP_COM.tuple2Str(Func) == "INS_KB_CMPX_TYP": func_INS_KB_CMPX_TYP()
    elif REP_COM.tuple2Str(Func) == "DEL_KB_CMPX_TYP_MPRC": func_DEL_KB_CMPX_TYP_MPRC()
    elif REP_COM.tuple2Str(Func) == "INS_KB_CMPX_TYP_MPRC": func_INS_KB_CMPX_TYP_MPRC()
    elif REP_COM.tuple2Str(Func) == "DEL_NV_CMPX": func_DEL_NV_CMPX()
    elif REP_COM.tuple2Str(Func) == "INS_NV_CMPX": func_INS_NV_CMPX()
    elif REP_COM.tuple2Str(Func) == "UPD_NV_CMPX": func_UPD_NV_CMPX()
    elif REP_COM.tuple2Str(Func) == "DEL_NV_CMPX_TYP": func_DEL_NV_CMPX_TYP()
    elif REP_COM.tuple2Str(Func) == "INS_NV_CMPX_TYP": func_INS_NV_CMPX_TYP()
    elif REP_COM.tuple2Str(Func) == "UPD_ST_001": func_UPD_ST_001()
    elif REP_COM.tuple2Str(Func) == "UPD_KB_CMPX_001": func_UPDATE_KMIG_KB_CMPX_TYP_MON_PRC("UPD_KB_CMPX_001")
    elif REP_COM.tuple2Str(Func) == "INS_NV_SALE": func_INS_KMIG_NV_SALE()



#Func 목록
def func_DEL_KB_BIG_REGN():REP_DAO.DELETE_KMIG_KB_BIG_REGN()
def func_INS_KB_BIG_REGN():REP_MIG.migRetBigAreaCode()
def func_DEL_KB_MID_REGN():REP_DAO.DELETE_KMIG_KB_MID_REGN()
def func_INS_KB_MID_REGN():REP_MIG.migRetMidAreaCode()
def func_DEL_KB_SMALL_REGN():REP_DAO.DELETE_KMIG_KB_SMALL_REGN()
def func_INS_KB_SMALL_REGN():REP_MIG.migRetSmallAreaCode()
def func_DEL_KB_CMPX():REP_DAO.DELETE_KMIG_KB_CMPX()
def func_INS_KB_CMPX(): REP_MIG.migComplex()
def func_DEL_KB_CMPX_TYP():REP_DAO.DELETE_KMIG_KB_CMPX_TYP()
def func_INS_KB_CMPX_TYP(): REP_MIG.migComplexTyp()
def func_DEL_KB_CMPX_TYP_MPRC():REP_DAO.DELETE_KMIG_KB_CMPX_TYP_MON_PRC()
def func_INS_KB_CMPX_TYP_MPRC(): REP_MIG.migMontlyPrice()
def func_DEL_NV_CMPX(): print("func_DEL_NV_CMPX")
def func_INS_NV_CMPX(): REP_MIG_NAVER.migNaverComplexList()
def func_UPD_NV_CMPX():
    try :
        REP_MIG.updateNVComplex()
    except Exception as e:
        REP_COM.log("updateNVComplex ERROR " + str(e),"ERROR")
def func_DEL_NV_CMPX_TYP() : print("func_DEL_NV_CMPX_TYP")
def func_INS_NV_CMPX_TYP() : REP_MIG.migNVComplexType()
def func_UPD_ST_001() : REP_MIG.mig_UPD_ST_001()
def func_UPDATE_KMIG_KB_CMPX_TYP_MON_PRC(FUNC_ID) : REP_MIG.mig_UPDATE_KMIG_KB_CMPX_TYP_MON_PRC(FUNC_ID)
def func_INS_KMIG_NV_SALE() : REP_MIG.migNVSale()
