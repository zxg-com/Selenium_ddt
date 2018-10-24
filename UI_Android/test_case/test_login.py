# coding:utf-8

'''
description:测试登录和退出功能
'''
import unittest

from UI_Android.pages import login_page,initpage,init_page
import time




class test_appium(unittest.TestCase):
    case_name = "正常登录"
    @classmethod
    def setUpClass(cls):
        #启动页
        cls.page = initpage.InitPage()



    def test_login(self):
        #----appium定位---

        # self.page.always_allow()
        # self.page.click_skip()
        # '''测试登录功能'''
        # # 登录页面
        # self.page=login_page.login_page(self.page)
        # self.page.click_zhanghaotab()
        # self.page.input_user('15011270128')
        # self.page.input_Pws('111111')
        # self.page.click_login()

        #---图形定位---
        self.page.always_allow()
        self.page.click_skip_btn()
        self.page=login_page.Login_page(self.page)
        self.page.click_tab()
        self.page.input_mobile('15011270128')
        self.page.imput_password('111111')
        self.page.click_login()

        self.page=init_page.Init_page(self.page)
        #time.sleep(3)
        #断言
        self.page.assertImgElement('立即更新按钮',self.page.loc_update_btn)

    @classmethod
    def tearDownClass(cls):
        cls.page.quit()

if __name__=='__main__':
    unittest.main()
