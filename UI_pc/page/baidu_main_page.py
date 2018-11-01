from selenium.webdriver.common.by import By
from UI_pc.common.Basepage import BasePage
from utils.file_reader import Readini,ExcelReader
from utils.config import DATA_PATH
from utils.log import logger
from utils.config import Img_path_cv
import os

class BaiDuMainPage(BasePage):


#------------------------selenium---------------------------------

    # loc_search_input = ('id', 'kw')
    # loc_search_button = ('id', 'su')
    # ecl_path = DATA_PATH + '//API.xls'
    # ecl = ExcelReader(excelpath=ecl_path, sheetname='元素')
    #
    #
    # loc_search_input = (ecl.rowsvalue(rowname='搜索输入框')[2],ecl.rowsvalue(rowname='搜索输入框')[3])
    # loc_search_button= (ecl.rowsvalue(rowname='搜索按钮')[2],ecl.rowsvalue(rowname='搜索按钮')[3])



    #
    #     #输入搜索词
    # def inputl(self,kw):
    #     in_put=self.find_element(*self.loc_search_input)
    #     in_put.clear()
    #     in_put.send_keys(kw)
    #     logger.info('搜索输入框输入内容')
    #
    # def but_click(self):
    #     #点击搜索按钮
    #     button=self.find_element(*self.loc_search_button)
    #     button.click()
    #     logger.info('点击搜索按钮')
    #

#--------------------------opencv-----------------------------
    item ='pc_baidu'
    page ='百度首页'
    element1='搜索输入框'
    element2 ='搜索按钮'
    backgroundXpath='/html/body'

    loc_search_input=os.path.join(Img_path_cv,item,page,element1+'.png')
    loc_search_button=os.path.join(Img_path_cv,item,page,element2+'.png')


    #输入搜索词汇
#self,backgroudXpath,msg,img,method,value=None
    def input_keys(self,value):
        self.pc_control(backgroudXpath=(self.backgroundXpath),msg='搜索输入框',img=(self.loc_search_input),method='输入',value=value)
    #点击搜索按钮
    def but_click(self):
        self.pc_control(backgroudXpath=(self.backgroundXpath),msg='搜索按钮',img=(self.loc_search_button),method='点击')

