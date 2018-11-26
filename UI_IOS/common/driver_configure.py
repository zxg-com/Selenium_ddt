#coding:utf-8
'''
description:driver配置
'''
from appium import webdriver
from utils.config import PACKAGE_PATH,Config,DRIVER_PATH

import time



class driver_configure:



    def IOSdriver(self):  #默认一个设备，自动获取devicesUUID
        '''获取driver'''
        try:
            #z执行appium语句



            package_path = PACKAGE_PATH + '/AllinmdIPhone.ipa'

            self.desired_caps1 = {}
            self.desired_caps1['platformName'] = 'Ios'  # 设备系统
            self.desired_caps1['platformVersion'] = '11.3.1'  # 设备系统版本
            self.desired_caps1['deviceName'] = 'iPhone'  # 设备名称
            self.desired_caps1["bundleId"] = "com.allinmd.socialapp"  #包名
            self.desired_caps1['autoAcceptAlerts']="true"  #弹窗默认跳过
            #self.desired_caps1['app'] = package_path
            self.desired_caps1['udid'] = "auto"   # devices
            self.desired_caps1['automationName'] = 'XCUITest'
            self.desired_caps1['noReset'] = 'True' #是否重置
            self.desired_caps1['newCommandTimeout'] = '6000' #超时时间
            self.desired_caps1['clearSystemFiles'] = 'true'
            # self.driver = webdriver.Remote("127.0.0.1:"+port+"/wd/hub", self.desired_caps1)
            self.driver = webdriver.Remote("127.0.0.1:4723/wd/hub", self.desired_caps1)
            return self.driver
        except Exception as  e:
            raise e


if __name__ == '__main__':
    dr=driver_configure()
    dr.IOSdriver()

