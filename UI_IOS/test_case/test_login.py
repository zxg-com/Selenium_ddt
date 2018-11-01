# coding:utf-8

'''
description:测试登录和退出功能
'''
import unittest
from UI_IOS.pages import login_page
import time




class test_appium(unittest.TestCase):
    case_name = "正常登录"
    @classmethod
    def setUpClass(cls):
        #启动页
        cls.page = login_page.Login_page()



    def test_login(self):
        #----appium定位---



        '''测试登录功能'''
        # 登录页面
        time.sleep(3)
        self.page.click_zhanghaotab()
        self.page.input_user("15011270128")
        self.page.input_Pws("111111")
        self.page.click_login()



    @classmethod
    def tearDownClass(cls):
        cls.page.quit()

if __name__=='__main__':
    unittest.main()
