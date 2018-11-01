#  页面元素集，操作元素的方法
import time
import os
from utils.cv import GraphicalLocator
from utils.config import  REPORT_PATH
from selenium.webdriver.support import  expected_conditions as EC
import datetime
from utils.log import logger
from selenium.webdriver.support.wait import WebDriverWait
from UI_pc.common.driver_configure import Driver_configure
from selenium.webdriver.common.action_chains import ActionChains
from utils.config import Img_path_cv

class BasePage():

    def __init__(self,page=None):
        if page:
            self.driver=page.driver
        else:
            dr = Driver_configure()
            driver = dr.get_driver()
            self.driver=driver

        #cv使用action
        self.action = ActionChains(self.driver)



    def get(self, url, maximize_window=True, implicitly_wait=30):    #get(url)

        self.driver.get(url)
        if maximize_window:
            self.driver.maximize_window()

        self.driver.implicitly_wait(implicitly_wait)  #全局等待30s


    #定位

#------------------------------------------selenium基础定位--------------------------
    def find_element(self, *args):       #find_element()
        try:
            WebDriverWait(self.driver,1).until(EC.visibility_of_element_located(args))
            return self.driver.find_element(*args)
        except Exception as e:
             logger.error('未找到指定元素'+str(args))
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
        #存储图片地址
        fp =  REPORT_PATH+ "/WebImage/"
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




#------------------------------------------OPEN-CV图像定位--------------------------


#find_element
    def find_element_cv(self,msg,img):
        '''
        :param msg: 元素描述
        :param img: 图
        :param th_shape: 图形阈值 
        :param th_histogram:直方图阈值 
        :return: 元素中心坐标（x,y）
        '''
        th_shape=0.8
        th_histogram=0.4
        cv = GraphicalLocator(self.driver)

        cv.find_me(img)
        #存储定位成功图片位置
        path = os.path.join(Img_path_cv, '测试过程定位截图')
        #cv.rectangle(path,img,msg)
        if cv.threshold['shape'] >= th_shape :#and cv.threshold['histogram'] >= th_histogram:
            print('元素定位-->【'+msg+'】图形匹配度'+str(cv.threshold['shape'])+'   颜色匹配度：'+str(cv.threshold['histogram']) + '元素【'+msg+'】   坐标：'+str(cv.center_x) + '，'+str(cv.center_y))
            return cv.center_x ,cv.center_y

        else:

            print('元素定位失败-->元素：【' + msg + '】图形匹配度' + str(cv.threshold['shape']) + '   颜色匹配度：' + str(cv.threshold['histogram']))
            return None




    #悬停
    def move(self,msg,img,backgroudXpath):
        action = ActionChains(self.driver)
        location=self.find_element_cv(msg,img)
        x=location[0]
        y=location[1]
        el = self.driver.find_element_by_xpath(backgroudXpath)
        action.move_to_element_with_offset(el,x,y).perform()
        print('元素操作成功-->悬停：[' + msg + ']')
        time.sleep(2)

    #click
    def move_and_click(self,msg,img,backgroudXpath):
        action = ActionChains(self.driver)
        location=self.find_element_cv(msg,img)
        x=location[0]
        y=location[1]
        el = self.driver.find_element_by_xpath(backgroudXpath)
        action.move_to_element_with_offset(el,x,y).click().perform()
        print('元素操作成功-->点击[' + msg + ']')
        self.driver.implicitly_wait(5)
        time.sleep(2)

    #send_keys
    def click_and_sendkeys(self, msg,img,backgroudXpath,value):
        action = ActionChains(self.driver)
        location = self.find_element_cv(msg, img)
        x = location[0]
        y = location[1]
        el = self.driver.find_element_by_xpath(backgroudXpath)
        action.move_to_element_with_offset(el, x, y).click().perform()
        print('元素操作成功-->点击[' + msg + ']')
        self.driver.implicitly_wait(5)
        action.send_keys(value).perform()
        print('元素操作-->[' + msg + ']输入：'+value)
        time.sleep(2)



    #assert
    def assertImgElement(self,msg,img):#阈值大于90  颜色阈值大于60
        '''
        :param img: 断言图片
        :param msg: 描述
        :return: 是否存在True/False
        '''
        cv_assert = GraphicalLocator(self.driver)
        th_sh = 0.6
        cv_assert.find_me(img)
        path = os.path.join(Img_path_cv,'测试过程定位截图')
        #cv_assert.rectangle(path, img, msg)
        if cv_assert.threshold['shape'] >= th_sh:
            print('断言元素--> 【'+msg+'】 存在,元素图形匹配度：'+str(cv_assert.threshold['shape']))
            pass
        else:
            print('断言元素--> 【' + msg + '】 不存在,元素图形匹配度：'+str(cv_assert.threshold['shape']))
            raise AssertionError(msg + '断言失败')
        time.sleep(1)




    def pc_control(self,backgroudXpath,msg,img,method,value=None):
        '''
        :param backgroudXpath: 页面背景xpath
        :param msg: 元素描述
        :param img: 图片路径
        :param method: 方法：点击/悬停/输入
        :param value: 输入的内容sendkeys
        :return: 
        '''

        if method == '点击':
            self.move_and_click(msg,img,backgroudXpath)
        elif method == '输入':
            self.click_and_sendkeys(msg,img,backgroudXpath,value)
        elif method == '悬停':
            self.move(msg,img,backgroudXpath)
        else:
            print(method+'输入有误，现支持点击/悬停/输入内容')

