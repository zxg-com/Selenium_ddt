#  页面元素集，操作元素的方法
import time
import os
from selenium import webdriver
from utils.config import DRIVER_PATH, REPORT_PATH
from utils.file_reader import Readini
from selenium.webdriver.support import  expected_conditions as EC
import re
import datetime
from utils.log import logger
from selenium.webdriver.support.wait import WebDriverWait



# 驱动路径
CHROMEDRIVER_PATH = DRIVER_PATH + '/chromedriver.exe'
IEDRIVER_PATH = DRIVER_PATH + '/IEDriverServer.exe'
FIREFOXDRIVER = DRIVER_PATH + '/geckodriver'
SAFARIDRIVER=DRIVER_PATH + '/safaridriver'
EDGEDRIVER=DRIVER_PATH + '/edgedriver.exe'


TYPES = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome, 'ie': webdriver.Ie,'safari':webdriver.Safari ,'edge':webdriver.Edge}
EXECUTABLE_PATH = {'firefox': FIREFOXDRIVER, 'chrome': CHROMEDRIVER_PATH, 'ie': IEDRIVER_PATH ,'safari':SAFARIDRIVER,'edge':EDGEDRIVER}


class UnSupportBrowserTypeError(Exception):
    pass



class BasePage(object):



    def __init__(self,driver):
        self.driver=driver
        # if page:
        #     self.driver=page.driver
        # else:
        #
        #     self._type = browser_type.lower()
        #     if self._type in TYPES:
        #         self.browser = TYPES[self._type]
        #     else:
        #         raise UnSupportBrowserTypeError('仅支持%s!' % ','.join(TYPES.keys()))
        #
        #     self.driver = self.browser(executable_path=EXECUTABLE_PATH[self._type])


    def get(self, url, maximize_window=True, implicitly_wait=30):    #get(url)
        self.driver.get(url)
        if maximize_window:
            self.driver.maximize_window()

        self.driver.implicitly_wait(implicitly_wait)  #全局等待30s


    #定位


    def find_element(self, *args):       #find_element()
        try:
            WebDriverWait(self.driver,1).until(EC.visibility_of_element_located(args))
            return self.driver.find_element(*args)
        except Exception as e:
             logger.error('未找到指定元素')
    #定位组
    def find_elements(self, *args):
        try:
            return self.driver.find_elements(*args)
        except Exception as e:
            logger.error(e)


    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def savePngName(self, name):
        """
        name：自定义图片的名称
        """
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fp =  REPORT_PATH+ "/Image/"
        tm = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        type = ".png"
        if os.path.exists(fp):
            filename = str(fp)  + str(tm) + str("_") + str(name) + str(type)
            return filename
        else:
            os.makedirs(fp)
            filename = str(fp) + str(tm) + str("_") + str(name) + str(type)
            return filename



    def saveScreenshot(self, name):
        """
        快照截图
        name:图片名称
        """
        # 获取当前路径
        # print os.getcwd()
        image = self.driver.save_screenshot(self.savePngName(name))

        return image

    def get_title(self):
        title=self.driver.title
        return title

    def execute_script(self,js):
        self.driver.execute_script(js)

    def scrollTop_firefox(self,px):
        '''
        :param px: 0顶部  10000底部 
        '''
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop="+px   # 设置0为顶部  滚动条与顶部的间距
        self.driver.execute_script(js)  # 执行js脚本
        time.sleep(3)

    def scrollTop_chrome(self,px):
        '''
        :param px: 0顶部  10000底部 
        '''
        time.sleep(2)
        js = "var q=document.body.scrollTop="+px   # 设置0为顶部  滚动条与顶部的间距
        self.driver.execute_script(js)  # 执行js脚本
        time.sleep(3)

    def get_cookies(self):
        cookies=self.driver.get_cookies()
        return cookies

    def add_cookies(self,dic):
        self.driver.add_cookie(dic)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def switch_frame(self,xpath):
        xy = self.driver.find_element_by_xpath(xpath)
        # 切换至iframe
        self.driver.switch_to.frame(xy)

    def switch_window(self):
        handles = self.driver.window_handles  # 所有窗口的句柄
        handle = self.driver.current_window_handle  # 获取当前页句柄
        self.driver.switch_to.window(handle)

    def accept_alert(self):
        self.driver.switch_to.alert().accept() #确认alert
