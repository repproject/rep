import DB
import pandas as pd
import SQL
#import csv

input_file = 'D:/NaverCloud/R/2021_ATCL\TCL/6394.csv'
input_file_header = 'D:/NaverCloud/R/2021_ATCL/Data_Log/'
input_file_tail = 'csv'

if __name__ == "__main__":


    for i in range(6442,6493):
        input_file = input_file_header + str(i) + '.' + input_file_tail
        conn = DB.repDBConnect()
        curs = conn.cursor()

        with open(input_file) as data:
            lines = data.readlines()
            for line in lines[1:]:  #header 제거
                value = line.split('|')
                dicAtclLog = {'LOG_SER_NUM': value[0], 'ERR_OCCR_DTM': value[1],
                                'AUDIT_DTM': value[2], 'GLOB_ID': value[3],
                                'USER_ID': value[4], 'LOGIN_ID' : value[5],
                                'ERR_MSG_OCCR_CTT' : value[6]
                            }

                SQL.insertBasicByTBLDic('ATCL_LOG',dicAtclLog,conn,curs)

        conn.commit()
        conn.close()


