# -*- coding:utf-8 -*-
from REP_COM import *
from bs4 import BeautifulSoup

userid = 1000000011

dicNaverURL = {
    "https://smartstore.naver.com/gonggami/products/4705579501": 0,  # 뉴네푸어
    "https://smartstore.naver.com/shyman/products/4843275185": 0, #착한마스크 샤이맨 19일 3회
    "https://smartstore.naver.com/pyeongpyoen/products/4690028600": 0,  #엔에이웰 상시게릴라 (23일 4~5시30분)
    "https://smartstore.naver.com/desind/products/4844267787": 0,  # 숨프리 (19일 7차 소형 판매예정 / kf94 흰색,검정 kf80흰색)
    #"https://smartstore.naver.com/neulhaerangmask/products/4632987981": 0,  # 늘해랑 일회용 마스크 매일오전10시
    #"https://smartstore.naver.com/sangkong/products/4762917002": 0,  # 상공양행마스크  3월2주차부터 화목구매가능
    #"https://smartstore.naver.com/mfbshop/products/4072435942": 0,  # 닥터퓨리(스토어샵공지사항 오픈시간공지 확인할것)
    #"https://smartstore.naver.com/korea-mask/products/4825762296": 0, #국대마스크(3일 11시~1시 게릴라)
    #"https://smartstore.naver.com/gonggami/products/4705579501": 0, #★★공감아이 (KF94 20매 19,900원)
    #"https://smartstore.naver.com/silkroadcp/products/4272027565": 0, #숨마스크(10매 11900원)
    #"https://smartstore.naver.com/aer-shop/products/4792484420" : 0, #아에르
    #"https://smartstore.naver.com/dkpharm_naturesvitamin/products/4810907388" : 0 ,#동국제약
    #"https://smartstore.naver.com/ygfac/products/3905641271" : 0, #나록스
    #"https://smartstore.naver.com/greenpiamarket/products/4792924692" : 0, #그린피아마켓
    #"https://smartstore.naver.com/carmang1825/products/4834056954" : 0 #해피키친

    #"https://smartstore.naver.com/kumaelectron/products/4836415470" : 0 #테스트
}

def runNaverMask():
    LogObejct = REP_COM.Logger("runNaverMask",Level="DEBUG")
    global Log
    sendMessage2("마스크 찾기 시작",436714227)
    Log.info("마스크 찾기 시작")
    while True:
        try:
            for dicUrl in dicNaverURL.keys():
                Log.debug("#####################URL#####################")
                Log.debug(str(dicUrl))
                page = get_html(dicUrl)

                soup = BeautifulSoup(page, 'html.parser')
                Log.debug("#####################SOUP#####################")
                soup2 = soup.find("div",{"class","btn_order"})
                Log.debug(soup2)
                if soup2 != None:
                    if soup2.find(class_="_buy_button"):
                        if dicNaverURL[dicUrl] == 0:
                            Log.info("Mask존재!!")
                            #sendMessage2("Test입니다.")
                            sendMessage2(dicUrl)
                            sendMessage2("마스크 찾았다")
                            dicNaverURL[dicUrl] = 1
                    else:
                        if dicNaverURL[dicUrl] == 1:
                            Log.debug("Mask없다")
                            Log.info("Mask종료!!")
                            #sendMessage2("Test입니다.")
                            sendMessage2("마스크 없어졌다" + str(dicUrl))
                            dicNaverURL[dicUrl] = 0
                else:
                    if dicNaverURL[dicUrl] == 1:
                        Log.debug("mask없다")
                        Log.info("Mask종료!!")
                        sendMessage2("마스크 없어졌다" + str(dicUrl))
                        dicNaverURL[dicUrl] = 0
                #time.sleep(0.4)
        except Exception as e :
            sendMessage2(str(dicUrl),436714227)
            sendMessage2(str(e),436714227)
            Log.error(str(e))

if __name__ == '__main__':
    runNaverMask()
    #migBBRegnLv1Code(batchContext)