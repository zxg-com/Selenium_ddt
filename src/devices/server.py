#coding=utf-8
#获取设备信息
from src.devices.doc_cmd import Doc_cmd
import threading
from utils.file_reader import Readini


class Saerver:
    def __init__(self):
        self.dos = Doc_cmd()
    #设备list
    def get_devices(self):
        '''
        获取设备信息
        :return: 
        '''
        devices_list=[]
        result_list = self.dos.excute_cmd_result('adb devices')

        #执行结果['List of devices attached', 'c824d603\tunauthorized', '']
        #['List of devices attached', '']
        #默认为空是就是2，所以要写成3
        if len(result_list)>=3:
            for i in  result_list:
                if 'List' in i:
                    continue
                else:
                    devices_info = i.split('\t')  #\t分割设备名和设备类型
                    if devices_info[1]:
                        devices_list.append(devices_info[0])
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
    def crete_command_list(self):
        '''
        生成命令行list，多个设备多个命令行
        #appium -p 4700 -bp 4701 -U 设备devicesName
        :return: command_list 根据设备数量决定
        '''
        read_ini=Readini()
        port=read_ini.get("EVIORMENT","port")
        b_port=read_ini.get("EVIORMENT","bp")
        command_list = []
        appium_port_list = self.create_port_list(int(port))  #监听端口list
        bootstrap_port_list = self.create_port_list(int(b_port))  #链接安卓端口list
        devices_list=self.get_devices()
        for i in  range(len(devices_list)):
            #命令
            command = "appium -p "+ str(appium_port_list[i]) + " -bp "+str(bootstrap_port_list[i]) + " -U "+devices_list[i] + " --no-reset --session-override"
            #-p  监听端口
            #-bp  是连接Android设备bootstrap的端口号，默认是4724
            #-U 链接设备名称
            #--session-override是指覆盖之前的session
            #--no-reset   每次启动不重启
            command_list.append(command)
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
            #self.dos.excute_cmd('taskkill -F -PID node.exe') #存在杀掉进程
            self.dos.excute_cmd('killall node') #mac 杀进程
            print('node进程清理完毕')
        else:
            pass

    # 执行 创建好的命令list
    def start_server(self, i):
        self.start_list = self.crete_command_list()
        self.dos.excute_cmd(self.start_list[i])

    #主要函数 多进程调用启动方法
    def main(self):
        '''
        多线程启动appium
        :return: 
        '''
        #先杀掉进程,清理环境
        self.kill_server()
        command_list=self.crete_command_list()
        for i in  range(len(command_list)):
            print("执行命令："+command_list[i])
            appium = threading.Thread(target=self.start_server,args=(i,))
            appium.start()
            print("该进程启动成功")


if __name__ == '__main__':
    server=Saerver()
    #print(server.get_devices())
    #print(server.create_port_list(4720))
    #print(server.crete_command_list())
    #server.kill_server()
    #server.main()
