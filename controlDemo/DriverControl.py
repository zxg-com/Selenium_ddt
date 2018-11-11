# from selenium import webdriver as driver1
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
#
# from appium import webdriver as driver2
# from appium.webdriver.common.touch_action import TouchAction
# import subprocess,sys,time,os
#
#
# #=====================================================
# #             ○  硬件控制，元素识别等 ○               #
# #=====================================================
# # 测试用例中所需的动作控制
# class WebControl(Base.Func_suite):
#     def __init__(self):
#         super().__init__()
#     def selenium_start(self):
#         for pa in (info.mapath, info.backpath, info.elementpath, info.resulthandle, info.temppath):
#             self.isExists(pa)
#         url=info.url
#         self.driver = driver1.Chrome()
#         self.driver.get(url)
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(4)
#     def screenshot(self, PicPath, PicName):
#         self.driver.save_screenshot(PicPath + PicName)
#     def click(self, x,y):
#         actions = ActionChains(self.driver)
#         el = self.driver.find_element_by_xpath(info.body)
#
#         actions.move_to_element_with_offset(el, x, y).perform()
#         actions.move_by_offset(0, offsetY).click().perform()
#         self.driver.implicitly_wait(6)
#     def sendkeys(self,x,y,msg,type):
#         actions = ActionChains(self.driver)
#         el = self.driver.find_element_by_xpath(info.body)
#         actions.move_to_element_with_offset(el, x, y).perform()
#         actions.move_by_offset(0, offsetY).click().perform()
#         actions.send_keys(msg).perform()
#         if type == "Sendkeys_B":
#             for i in range(1, 20):
#                 actions.send_keys(Keys.ESCAPE).perform()
#
#         self.driver.implicitly_wait(4)
#     def pressdown(self,x,y):
#         actions = ActionChains(self.driver)
#         el = self.driver.find_element_by_xpath(info.body)
#         actions.move_to_element_with_offset(el, x, y).perform()
#         actions.move_by_offset(0, offsetY).click().perform()
#         print("3333")
#         for i in range(1, 10):
#             actions.send_keys(Keys.DOWN).perform()
#         self.driver.implicitly_wait(4)
#     def scrolldown(self,value):
#         global offsetY
#         js = "var q=document.documentElement.scrollTop={}".format(value)
#         self.driver.execute_script(js)
#         offsetY +=value
#         time.sleep(2)
#     def scrollup(self):
#         js = "var q=document.documentElement.scrollTop=0"
#         self.driver.execute_script(js)
#         time.sleep(2)
#     def alertok(self):
#         try:
#            self.driver.switch_to.alert.accept()
#         except:
#             pass
#     def alertdis(self):
#         self.driver.switch_to.alert.dismiss()
#     def upload(self,x,y,file):
#             self.click(x,y)
#             time.sleep(1)
#             dialog = win32gui.FindWindow('#32770', '打开')  # 对话框
#             ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
#             ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
#             Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
#             button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
#             print(file)
#             win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, file)  # 往输入框输入绝对地址
#             win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
# class AndroidControl(Base.Func_suite):
#     def __init__(self):
#         super().__init__()
#
#     ######################################框架操作##########################################
#     """执行CMD，初始化框架缓存"""
#
#     def appium_start(self):
#         subprocess_call(info.AndroidStartcmd, shell=True)
#         for pa in (info.mapath, info.backpath, info.elementpath, info.resulthandle, info.temppath):
#             self.isExists(pa)
#         self.desired_caps = info.desired_caps
#         self.app = driver2.Remote('http://localhost:4723/wd/hub', self.desired_caps)
#         time.sleep(3)
#
#     """清理CMD"""
#
#     def appium_stop(self):
#         subprocess_call(info.AndroidEndcmd, shell=True)
#         ######################################手机操作##########################################
#
#     """点击屏幕坐标"""
#
#     def click(self, TP):
#         action = TouchAction(self.app)
#         action.press(x=int(TP[0]), y=int(TP[1])).wait(100).release().perform()
#
#     """传入参数，输入文字
#        SandkeysA 类型 直接输入信息
#        SandkeysB 类型 清空输入框 再输入"""
#
#     def sendkeys(self, TP, type,msg,devices):
#         action = TouchAction(self.app)
#         action.press(x=int(TP[0]), y=int(TP[1])).wait(200).release().perform()
#         if type == "Sendkeys_B":
#             self.app.press_keycode(123)
#             for i in range(1, 20):
#                 self.app.press_keycode(67)
#         cmd = '''adb -s %s shell am broadcast -a ADB_INPUT_TEXT --es msg "%s"''' % (devices,msg)
#         subprocess_call(cmd, shell=True)
#
#     """向上滑动屏幕 如：swipeUp(1000) 输入滑动距离"""
#
#     def swipeUp(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.5)  # x坐标
#         y1 = int(l[1] * 0.75)  # 起始y坐标
#         y2 = int(l[1] * 0.25)  # 终点y坐标
#         self.app.swipe(x1, y1, x1, y2, t)
#
#     """向下滑动屏幕"""
#
#     def swipeDown(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.5)  # x坐标
#         y1 = int(l[1] * 0.25)  # 起始y坐标
#         y2 = int(l[1] * 0.75)  # 终点y坐标
#         self.app.swipe(x1, y1, x1, y2, t)
#
#     """向左滑动屏幕"""
#
#     def swipeLeft(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.75)
#         y1 = int(l[1] * 0.5)
#         x2 = int(l[0] * 0.05)
#         self.app.swipe(x1, y1, x2, y1, t)
#
#     """向右滑动屏幕"""
#
#     def swipeRight(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.05)
#         y1 = int(l[1] * 0.5)
#         x2 = int(l[0] * 0.75)
#         self.app.swipe(x1, y1, x2, y1, t)
#
#     """模拟点击BACK键"""
#
#     def back(self):
#         self.app.keyevent(4)
#         time.sleep(0.5)
#
#     """实时截图
#        参数1 截图文件名，参数2 截图路径"""
#
#     def screenshot(self, PicPath, PicName):
#         self.app.save_screenshot(PicPath + PicName)
#
#     """获取桌面size"""
#     def getSize(self):
#         x = self.app.get_window_size()['width']
#         y = self.app.get_window_size()['height']
#         return (x, y)
# class AndroidControl2(Base.Func_suite):
#     def __init__(self):
#         super().__init__()
#     ######################################框架操作##########################################
#     """执行CMD，初始化框架缓存"""
#
#     def appium_start(self):
#         subprocess_call(info.AndroidStartcmd, shell=True)
#         for pa in (info.mapath, info.backpath, info.elementpath, info.resulthandle, info.temppath):
#             self.isExists(pa)
#         self.desired_caps = info.desired_caps1
#         self.app = driver2.Remote('http://localhost:4726/wd/hub', self.desired_caps)
#         time.sleep(3)
#
#     """清理CMD"""
#
#     def appium_stop(self):
#         subprocess_call(info.AndroidEndcmd, shell=True)
#         ######################################手机操作##########################################
#
#     """点击屏幕坐标"""
#
#     def click(self, TP):
#         action = TouchAction(self.app)
#         action.press(x=int(TP[0]), y=int(TP[1])).wait(100).release().perform()
#
#     """传入参数，输入文字
#        SandkeysA 类型 直接输入信息
#        SandkeysB 类型 清空输入框 再输入"""
#
#     def sendkeys(self, TP, type,msg,devices):
#         action = TouchAction(self.app)
#         action.press(x=int(TP[0]), y=int(TP[1])).wait(200).release().perform()
#         if type == "Sendkeys_B":
#             self.app.press_keycode(123)
#             for i in range(1, 20):
#                 self.app.press_keycode(67)
#         cmd = '''adb -s %s shell am broadcast -a ADB_INPUT_TEXT --es msg "%s"''' % (devices,msg)
#         subprocess_call(cmd, shell=True)
#
#     """向上滑动屏幕 如：swipeUp(1000) 输入滑动距离"""
#
#     def swipeUp(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.5)  # x坐标
#         y1 = int(l[1] * 0.75)  # 起始y坐标
#         y2 = int(l[1] * 0.25)  # 终点y坐标
#         self.app.swipe(x1, y1, x1, y2, t)
#
#     """向下滑动屏幕"""
#
#     def swipeDown(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.5)  # x坐标
#         y1 = int(l[1] * 0.25)  # 起始y坐标
#         y2 = int(l[1] * 0.75)  # 终点y坐标
#         self.app.swipe(x1, y1, x1, y2, t)
#
#     """向左滑动屏幕"""
#
#     def swipeLeft(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.75)
#         y1 = int(l[1] * 0.5)
#         x2 = int(l[0] * 0.05)
#         self.app.swipe(x1, y1, x2, y1, t)
#
#     """向右滑动屏幕"""
#
#     def swipeRight(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.05)
#         y1 = int(l[1] * 0.5)
#         x2 = int(l[0] * 0.75)
#         self.app.swipe(x1, y1, x2, y1, t)
#
#     """模拟点击BACK键"""
#
#     def back(self):
#         self.app.keyevent(4)
#         time.sleep(0.5)
#
#     """实时截图
#        参数1 截图文件名，参数2 截图路径"""
#
#     def screenshot(self, PicPath, PicName):
#         self.app.save_screenshot(PicPath + PicName)
#
#     """获取桌面size"""
#     def getSize(self):
#         x = self.app.get_window_size()['width']
#         y = self.app.get_window_size()['height']
#         return (x, y)
#
#
# class IOSControl(Base.Func_suite):
#     def __init__(self):
#         super().__init__()
#
#     ######################################框架操作##########################################
#     """执行CMD，初始化框架缓存"""
#     def appium_start(self):
#         for pa in (info.mapath, info.backpath, info.elementpath, info.resulthandle, info.temppath):
#             self.isExists(pa)
#         self.desired_caps = info.desired_caps
#         self.app = driver2.Remote('http://localhost:4723/wd/hub', self.desired_caps)
#         time.sleep(3)
#     ######################################手机操作##########################################
#     """点击屏幕坐标"""
#     def click(self, TP):
#         action = TouchAction(self.app)
#         action.press(x=int(TP[0]), y=int(TP[1])).wait(100).release().perform()
#
#     """传入参数，输入文字
#        SandkeysA 类型 直接输入信息
#        SandkeysB 类型 清空输入框 再输入"""
#     def sendkeys(self, TP, type, msg):
#         action = TouchAction(self.app)
#         action.press(x=int(TP[0]), y=int(TP[1])).wait(200).release().perform()
#         if type == "Sendkeys_B":
#             self.app.press_keycode(123)
#             for i in range(1, 20):
#                 self.app.press_keycode(67)
#         cmd = '''adb shell am broadcast -a ADB_INPUT_TEXT --es msg "%s"''' % msg
#         # subprocess_call(cmd, shell=True)
#
#     """传入参数，输入文字"""
#     def sendkeysOfIOS(self, number, value):
#         try:
#            list = self.app.find_elements_by_class_name("XCUIElementTypeTextField")
#            list[number].send_keys(value)
#         except:
#            pass
#
#     """传入参数，输入文字"""
#     def sendkeysOfPass(self, number, value):
#         try:
#            list = self.app.find_elements_by_class_name("XCUIElementTypeSecureTextField")
#            list[number].send_keys(value)
#         except:
#            pass
#
#     """传入参数，输入文字"""
#     def sendkeysOfValidCode(self, number, value):
#         try:
#            list = self.app.find_elements_by_class_name("XCUIElementTypeStaticText")
#            list[number].send_keys(value)
#         except:
#            pass
#
#     """传入参数，点击操作"""
#     def clickOfButton(self, number):
#         try:
#            list = self.app.find_elements_by_class_name("XCUIElementTypeButton")
#            list[number].click()
#         except:
#            pass
#
#     """IOS滑动操作"""
#     def swipeUpOfIOS(self, fromY ,fromX):
#         try:
#            self.app.execute_script('mobile: dragFromToForDuration',
#                               {'duration': 0, 'fromX': 374, 'fromY': fromY, 'toX': 374, 'toY': fromX})
#         except:
#            pass
#
#     """向上滑动屏幕 如：swipeUp(1000) 输入滑动距离"""
#     def swipeUp(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.5)  # x坐标
#         y1 = int(l[1] * 0.75)  # 起始y坐标
#         y2 = int(l[1] * 0.25)  # 终点y坐标
#         self.app.swipe(x1, y1, x1, y2, t)
#
#     """向下滑动屏幕"""
#     def swipeDown(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.5)  # x坐标
#         y1 = int(l[1] * 0.25)  # 起始y坐标
#         y2 = int(l[1] * 0.75)  # 终点y坐标
#         self.app.swipe(x1, y1, x1, y2, t)
#
#     """向左滑动屏幕"""
#     def swipeLeft(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.75)
#         y1 = int(l[1] * 0.5)
#         x2 = int(l[0] * 0.05)
#         self.app.swipe(x1, y1, x2, y1, t)
#
#     """向右滑动屏幕"""
#     def swipeRight(self, t):
#         l = self.getSize()
#         x1 = int(l[0] * 0.05)
#         y1 = int(l[1] * 0.5)
#         x2 = int(l[0] * 0.75)
#         self.app.swipe(x1, y1, x2, y1, t)
#
#     """模拟点击BACK键"""
#     def back(self):
#         self.app.keyevent(4)
#         time.sleep(0.5)
#
#     """实时截图
#        参数1 截图文件名，参数2 截图路径"""
#     def screenshot(self, PicPath, PicName):
#         self.app.save_screenshot(PicPath + PicName)
#
#     """获取桌面size"""
#     def getSize(self):
#         x = self.app.get_window_size()['width']
#         y = self.app.get_window_size()['height']
#         return (x, y)
#
