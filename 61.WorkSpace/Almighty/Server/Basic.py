from common.database.repSqlAlchemy import *

def merge(table):
    try:
        s.merge(table)
        print(table)
        s.commit()
    except Exception as e :
        print("Basic Except : " + e)
        return False