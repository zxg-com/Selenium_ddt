#coding:utf-8
import os
import subprocess



class Doc_cmd:

    def excute_cmd_result(self,command):
        result_list=[]
        result=os.popen(command).readlines()
        for i in  result:
            if i == '/n':
                continue
            result_list.append(i.strip('\n'))  #strip删除尾部字段
        return result_list

    def excute_cmd(self,command):
        os.system(command)

    def excute_cmd_mac(self,command):
        subprocess.Popen(command)

# if __name__ == '__main__':
#     dos = Doc_cmd()
#
#     print(dos.excute_cmd_result('adb devices'))
