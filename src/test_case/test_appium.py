# coding:utf-8
__author__ = 'Helen'
'''
description:测试登录和退出功能
'''
import unittest

from src.pages import login_page,initpage



class test_appium(unittest.TestCase):
    case_name = "正常登录"
    @classmethod
    def setUpClass(cls):
        #启动页
        cls.page = initpage.initPage()


    def test_01login(self):

        self.page.always_allow()
        self.page.click_skip()
        '''测试登录功能'''
        # 登录页面
        self.page=login_page.login_page(self.page)
        self.page.click_zhanghaotab()
        self.page.input_user('15011270128')
        self.page.input_Pws('111111')
        self.page.click_login()

    @classmethod
    def tearDownClass(cls):
        cls.page.quit()

if __name__=='__main__':
    unittest.main()