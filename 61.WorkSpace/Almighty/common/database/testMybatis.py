import mybatis_mapper2sql
# Parse Mybatis Mapper XML files
mapper, xml_raw_text = mybatis_mapper2sql.create_mapper(xml='database.xml')
# Get All SQL Statements from Mapper
statement = mybatis_mapper2sql.get_statement(mapper)
# Get SQL Statement By SQLId
statement = mybatis_mapper2sql.get_child_statement(mapper, 'sometable')
print(statement)

#전체 sql 출력
statement = mybatis_mapper2sql.get_statement(mapper, result_type='raw', reindent=True, strip_comments=True)
print(statement)

print("====================================================================")

statement = mybatis_mapper2sql.get_child_statement(mapper,'testForeach', reindent=True, strip_comments=False)
print(statement)
print("====================================================================")