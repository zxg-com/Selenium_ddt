#coding:utf-8
'''
description:UI页面公共类
'''
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.log import logger
from UI_IOS.common.driver_configure import driver_configure
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction
from utils.config import Config,Img_path_cv
from utils.cv import GraphicalLocator
import time
import subprocess
from appium.webdriver.common import touch_action
class Base_page:
    def __init__(self,page=None):
        if page:
            self.driver=page.driver
        else:
            dr = driver_configure()
            self.driver= dr.IOSdriver()

#----------appium-----------------------
    def find_element(self,*loc):
        '''重写find_element方法，显式等待'''

        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except Exception as e:
            logger.error('没定位到元素'+ str(loc))

    def find_elements(self,*loc):
        '''重写find_element方法，显式等待'''

        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_elements(*loc)
        except Exception as e:
            logger.error('没定位到元素组'+ str(loc))

    def send_keys(self,value,*loc):
        try:
           el=self.find_element(*loc)
           el.clear()
           el.send_keys(value)
        except Exception as  e:
            raise e

    def click_button(self,*loc):
        try:
            self.find_element(*loc)
            self.find_element(*loc).click()

        except Exception as  e:

            raise e

#---------appium-ios-by_ios_predicate-----------------

    #def find_element_ios(self, loc):
    #     '''重写find_element方法，显式等待'''
    #     try:
    #         self.driver.implicitly_wait(10)
    #         return self.driver.find_element_by_ios_predicate(loc)
    #     except Exception as e:
    #         logger.error('没定位到元素' + str(loc))
    #
    # def send_keys_ios(self, value, loc):
    #     try:
    #         self.find_element_ios(loc).clear()
    #         self.find_element_ios(loc).send_keys(value)
    #     except AttributeError as  e:
    #         raise e
    #
    # def click_button_ios(self, loc):
    #     try:
    #         self.find_element_ios(loc)
    #         self.find_element_ios(loc).click()
    #
    #     except AttributeError as  e:
    #         raise e



                #组合查找，多次操作查找
    def findLocal(self):
        x = 1
        while x == 1:
            if self.fack() == 1:
                self.swipe_up()  # 滑动操作,也可以是点击刷新按钮
                time.sleep(2)
                self.fack()
            else:
                print('找到了')
                x = 2

    def fack(self,*loc):
        n=1
        try:
            self.find_element(*loc).click()
        except Exception as  e:
            return n



    #切换webview
    def switch_webview(self):
        handles = self.driver.contexts  # 所有窗口的句柄
        self.driver.switch_to.context(handles[1])

    def switch_defaul_webview(self):
        self.driver.switch_to.context("NATIVE_APP")

    def swipe_left(self, ):
        '''左滑'''
        self.driver.execute_script("mobile:scroll", {"direction": "right"})

    def swipe_right(self):
        '''右滑'''
        self.driver.execute_script("mobile:scroll", {"direction": "left"})

    def swipe_down(self):
        '''下滑'''
        self.driver.execute_script("mobile:scroll", {"direction": "up"})

    def swipe_up(self):
        '''上滑'''
        self.driver.execute_script("mobile:scroll", {"direction": "down"})

    def quit(self):
        self.driver.quit()

     # 弹窗授权，每次都允许
    def always_allow(self):
        for i in range(4):
            try:
                self.driver.switch_to.alert.accept()
            except:
                pass

    def quit(self):
        self.driver.quit()




#----------------open-cv-----------------------
#find_element
    def find_element_cv(self,msg,img):
        '''
        :param msg: 元素描述
        :param img: 图
        :param th_shape: 图形阈值 
        :param th_histogram:直方图阈值 
        :return: 元素中心坐标（x,y）
        '''
        th_shape=0.6
        th_histogram=0.4
        cv = GraphicalLocator(self.driver)

        cv.find_me(img)
        #存储定位成功图片位置
        path = os.path.join(Img_path_cv, '测试过程定位截图')
        cv.rectangle(path,img,msg)
        if cv.threshold['shape'] >= th_shape :#and cv.threshold['histogram'] >= th_histogram:
            print('元素定位-->【'+msg+'】图形匹配度'+str(cv.threshold['shape'])+'   颜色匹配度：'+str(cv.threshold['histogram']) + '元素【'+msg+'】   坐标：'+str(cv.center_x) + '，'+str(cv.center_y))
            return cv.center_x ,cv.center_y

        else:

            print('元素定位失败-->元素：【' + msg + '】图形匹配度' + str(cv.threshold['shape']) + '   颜色匹配度：' + str(cv.threshold['histogram']))
            return None



#---------------------IOS opencv------------------
#adb shell input swipe x y x1 y1  1000  x=x1,y=y1长按/滑动 1000ms
# adb shell input keyevent  26 or 'KEYCODE_POWER'  按power键
    #click
    def move_and_click(self,msg,img):
        location=self.find_element_cv(msg,img)
        x=location[0]
        y=location[1]
        t_c=touch_action.TouchAction(self.driver)
        t_c.tap(x,y).perform()
        print('元素操作成功-->点击[' + msg + ']')
        self.driver.implicitly_wait(5)

    #send_keys
    def click_and_sendkeys(self, msg,img,value):

        location = self.find_element_cv(msg, img)
        x = location[0]
        y = location[1]
        t_c = touch_action.TouchAction(self.driver)
        t_c.tap(x, y).perform()
        print('元素操作成功-->点击[' + msg + ']')
        subprocess.getoutput('adb shell am broadcast -a ADB_INPUT_TEXT --es msg '+value)
        print('元素操作-->[' + msg + ']输入：'+value)
        self.driver.implicitly_wait(5)

    def sendkeysOfIOS(self, loc, value):
        try:
           el = self.app.find_elements_by_class_name(loc)
           el.send_keys(value)
        except:
           pass

    #assert
    def assertImgElement(self,msg,img):
        '''
        :param img: 断言图片
        :param msg: 描述
        :return: 是否存在True/False
        '''
        cv_assert = GraphicalLocator(self.driver)
        th_sh = 0.6
        cv_assert.find_me(img)
        path = os.path.join(Img_path_cv,'测试过程定位截图')
        cv_assert.rectangle(path, img, msg)
        if cv_assert.threshold['shape'] >= th_sh:
            print('断言元素--> 【'+msg+'】 存在,元素图形匹配度：'+str(cv_assert.threshold['shape']))
        else:
            print('断言元素--> 【' + msg + '】 不存在,元素图形匹配度：'+str(cv_assert.threshold['shape']))
            raise AssertionError(msg+'断言失败')

        time.sleep(1)




    def Android_control(self,msg,img,method,value=None):
        '''
        :param msg: 元素描述
        :param img: 图片路径
        :param method: 方法：点击/输入
        :param value: 输入的内容sendkeys
        :return: 
        '''

        if method == '点击':
            self.move_and_click(msg,img)
        elif method == '原生输入' or method == '输入':
            self.click_and_sendkeys(msg,img,value)
        else:
            print(method+'输入有误，现支持点击/输入内容')




