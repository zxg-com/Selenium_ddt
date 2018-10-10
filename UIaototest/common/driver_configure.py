##coding:utf-8
'''
description:driver配置
'''
import time
import os
from selenium import webdriver
from utils.config import DRIVER_PATH, REPORT_PATH
from utils.file_reader import Readini
import re
import datetime
from utils.log import logger



# 驱动路径
CHROMEDRIVER_PATH = DRIVER_PATH + '/chromedriver.exe'
IEDRIVER_PATH = DRIVER_PATH + '/IEDriverServer.exe'
FIREFOXDRIVER = DRIVER_PATH + '/geckodriver'
SAFARIDRIVER=DRIVER_PATH + '/safaridriver'
EDGEDRIVER=DRIVER_PATH + '/edgedriver.exe'

TYPES = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome, 'ie': webdriver.Ie,'safari':webdriver.Safari ,'edge':webdriver.Edge}
EXECUTABLE_PATH = {'firefox': FIREFOXDRIVER, 'chrome': CHROMEDRIVER_PATH, 'ie': IEDRIVER_PATH ,'safari':SAFARIDRIVER,'edge':EDGEDRIVER}





class Driver_configure():
    def __init__(self,browser_type="firefox"):
        self._type = browser_type.lower()
        '''获取driver'''
        if self._type in TYPES:
            self.browser = TYPES[self._type]
        else:
            logger.info('仅支持%s!' % ','.join(TYPES.keys()))

    def get_driver(self):
        try:
            self.driver = self.browser(executable_path=EXECUTABLE_PATH[self._type])
            return self.driver
        except Exception as  e:
            logger.error(e)