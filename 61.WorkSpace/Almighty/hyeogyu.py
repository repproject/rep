import requests
import time
from bs4 import BeautifulSoup

def get_html(url):
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html

def HGgetPrice():
    URL = "http://nland.kbstar.com/quics?page=B046949&QAction=763359&RType=json&B_CLEAR=1?%EB%A9%94%EB%89%B4%ED%83%80%EC%9E%85=S&%EB%AC%BC%EA%B1%B4%EC%A2%85%EB%B3%84%EA%B5%AC%EB%B6%84=01&%EB%B6%80%EB%8F%99%EC%82%B0%EB%8C%80%EC%A7%80%EC%97%AD%EC%BD%94%EB%93%9C=010000&%EB%B6%80%EB%8F%99%EC%82%B0%EC%86%8C%EC%A7%80%EC%97%AD%EC%BD%94%EB%93%9C=010103&%EB%B6%80%EB%8F%99%EC%82%B0%EC%A4%91%EC%A7%80%EC%97%AD%EC%BD%94%EB%93%9C=010100"
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')

    l = str(soup)

    aptlist = l.replace('"', '').replace('}', '').replace('{', '').replace(',', ':').replace('[', ':').replace(']',
                                                                                                               ':').split(
        ":")
    print("aptlist")
    print(aptlist)

    URL_PRICE_ORG = "http://nland.kbstar.com/quics?chgCompId=b057186&baseCompId=b057186&page=B046949&cc=b057186:b057186?GIS호출여부=1&nextPageYn=Y&물건식별자="

    for i in range(0, len(aptlist)):
        if aptlist[i] == "아파트명":
            print("time.sleep 전 ")
            print(aptlist[i])
            print("time.sleep 후 ")
            time.sleep(1)
            print("\n", aptlist[i + 1], " - ", aptlist[i + 17])
            html_price = get_html(
                URL_PRICE_ORG + aptlist[i + 17] + "&물건종별구분=01&부동산대지역명=서울특별시&부동산소지역명=대치동&부동산소지역코드=010103&부동산중지역명=강남구&아파트명=" +
                aptlist[i + 1])
            print("URL")
            print(URL_PRICE_ORG + aptlist[i + 17] + "&물건종별구분=01&부동산대지역명=서울특별시&부동산소지역명=대치동&부동산소지역코드=010103&부동산중지역명=강남구&아파트명=" +
                aptlist[i + 1])

            soup_price = BeautifulSoup(html_price, 'html.parser')

            price_one = soup_price.find("tbody").find_all("td", {"class", "t_r"})
            area_one = soup_price.find_all("a", {"class", "link"})

            for i in range(0, len(area_one)):
                print("면적 - ", str(area_one[i]).rsplit("<", 1)[0].rsplit(">", 1)[1])
                print("매매", "하위평균 - ", str(price_one[i * 8]).rsplit("<", 1)[0].rsplit(">", 1)[1],
                      " / 일반평균 - ", str(price_one[i * 8 + 1]).rsplit("<", 1)[0].rsplit(">", 1)[1],
                      " / 상위평균 - ", str(price_one[i * 8 + 2]).rsplit("<", 1)[0].rsplit(">", 1)[1])
                print("전세", "하위평균 - ", str(price_one[i * 8 + 3]).rsplit("<", 1)[0].rsplit(">", 1)[1],
                      " / 일반평균 - ", str(price_one[i * 8 + 4]).rsplit("<", 1)[0].rsplit(">", 1)[1],
                      " / 상위평균 - ", str(price_one[i * 8 + 5]).rsplit("<", 1)[0].rsplit(">", 1)[1])