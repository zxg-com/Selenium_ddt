
import unittest
from selenium.webdriver.common.by import By
from utils.config import  DATA_PATH
from utils.log import logger
from utils.file_reader import ExcelReader

from UIaototest.page.baidu_main_page import BaiDuMainPage
from UIaototest.page.baidu_result_page import BaiDuResultPage
from UIaototest.common.Basepage import BasePage
import ddt
import asserts



#excel输入数据
excelpath=DATA_PATH + '//API.xls'
ecl=ExcelReader(excelpath,'首页输入数据').get_ddtvalue()
ecl1 = ExcelReader(excelpath, sheetname='页面url')


@ddt.ddt
class TestBaiDu(unittest.TestCase):
        case_name = '百度搜索'
        @classmethod
        def setUpClass(cls):

        #     dr=driver_configure.Driver_configure()
        #     cls.driver=dr.get_driver()
            URL = ecl1.rowsvalue(rowname='百度首页')[1]  #excel取值
            cls.page = BaiDuMainPage()
            cls.page.get(URL)
            logger.info("打开" + URL)
            # tearDown 清理

        @ddt.data(*ecl)
        def test_search(self,data):
            self.page.inputl(data[1])
            logger.info('输入'+data[1])
            self.page.but_click()
            self.page.scrollTop_firefox('1000') #滑动滚轮
            self.page.saveScreenshot(name='百度结果页')  #截图

            self.page=BaiDuResultPage(self.page) # 页面跳转到result page,才可以用下一页内容的操作
            logger.info("页面进入搜索结果页")
            asserts.assert_in('百度', self.page.get_title())



        @classmethod
        def tearDownClass(cls):
            cls.page.close()

if __name__ == '__main__':
    unittest.main()