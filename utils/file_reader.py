#coding:utf-8
#********配合config读取yaml配置文件的读取及存储
#**********读取excel文件内容
import yaml
import os
from xlrd import open_workbook
from xlutils.copy import copy
import os
import codecs
import configparser
from xml.etree import ElementTree as ElementTree

#yaml文件读取
class YamlReader:
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property #当做属性调用 get方法可以连续调用
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load后是个generator，用list组织成列表
                f.close()
        return self._data


    def set_data(self,param,value,index_name):
        with open(self.yamlf, "rb", ) as f:
            data = dict(yaml.safe_load(f))
        data[index_name][param] = value   #更新data，添加加字典键和值
        f.close()
        # 将更新后的data写档
        with open(self.yamlf, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False)  # indent:缩进 block_seq_indent:区块缩
        f.close()

    def write_data(self,data):
        with open(self.yamlf,"a") as  f:
            yaml.dump(data,f)
        f.close()

    def clear_yaml(self):
        with open(self.yamlf, "w") as  f:
            f.truncate()  #清理文件
        f.close()



#excel文件读取
class ExcelReader:

    def __init__(self, excelpath,sheetname):
        if os.path.exists(excelpath):
            self.excelpath = excelpath
            self.f = open_workbook(self.excelpath)
            self.sheet = self.f.sheet_by_name(sheetname)
        else:
            raise FileNotFoundError('excel文件不存在！')
        self._data = []

    #取某一行的值list
    def rowsvalue(self,rowname):
        for i in range(1,self.sheet.nrows):
            self._data.append(self.sheet.row_values(i))
        for x in range(len(self._data)):
            if self._data[x][0] == str(rowname):
                 return self._data[x]


    #取固定单元格位置的值
    def cellvalue(self,rownum,colnum):
        cell=self.sheet.cell(rownum,colnum).value
        return cell


     #取出表内容，配合ddt使用 ddt.data(*cls)
    def get_ddtvalue(self):
        cls = []
        # 逐行获取内容
        nrows = self.sheet.nrows
        cols = self.sheet.ncols
        #按行取值
        for i in range(1,nrows):
            # 首行不获取,用首行首列的字符来区分 目前是case_name
            cls.append(self.sheet.row_values(i))
        return cls

     #写入excel数据  用xlutils
    def write_values(self,row,value,col=11):
        read_value=open_workbook(self.excelpath)  #必须每次都这么调用，不能写成self.f，那样只能写一次，需要写一次打开一次最新的excel文件
        write_data=copy(read_value)
        write_data.get_sheet(0).write(row,col,value)
        write_data.save(self.excelpath)




#ini读写

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_INI = os.path.join(BASE_PATH, 'config', 'config.ini')


class Readini():
    def __init__(self,path=CONFIG_INI):
        fd = open(path)
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(path, "w")
            file.write(data)
            file.close()
        fd.close()
        #初始化对象
        self.cf = configparser.ConfigParser()
        #读取配置文件
        self.cf.read(path)

    def get(self, item,name):   #获取Email目录下的name
        #根据name读取内容
        value = self.cf.get(item, name)   #item是【组名】，name是参数名
        return value



    def set(self, item,name, value): #item是【组名】，name是参数名，value是参数值

        #存储
        self.cf.set(item, name, value)
        # 打开文件
        f = open(CONFIG_INI, 'w+')
        #写入
        self.cf.write(f)
        f.close()

#读xml
CONFIG_XML=os.path.join(BASE_PATH, 'config', 'config.xml')
class XMLReader:

    def get_url_from_xml(self,itemsname ,name):  #取出对应item-name的子集
        url_list = []
          # 定义路径
        ite=itemsname
        tree = ElementTree.parse(CONFIG_XML)  # 定义xml操作对象
        for u in tree.findall(ite):  # 查找所有的url标签
            url_name = u.get('name')  # 获取所有的name
            if url_name == name:  # 存在name
                for c in u.getchildren():  # 取出里面的值
                    url_list.append(c.text)

        url = '/'.join(url_list)  # 以/来拼接url_list中的元素 a/b/c
        return url