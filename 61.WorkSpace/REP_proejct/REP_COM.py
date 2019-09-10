#import REP_TLGR_MSG

userid = 1000000001

def tuple2Str(tuple):
    return "%s" % tuple

def log(Message, Level): #ERROR INFO Debug
    try:
        if Level == "E":
           Message = "[E]" + Message
           print(str(Message))
           #REP_TLGR_MSG.sendMessage(str(Message))
        elif Level == "D":
            Message = "[D]" + Message
            print(str(Message))
        elif Level == "I":
            Message = "[I]" + Message
            print(str(Message))
    except Exception as e:
        print("텔레그램 Exception 발생")
