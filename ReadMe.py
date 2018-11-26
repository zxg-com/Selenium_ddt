
from utils.config import Config, DATA_PATH, REPORT_PATH
import json
from utils.file_reader import ExcelReader


"""
#====================================YAML====================================
from utils.config import Config,DATA_FILE
#Config(‘yaml路径’)  yml文件路径，默认取得是Config.yml
#调用yaml一级内容 DIRT
f=Config().get('EMAIL')
print(f)
#调用yaml二级内容 str\list\dirt
p=Config(DATA_FILE).get('PARAM').get('consultationId')
print(p)

#数据存入yaml文件【PARAM】里  有个问题：存入后是utf-8乱码，但取出来显示没问题
from utils.config import Config
Config(DATA_FILE).set('imkey','ccc')

#=====================================EXCEL ====================================
from utils.file_reader import ExcelReader,YamlReader
from utils.config import Config, DATA_PATH,DATA_FILE

excelpath = DATA_PATH + '/API.xlsx'  # excel路径
sheet = ExcelReader(excelpath, sheetname='API')  # 创建对象（表路径，分表名称）
L = sheet.rowsvalue(rowname=self.case_name)  # 根据行第一列的值，取整行的内容
#调用excel具体位置值   STR
f=sheet.cellvalue(1,5)
print(f)

====================================excel+ddt==============================
from utils.file_reader import ExcelReader
from utils.config import DATA_PATH
excelpath=DATA_PATH + '//API.xlsx'
ecl=ExcelReader(excelpath,'API').get_ddtvalue()
print(*ecl)

===================================excel写入数据===========================
#写入excel
from utils.file_reader import ExcelReader
from utils.config import DATA_PATH

ecel_path=DATA_PATH + "/keyword.xls"

e=ExcelReader(excelpath=ecel_path,sheetname='keywords')  #表名，sheet名
e.write_values(row=7,value='test')    # row，col坐标  ，value值

#=====================================ini读取====================================
from utils.file_reader import Readini

s=Readini().get(item='EMAIL',name='name')     #取
Readini().set(item='HEADERS',name='content-type',value='json')  #存
print(s)

#=====================================xml读取====================================

from utils.file_reader import XMLReader
xml=XMLReader().get_url_from_xml(itemsname='url',name="login")  #itemname一级名字 #name二级名字
print(xml)

#=====================================email发送报告====================================
#【config.yml】
EMAIL:
  title: 测试报告
  message: 测试报告见附件！
  password: zxg680210
  receiver: 342509492@qq.com   #收件人多个时，直接分号；隔开即可
  sender: zxg_com@163.com
  server: smtp.163.com

#调用邮件发送
from utils.mail import Email
report=REPORT_PATH+'/report.html'  #附件路径
e = Email(path=report)  # path附件，可以是多个附件，以list形式传入即可   其余内容已经封装进入email，邮件相关配置存储在config.yml中
e.send()


#====================================MySql ====================================
from utils.executeSql import db

#【comfig.yml】
DB_huizhen:
  host: wwwhuizhen.mysql.rds.aliyuncs.com
  user: ceshi
  passwd: (Djf9#8d
  port: 3317
  db: tocure_platform


sql="select * from tocure_customer_send_code order by confirm_time desc"
d=db(db_service='DB_huizhen')  #config_yml中数据库连接项名称，可根据输入的连接项名称切换数据库连接，子库较多时，定义多个子库即可
d.execute_sql_select(sql)
sqlresult=d.fetchOne()
print(type(sqlresult[9]))



#====================================调用接口测试client====================================
# 所有数据均来自excel
# 定义了cookie获取方法，调用后可以获取请求响应返回的cookies，可带入其他接口测试中

#参数值动态获取的，可以在excel中直接写成"consultationId":kwargs['consultationId']，通过调用send（）方法时直接传入参数即可send（consultationId=consultationId）
 
cookies= com_module.login_pc() #cookies
self.client = HTTPClient(self.case_name,cookies=cookies)  #有cookies传cookies
self.res = self.client.send(consultationId=consultationId) #自定义参数传入kwargs[]
Cookies=client.get_Cookies() #获取登录后的cookies 用作下一个接口传入

#======================================unittest ddt+excel 数据驱动模式============================================================

from utils.file_reader import ExcelReader
from utils.config import DATA_PATH
excelpath=DATA_PATH + '//API.xlsx'
ecl=ExcelReader(excelpath,'API').get_ddtvalue()
import ddt
import unittest


@ddt.ddt
class A(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @ddt.data(*ecl)

    def test(self, data):
        print(*ecl)

        print(data[1])


if __name__ == '__main__':
    unittest.main()


=======================================================================================================================

po:
1、抽象封装一个BasePage基类，基类应该拥有一个指向webdriver实例的属性
2、每一个Page都应该继承BasePage,并通过driver来管理本Page的元素，且将Page才操作都封装成一个个的方法
3、TestCase应该继成unittest.Testcase类，并依赖相应的Page类来实现相应的test step（即测试步骤）



1.unittest知识点每个方法名字前加test即可执行

2unittest知识点 setup()、teardown()，每个test用例方法执行前后都会调用该方法

3.unittest知识点 如果想让setup()和teardown()只执行一次，需要用到装饰器
@classmethod
def setUpClass(cls):
    pass
def tearDownClass(cls):
    pass
    
4.unittest单文件容器加载组件
import unittest
if __name__ == '__main__':
    suite=unittest.TestSuite
    suite.addTest(文件名（'方法名1'）)
    suite.addTest(文件名（'方法名2'）)
    unittest.TextTestRunner.run()
    
5.unittest跳过执行case方法
在方法前添加 @unittest.skip("描述信息随便写")

@unittest.skip("描述信息随便写") #跳过case02的执行
def testcase02：
    pass


6.unittest批量执行用例（多文件）
suite=unittest.defaultTestLoader.discover(start_dir='case路径文件夹',pattern='test_*.py')
unittest.TextTestRunner.run(suite)

unittest断言
7.assert(x,x,msg) #msg可以作为断言的自定义文案
assertEqual(a, b) 
判断a==b
assertNotEqual(a, b)
判断a！=b
assertTrue(x)
bool(x) is True
assertFalse(x)
bool(x) is False
assertIs(a, b)
a is b
assertIsNot(a, b)
 a is not b
assertIsNone(x)
 x is None
assertIsNotNone(x)
x is not None
assertIn(a, b) 
a in b
assertNotIn(a, b)
a not in b
assertIsInstance(a, b)
isinstance(a, b) 
assertNotIsInstance(a, b) 
not isinstance(a, b) 

8 html报告+unittest组件

suite=unittest.defaultTestLoader.discover(start_dir='case路径文件夹',pattern='test_*.py')
unittest.TextTestRunner.run(suite)

report=REPORT_PATH + "\report_uitest.html"
f= open(report,'wb')
runner=HTMLTestReportCN.HTMLTestRunner(stream=f,title='标题',description='描述',verbosity=2)
runner.run(suite)
f.close()


9。html报告截图功能

================================================关键字驱动======================================







=============================================方法函数 反射 getattr================================
def run_method(Object,mehtod):   #传入类名 和 方法名字符串
    obj=Object()
    mehtods = getattr(obj,mehtod)
    mehtods()           #执行函数
    

=================================================================================================
"""
