from sqlalchemy import *
from common.database.testReflect import *
from common.database.repSqlAlchemy import *

#select 기본
kmig_kb_regn = getTable('kmig_kb_regn')
print(kmig_kb_regn)
s = select (kmig_kb_regn)
conn = createConnection()

result = conn.execute(s)
for row in result:
    print(row)


#select 조건
s2 = select(kmig_kb_regn)
