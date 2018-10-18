# coding:utf-8
__author__ = 'Helen'
'''
description:UI页面公共类
'''
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.log import logger
from src.common.driver_configure import driver_configure
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction
from utils.config import Config


class Base_page:
    def __init__(self,page=None):
        if page:
            self.driver=page.driver
        else:
            dr = driver_configure()
            self.driver= dr.Androiddriver()

    def find_element(self,*loc):
        '''重写find_element方法，显式等待'''
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except Exception as e:
            logger.error('没定位到元素'+ str(loc))

    def send_keys(self,value,*loc):
        try:
            self.find_element(*loc).clear()
            self.find_element(*loc).send_keys(value)
        except AttributeError as  e:
            raise e

    def click_button(self,*loc):
        try:
            self.find_element(*loc)
            self.find_element(*loc).click()

        except AttributeError as  e:
            raise e



    def swipe_left(self,driver):
        '''左滑'''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        driver.swipe(x*3/4,y/4,x/4,y/4)

    def swipe_right(self,driver):
        '''右滑'''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        driver.swipe(x/4,y/4,x*3/4,y/4)

    def swipe_down(self,driver):
        '''下滑'''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        driver.swipe(x/2,y*3/4,x/2,y/4)

    def swipe_up(self,driver):
        '''上滑'''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        driver.swipe(x/2,y/4,x/2,y*3/4)

    def quit(self):
        self.driver.quit()

    #弹窗授权，每次都允许
    def always_allow(self):
        for i in range(5):
            loc = ("xpath", "//*[@text='允许']")  #安卓不同版本文案不同
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                e.click()
            except:
                pass


