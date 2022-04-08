import telegram
from telegram.ext import Updater, MessageHandler, Filters
from Server.ADM import *

#import REP_DAO
#import REP_COM
import time
my_token = '1983139538:AAELJcik78Ipp_-C3iFs7LXq_lgk-NK4Hfg' #JBoozleBot
#my_token2 = '1074073870:AAFnhfEFR9vYBMOUU666jE0Iy5RqdQON4Ew' #JMaskBot
#chat_id = 436714227

def sendTelegramMessage(str,token = my_token, id = None):
    #LogObejct = REP_COM.Logger("TELEGRAM")
    #Log = LogObejct.logger
    listStr = splitStringSize(str,1000)
    bot = telegram.Bot(token=token)  # bot을 선언합니다.
    if token == my_token:
        UserList = getRcvUserList()
        for user in UserList:
            str_chatid = user.tlgr_user_id
            try:
                for str in listStr:
                    bot.sendMessage(chat_id=int(str_chatid), text=str)
            except Exception as e:
                #Str 너무 긴 경우 수정 필요
                #logging.error("Telegram sendMessage Exception 발생 " + str(e))
                pass

def splitStringSize(str,size):
    """
    Telegram Size 제한으로 인하여
    1000 byte씩 잘라서 송신
    :param str: 커팅 전 발송 메세지 내용
    :param size: 커팅 사이즈
    :return: 커팅된 String List
    """
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

#삭제 처리(Fade Out 중)
#def sendMessage2(str,id=None):
#    if id == None:
#        sendMessage(str,my_token2)
#    else:
#        sendMessage(str, my_token2, id)

#def runBot():
#    bot = telegram.Bot(token=my_token2)  # bot을 선언합니다.
#    checkMessage(bot)


#def get_message(bot,update):
#    pass
#update.message.reply_text("Test입니다")
#update.message.reply_text(update.message.text)

#def Test():
#    updater = Updater(my_token2)

#    message_handler = MessageHandler(Filters.text, get_message)
#    updater.dispatcher.add_handler(message_handler)

#    updater.start_polling(timeout=3, clean=True)
    #updater.idle()

#436714227
if __name__ == '__main__':
    sendTelegramMessage('테스트')
    #bot = telegram.Bot(token=my_token)
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