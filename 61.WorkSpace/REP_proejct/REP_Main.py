import REP_JOB
#import REP_TLGR_MSG
import REP_COM


userid = 1000000001            #추후 사용하기 위해 만든

def main():

#    REP_TLGR_MSG.checkMessage() #Telegram 메시지 확인 - Bot으로부터 온 메시지를 확인.

    #JOB수행
    REP_JOB.doJOB('NVIN001')

if __name__ == '__main__':
    #try:
        main()
    # except Exception as e:
    #     REP_COM.log("ERROR " + str(e),"ERROR")
