#coding:utf-8
import cv2
import numpy
from io import BytesIO
from PIL import Image
from selenium import webdriver
import os
from selenium.webdriver.common.action_chains import ActionChains
import imghdr

class GraphicalLocator(object):

    def __init__(self,driver):

        #x，y位置以像素为单位从左边开始，顶角
        self.x = None
        self.y = None
        self.threshold = None  #阈值
        self.width = None
        self.height = None
        self.driver=driver

    @property
    def center_x(self):return self.x + int(self.width / 2) if self.x and self.width else None

    @property
    def center_y(self):return self.y + int(self.height / 2) if self.y and self.height else None


    def find_me(self,img_path):
        #查看图片格式
        try:
            imghdr.what(img_path)
        except FileNotFoundError as e:
            print('图片文件未发现:' + img_path)
            raise e
        # cv2.imread()接口读图像 直接返回numpy.ndarray 对象，读进来直接是BGR 格式数据格式在 0~255，通道格式为(W,H,C)
        img = cv2.imread(img_path)  # [width,height,3]
        self.height = img.shape[0]  # 高
        self.width = img.shape[1]   # 宽
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
                              cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),#模版图
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
        img_hist = cv2.calcHist([img], [0, 1, 2], None,
                                [8, 8, 8], [0, 256, 0, 256, 0, 256])
        comp_hist = cv2.compareHist(img_hist, scr_hist,
                                    cv2.HISTCMP_CORREL)

        # 保存阈值匹配：图形图像和图像直方图
        self.threshold = {'shape': round(img_match[1], 2)
                          ,'histogram': round(comp_hist, 2)}

        return scr

    def rectangle(self,path,img_path,msg):
        # 画矩形圈出识别图
        scr=self.find_me(img_path)
        s=cv2.rectangle(scr, (self.x, self.y),
                             (self.x + self.width, self.y + self.height),
                             (0, 0, 255), 2)
        #存画完的图

        cv2.imwrite(os.path.join(path,msg+'.jpg'), s)





