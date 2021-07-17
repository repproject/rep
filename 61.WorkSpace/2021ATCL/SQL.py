import DB

#TableDic으로 INSERT문을 만들어 넣는다.(단문)
def insertBasicByTBLDic(tableName,dicTBL,conn=None,curs=None):
    # DBConnection
    isConn = 1

    if curs == None:
        conn = DB.repDBConnect()
        curs = conn.cursor()
        isConn = 0

    sql = makeSQLBasicByTBLDic(tableName,dicTBL)

    curs.execute(sql)
    if isConn == 0:
        conn.commit()
        conn.close()

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
    sql = sql[:-1]+")"
    #sql += "'" + str(dicTBL['REG_USER_ID']) + "'" + ",NOW(),"+"'"+str(dicTBL['CHG_USER_ID'])+"'"+",NOW())"
    return sql