from common.database.repSqlAlchemy import *

def makeMeta():
    meta = MetaData()
    meta.reflect(bind=engine)
    return meta

def getClassTable(meta,className,tableName):
    try:
        tbl = Table(tableName.lower(), meta)

        #Table 없는 경우
        if len(tbl._columns) == 0:
            return "Table Not Found!!"

        classDeclare = "class " + className + "(Base,KTable):\n"
        classDeclare += "    __tablename__ = '" + tableName.upper() + "'\n\n"

        colInitDeclare = ""
        colReprBindStr = ""
        colReprParameter = ""
        for col in tbl._columns:
            if col.name != 'REG_USER_ID' and col.name != 'REG_DTM' and col.name != 'CHG_USER_ID' and col.name != 'CHG_DTM':
                colReprParameter += "str(self." + col.name.lower() + "), "
                colDeclare = "    " + col.name.lower() + " = KColumn("
                colTypeStr = str(col.type)
                print(col.name + colTypeStr)
                if colTypeStr[:7] == "DECIMAL":
                    colTypeStr = "Integer"
                    coltypeDeclare = colTypeStr
                else:
                    coltypeDeclare = colTypeStr.replace("VARCHAR", "String")
                colDeclare += coltypeDeclare
                if col.primary_key:
                    colDeclare += ", primary_key = True"
                if col.nullable:
                    colDeclare += ", nullable = True"
                else : colDeclare += ", nullable = False"
                classDeclare += colDeclare + ")\n"
                colInitDeclare += "        self." + col.name.lower() + " =  kwargs.pop('" + col.name.lower()

                if col.nullable == True:
                    colInitDeclare += "','"
                colInitDeclare += "')\n"

                colReprBindStr += "'%s', "

        #classDeclare += "    codeList = {}\n\n"
        classDeclare += "\n"
        classDeclare += "    def __init__(self, *args, **kwargs):\n"
        classDeclare += "        KTable.__init__(self)\n"
        classDeclare += colInitDeclare + "\n"
        classDeclare += "    def __repr__(self):\n"
        classDeclare += "        return \"<" + className + "(" + colReprBindStr[:-2] + "\" % (" + colReprParameter[
                                                                                                  :-2] + " + KTable.__repr__(self))\n"
    except Exception as e:
        print(e)
        return False
    return classDeclare