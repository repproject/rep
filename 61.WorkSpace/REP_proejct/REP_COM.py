#import REP_TLGR_MSG

def tuple2Str(tuple):
    return "%s" % tuple

def log(Message, Level): #ERROR INFO Debug
    try:
        if Level == "ERROR":
           print(str(Message))
           #REP_TLGR_MSG.sendMessage(str(Message))
    except Exception as e:
        print("텔레그램 Exception 발생")
    print(Message)
