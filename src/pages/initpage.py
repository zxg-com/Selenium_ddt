import os
from src.common.Base_page import Base_page
from utils.config import Img_path_cv
from appium.webdriver.common import mobileby

class InitPage(Base_page):
    #--------appium------
    # by=mobileby.By
    # skip_btn=(by.ID,'com.allin.social:id/kn')
    #
    # def click_skip(self):
    #     self.click_button(*self.skip_btn)


    #--------图形定位-------
    item = 'app_android_allinmd'
    page = '首次开屏页'
    skip_btn = '跳过'

    loc_skip_btn = os.path.join(Img_path_cv, item, page, skip_btn + '.png')


    def click_skip_btn(self):
        self.Android_control(msg='跳过按钮',img=self.loc_skip_btn,method='点击',value=None)
