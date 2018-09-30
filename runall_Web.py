import unittest
import os
from utils.HTMLTestReportCN import HTMLTestRunner
from utils.config import REPORT_PATH,UICASE_FILE
from utils.mail import Email
from utils.log import logger
import datetime

class RunAll():
    def __init__(self):
        self.caseListFile = os.path.join(UICASE_FILE,'suite', "caselist.txt")  # 用例汇总
        self.caseFile = os.path.join(UICASE_FILE,'case')  # 用例路径
        self.caseList = []
        # report = REPORT_PATH + '/report.html'
        # e = Email()
        # e.send()

    def set_case_list(self):
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self):
        self.set_case_list()  # 汇总case，形成list[case1,case2....]
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1] #取出指定的case名
            print(case_name + ".py")
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None) #从指定文件夹读用例
            suite_module.append(discover)  #取到所有要跑的case形成list[case1类/方法，case2类/方法......]

        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)#加入unittest组件里
        else:
            return None
        return test_suite

    def run(self):
        suite=self.set_case_suite()
        report = REPORT_PATH + "//UItestReport" + datetime.datetime.now().strftime("%Y%m%d-%H%H%S")  + ".html"
        try:

            if suite is not None:
                logger.info("*****开始执行测试*****")
                with open(report,'wb') as f:
                    runner = HTMLTestRunner(f, verbosity=2, title='UI测试报告', description='UI测试报告',tester='UI自动化测试')
                    runner.run(suite)
                f.close()
            else:
                logger.info("error：*****没发现测试用例*****")
        except Exception as ex:
            logger.error(ex)
            raise
        finally:
            logger.info("******测试结束******")
            #e = Email(path=report)  # 发邮件
            #e.send()

if __name__ == '__main__':
    RunAll().run()

