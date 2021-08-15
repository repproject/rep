import Server.COM

def doJob():
    JobSchedule = Server.COM.getJobSchd()
    print(JobSchedule)

if __name__ == '__main__':
    doJob()