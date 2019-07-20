import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import REP_DAO
import REP_URL
import REP_COM
import time
import REP_MIG


def get_naver_realasset():
    tupLeglCode = REP_DAO.SELECT_RET_LEGL_REGN_CD();
    for LeglCode in tupLeglCode:
        time.sleep(2)
        url = REP_URL.getURLNaverAptcode('A01','A1',REP_COM.tuple2Str(LeglCode))
        print(url)
        #r = requests.get(url)
        soup = soup = REP_MIG.getBeautifulShopFromKB(url) #BeautifulShop 공통 리턴 사용 (try catch 사용을 위해)

#    print(soup.find_all('', {'class': 'list_name'}))
        list_name = soup.find_all('', {'class': 'list_name'})

        for list in list_name:
            print(list.find("a").get('hscp_no'))
            print(list.find("a").text) #단지명
            print(list.find("a").get('mapx'))
            print(list.find("a").get('mapy'))

            dicNvAptCode = {'NV_CMPX_ID': list.find("a").get('hscp_no')
                           , 'NV_CMPX_NM': list.find("a").text
                           , 'GOV_LEGL_DONG_CD': LeglCode
                           , 'X_COOR_VAL': list.find("a").get('mapx')
                           , 'Y_COOR_VAL': list.find("a").get('mapy')}
            REP_DAO.INSERT_KMIG_NV_APT_CODE(dicNvAptCode)


if __name__ == '__main__':
    get_naver_realasset()