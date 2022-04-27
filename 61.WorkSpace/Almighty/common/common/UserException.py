class CrawlingEndException(Exception):  # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('No JobFuncExecStrd Need to End Crawling')

