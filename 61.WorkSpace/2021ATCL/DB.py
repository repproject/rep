import pymysql

repDBHost = "127.0.0.1"
repDBUser = "repwas"
repDBPassword = "0(repwas)"
repDBdb = "rep"
rebDBcharset = 'utf8'

def repDBConnect():  # DBConnection
    """

    :rtype: object
    """
    return pymysql.connect(host=repDBHost, user=repDBUser, password=repDBPassword, db=repDBdb, charset=rebDBcharset)

# if __name__ == "__main__":
# #     conn = repDBConnect()
# #
# #     print('test')