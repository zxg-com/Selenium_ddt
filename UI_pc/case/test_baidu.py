#coding:utf-8
import unittest
from selenium.webdriver.common.by import By
from utils.config import  DATA_PATH
from utils.log import logger
from utils.file_reader import ExcelReader

from UI_pc.page.baidu_main_page import BaiDuMainPage
from UI_pc.page.baidu_result_page import BaiDuResultPage
from UI_pc.common.Basepage import BasePage
import ddt
import asserts



#excel输入数据
excelpath=DATA_PATH + '//API.xls'
ecl=ExcelReader(excelpath,'首页输入数据').get_ddtvalue()
ecl1 = ExcelReader(excelpath, sheetname='页面url')
case_name='百度搜索'

@ddt.ddt
class TestBaiDu(unittest.TestCase):
    '''搜索功能'''
    case_name = '百度搜索'


    def setUp(self):

        URL = ecl1.rowsvalue(rowname='百度首页')[1]  # excel取值
        self.page = BaiDuMainPage()
        self.page.get(URL)
        logger.info("打开" + URL)

    # @classmethod
    # def setUpClass(cls):
    #
    #     URL = ecl1.rowsvalue(rowname='百度首页')[1]  #excel取值
    #     cls.page = BaiDuMainPage()
    #     cls.page.get(URL)
    #     logger.info("打开" + URL)
        # tearDown 清理

    #--------selenium环境操作---------

    # @ddt.data(*ecl)
    # def test_search(self,data):
    #     self.page.inputl(data[1])
    #     logger.info('输入'+data[1])
    #     self.page.but_click()
    #     self.page.scrollTop_firefox('1000') #滑动滚轮
    #     self.page.saveScreenshot(name='百度结果页')  #截图
    #
    #     self.page=BaiDuResultPage(self.page) # 页面跳转到result page,才可以用下一页内容的操作
    #     logger.info("页面进入搜索结果页")
    #     asserts.assert_in('百度', self.page.get_title())

    #--------open-cv环境操作----------
    @unittest.skip('测试跳过')
    def test_search01(self):
        '''搜索数字'''
        try:
            self.page.input_keys('12345')
            self.page.but_click()
            self.page=BaiDuResultPage(self.page)

            self.page.assertImgElement(img=self.page.loc_result,msg='12345图标')
            self.page.result_links()

        except:
            self.screenshot = self.page.driver.get_screenshot_as_base64()
            raise


    #@unittest.skip("跳过原因")
    def test_search02(self):
        ''''搜索文字'''
        try:
            self.page.input_keys('测试')
            self.page.but_click()
            self.page=BaiDuResultPage(self.page)

            self.page.assertImgElement(img=self.page.loc_result,msg='12345图标')
            self.page.result_links()
        except:

            self.screenshot = self.page.driver.get_screenshot_as_base64()
            raise


    def tearDown(self):
        self.page.close()

    # @classmethod
    # def tearDownClass(cls):
    #     cls.page.close()

if __name__ == '__main__':
    unittest.main()