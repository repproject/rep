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
import traceback

repDBHost = "127.0.0.1"
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
def setJson2TableDic(tableName,jSon,url=None,page=None,BatchContext=None):
    global Log
    dicTBL = getTableDic(tableName)
    for j in jSon:
        try:
            dicMigMapp[tableName][j]
        except Exception as e:
            try:
                Log.error("Json Parse - NoneRegistered column : " + str(j) + "/ TABLE NAME : " + str(tableName) + " / VALUE : " + str(jSon[j]))
                sendMessage("Json Parse - NoneRegistered column : " + str(j) + "/ TABLE NAME : " + str(tableName) + " / VALUE : " + str(jSon[j]))
            except Exception as e2:
                Log.error("Json Parse - NoneRegistered column : " + str(j) + "/ TABLE NAME : " + str(tableName))
                sendMessage("Json Parse - NoneRegistered column : " + str(j) + "/ TABLE NAME : " + str(tableName))
            dicKADM_JOB_FUNC_EXEC_MSG = dicTable['KADM_JOB_FUNC_EXEC_MSG']
            dicKADM_JOB_FUNC_EXEC_MSG['JOB_ID'] = BatchContext.getJOB_ID()
            dicKADM_JOB_FUNC_EXEC_MSG['ACT_ID'] = BatchContext.getACT_ID()
            dicKADM_JOB_FUNC_EXEC_MSG['FUNC_ID'] = BatchContext.getFUNC_ID()
            dicKADM_JOB_FUNC_EXEC_MSG['EXEC_DTM'] = BatchContext.getExecDtm()
            dicKADM_JOB_FUNC_EXEC_MSG['SEQ'] = 1
            if str(type(url)) == "<class 'str'>":
                dicKADM_JOB_FUNC_EXEC_MSG['REQ_URL'] = url
            else:
                dicKADM_JOB_FUNC_EXEC_MSG['REQ_URL'] = url.printURL()
            dicKADM_JOB_FUNC_EXEC_MSG['PAGE_CNTS'] = str(page)[2:2000]
            dicKADM_JOB_FUNC_EXEC_MSG['ECPT_CNTS'] = traceback.format_exc()[:2000]
            try:
                dicKADM_JOB_FUNC_EXEC_MSG['RMK_CNTS'] = j + ':' + str(jSon[j])
            except Exception as e2:
                pass
            dicKADM_JOB_FUNC_EXEC_MSG['REG_USER_ID'] = userid
            dicKADM_JOB_FUNC_EXEC_MSG['CHG_USER_ID'] = userid
            insertBasicByTBLDic('KADM_JOB_FUNC_EXEC_MSG', dicKADM_JOB_FUNC_EXEC_MSG)

    for col in dicMigMapp[tableName].keys():
        if dicMigMapp[tableName][col] != None:
            try:
                dicTBL[dicMigMapp[tableName][col]] = jSon[col]
            except Exception as e:
                pass
                #Log.debug("migNaverComplexList json Parsing Error" + str(e) + col)
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
def fetch(sqlId,dicBaiscCond):
    global Log
    try:
        conn = repDBConnect()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = REP_SQL.redSqlDic[sqlId]

        if str(type(dicBaiscCond)) == "<class 'dict'>":
            flagStart = 1
            for dicCondKey in dicBaiscCond.keys():
                if flagStart:
                    sql += " WHERE "
                    flagStart = 0
                else:
                    sql += " AND "

                sql += dicCondKey + " = " + "'" + str(dicBaiscCond[dicCondKey]) + "'"

        curs.execute(sql)
        Log.info("fetch : " + sql)
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
def insertBasicByTBLDicList(tableName,listDicTBL,RefConn=None):
    conn = None
    curs = None
    if RefConn == None:
        conn = repDBConnect()
        curs = conn.cursor()

    for dicTBL in listDicTBL:
        sql = makeSQLBasicByTBLDic(tableName, dicTBL)
        Log.info("insertBasicByTBLDicList : " + sql)
        try:
            curs.execute(sql)
        except pymysql.IntegrityError as e:
            Log.debug("insertBasicByTBLDicList IntegrityError : " + str(sql))

    if RefConn == None:
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
                    # if dicTBL[colName].replace("'","''")[-1] == '/':
                    #     sql2 += dicTBL[colName].replace("'", "''")[:-1]
                    # else:
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
        Log.info(sql)
        curs.execute(sql)
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
            column = child
            sql += " " + column + " = "
            if str(type(dic[child])) == "<class 'str'>":
                sql +="'" + str(dic[child]).replace("'","''") + "', "
            else:
                sql += str(dic[child]).replace("'", "''") + ", "
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
        #print("[E]텔레그램 메시지 중복")
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
        rtn = curs.execute(sql, (dicTlgrUser['RCV_TGT_YN'], user_id, dicTlgrUser['TLGR_USER_ID']))
        print(rtn)
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

##B2B_MIG

#Data Access Object 로 Data에 접근 하는 SQL 등을 관리하는 집합
#일별상품분석 테이블 DELETE
# def DeleteJMIG_DAY_PROD_ANAL(dic):
#     sql =  "DELETE FROM JMIG_DAY_PROD_ANAL " \
#            "WHERE PROD_ID = '" +  dic['PROD_ID'] + "'" \
#            "AND CRNC_CD = '" + dic['CRNC_CD'] + "'" \
#            "AND STD_YMD BETWEEN '" +  dic['START_YMD'] + "' AND '" +  dic['END_YMD'] +  "'"
#
#     return B2B_COM_Data.Delete(sql)

#일별상품분석 테이블 INSERT
def InsertJMIG_DAY_PROD_ANAL(dic):
    sql = "INSERT JMIG_DAY_PROD_ANAL " \
          "SELECT A.PROD_ID , A.CRNC_CD , A.STD_YMD , AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 5 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 5DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 7 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 7DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 20 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 20DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 28 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 28DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 60 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 60DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 84 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 84DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 120 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 120DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 168 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 168DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 240 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 240DAY_AVG_PRC " \
          ", AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 336 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END) 336DAY_AVG_PRC " \
          ", IFNULL(STD(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 20 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END),0) 20DAY_STDDEV " \
          ", IFNULL(((A.END_PRC-AVG(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 20 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END)) " \
          "/STD(CASE WHEN B.YMD_SEQ > A.YMD_SEQ - 20 AND B.YMD_SEQ <= A.YMD_SEQ THEN B.END_PRC END)),0) 20DAY_DEVA_DIV_STDV " \
          ",1000000001 REG_USER_ID ,NOW() REG_DTM ,1000000001 CHG_USER_ID ,NOW() CHG_DTM " \
          "FROM JMIG_DAY_PROD_PRC A INNER JOIN JMIG_DAY_PROD_PRC B ON A.PROD_ID = B.PROD_ID AND A.CRNC_CD = B.CRNC_CD " \
          "WHERE A.PROD_ID = '" +  dic['PROD_ID'] + "' AND A.CRNC_CD = '" +  dic['CRNC_CD'] + "' " \
          "AND A.STD_YMD BETWEEN '" + dic['START_YMD'] + "' AND '" + dic['END_YMD'] + "'" \
          "GROUP BY A.PROD_ID, A.CRNC_CD, A.STD_YMD"

    conn = repDBConnect()
    curs = conn.cursor()

    try :
        curs.execute(sql)
    except pymysql.IntegrityError as err:  # 기존에 대지역 코드가 존재할 수 있음
        log("INSERT 중복 발생 : " + str(dic), "INFO")
    conn.commit()
    conn.close()



#추가되지 않은 업종을 카테고리로 삽입한다.
def insertStockProdCtgrFromIndustryCode():
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "INSERT INTO jmig_prod_ctgr " \
                 "SELECT CONCAT('S','0',COM_CD) PROD_CTGR_ID " \
                 ", COM_CD_NM PROD_CTGR_NM " \
                 ", COM_CD_DESC PROD_CTGR_DESC " \
                 ", 'OP' CTGR_ST_CD " \
                 ", '2' LV_SEQ " \
                 ", 'S' UP_PROD_CTGR_ID " \
                 ", COM_CD CRWL_PROD_CTGR_ID " \
                 ", COM_CD_NM CRWL_PROD_CTGR_NM  " \
                 ", 1000000001 REG_USER_ID " \
                 ", NOW() REG_DTM " \
                 ", 1000000001 CHG_USER_ID " \
                 ", NOW() CHG_DTM " \
            "FROM JADM_COM_CD_DTL " \
            "WHERE COM_CD_ID = 'STK_INDS' " \
            "AND CONCAT('S','0',COM_CD) NOT IN (SELECT PROD_CTGR_ID FROM JMIG_PROD_CTGR)"

    try :
        curs.execute(sql)
    except pymysql.IntegrityError as err:  # 기존에 대지역 코드가 존재할 수 있음
        log("INSERT 중복 발생 : ", "INFO")
    conn.commit()
    conn.close()

#상품카테고리에 해당하고 거래소에 맞는 상품ID를 추출
def SELECT_CRWL_PROD_IDdic(dic):
    sql = "SELECT P.PROD_ID, P.CRWL_PROD_ID FROM JMIG_PROD P " \
         "WHERE P.PROD_CTGR_ID IN (SELECT PROD_CTGR_ID FROM JMIG_PROD_CTGR " \
        " WHERE UP_PROD_CTGR_ID = '" + dic['UP_PROD_CTGR_ID'].strip() + "')"
    if('EXMK_CD' in dic.keys()):
        sql = sql + " AND EXMK_CD = '" + dic['EXMK_CD'].strip() + "'"
    sql = sql + " AND PROD_ST_CD = 'OP' ORDER BY P.PROD_ID ASC"
    #return  selectDic(sql)

#상품카테고리에 해당하고 거래소에 맞는 상품ID를 추출
def SELECT_PROD_IDdic():
    sql = "SELECT P.PROD_ID FROM JMIG_PROD P " \
        " WHERE PROD_ST_CD = 'OP' " \
        " AND PROD_ID LIKE 'E%'" \
        " ORDER BY P.PROD_ID ASC" \

#    return  selectDic(sql)

#신규 카테고리 ID 체번
def selectNewProdCtgrId(UP_PROD_CTGR_ID):

    sql = "SELECT CONCAT(UP_PROD_CTGR_ID,LPAD(SUBSTRING(MAX(PROD_CTGR_ID),2,4) + 1,'4','0')) CTGR_ID FROM JMIG_PROD_CTGR WHERE UP_PROD_CTGR_ID = '" + UP_PROD_CTGR_ID + "'"
    # resultList = selectDic(sql)
    #
    # if resultList[0] == None:
    #     val = UP_PROD_CTGR_ID + "0001"
    # else:
    #     val = resultList[0]['CTGR_ID']
    # return val

#신규 상품 체번
def selectNewProdId(UP_PROD_CTGR_ID):
    sql = "SELECT CONCAT('" + UP_PROD_CTGR_ID + "',LPAD(SUBSTRING(MAX(P.PROD_ID),3,9)+1,9,'0')) PROD_ID " \
        "FROM JMIG_PROD P WHERE PROD_ID LIKE '" + UP_PROD_CTGR_ID + "_________'"
#    resultList = selectDic(sql)
#    if resultList[0]['PROD_ID'] == None:
#        val = UP_PROD_CTGR_ID + "000000001"
#    else:
#        val = resultList[0]['PROD_ID']
#    return val

#텔레그램 사용자목록 조회
def SELECT_kadm_tlgr_RCV_usertup():
    sql = "SELECT TLGR_USER_ID FROM jadm_tlgr_user WHERE RCV_TGT_YN = 'Y'"
#    return selectTup(sql)

#주가 이력 조회
def selectDayProdPrc(dicParam):

    sql = "SELECT DPP.STD_YMD, DPP.NOW_PRC, DPP.OPEN_PRC, DPP.END_PRC, DPP.HIGH_PRC, DPP.LOW_PRC, DPP.DEAL_AMT, DPP.LSTD_STK_CNT, DPP.OPEN_PRC_TOT_AMT, DPP.FRNR_PSES_CNT, DPP.FRNR_PSES_RATE, DPP.CHG_PRC_YMD, DPP.CHG_PRC_RATE, DPP.ORGN_PURE_BUY_CNT, DPP.ORGN_ACCM_PURE_BUY_CNT, DPP.STK_ROTE_RATE, DPP.YMD_SEQ" \
          ", DPA.5DAY_AVG_PRC, DPA.7DAY_AVG_PRC, DPA.20DAY_AVG_PRC, DPA.28DAY_AVG_PRC, DPA.60DAY_AVG_PRC, DPA.84DAY_AVG_PRC, DPA.120DAY_AVG_PRC, DPA.128DAY_AVG_PRC, DPA.240DAY_AVG_PRC, DPA.336DAY_AVG_PRC, DPA.20DAY_STDV, DPA.20DAY_DEVA_DIV_STDV " \
    "FROM JMIG_DAY_PROD_PRC DPP " \
    "INNER JOIN JMIG_DAY_PROD_ANAL DPA " \
    "ON DPP.PROD_ID = DPA.PROD_ID AND DPP.CRNC_CD = DPA.CRNC_CD AND DPP.STD_YMD = DPA.STD_YMD " \
    "WHERE DPP.PROD_ID = '" +  dicParam['PROD_ID'] + "'" \
    "AND DPP.CRNC_CD = '" +  dicParam['CRNC_CD'] + "'" \
    "AND DPP.STD_YMD BETWEEN '" + dicParam['STD_OPEN_YMD'] + "' AND '" + dicParam['STD_END_YMD'] + "' "
    "ORDER BY DPP.STD_YMD ASC"

#    resultList = selectDic(sql)

#    return resultList

def selectInitialDealAmt(dicParam):
    sql = "SELECT DEAL_AMT" \
        " FROM JMIG_DAY_SIML_TRAD" \
        " WHERE PROD_ID = '" +  dicParam['PROD_ID'] + "'" \
        " AND CRNC_CD = '" +  dicParam['CRNC_CD'] + "'" \
        " AND PEFM_DTM = '" +  dicParam['PEFM_DTM'] + "'" \
        " AND PTN_ID = '" + dicParam['PTN_ID'] + "'" \
        " AND SIML_TRAD_SEQ = 1"

#    resultList = selectDic(sql)
#    val = resultList[0]['DEAL_AMT']
#    return val

def selectJMIG_DAY_SIML_TRAD(dicParam):
    sql = "SELECT STD_YMD, SIML_TRAD_SEQ, BUY_SELL_CL_CD, DEAL_CNT, DEAL_AMT" \
        " FROM JMIG_DAY_SIML_TRAD" \
        " WHERE PROD_ID = '" +  dicParam['PROD_ID'] + "'" \
        " AND CRNC_CD = '" +  dicParam['CRNC_CD'] + "'" \
        " AND PEFM_DTM = '" +  dicParam['PEFM_DTM'] + "'" \
        " AND PTN_ID = '" + dicParam['PTN_ID'] + "'"
#    return selectDic(sql)

def selectProdCtgrIdbyProdId(dicParam):
    sql = "SELECT PROD_CTGR_ID" \
        " FROM JMIG_PROD" \
        " WHERE PROD_ID = '" +  dicParam['PROD_ID'] + "'"

#    resultList = selectDic(sql)
#    val = resultList[0]['PROD_CTGR_ID']
#    return val

def selectCountCrwlProdID(dicParam):
    sql = "SELECT COUNT(*) CNT FROM JMIG_PROD P INNER JOIN JMIG_PROD_CTGR C2 " \
          "ON P.PROD_CTGR_ID = C2.PROD_CTGR_ID AND C2.UP_PROD_CTGR_ID = '" + dicParam['UP_PROD_CTGR_ID'] + "'" \
          "WHERE CRWL_PROD_ID = '" + dicParam['CRWL_PROD_ID'] + "'" \

#    resultList = selectDic(sql)
#    val = resultList[0]['CNT']
#    return val

def selectFuncByJOB_id2tup(JOB_ID):
    conn = repDBConnect()
    curs = conn.cursor()
    sql = "SELECT F.FUNC_ID FROM KADM_JOB J , KADM_JOB_ACT JA, KADM_ACT A, KADM_ACT_FUNC AF, KADM_FUNC F WHERE " \
          "J.JOB_ID = JA.JOB_ID AND JA.ACT_ID = A.ACT_ID AND A.ACT_ID = AF.ACT_ID AND AF.FUNC_ID = F.FUNC_ID AND " \
          "AF.USE_YN = 'Y' AND JA.USE_YN = 'Y' AND J.JOB_ID = %s ORDER BY JA.EXEC_SEQ ASC, AF.EXEC_SEQ ASC "
    curs.execute(sql, (JOB_ID))
    tup = curs.fetchall()
    conn.close()
    return tup

def selecMaxStdYmdFromDayProdPrc(dicParam):
    sql = "SELECT MAX(STD_YMD) MAX_STD_YMD " \
          "FROM JMIG_DAY_PROD_PRC WHERE PROD_ID IN " \
          "(SELECT PROD_ID FROM JMIG_PROD P INNER JOIN JMIG_PROD_CTGR PC ON P.PROD_CTGR_ID = PC.PROD_CTGR_ID WHERE PC.UP_PROD_CTGR_ID = '" + dicParam['UP_PROD_CTGR_ID'] +"')"

#    resultList = selectDic(sql)
#    val = resultList[0]['MAX_STD_YMD']
#    return val

def deleteJMIG_PROD_PRCStock(dicParam):
    sql = "DELETE FROM JMIG_DAY_PROD_PRC WHERE PROD_ID " \
          "IN (SELECT PROD_ID FROM JMIG_PROD P " \
          "INNER JOIN JMIG_PROD_CTGR PC " \
          "ON P.PROD_CTGR_ID = PC.PROD_CTGR_ID WHERE PC.UP_PROD_CTGR_ID = '" + dicParam['UP_PROD_CTGR_ID'] + "') " \
          "AND STD_YMD = '" + dicParam['STD_YMD'] + "'"

#    return B2B_COM_Data.Delete(sql)

def selectYmdSeqJMIG_DAY_PROD_PRC(dicParam):
    sql = "	SELECT IFNULL(" \
          " (SELECT " \
          "     (SELECT YMD_SEQ	" \
          "     FROM JMIG_DAY_PROD_PRC JDPP " \
          "     WHERE PROD_ID ='" + dicParam['PROD_ID'] + "'" \
          "     AND CRNC_CD = '" + dicParam['CRNC_CD'] + "'" \
          "     AND STD_YMD = (SELECT MAX(STD_YMD) FROM JMIG_DAY_PROD_PRC WHERE PROD_ID = '" + dicParam['PROD_ID'] +"' AND CRNC_CD = '"+ dicParam['CRNC_CD'] +"' AND YMD_SEQ IS NOT NULL)))" \
          ",1) YMD_SEQ"

#    resultList = selectDic(sql)
#    val = resultList[0]['YMD_SEQ']
#    return val

def updateYmdSeqJMIG_DAY_PROD_PRC(dicParam):
    sql = "UPDATE JMIG_DAY_PROD_PRC A " \
          "INNER JOIN (	SELECT (CASE @PROD_ID WHEN a.PROD_ID THEN @ROWNUM:=@ROWNUM+1 ELSE @ROWNUM :=1 END) rnum, 		   (@PROD_ID:=a.PROD_ID) PROD_ID, 		   a.CRNC_CD, 		   a.STD_YMD	" \
          "FROM JMIG_DAY_PROD_PRC a 		,(SELECT @ROWNUM := 0, @PROD_ID :='' FROM DUAL) b 	" \
          "WHERE a.PROD_ID = '" + dicParam['PROD_ID'] +"'     AND a.CRNC_CD = '" + dicParam['CRNC_CD'] +"' 	ORDER BY a.PROD_ID, a.CRNC_CD, a.STD_YMD ASC )B " \
          "ON A.PROD_ID = B.PROD_ID AND A.CRNC_CD = B.CRNC_CD AND A.STD_YMD = B.STD_YMD SET A.YMD_SEQ = B.rnum   , A.CHG_USER_ID = '" + dicParam['CHG_USER_ID'] +"'   , A.CHG_DTM = NOW() " \
          "WHERE A.PROD_ID ='" + dicParam['PROD_ID'] +"' AND A.CRNC_CD = '" + dicParam['CRNC_CD'] +"'"

#    return B2B_COM_Data.Update(sql)

def selectBuyCntPTNT000100002(dicParam):
    sql = "SELECT (SELECT YMD_SEQ 	FROM JMIG_DAY_PROD_PRC	WHERE PROD_ID = '" + dicParam['PROD_ID'] +"' AND CRNC_CD = '" + dicParam['CRNC_CD'] +"' AND STD_YMD = '" + dicParam['STD_YMD'] +"')  " \
          "- IFNULL((SELECT YMD_SEQ 	FROM JMIG_DAY_PROD_PRC	WHERE PROD_ID = '" + dicParam['PROD_ID'] +"'	AND CRNC_CD = '" + dicParam['CRNC_CD'] +"'	AND STD_YMD = (		SELECT MAX(STD_YMD) 		FROM JMIG_DAY_SIML_TRAD		WHERE PROD_ID = '" + dicParam['PROD_ID'] +"'		AND CRNC_CD = '" + dicParam['CRNC_CD'] +"'		AND PEFM_DTM = '" + dicParam['PEFM_DTM'] +"'		AND PTN_ID = '" + dicParam['PTN_ID'] +"'	))," \
          "(SELECT MIN(YMD_SEQ) - 1 FROM JMIG_DAY_PROD_PRC WHERE PROD_ID = '" + dicParam['PROD_ID'] +"' AND CRNC_CD = '" + dicParam['CRNC_CD'] +"' AND STD_YMD >= '" + dicParam['STD_OPEN_YMD'] +"')) CNT"

    resultList = selectDic(sql)
    val = resultList[0]['CNT']
#    return val

#일별상품분석 테이블 DELETE
def deleteJMIG_SNRO_PTNbySNRO_ID(dic):
    sql =  "DELETE FROM JMIG_SNRO_PTN " \
           "WHERE SNRO_ID = '" +  dic['SNRO_ID'] + "'" \

#    return B2B_COM_Data.Delete(sql)

#일별상품분석 테이블 INSERT
def InsertJMIG_SNRO_PTN(dic):
    sql = "INSERT INTO JMIG_SNRO_PTN (SNRO_ID, PTN_ID, REG_USER_ID, REG_DTM, CHG_USER_ID, CHG_DTM)" \
          "SELECT " + dic['SNRO_ID'] + " SNRO_ID ,PTN_ID  PTN_ID , " + dic['REG_USER_ID'] + " REG_USER_ID, NOW() REG_DTM,  " + dic['CHG_USER_ID'] + "  CHG_USER_ID, NOW() CHG_DTM  " \
          "FROM JMIG_PTN PTN WHERE PTN.DEL_YN = 'N'"

    conn = repDBConnect()
    curs = conn.cursor()

    try :
        curs.execute(sql)
    except pymysql.IntegrityError as err:  # 기존에 대지역 코드가 존재할 수 있음
        log("INSERT 중복 발생 : " + str(dic), "INFO")
    conn.commit()
    conn.close()

def selectPerformParamter(dic):
    sql = "SELECT PTN_ID, STD_OPEN_YMD, STD_END_YMD, PROD_ID, SPROD.CRNC_CD " \
          "FROM JMIG_SNRO_PTN SP " \
          "INNER JOIN JMIG_SNRO S ON SP.SNRO_ID = S.SNRO_ID " \
          "INNER JOIN JMIG_SNRO_PROD SPROD ON S.SNRO_ID = SPROD.SNRO_ID " \
          "WHERE SP.SNRO_ID = '" + dic['SNRO_ID'] + "'" \
          "AND SP.PTN_ID != 'T000100001'" \
          "ORDER BY (SELECT PTN_NM FROM JMIG_PTN P WHERE P.PTN_ID = SP.PTN_ID)"

#    return selectDic(sql)

def insertJMIG_PTN_SIML_PROD_EVAL(dicParam):

    sql = "INSERT INTO JMIG_PTN_SIML_PROD_EVAL (PTN_ID,PEFM_DTM,PROD_ID,CRNC_CD,REMN_CNT,PAL_AMT,PRFT_RATE,REG_USER_ID,REG_DTM,CHG_USER_ID,CHG_DTM,TOT_BUY_AMT,TOT_SELL_AMT,CMP_PTN_ID,INV_AMT)" \
        "SELECT PTN_ID, PEFM_DTM, PROD_ID, '" +  dicParam['CRNC_CD'] + "' CRNC_CD" \
        ", SUM(CASE WHEN BUY_SELL_CL_CD = 'S' THEN DEAL_CNT * -1 ELSE DEAL_CNT END)               REMN_CNT" \
        ", SUM(CASE WHEN BUY_SELL_CL_CD = 'S' THEN DEAL_AMT ELSE DEAL_AMT * -1 END)               PAL_AMT" \
        ", SUM(CASE WHEN BUY_SELL_CL_CD = 'S' THEN DEAL_AMT ELSE DEAL_AMT * -1 END)/(SELECT INV_AMT FROM JMIG_SNRO_PROD WHERE SNRO_ID = '" + dicParam['SNRO_ID'] + "' AND PROD_ID = '" + dicParam['PROD_ID'] + "')  PRFT_RATE	" \
        ", '" +  dicParam['REG_USER_ID'] + "' REG_USER_ID" \
        ", NOW() REG_DTM" \
        ", '" + dicParam['CHG_USER_ID'] + "' CHG_USER_ID" \
        ", NOW() CHG_DTM" \
        ", SUM(CASE WHEN BUY_SELL_CL_CD = 'B' THEN DEAL_AMT * DEAL_CNT END) TOT_BUY_AMT " \
        ", SUM(CASE WHEN BUY_SELL_CL_CD = 'S' THEN DEAL_AMT * DEAL_CNT END) TOT_SELL_AMT" \
        ", 'T000100003' CMP_PTN_ID" \
        ", (SELECT INV_AMT FROM JMIG_SNRO_PROD WHERE SNRO_ID = '" + dicParam['SNRO_ID'] + "' AND PROD_ID = '" + dicParam['PROD_ID'] + "') INV_AMT" \
        " FROM JMIG_DAY_SIML_TRAD" \
        " WHERE PTN_ID = '" + dicParam['PTN_ID'] + "'" \
        " AND PEFM_DTM = '" + dicParam['PEFM_DTM'] + "'" \
        " AND PROD_ID = '" + dicParam['PROD_ID'] + "'"

    conn = repDBConnect()
    curs = conn.cursor()

    try :
        curs.execute(sql)
    except pymysql.IntegrityError as err:  # 기존에 대지역 코드가 존재할 수 있음
        log("INSERT 중복 발생 : " + str(dicParam), "INFO")
    conn.commit()
    conn.close()

def updatePRFT_RATE_EVAL(dic):
    sql = "UPDATE JMIG_PTN_SIML_PROD_EVAL PSE " \
          "INNER JOIN JMIG_PTN_SIML PS ON PS.PTN_ID = PSE.PTN_ID AND PS.PEFM_DTM = PSE.PEFM_DTM AND PS.PROD_ID = PSE.PROD_ID AND PS.SNRO_ID = '" + dic['SNRO_ID'] + "' AND PS.SNRO_PEFM_DTM = '" + dic['SNRO_PEFM_DTM'] + "' " \
          "INNER JOIN JMIG_PTN_SIML_PROD_EVAL PSE2 ON PSE2.PTN_ID = PSE.CMP_PTN_ID AND PSE2.PROD_ID = PS.PROD_ID " \
          "INNER JOIN JMIG_PTN_SIML PS2 ON PS2.PTN_ID = PSE2.PTN_ID AND PS2.PEFM_DTM = PSE2.PEFM_DTM AND PS2.PROD_ID = PSE2.PROD_ID AND PS2.SNRO_ID = '" + dic['SNRO_ID'] + "' AND PS2.SNRO_PEFM_DTM = '" + dic['SNRO_PEFM_DTM'] + "' " \
          "SET PSE.BUY_RATE = PSE.TOT_BUY_AMT/PSE2.TOT_BUY_AMT , PSE.OVER_PRFT_RATE = 1-(PSE.TOT_BUY_AMT/PSE2.TOT_BUY_AMT) , " \
          "PSE.OVER_PRFT_AMT = (1-(PSE.TOT_BUY_AMT/PSE2.TOT_BUY_AMT))*(SELECT SP.INV_AMT FROM JMIG_SNRO_PROD SP WHERE SP.SNRO_ID = '" + dic['SNRO_ID'] + "' AND SP.PROD_ID = PSE.PROD_ID AND SP.CRNC_CD = PSE.CRNC_CD)," \
          "PSE.CHG_USER_ID = '" + dic['CHG_USER_ID'] + "' , PSE.CHG_DTM = NOW()"

    conn = repDBConnect()
    curs = conn.cursor()

    try :
        curs.execute(sql)
    except pymysql.IntegrityError as err:  # 기존에 대지역 코드가 존재할 수 있음
        log("INSERT 중복 발생 : " + str(dic), "INFO")
    conn.commit()
    conn.close()

def insertJMIG_SIM_TRADbyT000100003(dic):
    sql = ""
    sql = sql + "INSERT INTO jmig_day_siml_trad                                                                                                                                    "
    sql = sql + "SELECT DPP.PROD_ID PROD_ID                                                                                                                                        "
    sql = sql + "     , DPP.CRNC_CD CRNC_CD                                                                                                                                        "
    sql = sql + "     , DPP.STD_YMD STD_YMD                                                                                                                                        "
    sql = sql + "     , '" + dic['PEFM_DTM'] + "' PEFM_DTM                                                                                                                                            "
    sql = sql + "     , '" + dic['PTN_ID'] + "' PTN_ID                                                                                                                                              "
    sql = sql + "     , (DPP.YMD_SEQ - (SELECT MIN(YMD_SEQ) FROM JMIG_DAY_PROD_PRC WHERE PROD_ID = '" + dic['PROD_ID'] + "' AND CRNC_CD = '" + dic['CRNC_CD'] + "' AND STD_YMD >= '" + dic['STD_OPEN_YMD'] + "') + 1) SIML_TRAD_SEQ  "
    sql = sql + "     , 'B' BUY_SELL_CL_CD                                                                                                                                         "
    sql = sql + "     , 1 DEAL_CNT                                                                                                                                                 "
    sql = sql + "     , DPP.END_PRC DEAL_AMT                                                                                                                                       "
    sql = sql + "     , '1000000001' REG_USER_ID                                                                                                                                   "
    sql = sql + "     , NOW() REG_DTM                                                                                                                                              "
    sql = sql + "	 , '1000000001' CHG_USER_ID                                                                                                                                    "
    sql = sql + "     , NOW() CHG_DTM                                                                                                                                              "
    sql = sql + "FROM JMIG_DAY_PROD_PRC DPP                                                                                                                                        "
    sql = sql + "WHERE DPP.PROD_ID = '" + dic['PROD_ID'] + "'                                                                                                                                  "
    sql = sql + "AND DPP.CRNC_CD = 'KRW'                                                                                                                                           "
    sql = sql + "AND DPP.STD_YMD BETWEEN '" + dic['STD_OPEN_YMD'] + "' AND '" + dic['STD_END_YMD'] + "'                                                                                                                 "

    conn = repDBConnect()
    curs = conn.cursor()

    try :
        curs.execute(sql)
    except pymysql.IntegrityError as err:  # 기존에 대지역 코드가 존재할 수 있음
        log("INSERT 중복 발생 : " + str(dic), "INFO")
    conn.commit()
    conn.close()
