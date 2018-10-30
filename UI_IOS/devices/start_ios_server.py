from UI_IOS.devices.doc_cmd import Doc_cmd
import threading
from utils.file_reader import Readini,YamlReader
from utils.config import DRIVER_PATH
from utils.config import Config
import time
import subprocess
import os

class IOS_Server:
    def __init__(self):
        self.dos = Doc_cmd()
#        self.devices_list=self.get_devices()
        evpath = DRIVER_PATH + '/Android_environment.yml'
        self.yaml = YamlReader(evpath)
        self.uuid=self.get_devices_uuid()

    def get_devices_uuid(self):
        devices_list=self.dos.excute_cmd_result('idevice_id -l')
        if len(devices_list)>0:
            return devices_list[0]
        else:
            print('设备为空，请检查USB连接')
            return None



    def build_WDA_appium(self):
        #切换路径 到WDA
        os.chdir('/usr/local/lib/node_modules/appium/node_modules/appium-xcuitest-driver/WebDriverAgent/')
        time.sleep(1)
        print('正在执行命令：xcodebuild -project WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination id=' + self.uuid + ' test')
        uuid_id='id='+self.uuid
        self.dos.excute_cmd_mac(['xcodebuild','-project','WebDriverAgent.xcodeproj','-scheme','WebDriverAgentRunner','-destination',uuid_id,'test'])
        os.chdir(os.path.split(os.path.realpath(__file__))[0])



    def clear_evior(self):
        server_list = self.dos.excute_cmd_result('ps aux | grep node')  # mac/linux查看进程
        if len(server_list) > 0:
            # self.dos.excute_cmd('taskkill -F -PID node.exe') #windows杀掉进程
            self.dos.excute_cmd('killall node')  # mac 杀进程
            self.dos.excute_cmd('killall node')
            print('node进程清理完毕')
        else:
            pass

        server_list_xcode = self.dos.excute_cmd_result('ps aux | grep xcode')  # mac/linux查看进程
        if len(server_list_xcode) > 0:
            # self.dos.excute_cmd('taskkill -F -PID node.exe') #windows杀掉进程
            self.dos.excute_cmd('killall xcodebuild')  # mac 杀进程
            self.dos.excute_cmd('killall xcodebuild')
            print('xcode进程清理完毕')
        else:
            pass




    def main(self):

        self.clear_evior()
        self.build_WDA_appium()
        print('正在执行命令：appium --session-override')
        self.dos.excute_cmd_mac(['appium','--session-override'])
        time.sleep(15)
        print('appium 已启动')




if __name__ == '__main__':
    s=IOS_Server()
    #s.clear_evior()
    s.main()
