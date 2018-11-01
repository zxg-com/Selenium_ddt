# coding:utf-8

'''
description:driver配置
'''
from appium import webdriver
from utils.config import PACKAGE_PATH,Config,DRIVER_PATH
from UI_Android.devices.server import Server
import time



class driver_configure:



    def Androiddriver(self,i=0):  #默认一个设备，自动获取devicesUUID
        '''获取driver'''
        try:
            #z执行appium语句

            evpath = DRIVER_PATH + '/Android_environment.yml'
            port = Config(evpath).get("device"+str(i) ).get('port')
            package_path = PACKAGE_PATH + '/Allinmd_v2.5.6_auto_online.apk'

            self.desired_caps1 = {}
            self.desired_caps1['platformName'] = 'Android'  # 设备系统
            self.desired_caps1['platformVersion'] = '7.1.2'  # 设备系统版本
            self.desired_caps1['deviceName'] = 'Android'  # 华为mate10设备名称
            self.desired_caps1['app'] = package_path
            #self.desired_caps1['udid'] = "49652d02"   # devices
            self.desired_caps1['appPackage'] = 'com.allin.social'
            self.desired_caps1['automationName'] = 'Appium'
            self.desired_caps1['appActivity'] = 'com.allin.social.WelcomeActivity'
            self.desired_caps1['noReset'] = 'True'
            self.desired_caps1['newCommandTimeout'] = '600'
            self.driver = webdriver.Remote("127.0.0.1:"+port+"/wd/hub", self.desired_caps1)
            return self.driver
        except Exception as  e:
            raise e




    # def getdriver1(self,i=0):
    #     '''获取driver'''
    #     try:
    #         server=Server()
    #         server.main()
    #         time.sleep(5)
    #         self.desired_caps1 = {}
    #         evpath = DRIVER_PATH + '/Android_environment.yml'
    #         port = Config(evpath).get("device" + str(i)).get('port')
    #         package_path = PACKAGE_PATH + '/Allinmd_v2.5.6_auto_online.apk'
    #         self.desired_caps1['platformName'] = 'Android'  # 设备系统
    #         self.desired_caps1['platformVersion'] = '7.1.2'  # 设备系统版本
    #         self.desired_caps1['deviceName'] = 'Android'  # 华为mate10设备名称
    #         self.desired_caps1['app'] = package_path
    #         # self.desired_caps1['udid'] = "49652d02"   # devices
    #         self.desired_caps1['appPackage'] = 'com.allin.social'
    #         self.desired_caps1['automationName'] = 'Appium'
    #         self.desired_caps1['appActivity'] = 'com.allin.social.WelcomeActivity'
    #         self.desired_caps1['noReset'] = 'False'
    #         self.desired_caps1['newCommandTimeout'] = '600'
    #         self.driver = webdriver.Remote("127.0.0.1:" + port + "/wd/hub", self.desired_caps1)
    #
    #
    #
    #         return self.driver
    #     except Exception as  e:
    #         raise e
    #
