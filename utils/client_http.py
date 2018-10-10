"""
API
添加用于接口测试的client，对于HTTP接口添加HTTPClient，发送http请求。
还可以封装TCPClient，用来进行tcp链接，测试socket接口等等。
"""
from utils.file_reader import ExcelReader,YamlReader
from utils.config import Config, REPORT_PATH,DATA_PATH,DATA_FILE
import requests
from utils.config import Config
from utils.log import logger
import json
METHODS = ['GET', 'POST', 'HEAD', 'TRACE', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']


class UnSupportMethodException(Exception):
    """当传入的method的参数不是支持的类型时抛出此异常。"""
    pass


class HTTPClient(object):

    def __init__(self,case_name, cookies=None):

        """headers: 字典。 例：headers={'Content_Type':'text/html'}，cookies也是字典。"""
        self.case_name = case_name

        excelpath = DATA_PATH + '/API.xlsx'  # excel路径

        sheet = ExcelReader(excelpath, sheetname='API')  # 创建对象（表路径，分表名称）
        L = sheet.rowsvalue(rowname=self.case_name)  # 功能名称

        #######excel中接口信息#####

        self.terminal = L[1]  # 终端
        self.module = L[2]  # 模块
        self.Httpcheme = L[3]
        self.method = str(L[4]).upper()  # 方法 （大写）
        self.domain = L[5]  # 域名前缀
        self.route = L[6]  # url路径
        self.headers = L[7]  # headers转成字典
        if self.headers !="":
            self.headers = eval(L[7])
        self.transfer1 = L[8]  # 参数类型param、qurry等
        self.param1 = L[9]  # 参数值
        self.transfer2 = L[10]  # 参数类型param、qurry等
        self.param2 = L[11]  # 参数值
        self.data = L[12]   #data数据
        self.url = self.Httpcheme + self.domain + self.route  # 完成url路径拼接
        self.session = requests.session()
        self.cookies=cookies
        self.response = None
        self.set_headers(self.headers)
        self.set_cookies(self.cookies)
        if self.method not in METHODS:
            logger.error('不支持的method:{0}，请检查传入参数！'.format(self.method))
        print("测试用例:【" + self.case_name + "】开始前准备")

    def set_headers(self, headers):

        if headers:
            self.session.headers.update(headers)

    def set_cookies(self, cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def send(self,data=None,timeout=5, **kwargs):


        try:
            print("----------接口测试开始执行----------\n")
            print("【用例名称】: "+self.case_name+"\n"
                  "【终端】：" + self.terminal + "\n"
                  "【模块】:" + self.module + "\n"
                  "【方法】:" + self.method + "\n"
                  "【url】:" + self.url + "\n"
                  "【HEADERS】:" + str(self.session.headers) + "\n"
                  "【Cookies】: "+ str(requests.utils.dict_from_cookiejar(self.session.cookies))
                  )

            """
            #让param参数值传入转化后的字典中  ,param在send方法时传入即可，默认都从data.yml中取
            #把值写成属性名称，将属性名称在用例中创建好即可 excel中直接写成"consultationId":consultationId
           """

            if self.param1 != "":
                self.param1 = eval(self.param1)
                if self.param2 !="":
                    self.param2 = eval(self.param2)
                    params = {self.transfer1: str(self.param1), self.transfer2: str(self.param2)}
                else:
                    params = {self.transfer1: str(self.param1)}
            else:
                params = None

            if self.data != "":
                self.data = eval(self.data)
            print(self.data)
            print("【传入参数param】：" + str(params)+"\n【传入参数data】： "+ str(self.data)+"\n")
            self.response = self.session.request(method=self.method, url=self.url,params=params, data=self.data,headers=self.headers,cookies=self.cookies, timeout=timeout)
            print("------------测试结果------------\n【响应结果】" +self.response.text+"\n\n")
            self.response.encoding = 'utf-8'
            logger.debug('{0} {1}'.format(self.method, self.url))
            logger.debug('请求成功: {0}\n{1}'.format(self.response,self.response.text))
            print("\n------------测试结束------------\n")
            return self.response

        except TimeoutError:
            logger.error("请求超时")

    def get_Cookies(self):   #获得页面cookies
        c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
        c.set('cookie-name', 'cookie-value')
        self.session.cookies.update(c)
        return self.session.cookies.get_dict()
