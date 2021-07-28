# -*- coding:utf-8 -*-
import selenium

from common.common.URL import *
from REP_COM import *
from bs4 import BeautifulSoup
import urllib

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#import numpy as np

userid = 1000000011

dicCoupangURL = {
    "https://www.coupang.com/np/search?q=kf+%EB%A7%88%EC%8A%A4%ED%81%AC+%EB%8C%80%ED%98%95&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true":"KF 대형 로켓"
    #"https://www.coupang.com/np/search?q=kf94&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=recent&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true": "KF94로켓"
    #,"https://www.coupang.com/np/search?q=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80+%EB%A7%88%EC%8A%A4%ED%81%AC+kf80&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=auto&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true" : "KF80 로켓"
    #,"https://www.coupang.com/np/search?q=%ED%83%90%EC%82%AC%EB%A7%88%EC%8A%A4%ED%81%AC&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket_wow%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true" : "탐사 마스크"
    #,"https://www.coupang.com/np/search?q=%EC%9B%B0%ED%82%B5%EC%8A%A4%EB%A7%88%EC%8A%A4%ED%81%ACkf94&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true" : "웰킵스마스크kf94"
    #,"https://www.coupang.com/np/search?q=%EC%9B%B0%ED%82%B5%EC%8A%A4%EB%A7%88%EC%8A%A4%ED%81%ACkf80&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true" : "웰킵스마스크kf80"
    #,"https://www.coupang.com/np/search?q=%ED%81%AC%EB%A6%AC%EB%84%A5%EC%8A%A4%EB%A7%88%EC%8A%A4%ED%81%ACkf94%EB%8C%80%ED%98%95&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true" : "#크리넥스마스크kf94대형"
    #,"https://www.coupang.com/np/search?component=&q=%EC%8B%A0%EB%9D%BC%EB%A9%B4&channel=user" : "신라면"#TEST
}

dicCoupangProduct = {

}

mainUrl = "https://coupang.com/"
basicLink = "/vp/products"

def runCoupangMask():
    LogObejct = REP_COM.Logger("runCoupangMask",Level="DEBUG")
    global Log
    sendMessage2("쿠팡 마스크 찾기 시작",436714227)
    Log.info("쿠팡 마스크 찾기 시작")



    while True:
        try:
            for dicUrl in dicCoupangURL.keys():
                Log.info("#####################URL#####################")
                Log.info(str(dicUrl))
                url = str(dicUrl)
                hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
                preReq = urllib.request.Request(url, headers=hdr)
                req = urllib.request.urlopen(preReq)
                page = req.read()
                #print(page)
                soup = BeautifulSoup(page, 'html.parser')
                Log.debug("#####################SOUP#####################")

                soup2 = soup.find("ul",id="productList")
                #print(soup2)

                soup3 = soup2.find_all("li")
                Log.debug(soup3)

                if soup3 != None:
                    for child in soup3:
                        link = child.find("a")['href']

                        if dicCoupangProduct.get(link) == None : #미등록상품
                            dicCoupangProduct[link] = 0

                        if child.find("div",{"class","out-of-stock"}) == None:  #품절X > 입고상태
                            if dicCoupangProduct[link] == 0:
                                Log.info("Mask있다")
                                Log.info(str(child))
                                productUrl = mainUrl + link
                                sendMessage2(productUrl,436714227)
                                sendMessage2(productUrl, 850743756)
                                sendMessage2("마스크 ㄸㄸㄸ \n -JMaskBot 쿠팡 베타버전(오송신 가능)\n" + dicCoupangURL[dicUrl],436714227)
                                sendMessage2("마스크 ㄸㄸㄸ \n -JMaskBot 쿠팡 베타버전(오송신 가능)\n" + dicCoupangURL[dicUrl],850743756)
                                Log.info(productUrl)
                                dicCoupangProduct[link] = 1
                        else:   #품절상태
                            if dicCoupangProduct[link] == 1:
                                Log.info("Mask없다")
                                Log.info(str(child))
                                productUrl = mainUrl + link
                                sendMessage2("마스크 ㅂㅂ\n"  + dicCoupangURL[dicUrl],436714227)
                                sendMessage2("마스크 ㅂㅂ\n" + dicCoupangURL[dicUrl],850743756)
                                Log.info(productUrl)
                                dicCoupangProduct[link] = 0
                else:   #상품검색불가
                    # if dicCoupangProduct[link] == 1:
                    #     Log.info("Mask없다")
                    #     productUrl = mainUrl + link
                    Log.error("li ProductList 탐색 오류 : " + page)
                    sendMessage2("li ProductList 탐색 오류\n"  + dicCoupangURL[dicUrl],436714227)
                    # Log.info(productUrl)
                    # dicCoupangProduct[link] = 0
        except Exception as e :
            sendMessage2(str(dicUrl),436714227)
            sendMessage2(str(e),436714227)
            Log.error(str(e))

def buyCoupang():

    LogObejct = REP_COM.Logger("runCoupangMask",Level="DEBUG")
    global Log

    # 로그인할 유저정보를 넣어줍시다. (모두 문자열입니다!)
    dicPostParam = {
        'email' : 'bagjiil@ajou.ac.kr'
        ,'password' : 'afe68400'
        ,'rememberMe' : 'false'
        ,'token' : ''
        ,'captchaAnswer' : ''
        ,'returnUrl' : 'https%25253A%25252F%25252Fwww.coupang.com%25252Fnp%25252Fpost%25252Flogin%25253Fr%25253Dhttps%2525253A%2525252F%2525252Fwww.coupang.com%2525252F'
    }

    cart_id = 1583838804692
    old_cart_id = 0

    searchText = "KF 마스크 대형"

    urlLogin = 'https://login.coupang.com/login/login.pang'
    driver = webdriver.Chrome('C:/Users/Ceasar.DESKTOP-AQTREV4/PycharmProjects/rep/61.WorkSpace/REP_proejct/driver/chromedriver.exe')
    driver.get(urlLogin)

    #id입력
    input_id = driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[1]/div[1]/div[1]/label/span[2]/input")
    input_id.clear()
    input_id.send_keys(dicPostParam['email'])

    #password입력
    input_password = driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[1]/div[2]/div[1]/label/span[2]/input")
    input_password.clear()
    input_password.send_keys(dicPostParam['password'])

    button_login = driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[5]/button")
    button_login.click()

    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.ID, 'headerSearchBtn')))

    #로그인 완료
    #searchURL = 'https://www.coupang.com/np/search?q=kf+%EB%A7%88%EC%8A%A4%ED%81%AC+%EB%8C%80%ED%98%95&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true'
    #searchURL = 'https://www.coupang.com/np/search?q=%EC%8B%A0%EB%9D%BC%EB%A9%B4&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket_wow%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true'
    searchURL = 'https://www.coupang.com/np/search?q=%EB%AC%BC&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket_wow%2Ccoupang_global&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36&rocketAll=true'
    cartURL = 'https://www.coupang.com/vp/products/27613130?itemId=367373530&vendorItemId=3892220508&q=%EB%AC%BC&itemsCount=36&searchId=2440a5c6744446e78ad42eba395928ac&rank=6&isAddedCart='

    driver.get(cartURL)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/section/div[1]/div/div[3]/div[14]/div[2]/div[2]/button[2]')))

    button_cart_buy = driver.find_element_by_xpath(
        "/html/body/div[1]/section/div[1]/div/div[3]/div[14]/div[2]/div[2]/button[2]")
    button_cart_buy.click()

    #
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[9]/div[3]/button[2]')))
    test_buy_url = driver.current_url
    cart_id = int(test_buy_url[45:57])
    print("SET : " + str(cart_id))

    while True:
        try:
            for i in range(1,2000):
                driver.get(searchURL)

                wait = WebDriverWait(driver, 20)
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-product')))

                page = driver.page_source

                soup = BeautifulSoup(page, 'html.parser')
                Log.debug("#####################SOUP#####################")
                soup2 = soup.find("ul", id="productList")
                soup3 = soup2.find_all("li")
                Log.debug(soup3)

                if soup3 != None:
                    for child in soup3:
                        link = child.find("a")['href']

                        if dicCoupangProduct.get(link) == None:  # 미등록상품
                            dicCoupangProduct[link] = 0

                        if child.find("div", {"class", "out-of-stock"}) == None:  # 품절X > 입고상태
                            if dicCoupangProduct[link] == 0:

                                #상품 선택 페이지
                                productUrl = mainUrl + link
                                driver.get(productUrl)
                                wait = WebDriverWait(driver, 20)
                                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'subscribe-radio-btn')))

                                #구매id 체번
                                #sdpKey체번
                                buy_page = driver.page_source
                                index = buy_page.find('sdpVisitKey')
                                parse = buy_page[buy_page.find('sdpVisitKey'):index+100]
                                start = parse.find(":")
                                end = parse.find(",")

                                dicBasicParam = {
                                    'id' : child.get('id')                             #27613130
                                    ,'vendorItemId' : child.get('data-vendor-item-id') #3213757282
                                    ,'ItemId' : child.find('a')['data-item-id']        #data-item-id="109846121"
                                    ,'sdpKey' :  parse[start+2:end-1]                  #3m0vyhuqrk5fx42s63
                                }

                                print(dicBasicParam)

                                dicparam = {
                                    'items' : (dicBasicParam['vendorItemId'],1)
                                    ,'clickProductId' : dicBasicParam['id']
                                    ,'landProductId': dicBasicParam['id']
                                    ,'clickItemId' : dicBasicParam['ItemId']
                                    ,'cartItemId' : dicBasicParam['ItemId']
                                    ,'sdpVisitKey' : dicBasicParam['sdpKey']
                                    ,'q' : 'KF 마스크 대형'
                                    #searchId
                                }


                                while True:
                                    #구매 페이지
                                    url2 = "https://checkout.coupang.com/direct/checkout/" + str(cart_id) + "?item%5B%5D="

                                    dicparam2 = {
                                        'items': (dicBasicParam['vendorItemId'], 1)
                                    }

                                    url2 += dicBasicParam['vendorItemId'] + '%3A1'
                                    print("test")
                                    driver.get(url2)

                                    wait = WebDriverWait(driver, 20)
                                    try:
                                        wait.until(EC.element_to_be_clickable((By.ID, 'paymentBtn')))
                                    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
                                        old_cart_id = cart_id
                                        cart_id += 20000
                                        continue
                                    break


                                #button_payment = driver.find_element(By.ID, 'paymentBtn')
                                button_aggre = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[9]/div[1]/div[1]/label/div[1]/p/input")
                                button_aggre.click()

                                button_payment = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[9]/div[3]/button[2]")
                                #print(button_payment)
                                button_payment.click()
                                sendMessage2("Mask구매 완료", 436714227)
                                time.sleep(30)
                                exit()
                                dicCoupangProduct[link] = 1
                        else:  # 품절상태
                            if dicCoupangProduct[link] == 1:
                                Log.info("Mask없다")
                                Log.info(str(child))
                                productUrl = mainUrl + link
                                Log.info(productUrl)
                                dicCoupangProduct[link] = 0
                else:  # 상품검색불가436714227
                    # if dicCoupangProduct[link] == 1:
                    #     Log.info("Mask없다")
                    #     productUrl = mainUrl + link
                    Log.error("li ProductList 탐색 오류 : " + page)
                    sendMessage2("li ProductList 탐색 오류\n" + dicCoupangURL[searchURL], 436714227)
                    # Log.info(productUrl)
                    # dicCoupangProduct[link] = 0
                #rand_arr = np.random.int(1)
                #print(rand_arr)
                time.sleep(0.3)
                cart_id += 2499
                #print(cart_id)

            driver.get(cartURL)

            wait = WebDriverWait(driver, 20)
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/div[1]/div/div[3]/div[13]/div[2]/div[2]/button[2]')))

            button_cart_buy = driver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div/div[3]/div[13]/div[2]/div[2]/button[2]")
            button_cart_buy.click()

            #
            wait = WebDriverWait(driver, 20)
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[9]/div[3]/button[2]')))
            test_buy_url = driver.current_url
            cart_id = int(test_buy_url[45:57])
            print("SET : " + str(cart_id))

        except Exception as e:
            print(str(e))



if __name__ == '__main__':
    #buyCoupang()
    runCoupangMask()
    #migBBRegnLv1Code(batchContext)