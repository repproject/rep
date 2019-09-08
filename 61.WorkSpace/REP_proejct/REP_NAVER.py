#-*- coding:utf-8 -*-
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import REP_DAO
import REP_URL
import REP_COM
import time
import REP_MIG

# def get_naver_realasset():
#     url = 'http://land.naver.com/article/articleList.nhn?' \
#           + 'rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04' \
#           + '&cortarNo=1168010600'\
#           + '&page=' + str('1')
#
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, "html5lib")
#
#     table = soup.find('table')
#     trs = table.tbody.find_all('tr')
#
#     value_list = []
#
#     for tr in trs[::2]:
#         tds = tr.find_all('td')
#         cols = [' '.join(td.text.strip().split()) for td in tds]
#
#         if '_thumb_image' not in tds[3]['class']:
#             cols.insert(3, '')
#
#         # print(cols)
#         거래 = cols[0]
#         종류 = cols[1]
#         확인일자 = datetime.strptime(cols[2], '%y.%m.%d.')
#         현장확인 = cols[3]
#         매물명 = cols[4]
#         면적 = cols[5]
#         공급면적 = re.findall('공급면적(.*?)㎡', 면적)[0].replace(',', '')
#         전용면적 = re.findall('전용면적(.*?)㎡', 면적)[0].replace(',', '')
#         공급면적 = float(공급면적)
#         전용면적 = float(전용면적)
#         층 = cols[6]
#         if cols[7].find('호가일뿐 실거래가로확인된 금액이 아닙니다') >= 0:
#             pass  # 단순호가 별도 처리하고자 하면 내용 추가
#         매물가 = int(cols[7].split(' ')[0].replace(',', ''))
#         연락처 = cols[8]
#
#         value_list.append([거래, 종류, 확인일자, 현장확인, 매물명, 공급면적, 전용면적, 층, 매물가, 연락처])
#
#     cols = ['거래', '종류', '확인일자', '현장확인', '매물명', '공급면적', '전용면적', '층', '매물가', '연락처']
#     df = pd.DataFrame(value_list, columns=cols)
#     return df

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