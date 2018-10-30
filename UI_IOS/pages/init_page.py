# coding:utf-8

'''
description:登录页
'''
from UI_IOS.common import Base_page
from appium.webdriver.common import mobileby
from utils.config import Img_path_cv
import os

class Init_page(Base_page.Base_page):



    # --------图形定位-------
    item = 'app_android_allinmd'
    page = '首页'
    update_btn='立即更新.png'

    loc_update_btn = os.path.join(Img_path_cv, item, page, update_btn )

