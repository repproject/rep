from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine("mysql+pymysql://repwas:0(repwas)@rep.iptime.org/rep", echo=True, future=True)  # 엔진생성
s = Session(engine)

def getEngine():  # 엔진생성
    return engine

def createSessionmaker(): #sessionmaker
    session = sessionmaker(engine)
    return session

def createSession(): #session
    session = Session(engine)
    return session

def createConnection(): #connect
    return getEngine().connect()

def begin():
    try:
        s.begin()
    except Exception as e :
        print(e)






#with engine.connect() as conn:
    # result = conn.execute(text("select 'hello world'"))
    # print(result.all())
    #
    # result = conn.execute(text("select * from kmig_nv_cmpx where nv_cmpx_id < 10"))
    # for row in result:
    #     print(row)

# if __name__ == "__main__":
#     print(engine.url)
