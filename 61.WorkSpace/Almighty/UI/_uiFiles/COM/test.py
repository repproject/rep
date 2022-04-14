import datetime
from Server.Basic import *

if __name__ == "__main__" :
    url = "https://m.land.naver.com/cluster/ajax/articleList?itemId=&mapKey=&lgeo=&showR0=&rletTpCd=APT%3AOPST%3AVL%3AABYG%3AOBYG%3AJGC%3AJWJT%3ADDDGG%3ASGJT%3AHOJT%3AJGB%3AOR%3AGSW%3ASG%3ASMS%3AGJCG%3AGM%3ATJ%3AAPTHGJ&tradTpCd=A1%3AB1%3AB2%3AB3&z=14&lat=37.433673&lon=127.134285&btm=37.411315&lft=127.0798254&top=37.4560243&rgt=127.1887446&totCnt=830&cortarNo=4113310100&sort=rank&page=3"

    page = get_html(url, 'GET')


    #now = datetime.datetime.now().strftime('%Y%m%d')
    #nowDate = now.strftime('%Y%m%d')
    #print(nowDate)
    # lst = {'com_cd_grp' : 'ABC','com_cd_grp_nm' : 'BBB','del_yn' : 'N'}
    # a = ComCdLst(**lst)
    # print(a)

    # dic1 = {'a':'aa','b':'bb'}
    # dic2 = {'b':'bbb','c':'cc'}
    # dic3 = {**dic2,**dic1}
    # print(dic3)

    #text = None
    #print(text)
    #menu = Menu('test',None,None,None,None,None)
    pass