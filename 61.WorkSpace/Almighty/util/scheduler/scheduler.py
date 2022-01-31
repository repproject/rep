from apscheduler.schedulers.background import BackgroundScheduler
from Server.ADM import *
from common.Batch.Basic import *
from common.Batch.doJob import *

# Cron 방식 - Cron 표현식으로 Python code 를 수행
# Date 방식 - 특정 날짜에 Python code 를 수행
# Interval 방식 - 일정 주기로 Python code 를 수행

def doSchedule():    #JOB수행
    sched = BackgroundScheduler()
    listJobExec = getJobSchd()
    print(listJobExec)
    for jobExec in listJobExec:

        #값 -> 변수로 세팅 숫자는 Integer로 변환
        jobId = jobExec[1].job_id               #Job Id
        jobSeq = jobExec[1].job_seq             #Job Seq
        execPerdCd = jobExec[1].exec_perd_cd    #실행주기 CYCL:cycle, DAY:요일, DD:일, HH:24, MM:월
        if isNotNull(jobExec[1].exec_mm): execMM = int(jobExec[1].exec_mm)             #실행월
        else: execMM = None
        if isNotNull(jobExec[1].exec_mm): execDD = int(jobExec[1].exec_dd)             #실행일
        else: execDD = None  # 실행월
        if isNotNull(jobExec[1].exec_hh): execHH = int(jobExec[1].exec_hh)             #실행시
        else: execHH = None
        if isNotNull(jobExec[1].exec_mi): execMI = int(jobExec[1].exec_mi)             #실행분
        else: execMI = None
        execDayCd = jobExec[1].exec_day_cd      #실행요일
        if isNotNull(jobExec[1].cycl_mi): cyclMi = int(jobExec[1].cycl_mi)             #반복분
        else: cyclMi = None
        imdiExecYn = jobExec[1].imdi_exec_yn    #즉시실행여부
        jobNm = jobExec[0].job_nm               #Job명

        if execPerdCd == 'DAY' or execPerdCd == 'DD' or execPerdCd == 'HH' or execPerdCd == 'MM': #주기작업(요일,월,일,시간)의 경우
            if execPerdCd == 'DD':
                sched.add_job(doJob, 'cron', month='*',day='*',hour=execHH, minute=execMI, second=1,day_of_week = '*', id=jobId, args=[jobId])

    sched.start()

    while True:
        print("Running...")
        time.sleep(1)

def test():
    sendTelegramMessage('hi')

if __name__ == '__main__':
    #test()
    doSchedule()
