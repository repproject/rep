import requests

def getMarketCode():    #BeautifulShop Class로 특정 Page를 Return한다.
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "false"}
    response = requests.request("GET", url, params=querystring)
    print(response.text)

if __name__== '__main__':
    getMarketCode()