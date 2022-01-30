from apscheduler.schedulers.background import BackgroundScheduler
from Server.ADM import *

def doSchedule():    #JOB수행
    sched = BackgroundScheduler()
    r = getJobSchd()
    print(r)

if __name__ == '__main__':
    doSchedule()
