#coding = utf-8
import  pymysql
from utils.log import logger
from utils.config import Config



class db():

    def __init__(self,db_service):
        DB = Config().get(db_service)  #根据config.yml中的数据库终端来决定连接
        self.host = DB['host']
        self.user = DB['user']
        self.passwd = DB['passwd']
        self.port = DB['port']
        self.db = DB['db']

        config = {'host': str(self.host),
                  'user': self.user,
                  'passwd': self.passwd,
                  'port': int(self.port),
                  'db': self.db}

        try:
            self.database = pymysql.connect(**config)  #数据库连接  **config将字典转化为字符串host='',user=''....
            self.cursor = self.database.cursor()  # 使用cursor()方法获取操作游标
        except Exception as e:
            logger.error("数据库连接失败"+str(e))


    def execute_sql_select(self,sql):  #仅查询
        self.cursor.execute(sql)

    def execute_sql_others(self,sql):  #修改、删除、插入数据等
        self.cursor.execute(sql)
        self.database.commit()
        self.database.close()

    def fetchAll(self):
        resultsAll = self.cursor.fetchall()  # 一行多值 使用for循环取出row[0]，如下代码 结果都是元祖，可以使用re.findall(正则)[0] 取具体值
        self.database.close()
        return resultsAll


    def fetchOne(self):
        resultsOne = self.cursor.fetchone()  # 一个值
        self.database.close()
        return resultsOne

    def fetchCount(self):   #rowCount统计条数
        resultsCount = self.cursor.rowcount
        self.database.close()
        return  resultsCount

