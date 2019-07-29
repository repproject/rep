#import telegram
import REP_DAO
my_token = '495069941:AAHXf-j_f97clXuEI5P0lpnbyPKcUfmVtYs' #JBoozleBot
#chat_id = 436714227

def checkMessage():
    try:
        bot = telegram.Bot(token=my_token)  # bot을 선언합니다.
        updates = bot.getUpdates()  # 업데이트 내역을 받아옵니다.

        for u in updates:  # 내역중 메세지를 출력합니다.
            print(u.message.message_id)
            dicTlgrMsg = {'TLGR_MSG_ID': u.message.message_id, 'TLGR_MSG_CNTS': str(u)}
            if REP_DAO.INSERT_KADM_TLGR_MSG(dicTlgrMsg) == '100':   #INSERT가 정상일때
                if u.message.text[0] == '-': #정의된명령어
                    splitMessage = u.message.text.split(' ')
                    if splitMessage[0][1:] == "등록" :
                        print("[텔레그램 사용자등록]",u.message.chat.id,splitMessage[1])
                        dicTlgrUser= {'TLGR_USER_ID': u.message.chat.id, 'TLGR_USER_NM': splitMessage[1],'RCV_TGT_YN' : 'Y'}
                        if(REP_DAO.INSERT_KADM_TLGR_USER(dicTlgrUser) == '100'):
                            sendMessage("[텔레그램 사용자등록 완료] " + str(u.message.chat.id) + " " + splitMessage[1])
                            print("[텔레그램 사용자등록 완료] " + str(u.message.chat.id) + " " + splitMessage[1])
                        else:
                            print("[텔레그램 사용자등록 실패] " + str(u.message.chat.id) + " " + splitMessage[1])
                    elif splitMessage[0][1:] == "수신해제":
                        print("[텔레그램 수신해제]", u.message.chat.id)
                        dicTlgrUser = {'TLGR_USER_ID': u.message.chat.id, 'RCV_TGT_YN': 'N'}
                        if(REP_DAO.UPDATE_KADM_TLGR_USER_RCV_TGT_YN(dicTlgrUser) == '100'):
                            sendMessage("[텔레그램 수신해제 완료] " + str(u.message.chat.id))
                            print("[텔레그램 수신해제 완료] " + str(u.message.chat.id))
                        else:
                            print("[텔레그램 수신해제 실패] " + str(u.message.chat.id) + " " + splitMessage[1])
                    elif splitMessage[0][1:] == "수신등록":
                        print("[텔레그램 수신등록]", u.message.chat.id)
                        dicTlgrUser = {'TLGR_USER_ID': u.message.chat.id, 'RCV_TGT_YN': 'Y'}
                        if(REP_DAO.UPDATE_KADM_TLGR_USER_RCV_TGT_YN(dicTlgrUser) == '100'):
                            sendMessage("[텔레그램 수신등록 완료] " + str(u.message.chat.id))
                            print("[텔레그램 수신등록 완료] " + str(u.message.chat.id))
                        else:
                            print("[텔레그램 수신등록 실패] " + str(u.message.chat.id) + " " + splitMessage[1])
                    elif splitMessage[0][1:] == "?" or splitMessage[0][1:] == "사용문의":
                        print("[텔레그램 사용문의]", u.message.chat.id)
                        sendMessage("- 사용자등록 이름 (ex) -사용자등록 박지일\n -수신등록 \n -수신해제 \n -사용자등록 ", str(u.message.chat.id))
    except Exception as err:  # 기존에 소지역 코드가 존재할 수 있음
        print("[텔레그램ERROR발생]")
#        print(u.message.chat.id)
#        print(u.message.text)
#        print(u.message)

def sendMessage(str):
    print("메시지 송신" + str)
    bot = telegram.Bot(token=my_token)  # bot을 선언합니다.
    chat_id_tup = REP_DAO.SELECT_kadm_tlgr_RCV_usertup() #사용자 조회
    for chatid in chat_id_tup:
        str_chatid=''.join(chatid)
        print("메시지 송신" + str + str_chatid)
        bot.sendMessage(chat_id=int(str_chatid), text=str)

#if __name__ == '__main__':
#    main()

#https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html
#박지일id : 436714227
#{'new_chat_members': [], 'delete_chat_photo': False,
# 'group_chat_created': False,
# 'from': {'language_code': 'ko', 'id': 436714227, 'first_name': '케빈', 'is_bot': False, 'last_name': 'Brown'},
# 'channel_chat_created': False, 'new_chat_photo': [], 'photo': [], 'new_chat_member': None, 'message_id': 2, 'date': 1514088448, 'caption_entities': [], 'entities': [], 'supergroup_chat_created': False,
# 'chat': {'id': 436714227, 'type': 'private', 'last_name': 'Brown', 'first_name': '케빈'}, 'text': 'Rrrr'}