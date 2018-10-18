import cv2
import numpy
from io import BytesIO
from PIL import Image
from utils.config import Config
from selenium.webdriver.common.action_chains import ActionChains
from utils.log import logger

class GraphicalLocator(object):


    def __init__(self, elementName,img_path,driver):
        self.locator = img_path
        #x，y位置以像素为单位从左边开始，顶角
        self.x = None
        self.y = None
        self.driver=driver
        #cv2.imread()接口读图像 直接返回numpy.ndarray 对象，读进来直接是BGR 格式数据格式在 0~255，通道格式为(W,H,C)
        self.img = cv2.imread(img_path) # [width,height,3]
        self.height = self.img.shape[0]  #高
        self.width = self.img.shape[1]   #宽
        self.threshold = None  #阈值

        self.elementName=elementName



        # self.action = ActionChains(self.driver)
        # self.threshold_shape = Config.get('EVIORMENT').get('threshold_shape')
        # self.threshold_histogram = Config.get('EVIORMENT').get('threshold_histogram')


    @property
    def center_x(self):return self.x + int(self.width / 2) if self.x and self.width else None

    @property
    def center_y(self):return self.y + int(self.height / 2) if self.y and self.height else None


    def find_element(self):
        logger.info('定位元素： '+self.elementName+' 中。。。')
        print('定位元素： '+self.elementName+' 中。。。')
        # ＃清除最后找到的坐标
        self.x = self.y = None
        # 获取网页的当前屏幕截图
        scr = self.driver.get_screenshot_as_png()
        # 将img转换为BytesIO
        scr = Image.open(BytesIO(scr))
        # 转换为OpenCV接受的uint8格式 dtype数据传入格式
        # astype 转换为uint8以保存图像
        scr = numpy.asarray(scr, dtype=numpy.float32).astype(numpy.uint8)
        # 将图像从BGR转换为RGB格式
        # 用cvtColor获得原图像RGB的副本
        scr = cv2.cvtColor(scr, cv2.COLOR_BGR2RGB)

        # 图像匹配仅适用于灰色图像（从RGB / BGR到灰度等级的颜色转换）
        #得到结果图像最小值，最大值，最小索引(x,y)，最大索引（x1,y1）
        img_match = cv2.minMaxLoc(
            #模版匹配 返回匹配阈值
            cv2.matchTemplate(cv2.cvtColor(scr, cv2.COLOR_RGB2GRAY),#搜索图
                              cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY),#模版图
                              cv2.TM_CCOEFF_NORMED)  #匹配方法
        )

        # 计算找到的元素
        self.x = img_match[3][0] #最大值索引x
        self.y = img_match[3][1] #最大值索引y

        # 从匹配模板图像的完整屏幕截图裁剪部分
        scr_crop = scr[self.y:(self.y + self.height),
                   self.x:(self.x + self.width)]

        # 两个模板的＃计算颜色直方图
        # 和匹配的图像和对它们进行比较
        #直方图是图像中像素强度分布的图形表达方式
        scr_hist = cv2.calcHist([scr_crop], [0, 1, 2], None,
                                [8, 8, 8], [0, 256, 0, 256, 0, 256])
        img_hist = cv2.calcHist([self.img], [0, 1, 2], None,
                                [8, 8, 8], [0, 256, 0, 256, 0, 256])
        comp_hist = cv2.compareHist(img_hist, scr_hist,
                                    cv2.HISTCMP_CORREL)

        # 保存阈值匹配：图形图像和图像直方图
        self.threshold = {'shape': round(img_match[1], 2)
                          ,'histogram': round(comp_hist, 2)}

        return scr

    def rectangle(self):
        # 画矩形圈出识别图
        s=cv2.rectangle(self.find_me(), (self.x, self.y),
                             (self.x + self.width, self.y + self.height),
                             (0, 0, 255), 2)
        cv2.imwrite('origin.jpg', s)

    def send_key(self, msg):

        self.find_element()
        logger.info('正在元素' + self.elementName + '输入信息' + msg)
        if self.threshold['shape'] >= self.threshold_shape and self.threshold['histogram'] >= self.threshold_histogram:
            self.action.send_keys(msg).perform()
        else:
            logger.error('未能定位到元素：' + self.elementName)
            logger.info("图形阈值：" + str(img_check.threshold['shape']))
            logger.info("直方图阈值：" + str(img_check.threshold['histogram']))
            print('未能定位到元素：' + self.elementName)
            print("图形阈值：" + str(img_check.threshold['shape']))
            print("直方图阈值：" + str(img_check.threshold['histogram']))

    def move_and_click(self):
        self.find_element()
        if self.threshold['shape'] >= self.threshold_shape and self.threshold['histogram'] >= self.threshold_histogram:
            self.action.move_by_offset(self.center_x, self.center_y)
            self.action.click().perform()

    def scroll_window(self, x):
        js = "var q=document.documentElement.scrollTop=" + x
        self.driver.execute_script(js)

# from selenium.webdriver.common.action_chains import ActionChains
# from selenium import webdriver
# import os,time
# driverpath=os.path.split(os.path.realpath(__file__))[0] + "/geckodriver"
# print(driverpath)
# driver=webdriver.Firefox(executable_path=driverpath)
# driver.get("http://www.yi-ding.net.cn/")
# driver.maximize_window()
#
#
#
#
#
# picpath=os.path.split(os.path.realpath(__file__))[0] + "/pic/more.jpeg"
# img_check = GraphicalLocator(picpath,driver)
# img_check.find_element()
#
# #判断形状阈值大于0.8 颜色阈值大于0.4  符合条件true
# if img_check.threshold['shape'] >= 0.8  and img_check.threshold['histogram'] >= 0.4:
#     img_check.move_and_click()
#
# else:
#     print("图形阈值："+str(img_check.threshold['shape']))
#     print("直方图阈值："+str(img_check.threshold['histogram']))



