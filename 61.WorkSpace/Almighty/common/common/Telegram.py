import telegram
from telegram.ext import Updater, MessageHandler, Filters

import REP_DAO
import REP_COM
import time
my_token = '1983139538:AAELJcik78Ipp_-C3iFs7LXq_lgk-NK4Hfg' #JBoozleBot
#my_token2 = '1074073870:AAFnhfEFR9vYBMOUU666jE0Iy5RqdQON4Ew' #JMaskBot
#chat_id = 436714227

def checkMessage(bot):

    LogObejct = REP_COM.Logger("TELEGRAM")
    Log = LogObejct.logger
    Log.info("start telegram bot")

    while True :
        try:
            updates = bot.getUpdates(offset=1000,limit = 1000, timeout=10)  # 업데이트 내역을 받아옵니다.
            for u in updates:  # 내역중 메세지를 출력합니다.
                Log.info("Updating...")
                print(u.message)
                dicTlgrMsg = {'TLGR_MSG_ID': u.message.message_id, 'TLGR_MSG_CNTS': str(u)}
                try:
                    rtn = REP_DAO.INSERT_KADM_TLGR_MSG(dicTlgrMsg)
                except Exception as err:
                    rtn = '0'
                    Log.error("[텔레그램 Message Insert ERROR 발생]" + str(err))
                    #sendMessage2("[텔레그램 ERROR 발생]" + str(err), 436714227)

                if rtn == '100':   #INSERT가 정상일때
                    Log.info("신규메세지 : " + str(dicTlgrMsg))
                    #if u.message.text[0] == '-': #정의된명령어
                    splitMessage = u.message.text.split(' ')
                    if splitMessage[0][1:] == "등록"  or splitMessage[0][0:] == "등록":
                        print("####################")
                        print(u.message.chat.last_name)
                        if u.message.chat.last_name == None:
                            name = u.message.chat.first_name
                        else:
                            name = u.message.chat.last_name + u.message.chat.first_name
                        dicTlgrUser= {'TLGR_USER_ID': u.message.chat.id, 'TLGR_USER_NM': name,  'RCV_TGT_YN' : 'Y', 'SEND_CL_CD' : 'M'}
                        Log.info("[텔레그램 신규 사용자 등록" + str(dicTlgrUser))
                        if(REP_DAO.INSERT_KADM_TLGR_USER(dicTlgrUser) == '100'):
                            sendMessage2("[텔레그램 사용자등록 완료] " + str(dicTlgrUser),436714227)
                            sendMessage2("[텔레그램 사용자등록 완료] " + str(dicTlgrUser),int(u.message.chat.id))
                            print("[텔레그램 사용자등록 완료] " + str(u.message.chat.id) + " " + dicTlgrUser['TLGR_USER_NM'])
                        else:
                            print("[텔레그램 사용자등록 실패] " + str(u.message.chat.id) + " " + dicTlgrUser['TLGR_USER_NM'])
                            sendMessage2("[텔레그램 사용자등록 실패] " + str(dicTlgrUser), int(u.message.chat.id))
                    elif splitMessage[0][1:] == "수신해제":
                        print("[텔레그램 수신해제]" + str(u.message.chat.id))
                        dicTlgrUser = {'TLGR_USER_ID': u.message.chat.id, 'RCV_TGT_YN': 'N'}
                        if(REP_DAO.UPDATE_KADM_TLGR_USER_RCV_TGT_YN(dicTlgrUser) == '100'):
                            sendMessage2("[텔레그램 수신해제 완료] " + str(dicTlgrUser),436714227)
                            sendMessage2("[텔레그램 수신해제 완료] " + str(dicTlgrUser),int(u.message.chat.id))
                            print("[텔레그램 수신해제 완료] " + str(u.message.chat.id) + " " + dicTlgrUser['TLGR_USER_NM'])
                        else:
                            print("[텔레그램 수신해제 실패] " + str(u.message.chat.id) + " " + dicTlgrUser['TLGR_USER_NM'])
                            sendMessage2("[텔레그램 수신해제 실패] " + str(dicTlgrUser), int(u.message.chat.id))
                    elif splitMessage[0][1:] == "수신등록":
                        print("[텔레그램 수신등록]", u.message.chat.id)
                        dicTlgrUser = {'TLGR_USER_ID': u.message.chat.id, 'RCV_TGT_YN': 'Y'}
                        if(REP_DAO.UPDATE_KADM_TLGR_USER_RCV_TGT_YN(dicTlgrUser) == '100'):
                            sendMessage2("[텔레그램 수신등록 완료] " + str(dicTlgrUser),436714227)
                            sendMessage2("[텔레그램 수신등록 완료] " + str(dicTlgrUser),int(u.message.chat.id))
                            print("[텔레그램 수신등록 완료] " + str(u.message.chat.id) + " " + str(dicTlgrUser))
                        else:
                            print("[텔레그램 수신등록 실패] " + str(u.message.chat.id) + " " + str(dicTlgrUser))
                            sendMessage2("[텔레그램 수신등록 실패] " + str(dicTlgrUser),int(u.message.chat.id))
                    elif splitMessage[0][1:] == "?" or splitMessage[0][1:] == "사용문의" or splitMessage[0][1:] == "start":
                        print("[텔레그램 사용문의]", u.message.chat.id)
                        sendMessage2("-등록 : 최초등록 \n-수신등록 : 수신여부Y \n-수신해제 : 수신여부N\n채널들어와서\n ☞-등록 이라고 입력하면됩니다", u.message.chat.id)
                else:
                    Log.debug("중복")
                splitMessage = None
            time.sleep(0.5)
        except Exception as err:
             Log.error("[텔레그램 ERROR 발생]" + str(err))
             sendMessage2("[텔레그램 ERROR 발생]" + str(err),436714227)

def sendTelegramMessage(str,token = my_token, id = None):
    #LogObejct = REP_COM.Logger("TELEGRAM")
    #Log = LogObejct.logger
    listStr = splitStringSize(str,1000)
    bot = telegram.Bot(token=token)  # bot을 선언합니다.
    if token == my_token:
        dicTlgrUserIdList = REP_DAO.fetch("selectKADM_TLGR_RCV_USER_Boozle", "")  # 사용자 조회
    # elif token == my_token2:
    #     dicTlgrUserIdList = REP_DAO.fetch("selectKADM_TLGR_RCV_USER","") #사용자 조회

    if id == None:
        for dicTlgrUserId in dicTlgrUserIdList:
            str_chatid = dicTlgrUserId['TLGR_USER_ID']
            try:
                for str in listStr:
                    bot.sendMessage(chat_id=int(str_chatid), text=str)
            except Exception as e:
                #Str 너무 긴 경우 수정 필요
                #logging.error("Telegram sendMessage Exception 발생 " + str(e))
                pass
    else:
        for str in listStr:
            bot.sendMessage(chat_id=int(id), text=str)

def splitStringSize(str,size):
    startIndex = 0
    list = []
    while True:
        if len(str) < startIndex + size:
            list.append(str[startIndex:])
            break
        else:
            list.append(str[startIndex:startIndex+size])
            startIndex = startIndex + size
    return list


def sendMessage2(str,id=None):
    if id == None:
        sendMessage(str,my_token2)
    else:
        sendMessage(str, my_token2, id)

def runBot():
    bot = telegram.Bot(token=my_token2)  # bot을 선언합니다.
    checkMessage(bot)


def get_message(bot,update):
    pass
    #update.message.reply_text("Test입니다")
    #update.message.reply_text(update.message.text)


def Test():

    updater = Updater(my_token2)

    message_handler = MessageHandler(Filters.text, get_message)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling(timeout=3, clean=True)
    #updater.idle()


#436714227
if __name__ == '__main__':
    bot = telegram.Bot(token=my_token)
    #bot.sendMessage(436714227,'테스트')
    #bot.send_message(436714227,'테스트')
    #sendTelegramMessage('테스트')
    #Test()
    #runBot()


#https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html
#박지일id : 436714227
#{'new_chat_members': [], 'delete_chat_photo': False,
# 'group_chat_created': False,
# 'from': {'language_code': 'ko', 'id': 436714227, 'first_name': '케빈', 'is_bot': False, 'last_name': 'Brown'},
# 'channel_chat_created': False, 'new_chat_photo': [], 'photo': [], 'new_chat_member': None, 'message_id': 2, 'date': 1514088448, 'caption_entities': [], 'entities': [], 'supergroup_chat_created': False,
# 'chat': {'id': 436714227, 'type': 'private', 'last_name': 'Brown', 'first_name': '케빈'}, 'text': 'Rrrr'}