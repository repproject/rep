from common.database.repSqlAlchemy import *
from Server.module import getCol
from Server.module import getTbl
import traceback

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
        classDeclare += "    __tablename__ = '" + tableName.lower() + "'\n\n"

        colInitDeclare = ""
        relDeclare = ""
        dicRelDeclare = {}
        colReprBindStr = ""
        colReprParameter = ""

        for col in tbl._columns:
            if col.name != 'REG_USER_ID' and col.name != 'REG_DTM' and col.name != 'CHG_USER_ID' and col.name != 'CHG_DTM':
                colReprParameter += "str(self." + col.name.lower() + "), "
                colDeclare = "    " + col.name.lower() + " = KColumn("
                colTypeStr = str(col.type)
                TblCol = getCol(tableName,col.name.lower())
                if TblCol != None : #컬럼값이 저장되어 있지 않은 Case를 가정 필요
                    ParentTbl = getTbl(TblCol.pant_tbl_nm)
                    if ParentTbl != None:
                        ParentClassNm = ParentTbl.cls_nm

                if colTypeStr[:7] == "DECIMAL":
                    colType2 = colTypeStr.split("(")[1]
                    colType3 = colType2.split(",")[1]
                    colType3 = colType3.replace(" ","").replace(")", "")
                    if int(colType3) > 0 : colTypeStr = "Float"
                    else : colTypeStr = "Integer"
                    coltypeDeclare = colTypeStr
                else:
                    coltypeDeclare = colTypeStr.replace("VARCHAR", "String")
                colDeclare += coltypeDeclare
                if col.primary_key:
                    colDeclare += ", primary_key = True"
                if col.nullable:
                    colDeclare += ", nullable = True"
                else : colDeclare += ", nullable = False"

                dicColRelDeclare = {}
                if TblCol != None:
                    if len(TblCol.pant_tbl_nm) > 0 and len(TblCol.pant_col_nm) > 0:
                        if TblCol.pant_tbl_nm not in dicRelDeclare.keys(): dicRelDeclare[TblCol.pant_tbl_nm] = {}
                        dicRelDeclare[TblCol.pant_tbl_nm][col.name.lower()] = TblCol.col_nm
                        dicRelDeclare[TblCol.pant_tbl_nm]['ParentClassNm'] = ParentClassNm

                #col.server_default.arg.text
                #if col.server_default != None:
                #    colDeclare += ", server_default = True"

                if TblCol != None :
                    if TblCol.col_doma_cd == 'CD':
                        colDeclare += ", kcom_cd_domain = True, kcom_cd_grp = '"
                        colDeclare += TblCol.col_doma_val
                        colDeclare += "'"
                classDeclare += colDeclare + ")\n"
                colInitDeclare += "        self." + col.name.lower() + " =  kwargs.pop('" + col.name.lower() + "'"

                if TblCol != None :
                    if len(TblCol.bas_val) > 0:
                        colInitDeclare += ",'" + TblCol.bas_val + "'"
                    else:
                        if col.nullable == True:
                            colInitDeclare += ",''"
                colInitDeclare += ")\n"

                colReprBindStr += "'%s', "

        ##############컬럼별 세팅 완료#################

        for keydRD in dicRelDeclare:
            relTableDeclare = "    " + dicRelDeclare[keydRD]['ParentClassNm'].lower() + " = relationship('" + dicRelDeclare[keydRD]['ParentClassNm'] + "',primaryjoin = "
            i = 0 #컬럼용 iterator
            if len(dicRelDeclare[keydRD]) > 2 :
                relTableDeclare += "and_("
            for keydRDcol in dicRelDeclare[keydRD]:
                if keydRDcol != 'ParentClassNm':
                    if i > 0: relTableDeclare += " , "
                    relTableDeclare += keydRDcol.lower() + "==" + dicRelDeclare[keydRD]['ParentClassNm'] + "." + dicRelDeclare[keydRD][keydRDcol]
                    i += 1
            if len(dicRelDeclare[keydRD]) > 2:  relTableDeclare += ")"
            relTableDeclare += ", foreign_keys = ["
            i = 0
            for  keydRDcol in dicRelDeclare[keydRD]:
                if keydRDcol != 'ParentClassNm':
                    if i > 0: relTableDeclare += " , "
                    relTableDeclare += dicRelDeclare[keydRD]['ParentClassNm'] + "." +dicRelDeclare[keydRD][keydRDcol]
                    i += 1
            relTableDeclare += "])\n"
            relDeclare += relTableDeclare

#        relDeclare += "    " + ParentClassNm.lower() + " = relationship('" + ParentClassNm + "',primaryjoin = " \
#                      + col.name.lower() + " == " + ParentClassNm + "." + TblCol.col_nm + ", foreign_keys=" \
#                      + ParentClassNm + "." + TblCol.col_nm + ")\n"

        #classDeclare += "    codeList = {}\n\n"
        classDeclare += "\n"
        classDeclare += relDeclare + "\n"
        classDeclare += "    def __init__(self, *args, **kwargs):\n"
        classDeclare += "        KTable.__init__(self)\n"
        classDeclare += colInitDeclare + "\n"
        classDeclare += "    def __repr__(self):\n"
        classDeclare += "        return \"<" + className + "(" + colReprBindStr[:-2] + "\" % (" + colReprParameter[
                                                                                                  :-2] + " + KTable.__repr__(self))\n"
    except :
        logging.error(traceback.format_exc())
        return False
    return classDeclare