def getDicFromListTable(lt):
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

