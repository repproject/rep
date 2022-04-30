from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import *
from sqlalchemy.orm import *
import logging
from datetime import date, timedelta, datetime

sqla_logger = logging.getLogger('sqlalchemy')
sqla_logger.propagate = False
sqla_logger.setLevel(level=logging.ERROR)

# active_db_url = 'mysql+pymysql://repwas:0(repwas)@rep.iptime.org/rep'
# db_log_file_name = 'db.log'
# db_handler = logging.FileHandler(db_log_file_name)
# db_handler.setLevel(logging.ERROR)
# sqla_logger.addHandler(db_handler)
engine = create_engine("mysql+pymysql://repwas:0(repwas)@rep.iptime.org/rep", echo=False, future=True, convert_unicode = True)  # 엔진생성 #echo = print SQL
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
