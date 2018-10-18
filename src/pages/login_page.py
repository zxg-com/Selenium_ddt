# coding:utf-8

'''
description:登录页
'''
from src.common import Base_page
from appium.webdriver.common import mobileby


class login_page(Base_page.Base_page):
    by = mobileby.By
    suibiankankan_button = (by.ID,"com.allin.social:id/md")
    zhanghao_tab =(by.XPATH,"//android.widget.TextView[contains(@text,'账号密码登录')]")
    input_mobile = (by.XPATH,"//*[contains(@text,'请输入手机号/邮箱')]")
    input_password = (by.XPATH,"//*[contains(@text,'请输入登录密码')]")
    login_btn=(by.ID,"com.allin.social:id/m_")

    # zhanghao_tab = src_path + 'tab' + ".jpeg"
    # input_mobile = src_path + 'mobile' + ".jpeg"
    # input_password = src_path + 'password' + ".jpeg"
    # login_btn = src_path + 'login' + ".jpeg"


    def click_zhanghaotab(self):
        self.click_button(*self.zhanghao_tab)

    def input_user(self,username):
        self.send_keys(username,*self.input_mobile)

    def input_Pws(self,password):
        self.send_keys(password,*self.input_password)

    def click_login(self):
        self.click_button(*self.login_btn)