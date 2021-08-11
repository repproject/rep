from DAO.KALL import *

def getDicFromListTable(lt):
    r"""
        Table 객체(리스트)를 Dictionary 타입으로 변경한다
        중복된 컬럼명은 먼저 선언된 테이블이 우선한다.
    :param lt:
    :return:
    """
    listRslt = []

    try:
        len(lt)
    except TypeError as te:
        lt = [lt]

    for rslt in lt:
        dicRslt = {}
        if str(type(rslt)) != "<class 'sqlalchemy.engine.row.Row'>":
            rslt = [rslt]
        for i, tb in enumerate(rslt):
            for col in tb.__table__.c:
                colName = str(col).split('.')[1]
                if colName not in dicRslt.keys():
                    dicRslt[colName] = getattr(tb,colName)
        listRslt.append(dicRslt)
    return listRslt


def getListTableFromDic(dic):
    r"""
        [테이블][컬럼] 형태의 dictionary를 Table 객체로 바꾸어 Return 한다.
        여러개의 테이블을 수용가능하다.
        테이블클래스가 생성되어 있지 않으면 NameError 가 발생
    :param dic:
    :return:
    """
    listTable = []

    for key in dic:
        kwargs = {**dic[key]}
        strExec = key + "(**kwargs)"
        listTable.append(eval(strExec))
    return listTable