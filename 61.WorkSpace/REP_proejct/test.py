import REP_JOB
import sqlalchemy
#import telegram
my_token = '495069941:AAHXf-j_f97clXuEI5P0lpnbyPKcUfmVtYs'
chat_id = 436714227




def main():
    bot = telegram.Bot(token=my_token)  # bot을 선언합니다.
    getMessage(bot)
    #bot.sendMessage(chat_id=chat_id, text="저는 봇입니다.")
    #bot.sendMessage(chat_id=chat_id, text="저는 봇입니다.")

def getMessage(bot):
    updates = bot.getUpdates()  # 업데이트 내역을 받아옵니다.
    for u in updates:  # 내역중 메세지를 출력합니다.
        print(u.message)

def testmyBatis():
    print("testMyBatis")
    sql_id = "test"
    mapper, xml_raw_text = mybatis_mapper2sql.create_mapper(xml='mybatis_mapper.xml')
    statement = mybatis_mapper2sql.get_statement(mapper)
    statement = mybatis_mapper2sql.get_child_statement(mapper, sql_id)



if __name__ == '__main__':
    #main()
    testmyBatis()

#https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html
#박지일id : 436714227