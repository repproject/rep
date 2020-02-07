from idna import unicode

import REP_JOB
import telegram
import REP_TLGR_MSG
my_token = '495069941:AAHXf-j_f97clXuEI5P0lpnbyPKcUfmVtYs'
chat_id = 436714227
import mybatis_mapper2sql

def main():
    bot = telegram.Bot(token=my_token)  # bot을 선언합니다.
    getMessage(bot)
    #bot.sendMessage(chat_id=chat_id, text="저는 봇입니다.")
    #bot.sendMessage(chat_id=chat_id, text="저는 봇입니다.")

def getMessage(bot):
    updates = bot.getUpdates()  # 업데이트 내역을 받아옵니다.
    for u in updates:  # 내역중 메세지를 출력합니다.
        print(u.message)



def sms_msg_cut(str, dstlen):
# 2017.11. 9 - LSH
# dstlen 길이로 나누어 list 에 담는다.
    text = ""
    strlist = []
    for s in unicode(str) :
        try :
            stemp = text + s
            strlen = len ( stemp.decode('utf-8').encode('euc-kr') )
            if strlen > dstlen :
                strlist.append(text)
                text = s
            else :
                text = stemp
        except :
            continue

    # 마지막 김밥 꼬다리 저장.
    strlist.append (text)
    return strlist




if __name__== '__main__':
    # batchContext = BatchContext()
    # LogFunction_TEST(logger,1,"TEST","Name")
    str = ""
    for i in range(1,4097):
        str = str + "박지일"

    print(str[0:5])






    for l in list:
        print(l)



    #main()
    #getMessage()
    #REP_TLGR_MSG.sendMessage("TEST")

#https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html
#박지일id : 436714227