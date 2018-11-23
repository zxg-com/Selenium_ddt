# coding:utf-8
#获取设备信息
from UI_Android.devices.doc_cmd import Doc_cmd
import threading
from utils.file_reader import Readini,YamlReader
from utils.config import DRIVER_PATH
from utils.config import Config
import time


class Server:
    def __init__(self):
        self.dos = Doc_cmd()
        self.devices_list=self.get_devices()
        evpath = DRIVER_PATH + '/Android_environment.yml'
        self.yaml = YamlReader(evpath)
    #设备list
    def get_devices(self):
        '''
        获取设备信息
        :return: 
        '''
        devices_list=[]
        result_list = self.dos.excute_cmd_result('adb devices')
        #执行结果['List of devices attached', '2ed0d2f3\tdevice', 'c824d603\tdevice', '']
        #['List of devices attached', '']
        #默认为空是就是2，所以要写成3
        if len(result_list)>=3:
            for i in  result_list:
                if i !="":
                    if 'List' in i:
                        continue
                    else:
                        devices_info = i.split('\t')  #\t分割设备名和设备类型
                        if i.split('\t')[1]:
                            devices_list.append(i.split('\t')[0])
            return devices_list
        else:
            return None

    #检测端口是否可用，可用直接创建端口list
    def port_is_used(self,number):
        '''
        判断端口number是否被占用
        :return: 
        '''
        self.dos = Doc_cmd()
        #result=self.dos.excute_cmd_result('netstat -ano | findstr '+str(number))  #windows下端口占用
        result=self.dos.excute_cmd_result('lsof -i:'+str(number))    #mac/linux下检查端口占用

        if len(result)>0:
            flag=False
        else:
            flag=True
        return flag


    def create_port_list(self,start_port):
        '''
        生成可用端口list前，需检查port是否可用
        :param start_port:  
        :return: port_list
        '''
        port_list=[]  #端口个数由设备个数决定
        devices_list=self.get_devices()
        if devices_list :
            while len(port_list)!=len(devices_list):
                if self.port_is_used(start_port) == True:
                    port_list.append(start_port)
                start_port=start_port+1
            return port_list
        else:
            print("生成可用端口失败")
            return None

    #命令appium
    def crete_command_list(self,i):
        '''
        生成命令行list，多个设备多个命令行
        #appium -p 4700 -bp 4701 -U 设备devicesName
        :return: command_list 根据设备数量决定
        '''
        port=Config().get('EVIORMENT').get('port')
        b_port=Config().get('EVIORMENT').get('bp')
        command_list = []
        appium_port_list = self.create_port_list(int(port))  #监听端口list
        bootstrap_port_list = self.create_port_list(int(b_port))  #链接安卓端口list

        # for i in  range(len(self.devices_list)):
            #命令
        command = "appium -p "+ str(appium_port_list[i]) + " -bp "+str(bootstrap_port_list[i]) + " -U "+self.devices_list[i] + "  --session-override"+'\n'
        #-p  监听端口
        #-bp  是连接Android设备bootstrap的端口号，默认是4724
        #-U 链接设备名称
        #--session-override是指覆盖之前的session
        #--no-reset   每次启动不重启
        command_list.append(command)
        #写入yaml
        deviceInfo ={"device"+str(i):{'port':str(appium_port_list[i]),'deviceName':str(self.devices_list[i]),'bp':str(bootstrap_port_list[i])}}

        self.yaml.write_data(data=deviceInfo)

        return command_list


    def kill_server(self):
        '''
        杀掉appium进程
        :return: 
        '''
        #获取进程列表
        #server_list = self.dos.excute_cmd_result('tasklist | find "node.exe"') #windows查看进程
        server_list = self.dos.excute_cmd_result('ps aux | grep node') #mac/linux查看进程
        if len(server_list)>0:
            #self.dos.excute_cmd('taskkill -F -PID node.exe') #windows杀掉进程
            self.dos.excute_cmd_mac('killall node') #mac 杀进程
            print('node进程清理完毕')
        else:
            pass

    # 执行 创建好的命令list
    def start_server(self, i):
        self.start_list = self.crete_command_list(i)
        print("执行命令： " + self.start_list[0])
        self.dos.excute_cmd_mac(self.start_list[0])


    #主要函数 多进程调用启动方法
    def main(self):
        '''
        多线程启动appium
        :return: 
        '''
        #清理yaml里创建成功的设备信息
        self.yaml.clear_yaml()
        #先杀掉进程,清理环境
        self.kill_server()
        time.sleep(2)
        try:
            thread_list=[]
            for i in  range(len(self.devices_list)):

                appium=threading.Thread(target=self.start_server,args=(i,))
                thread_list.append(appium)

            for t in thread_list:
                t.start()
                time.sleep(10)
                print("该进程启动成功")

        except Exception as ex:
            print('请检查设备列表是否为空')

if __name__ == '__main__':
    server=Server()
    #print(server.get_devices())
    #print(server.create_port_list(4720))
    #print(server.crete_command_list())
    #server.kill_server()
    server.main()
