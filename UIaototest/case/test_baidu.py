import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestReportCN import HTMLTestRunner
from utils.mail import Email
import datetime
from UIaototest.page import baidu_result_page,baidu_main_page
from UIaototest.common.Basepage import BasePage
from utils.config import DATA_FILE
import ddt
from UIaototest.common import driver_configure

#excel输入数据
excelpath=DATA_PATH + '//API.xls'
ecl=ExcelReader(excelpath,'首页输入数据').get_ddtvalue()
ecl1 = ExcelReader(excelpath, sheetname='页面url')


@ddt.ddt
class TestBaiDu(unittest.TestCase):
        case_name = '百度搜索'
        @classmethod
        def setUpClass(cls):
        # def setUp(self):
            dr=driver_configure.Driver_configure()
            cls.driver=dr.get_driver()
            URL = ecl1.rowsvalue(rowname='百度首页')[1]  #excel取值
            cls.baidu_main_p=baidu_main_page.BaiDuMainPage(cls.driver)
            cls.baidu_main_p.get(URL)
            logger.info("打开" + URL)
            # tearDown 清理

        @ddt.data(*ecl)
        def test_search(self,data):
            self.baidu_main_p.inputl(data[1])
            logger.info('输入'+data[1])
            self.baidu_main_p.but_click()
            self.baidu_main_p.scrollTop_firefox('1000') #滑动滚轮
            self.baidu_main_p.saveScreenshot(name='百度结果页')  #截图

            self.baidu_result_p = baidu_result_page.BaiDuResultPage(self.driver) # 页面跳转到result page,才可以用下一页内容的操作
            logger.info("页面进入搜索结果页")
            links = self.baidu_result_p.result_links
            # for link in links:
            #     print(link.text)
            print(self.baidu_result_p.get_title())\


        @classmethod
        def tearDownClass(cls):
            cls.driver.close()

        # def tearDown(self):
        #     self.driver.close()



# if __name__ == '__main__':
#     report = REPORT_PATH + "//report.html"
#     with open(report, 'wb') as ff:
#         runner = HTMLTestRunner(ff, verbosity=2, title='UI测试报告', description='UI测试报告', tester='会诊自动化测试')
#         runner.run(TestBaiDu('test_search'))
#         e = Email(title='百度搜索测试报告',
#                   # 初始化时传入全部所需数据，message是正文，可不填，path可以传list或者str；receiver支持多人，用”;”隔开就行
#                   message='这是今天的测试报告，请查收！',
#                   receiver='342509492@qq.com',
#                   server='smtp.163.com',
#                   sender='zxg_com@163.com',
#                   password='zxg680210',
#                   path=report  # 单个附件str 多个list
#                   )
#         e.send()
