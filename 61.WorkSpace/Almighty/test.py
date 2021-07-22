from DAO.KADM import *
from DAO.KTable import *

if __name__ == "__main__" :
    #dtl = ComCdDtl('a','b','c','d',1,'e','f','g','h','i','j','k')
    lst = {'com_cd_grp' : 'ABC','com_cd_grp_nm' : 'BBB','del_yn' : 'N'}
    #lst = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    a = ComCdLst(lst)
    print(a)

    #text = None
    #print(text)
    #menu = Menu('test',None,None,None,None,None)
    pass