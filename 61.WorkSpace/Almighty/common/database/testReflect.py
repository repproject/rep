from sqlalchemy import *
from sqlalchemy.orm import*
from common.database.repSqlAlchemy import *
import pandas as pd
from pandas.io import sql

# meta = MetaData()
# meta.reflect(bind=engine)
#kmig_kb_regn = meta.tables['kmig_kb_regn'] #테이블참조방법
#engine = create_engine("mysql+pymysql://repwas:0(repwas)@rep.iptime.org/rep", echo=True, future=True)  # 엔진생성

def getTable(tableName):
    print('getTable')
    print(engine)
    return meta.tables[tableName]

def makeMeta():
    meta = MetaData()
    meta.reflect(bind=engine)
    return meta

def makeEngine():
    engine = create_engine("mysql+pymysql://repwas:0(repwas)@rep.iptime.org/rep", echo=True, future=True)  # 엔진생성
    return engine

def getTable(tableName):
    meta = makeMeta()
    return Table(tableName,meta)



if __name__ == "__main__":
    print("_".join([]))

    meta = makeMeta()
    tableName = 'kadm_tbl_col'
    className = 'ComCdDtl'
    tbl = meta.tables.get(tableName)

    #속성값 출력
    for col in tbl._columns:
        print("#################" + col.name + "#######################")
        print(col.server_default)
        if col.server_default != None :
            print(col.server_default.arg.text)

        # df = col.server_default
        # for attr in df.__dir__():
        #     try:
        #         print(attr + " : " + str(getattr(col,attr)))
        #     except: pass

        # for attr in col.__dir__():
        #     print(attr + " : " + str(getattr(col,attr)))
            #print(col.attr)
        #print(col.name.lower() + " = KColumn(")
        #print(col.type)

    #print(tbl.)
    #print(tbl)
    # print(getClassTable(meta,className,tableName))

    # engine = makeEngine()
    # Session = sessionmaker(bind=engine)
    # session = Session()

    #menu = relationship("kadm_menu")

    # print(meta.tables)
    # menu = meta.tables.get('kadm_menu')
    # print(menu.__getattribute__())

    #menu = Table('kadm_menu',meta)
    #print(menu)
    #print(menu.get_children)

    #print(tbl.__dir__())
    #print(tbl._columns)
    #print(tbl.exported_columns)

    # dic = {'a':'b'}
    # print(dic)
    # print(dic['a'])

    #print(meta.tables['kadm_menu'])
    #menu = meta.table['kadm_menu']
    # menu = meta.tables['kadm_menu']
    # print(meta)
    # print('test')
    # print(menu)
    #
    # result = session.query(menu).filter(menu.menu_lv.match(1))
    # print(result)
    #










