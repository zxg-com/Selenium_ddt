# coding:utf-8

'''
description:测试登录和退出功能
'''
import unittest
from UI_IOS.pages import login_page
import time
from utils.HTMLTestReportCN_screenshot import Screenshot



class test_appium(unittest.TestCase):
    '''登录功能'''
    case_name = "正常登录"
    @classmethod
    def setUpClass(cls):
        #启动页
        cls.page = login_page.Login_page()



    def test_login(self):
        '''测试登录功能'''
        # 登录页面
        try:
            time.sleep(3)
            self.page.click_zhanghaotab()
            self.page.input_user("15011270128")
            self.page.input_Pws("111111")
            self.page.click_login()
        except:
            Screenshot.get_screenshot(self.page.driver)
            raise



    @classmethod
    def tearDownClass(cls):
        cls.page.quit()

if __name__=='__main__':
    unittest.main()
