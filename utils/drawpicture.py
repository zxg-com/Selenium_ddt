
from utils.config import BASE_PATH,DRIVER_PATH,REPORT_PATH
from PIL import Image, ImageDraw, ImageFont
import datetime



def draw_Report_Pic(title,case_num,pass_num,fail_num,err_num,percent_pass):
    '''
    :param title: 报告标题
    :param case_num: 用例数量
    :param pass_num: 通过量
    :param fail_num: 失败数量
    :param err_num: 错误数量
    :param percent_pass: 通过百分比
    :return: 
    '''
    setFont = ImageFont.truetype(DRIVER_PATH+'/Font/Hiragino Sans GB.ttc', 38) #字体库
    img=DRIVER_PATH+'/report_background.png'
    image = Image.open(img)
    draw = ImageDraw.Draw(image)

    til=str(title)
    casenum=str(case_num)
    passnum=str(pass_num)
    failnum=str(fail_num)
    errnum=str(err_num)
    percent=str(percent_pass)

    draw.text((294, 57), til, font=setFont, fill=(255,255,255))  #标题
    draw.text((573, 142), casenum, font=setFont, fill=(255,255,255))  #用例条数
    draw.text((573, 205), passnum, font=setFont, fill=(255,255,255)) #通过数
    draw.text((573, 268), failnum, font=setFont, fill=(255,255,255))  #失败数
    draw.text((573, 331), errnum, font=setFont, fill=(255,255,255)) #错误数
    draw.text((540, 392), percent, font=setFont, fill=(255,255,255))  #通过率
    #存入report-缩略图文件夹路径
    image.save(REPORT_PATH+'/thumbnail_img/'+title+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.png','PNG')

# if __name__ == '__main__':
#     s=draw_Report_Pic('安卓测试报告',100,90,1,9,70)
#     #s.show()

