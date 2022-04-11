# #import B2B_MIG_BTC
# import B2B_MIG_Stock
# import B2B_TLGR
# import B2B_JOB
# import pymysql
# import B2B_COM
# import B2B_SIML
# import B2B_COM_Data
# import sys

from Server.ADM import *
import common.Batch.Crawling
from common.Batch.Basic import *

userid = '1000000001'

# def main():
#     #B2B_JOB.doJOB(sys.argv)
#     #B2B_SIML.simulTest()
#
#     # try:
#     #     B2B_MIG_Stock.migStockDayPrice();
#     # except Exception as err:
#     #     B2B_COM.log(err,"ERROR")

def do(job_id):
    """
    Job을 실행하는 함수이다.
    :param job_id:
    :return:
    """

    blog.info("Do Job Start : " + job_id)
    listFunc = getJobFuncAct(job_id)

    if len(listFunc) == 0:  #Function이 등록되지 않은 경우
        logMessage = "Function is not registerd in job : " + job_id
        blog.error(logMessage)
        sendTelegramMessage(logMessage)
        return False

    blog.info("Function of Job List is...")
    blog.info(listFunc)

    for Func in listFunc:
        function = Func[4]
        job = Func[0]

        if function.func_cl_cd == 'CRWL':
            batchContext = simpleBatchContext("[" + job.job_id + "][" + job.job_nm + "][" + function.func_id + "][" + function.func_nm +"][" + function.func_cl_cd + "]")
            CrawlObject =  common.Batch.Crawling.Crawling(function.src_func_nm, function.ref1, batchContext)
            CrawlObject.run()

#첫 수행 문장
if __name__ == '__main__':
    blog.info("START JOB doJOB main...")
    #blog.info("parameter : " + *args)
    #doJob('BBMG001')
    #main()