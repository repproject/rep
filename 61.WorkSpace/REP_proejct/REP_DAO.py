from typing import Any, Union, Tuple
import pymysql
import REP_Main
import REP_TLGR_MSG
from REP_COM import *
import REP_SQL
from REP_DAO import *
from REP_TABLE import *
from REP_MIG_MAPP import *
from REP_TLGR_MSG import *
import json

repDBHost = "ceasar.iptime.org"
repDBUser = "repwas"
repDBPassword = "0(repwas)"
repDBdb = "rep"
rebDBcharset = 'utf8'

def repDBConnect():  # DBConnection
    return pymysql.connect(host=repDBHost, user=repDBUser, password=repDBPassword, db=repDBdb, charset=rebDBcharset)

def getrepDBcursor(): #DBCursor
    return repDBConnect().cursor()

def getTableDic(tableName):
    global Log
    try:
        dicTBL = dicTable[tableName]
    except KeyError as e:
        Log.Error("REP_TABLE 미존재 : " + str(e))
        sendMessage("REP_TABLE 미존재 : " +str(e))
    except Exception as e:
        Log.Error(str(e))
        sendMessage(str(e))
    else:
        initializeTableDic(dicTBL)
        return dicTBL

#JSON을 TABLE DIC으로 변환한다.
def setJson2TableDic(tableName,jSon):
    global Log
    dicTBL = getTableDic(tableName)
    for col in dicMigMapp[tableName].keys():
        try:
            dicTBL[dicMigMapp[tableName][col]] = jSon[col]
        except Exception as e:
            pass
            Log.debug("migNaverComplexList json Parsing Error" + str(e) + col)
    return dicTBL

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

#sqlId로 SQL을 가져와 Data를 fetch한다.
def fetch(sqlId,dicParam):
    global Log
    try:
        conn = repDBConnect()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = REP_SQL.redSqlDic[sqlId]
        curs.execute(sql)
        dic: Union[Tuple, Any] = curs.fetchall()
        conn.close()
    except Exception as e:
        Log.error(str(e))
        sendMessage(str(e))
        Log.error(sqlId + ":" + sql)
        sendMessage(sqlId + ":" + sql)
        return dic
    return dic

#TableDic으로 INSERT문을 만들어 넣는다.
def insertBasicByTBLDic(tableName,dicTBL):
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    sql = makeSQLBasicByTBLDic(tableName,dicTBL)

    Log.info("insertBasicByTBLDic : " + sql)
    curs.execute(sql)
    conn.commit()
    conn.close()

#ListTableDic을 insert후 한번에 Commit한다.
def insertBasicByTBLDicList(tableName,listDicTBL):
    conn = repDBConnect()
    curs = conn.cursor()
    for dicTBL in listDicTBL:
        sql = makeSQLBasicByTBLDic(tableName, dicTBL)
        Log.info("insertBasicByTBLDicList : " + sql)
        curs.execute(sql)
    conn.commit()
    conn.close()

#TableDic으로 INSERT문을 만들어 넣는다.(단문)
def makeSQLBasicByTBLDic(tableName,dicTBL):
    sql = "INSERT INTO "
    sql += tableName
    sql += " ("

    sql2 = ""

    for colName in dicTBL.keys():
        if str(type(dicTBL[colName])) == "<class 'str'>" and colName != 'REG_DTM' and colName != 'CHG_DTM':
            if len(dicTBL[colName]) == 0:
                continue

        sql += colName
        sql += ","
        if(colName != 'REG_USER_ID' and colName != 'CHG_USER_ID' and colName != 'REG_DTM' and colName != 'CHG_DTM' ):
            if(dicTBL[colName] != None):
                if(str(type(dicTBL[colName])) == "<class 'str'>"):
                    sql2 += "'"
                    sql2 += dicTBL[colName].replace("'","''")
                    sql2 += "'"
                else:
                    sql2 += str(dicTBL[colName])
            else:
                sql2 += "''"
            sql2 += ','

    sql = sql[0:-1]
    sql += ") VALUES ("
    sql += sql2
    sql += "'" + str(dicTBL['REG_USER_ID']) + "'" + ",NOW(),"+"'"+str(dicTBL['CHG_USER_ID'])+"'"+",NOW())"
    return sql

def insertListByTBLDic(tableName,listDicTBL):
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()
#        for dicTBL in listDicTBL:
#        pass

    conn.commit()
    conn.close()

#기본조건(=)을 가진 update
def updateBaiscByTBLDic(tableName,dicTBL,dicBaiscCond):
    global Log
    try:
        conn = repDBConnect()
        curs = conn.cursor()
        sql = UPDATECombyDic(tableName,dicTBL,0)
        sql += ",CHG_DTM = NOW()"

        flagStart = 1
        for dicCondKey in dicBaiscCond.keys():
            if flagStart:
                sql += " WHERE "
                flagStart = 0
            else:
                sql += " AND "

            sql += dicCondKey + " = " + "'" + str(dicBaiscCond[dicCondKey]) + "'"

        curs.execute(sql)
        Log.debug(sql)
        conn.commit()
        conn.close()

    except Exception as e:

        Log.error("####################ERROR[updateBaiscByTBLDic]####################")
        Log.error("SQL ERROR :" + sql)
        sendMessage("SQL ERROR : " + sql)
        Log.error("Exception :" + str(e))
        sendMessage("Exception :" + str(e))
        return False

#update 공통 Dictionary에 존재하는 KEY에 대해서만 UPDATE문장을 만들어 준다.
def UPDATECombyDic(TABLE_NAME,dic,isValidateNull):
    sql = "UPDATE " + TABLE_NAME + " SET "
    for child in dic.keys():
        #빈값은 갱신 제외
        if isValidateNull == 1 or len(str(dic[child])) > 0 and dic[child] != None :
            sql += " " + child + " = '" + str(dic[child]).replace("'","''") + "', "
    return sql[0:-2] #마지막 Comma는 제외

def INSERT_KMIG_NV_CMPX(dicNvCmpx):  # 네이버아파트코드삽입
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """INSERT INTO KMIG_NV_CMPX (NV_CMPX_ID, NV_CMPX_NM, GOV_LEGL_DONG_CD, NV_CMPX_KND, BAS_ADDR, DTL_ADDR , X_COOR_VAL , Y_COOR_VAL , TOT_HSHL_CNT , TOT_DONG_CNT , MAX_FLR , MIN_FLR , CMPL_YYMM, SALE_CNT, JS_CNT, WS_CNT, SHRT_RENT_CNT, `REG_USER_ID`, `REG_DTM`, `CHG_USER_ID`, `CHG_DTM`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),%s,NOW())"""

    try:
        curs.execute(sql, (dicNvCmpx['NV_CMPX_ID'].strip(),
                           dicNvCmpx['NV_CMPX_NM'].strip(),
                           dicNvCmpx['GOV_LEGL_DONG_CD'].strip(),
                           dicNvCmpx['NV_CMPX_KND'].strip(),
                           dicNvCmpx['BAS_ADDR'].strip(),
                           dicNvCmpx['DTL_ADDR'].strip(),
                           dicNvCmpx['X_COOR_VAL'],
                           dicNvCmpx['Y_COOR_VAL'],
                           dicNvCmpx['TOT_HSHL_CNT'],
                           dicNvCmpx['TOT_DONG_CNT'],
                           dicNvCmpx['MAX_FLR'],
                           dicNvCmpx['MIN_FLR'],
                           dicNvCmpx['CMPL_YYMM'].strip(),
                           dicNvCmpx['SALE_CNT'],
                           dicNvCmpx['JS_CNT'],
                           dicNvCmpx['WS_CNT'],
                           dicNvCmpx['SHRT_RENT_CNT'],
                           user_id,user_id))
    except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
        print("[E]네이버아파트코드 중복")

    conn.commit()
    conn.close()

def SELECT_RET_LEGL_REGN_CD():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "SELECT LEGL_DONG_CD FROM KRED_LEGL_DONG WHERE LV_CD = '3' ORDER BY LEGL_DONG_CD ASC"
    curs.execute(sql)
    tup = curs.fetchall()
    conn.close()
    return tup

def INSERT_KMIG_KB_BIG_REGN(dicRetBigArea):  # 대지역코드 삽입
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """INSERT INTO KMIG_KB_REGN (KB_REGN_CD, KB_REGN_NM, UP_KB_REGN_CD, LV_CD, REG_USER_ID, REG_DTM, CHG_USER_ID, CHG_DTM) VALUES (%s,%s,%s,%s,%s,NOW(),%s,NOW())"""

    try:
        curs.execute(sql, (dicRetBigArea['KB_REGN_CD'].strip(), dicRetBigArea['KB_REGN_NM'].strip(),
                           dicRetBigArea['UP_KB_REGN_CD'].strip(), "1", user_id, user_id))
    except pymysql.IntegrityError as err:  # 기존에 대지역 코드가 존재할 수 있음
        print("[E]대지역코드 중복")

    conn.commit()
    conn.close()


def INSERT_KMIG_KB_MID_REGN(dicRetMidArea):  # 중지역코드 삽입
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """INSERT INTO KMIG_KB_REGN (KB_REGN_CD, KB_REGN_NM, UP_KB_REGN_CD, LV_CD, REG_USER_ID, REG_DTM, CHG_USER_ID, CHG_DTM) VALUES (%s,%s,%s,%s,%s,NOW(),%s,NOW())"""
    try:
        curs.execute(sql, (dicRetMidArea['KB_REGN_CD'].strip(), dicRetMidArea['KB_REGN_NM'].strip(),
                           dicRetMidArea['UP_KB_REGN_CD'].strip(), "2", user_id, user_id))
    except pymysql.IntegrityError as err:  # 기존에 중지역 코드가 존재할 수 있음
        print("[E]중지역코드 중복")
    conn.commit()
    conn.close()


def INSERT_KMIG_KB_SMALL_REGN(dicRetSmallArea):  # 소지역코드 삽입
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """INSERT INTO KMIG_KB_REGN (KB_REGN_CD, KB_REGN_NM, UP_KB_REGN_CD, LV_CD, REG_USER_ID, REG_DTM, CHG_USER_ID, CHG_DTM) VALUES (%s,%s,%s,%s,%s,NOW(),%s,NOW())"""
    try:
        curs.execute(sql, (dicRetSmallArea['KB_REGN_CD'].strip(), dicRetSmallArea['KB_REGN_NM'].strip(),
                           dicRetSmallArea['UP_KB_REGN_CD'].strip(), "3", user_id, user_id))
    except pymysql.IntegrityError as err:  # 기존에 소지역 코드가 존재할 수 있음
        print("[E]소지역코드 중복")
    conn.commit()
    conn.close()


def INSERT_KMIG_KB_CMPX(dicRetSmallArea):  # 물건식별자 삽입
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """INSERT INTO KMIG_KB_CMPX (CMPX_IDF_ID,CMPX_IDF_NM,KB_REGN_CD,X_COOR_VAL,Y_COOR_VAL,REG_USER_ID,REG_DTM,CHG_USER_ID,CHG_DTM) VALUES (%s,%s,%s,%s,%s,%s,NOW(),%s,NOW())"""
    try:
        curs.execute(sql, (dicRetSmallArea['CMPX_IDF_ID'].strip(), dicRetSmallArea['CMPX_IDF_NM'].strip(),
                           dicRetSmallArea['KB_REGN_CD'].strip(), dicRetSmallArea['X_COOR_VAL'].strip(),
                           dicRetSmallArea['Y_COOR_VAL'].strip(), user_id, user_id))
    except pymysql.IntegrityError as err:  # 기존에 소지역 코드가 존재할 수 있음
        print("[E]물건식별자 중복")
    conn.commit()
    conn.close()


def INSERT_KMIG_KB_CMPX_TYP(dicComplexTyp):  # 소지역코드 삽입
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """INSERT INTO KMIG_KB_CMPX_TYP (CMPX_IDF_ID,HOUSE_TYP_SEQ,HOUSE_TYP_NM,REG_USER_ID,REG_DTM,CHG_USER_ID,CHG_DTM) VALUES (%s,%s,%s,%s,NOW(),%s,NOW())"""
    try:
        curs.execute(sql, (dicComplexTyp['CMPX_IDF_ID'].strip(), dicComplexTyp['HOUSE_TYP_SEQ'].strip(),
                           dicComplexTyp['HOUSE_TYP_NM'].strip(), user_id, user_id))
    except pymysql.IntegrityError as err:  # 기존에 소지역 코드가 존재할 수 있음
        print("[E]주택형 삽입 중복")
    conn.commit()
    conn.close()


def INSERT_KMIG_KB_CMPX_TYP_MON_PRC(curs, dicCmpxTypMonPrc):  # 물건식별자 삽입
    # DBConnection
    # conn = repDBConnect()
    # curs = conn.cursor()

    print(dicCmpxTypMonPrc)
    # 초기변수 세팅
    user_id = REP_Main.userid
    sql = """INSERT INTO kmig_kb_cmpx_typ_mon_prc (`CMPX_IDF_ID`,`HOUSE_TYP_SEQ`,`STD_YYMM`,`UP_AVG_PRC`,`GNRL_AVG_PRC`,`DOWN_AVG_PRC`,`UP_JS_AVG_PRC`,`GNRL_JS_AVG_PRC`,`DOWN_JS_AVG_PRC`,`REG_USER_ID`,`REG_DTM`,`CHG_USER_ID`,`CHG_DTM`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),%s,NOW())"""
    try:
        curs.execute(sql, (dicCmpxTypMonPrc['CMPX_IDF_ID'].strip(), str(dicCmpxTypMonPrc['HOUSE_TYP_SEQ']),
                           dicCmpxTypMonPrc['STD_YYMM'].strip(), dicCmpxTypMonPrc['UP_AVG_PRC'].strip(),
                           dicCmpxTypMonPrc['GNRL_AVG_PRC'].strip(), dicCmpxTypMonPrc['DOWN_AVG_PRC'].strip(),
                           dicCmpxTypMonPrc['UP_JS_AVG_PRC'].strip(), dicCmpxTypMonPrc['GNRL_JS_AVG_PRC'].strip(),
                           dicCmpxTypMonPrc['DOWN_JS_AVG_PRC'].strip(), user_id, user_id))
    except pymysql.IntegrityError as err:
        print("[E]KB주택형월별시세 중복")
        #conn.commit()
        #conn.close()


def INSERT_KADM_TLGR_USER(dicTlgrUser):
    returnCode = '100'
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()
    # 초기변수 세팅
    user_id = REP_Main.userid
    sql = """INSERT INTO kadm_tlgr_user(`TLGR_USER_ID`, `TLGR_USER_NM`, `RCV_TGT_YN`, `REG_USER_ID`, `REG_DTM`, `CHG_USER_ID`, `CHG_DTM`)  VALUES( %s, %s, %s, %s, NOW(), %s, NOW())"""
    try:
        curs.execute(sql, (str(dicTlgrUser['TLGR_USER_ID']).strip(), dicTlgrUser['TLGR_USER_NM'].strip(),
                           dicTlgrUser['RCV_TGT_YN'].strip(), user_id, user_id))
    except pymysql.IntegrityError as err:
        print("[E]텔레그램 사용자 중복")
        returnCode = '200'
    conn.commit()
    conn.close()
    return returnCode


def INSERT_KADM_TLGR_MSG(dicTlgrMsg):
    returnCode = '100'
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid
    sql = """INSERT INTO KADM_TLGR_MSG(`TLGR_MSG_ID`, `TLGR_MSG_CNTS`, `REG_USER_ID`, `REG_DTM`, `CHG_USER_ID`, `CHG_DTM`)  VALUES( %s, %s, %s, NOW(), %s, NOW())"""
    try:
        curs.execute(sql, (str(dicTlgrMsg['TLGR_MSG_ID']).strip(), dicTlgrMsg['TLGR_MSG_CNTS'], user_id, user_id))
    except pymysql.IntegrityError as err:
        print("[E]텔레그램 메시지 중복")
        returnCode = '301'
    conn.commit()
    conn.close()
    return returnCode

def SELECT_NV_CMPX_ID_CDdic():
    conn = repDBConnect()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    #sql = "SELECT NV_CMPX_ID, 'A01' as CMPX_CTGR FROM KMIG_NV_CMPX ORDER BY NV_CMPX_ID ASC"
    sql = "SELECT NV_CMPX_ID, CMPX_CTGR FROM KMIG_NV_CMPX WHERE NV_CMPX_ID NOT IN (SELECT NV_CMPX_ID FROM KMIG_NV_CMPX_TYP) ORDER BY NV_CMPX_ID ASC"
    curs.execute(sql)
    dic = curs.fetchall()
    conn.close()
    return dic

def INSERT_KMIG_NV_APT_CODE(dicNvAptCode):  # 네이버아파트코드삽입
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """INSERT INTO KMIG_NV_CMPX (NV_CMPX_ID, NV_CMPX_NM, X_COOR_VAL, Y_COOR_VAL, GOV_LEGL_DONG_CD,  `REG_USER_ID`, `REG_DTM`, `CHG_USER_ID`, `CHG_DTM`) VALUES (%s,%s,%s,%s,%s, %s, NOW(), %s, NOW())"""

    try:
        curs.execute(sql, (dicNvAptCode['NV_CMPX_ID'].strip(), dicNvAptCode['NV_CMPX_NM'].strip(),
                           dicNvAptCode['X_COOR_VAL'].strip(), dicNvAptCode['Y_COOR_VAL'].strip(), dicNvAptCode['GOV_LEGL_DONG_CD'], user_id, user_id))
    except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
        print("[E]네이버아파트코드 중복")

    conn.commit()
    conn.close()

def INSERT_KMIG_NV_CMPX_BUS(dicNvCmplexBus):  # 네이버아파트코드삽입
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """INSERT INTO KMIG_NV_CMPX_BUS (NV_CMPX_ID, BUS_NUM, `REG_USER_ID`, `REG_DTM`, `CHG_USER_ID`, `CHG_DTM`) VALUES (%s,%s,%s, NOW(), %s, NOW())"""

    try:
        curs.execute(sql, (dicNvCmplexBus['NV_CMPX_ID'].strip(), dicNvCmplexBus['BUS_NUM'].strip(),user_id, user_id))
    except pymysql.IntegrityError as err:  # 기존에 네이버아파트 코드가 존재할 수 있음
        print("[E]단지버스 중복")
        print(dicNvCmplexBus)

    conn.commit()
    conn.close()

def SELECT_RET_BIG_AREA_CD2tup():
    # curs = REP_Main.conn.cursor(pymysql.cursors.DictCursor)
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "SELECT KB_REGN_CD FROM KMIG_KB_REGN WHERE LV_CD = '1' ORDER BY KB_REGN_CD ASC"
    curs.execute(sql)
    tup = curs.fetchall()
    conn.close()
    return tup


def SELECT_RET_MID_AREA_CD2tup():
    # curs = REP_Main.conn.cursor(pymysql.cursors.DictCursor)
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "SELECT KB_REGN_CD FROM KMIG_KB_REGN WHERE LV_CD = '2' ORDER BY KB_REGN_CD ASC"
    curs.execute(sql)
    tup = curs.fetchall()
    conn.close()
    return tup


def SELECT_RET_SMALL_AREA_CD2tup():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "SELECT KB_REGN_CD FROM KMIG_KB_REGN WHERE LV_CD = '3' ORDER BY KB_REGN_CD ASC"
    curs.execute(sql)
    tup = curs.fetchall()
    conn.close()
    return tup





def SELECT_RET_CMPX_CD2dic():
    conn = repDBConnect()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT CMPX_IDF_ID, KB_REGN_CD as SMALL_KB_REGN_CD FROM KMIG_KB_CMPX ORDER BY CMPX_IDF_ID ASC"
    curs.execute(sql)
    dic = curs.fetchall()
    conn.close()
    return dic


def SELECT_RET_CMPX_TYP_CD2dic():
    conn = repDBConnect()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT a.CMPX_IDF_ID, a.HOUSE_TYP_SEQ, b.KB_REGN_CD as SMALL_KB_REGN_CD FROM KMIG_KB_CMPX_TYP a, kmig_kb_cmpx b where a.cmpx_idf_id = b.cmpx_idf_id  AND A.CMPX_IDF_ID > 'KBA009000' ORDER BY CMPX_IDF_ID ASC, a.HOUSE_TYP_SEQ"
    curs.execute(sql)
    dic = curs.fetchall()
    conn.close()
    return dic


def SELECT_FUNCbyJOB_ID2dic(JOB_ID):
    conn = repDBConnect()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT J.JOB_ID, J.JOB_NM, F.FUNC_ID, F.FUNC_NM, A.ACT_ID, A.ACT_NM, F.FUNC_ID, F.FUNC_NM FROM KADM_JOB J , KADM_JOB_ACT JA, KADM_ACT A, KADM_ACT_FUNC AF, KADM_FUNC F WHERE " \
          "J.JOB_ID = JA.JOB_ID AND JA.ACT_ID = A.ACT_ID AND A.ACT_ID = AF.ACT_ID AND AF.FUNC_ID = F.FUNC_ID AND " \
          "AF.USE_YN = 'Y' AND JA.USE_YN = 'Y' AND J.JOB_ID = %s ORDER BY JA.EXEC_SEQ ASC, AF.EXEC_SEQ ASC "
    curs.execute(sql, (JOB_ID))
    tup = curs.fetchall()
    conn.close()
    return tup

def SELECT_KMIG_NV_CMPXtup():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "SELECT NV_CMPX_ID FROM KMIG_NV_CMPX WHERE NV_CMPX_ID = '101608' ORDER BY NV_CMPX_ID"
    curs.execute(sql)
    tup = curs.fetchall()
    conn.close()
    return tup

def SELECT_KADM_FUNC_TGT_TBL2dic(dicFuncTbl):
    conn = repDBConnect()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT FINL_CHG_YYMM, FINL_CHG_YMD FROM KADM_FUNC_TGT_TBL WHERE TBL_NM = %s AND FUNC_ID = %s"
    curs.execute(sql, (dicFuncTbl['TBL_NM'].strip(), dicFuncTbl['FUNC_ID'].strip()))
    dic = curs.fetchall()
    conn.close()
    return dic

def DELETE_KMIG_KB_BIG_REGN():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "DELETE FROM KMIG_KB_REGN WHERE LV_CD = '1'"
    curs.execute(sql)
    conn.commit()
    conn.close()


def DELETE_KMIG_KB_MID_REGN():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "DELETE FROM KMIG_KB_REGN WHERE LV_CD = '2'"
    curs.execute(sql)
    conn.commit()
    conn.close()


def DELETE_KMIG_KB_SMALL_REGN():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "DELETE FROM KMIG_KB_REGN WHERE LV_CD = '3'"
    curs.execute(sql)
    conn.commit()
    conn.close()


def DELETE_KMIG_KB_CMPX():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "DELETE FROM KMIG_KB_CMPX"
    curs.execute(sql)
    conn.commit()
    conn.close()


def DELETE_KMIG_KB_CMPX_TYP():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "DELETE FROM KMIG_KB_CMPX_TYP"
    curs.execute(sql)
    conn.commit()
    conn.close()


def DELETE_KMIG_KB_CMPX_TYP_MON_PRC():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "DELETE FROM KMIG_KB_CMPX_TYP_MON_PRC"
    curs.execute(sql)
    conn.commit()
    conn.close()


def UPDATE_KMIG_KB_PRC_STAT_001(startCMPX_IDF_ID, endCMPX_IDF_ID):
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """UPDATE kmig_kb_prc_stat KCTMP"""
    sql += """ SET 6M_PRC = (SELECT GNRL_AVG_PRC FROM KMIG_KB_CMPX_TYP_MON_PRC KCTMP6M WHERE KCTMP.CMPX_IDF_ID = KCTMP6M.CMPX_IDF_ID AND KCTMP.HOUSE_TYP_SEQ = KCTMP6M.HOUSE_TYP_SEQ AND (CASE WHEN  SUBSTR(KCTMP.STD_YYMM - 6,5,2)  = '00' THEN KCTMP.STD_YYMM - 6 - 88 WHEN SUBSTR(KCTMP.STD_YYMM - 6,5,2)  > '12' THEN KCTMP.STD_YYMM - 6 - 88 ELSE KCTMP.STD_YYMM - 6 END) = KCTMP6M.STD_YYMM) """
    sql += """, 6M_JS_PRC = (SELECT GNRL_AVG_PRC FROM KMIG_KB_CMPX_TYP_MON_PRC KCTMP6M WHERE KCTMP.CMPX_IDF_ID = KCTMP6M.CMPX_IDF_ID AND KCTMP.HOUSE_TYP_SEQ = KCTMP6M.HOUSE_TYP_SEQ AND (CASE WHEN  SUBSTR(KCTMP.STD_YYMM - 6,5,2)  = '00' THEN KCTMP.STD_YYMM - 6 - 88 WHEN SUBSTR(KCTMP.STD_YYMM - 6,5,2)  > '12' THEN KCTMP.STD_YYMM - 6 - 88 ELSE KCTMP.STD_YYMM - 6 END) = KCTMP6M.STD_YYMM) """
    sql += """, CHG_USER_ID = %s , CHG_DTM = NOW() WHERE CMPX_IDF_ID BETWEEN %s AND %s"""
    try:
        curs.execute(sql, (user_id, startCMPX_IDF_ID, endCMPX_IDF_ID))
    except Exception as err:  # 기존에 소지역 코드가 존재할 수 있음
        REP_COM.log("UPDATE_KMIG_KB_PRC_STAT_001 Exception 발생[start_CMPX_IDF_ID : " + startCMPX_IDF_ID + " endCMPX_IDF_ID : " + endCMPX_IDF_ID + str(err),"ERROR")
    conn.commit()
    conn.close()

def UPDATE_KMIG_NV_CMPX(dicNVCmpx):
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    sql = UPDATECombyDic("KMIG_NV_CMPX",dicNVCmpx)
    sql += ", CHG_DTM = NOW()"
    sql += " WHERE NV_CMPX_ID = " + dicNVCmpx['NV_CMPX_ID']

    try:
        curs.execute(sql)
    except Exception as err:  # 기존에 소역 코드가 존재할 수 있음
        REP_COM.log("네이버 단지 갱신 [NV_CMPX_ID : " + dicNVCmpx['NV_CMPX_ID'] + "]\n" + str(err),"ERROR")
    conn.commit()
    conn.close()

def UPDATE_KADM_TLGR_USER_RCV_TGT_YN(dicTlgrUser):
    returnCode = '100'
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid

    # SQL
    sql = """UPDATE kadm_tlgr_user SET RCV_TGT_YN = %s,CHG_USER_ID = 1,CHG_DTM = %s WHERE TLGR_USER_ID = %s"""

    try:
        curs.execute(sql, (dicTlgrUser['RCV_TGT_YN'], user_id, dicTlgrUser['TLGR_USER_ID']))
    except Exception as err:  # 기존에 소지역 코드가 존재할 수 있음
        print("[E]텔레그램 사용자 수신해제중 ERROR")
        returnCode = '200'
    conn.commit()
    conn.close()
    return returnCode

def INSERT_KMIG_NV_CMPX_TYP(dicNVComplexType,conn,curs):
        # DBConnection

        # 초기변수 세팅
        user_id = REP_Main.userid

        # SQL
        sql = """INSERT INTO KMIG_NV_CMPX_TYP (NV_CMPX_ID, NV_CMPX_TYP_SEQ, CMPX_TYP_NM, SPLY_AREA, ONLY_AREA, DOOR_STRC, ROOM_CNT, BATH_CNT, SOH_HSHL_CNT, IMG_URL, REG_USER_ID, REG_DTM, CHG_USER_ID, CHG_DTM) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),%s,NOW())"""

        try:
            curs.execute(sql,
                         (dicNVComplexType['NV_CMPX_ID'].strip(), dicNVComplexType['NV_CMPX_TYP_SEQ'].strip(), dicNVComplexType['CMPX_TYP_NM'].strip(), dicNVComplexType['SPLY_AREA'].strip(), dicNVComplexType['ONLY_AREA'].strip(), dicNVComplexType['DOOR_STRC'].strip(), dicNVComplexType['ROOM_CNT'].strip(), dicNVComplexType['BATH_CNT'].strip(), dicNVComplexType['SOH_HSHL_CNT'].strip(), dicNVComplexType['IMG_URL'].strip(), user_id, user_id))
        except pymysql.IntegrityError as err:
            print("네이버물건형 중복")
            print(dicNVComplexType)


def UPDATE_KMIG_KB_CMPX_001(dicKBCmpx):
    # DBConnection
    conn = repDBConnect()
    curs = conn.cursor()

    sql = UPDATECombyDic("KMIG_KB_CMPX",dicKBCmpx)
    sql += ", CHG_DTM = NOW()"
    sql += " WHERE CMPX_IDF_ID = '" + dicKBCmpx['CMPX_IDF_ID']+"'"

    try:
        curs.execute(sql)
    except Exception as err:  # 기존에 소역 코드가 존재할 수 있음
        REP_COM.log("KB 단지 갱신 [CMPX_IDF_ID : " + dicKBCmpx['CMPX_IDF_ID'] + "]\n" + str(err),"ERROR")
    conn.commit()
    conn.close()

def UPDATE_KMIG_KB_CMPX_TYP_MON_PRC(curs, dicCmpxTypMonPrc):  # 물건식별자 삽입
    # DBConnection
    # conn = repDBConnect()
    # curs = conn.cursor()

    # 초기변수 세팅
    user_id = REP_Main.userid
    sql = UPDATECombyDic("KMIG_KB_CMPX_TYP_MON_PRC", dicCmpxTypMonPrc)
    sql += ", CHG_DTM = NOW()"
    sql += " WHERE CMPX_IDF_ID = '" + dicCmpxTypMonPrc['CMPX_IDF_ID'] + "'"
    sql += " AND HOUSE_TYP_SEQ = '" + str(dicCmpxTypMonPrc['HOUSE_TYP_SEQ']) + "'"
    sql += " AND STD_YYMM = '" + dicCmpxTypMonPrc['STD_YYMM'] + "'"

    curs.execute(sql)


