import urllib.request
from bs4 import BeautifulSoup

def JIGgetPrice():
    # 맞춤시세조회
    # http://nland.kbstar.com/quics?page=B047172&cc=b028364:b057198
    # 단지과거시세
    # http://nland.kbstar.com/quics?page=B047172&cc=b028364:b057487


    # url="http://nland.kbstar.com/quics?page=B047172&cc=b028364:b057487&물건종별구분=01&물건식별자=KBA007445&주택형일련번호=&부동산대지역코드=010000&부동산중지역코드=010200&부동산소지역코드=010201" #안되네
    url = "http://nland.kbstar.com/quics?page=B047172&cc=b028364:b057487&%EB%AC%BC%EA%B1%B4%EC%A2%85%EB%B3%84%EA%B5%AC%EB%B6%84=01&%EB%AC%BC%EA%B1%B4%EC%8B%9D%EB%B3%84%EC%9E%90=KBA007445&%EC%A3%BC%ED%83%9D%ED%98%95%EC%9D%BC%EB%A0%A8%EB%B2%88%ED%98%B8=&%EB%B6%80%EB%8F%99%EC%82%B0%EB%8C%80%EC%A7%80%EC%97%AD%EC%BD%94%EB%93%9C=010000&%EB%B6%80%EB%8F%99%EC%82%B0%EC%A4%91%EC%A7%80%EC%97%AD%EC%BD%94%EB%93%9C=010200&%EB%B6%80%EB%8F%99%EC%82%B0%EC%86%8C%EC%A7%80%EC%97%AD%EC%BD%94%EB%93%9C=010201"

    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req).read()
    str_data = str(data)
    print(str_data)
    real_data = str_data[2:]
    soup = BeautifulSoup(real_data, 'html.parser')
    print(soup.find_all("td", {"class": "t_r"}))