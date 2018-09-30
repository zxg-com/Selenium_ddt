from selenium.webdriver.common.by import By
from UIaototest.common.Basepage import BasePage
from utils.file_reader import Readini,ExcelReader
from utils.config import DATA_PATH
from utils.log import logger


class BaiDuMainPage(BasePage):
    # loc_search_input = ('id', 'kw')
    # loc_search_button = ('id', 'su')
    ecl_path = DATA_PATH + '//API.xls'
    ecl = ExcelReader(excelpath=ecl_path, sheetname='元素')


    loc_search_input = (ecl.rowsvalue(rowname='搜索输入框')[2],ecl.rowsvalue(rowname='搜索输入框')[3])
    loc_search_button= (ecl.rowsvalue(rowname='搜索按钮')[2],ecl.rowsvalue(rowname='搜索按钮')[3])




        #输入搜索词
    def inputl(self,kw):
        in_put=self.find_element(*self.loc_search_input)
        in_put.clear()
        in_put.send_keys(kw)
        logger.info('搜索输入框输入内容')

    def but_click(self):
        #点击搜索按钮
        button=self.find_element(*self.loc_search_button)
        button.click()
        logger.info('点击搜索按钮')

