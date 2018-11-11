from selenium.webdriver.common.by import By
from UI_pc.page.baidu_main_page import BaiDuMainPage
from UI_pc.common.Basepage import BasePage
from utils.config import Img_path_cv
import os

class BaiDuResultPage(BasePage):

    #--------------selenium---------------
    loc_result_links = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    item = 'pc_baidu'
    page = '百度结果页'
    element1 = '12345图标'

    backgroundXpath = '/html/body'

    loc_result = os.path.join(Img_path_cv, item, page, element1 + '.png')
    def result_links(self):

        print("进入结果页")




