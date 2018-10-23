# coding:utf-8

'''
description:登录页
'''
from src.common import Base_page
from appium.webdriver.common import mobileby
from utils.config import Img_path_cv
import os

class Login_page(Base_page.Base_page):

    #-----------appium----------

    # by = mobileby.By
    # suibiankankan_button = (by.ID,"com.allin.social:id/md")
    # zhanghao_tab =(by.XPATH,"//android.widget.TextView[contains(@text,'账号密码登录')]")
    # input_mobile = (by.XPATH,"//*[contains(@text,'请输入手机号/邮箱')]")
    # input_password = (by.XPATH,"//*[contains(@text,'请输入登录密码')]")
    # login_btn=(by.ID,"com.allin.social:id/m_")
    #
    # # zhanghao_tab = src_path + 'tab' + ".jpeg"
    # # input_mobile = src_path + 'mobile' + ".jpeg"
    # # input_password = src_path + 'password' + ".jpeg"
    # # login_btn = src_path + 'login' + ".jpeg"
    #
    #
    # def click_zhanghaotab(self):
    #     self.click_button(*self.zhanghao_tab)
    #
    # def input_user(self,username):
    #     self.send_keys(username,*self.input_mobile)
    #
    # def input_Pws(self,password):
    #     self.send_keys(password,*self.input_password)
    #
    # def click_login(self):
    #     self.click_button(*self.login_btn)


    # --------图形定位-------
    item = 'app_android_allinmd'
    page = '登录页'
    tab = '账号密码登录tab'
    login_btn='登录按钮'
    mibole_input='手机号输入框'
    password_input='密码输入框'

    loc_tab = os.path.join(Img_path_cv, item, page, tab + '.png')
    loc_login_btn = os.path.join(Img_path_cv, item, page, login_btn + '.png')
    loc_mibole_input = os.path.join(Img_path_cv, item, page, mibole_input + '.png')
    loc_password_input = os.path.join(Img_path_cv, item, page, password_input + '.png')


    def click_tab(self):
        self.Android_control(msg='账号密码登录tab', img=self.loc_tab, method='点击', value=None)

    def input_mobile(self,value):
        self.Android_control(msg='手机号输入框', img=self.loc_mibole_input, method='输入', value=value)

    #原生输入，指一些原生键盘，无法使用自定义安装的键盘
    def imput_password(self, value):
        self.Android_control(msg='密码输入框', img=self.loc_password_input, method='原生输入', value=value)

    def click_login(self):
        self.Android_control(msg='登录按钮', img=self.loc_login_btn, method='点击', value=None)
