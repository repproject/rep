from DAO.KADM import *

def getCol(strTblNm,strColNm):
    return s.query(TblCol).filter_by(tbl_nm=strTblNm).filter_by(col_nm=strColNm).first()
