#画缩略图
#给企业号发报告功能
from utils.config import DRIVER_PATH
from PIL import Image, ImageDraw, ImageFont
import requests
import json
from utils.config import Config,REPORT_PATH


def draw_Report_Pic(title,case_num,pass_num,fail_num,err_num,percent_pass,starttime):
    '''
    :param title: 报告标题
    :param case_num: 用例数量
    :param pass_num: 通过量
    :param fail_num: 失败数量
    :param err_num: 错误数量
    :param percent_pass: 通过百分比
    :param starttime: 测试开始时间
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
    start_time=starttime

    draw.text((294, 57), til, font=setFont, fill=(255,255,255))  #标题
    draw.text((573, 142), casenum, font=setFont, fill=(255,255,255))  #用例条数
    draw.text((573, 205), passnum, font=setFont, fill=(255,255,255)) #通过数
    draw.text((573, 268), failnum, font=setFont, fill=(255,255,255))  #失败数
    draw.text((573, 331), errnum, font=setFont, fill=(255,255,255)) #错误数
    draw.text((540, 392), percent, font=setFont, fill=(255,255,255))  #通过率
    #存入report-缩略图文件夹路径
    image.save(REPORT_PATH+'/thumbnail_img/'+title+'_'+start_time+'.png','PNG')





def get_access_token():
    """
    获取微信全局接口的凭证(默认有效期俩个小时)
    如果不每天请求次数过多, 通过设置缓存即可
    """
    corpid = Config().get('WECHART').get('corpid')
    corpsecret = Config().get('WECHART').get('corpsecret')
    result = requests.get(
        url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?",
        params={
            "corpid": corpid,    #appid
            "corpsecret": corpsecret,  #秘钥
        }
    ).json()
    if result.get("access_token"):
        access_token = result.get('access_token')
    else:
        access_token = None
    return access_token

def sendmsg(test_title,pic_Nmae,report_name,start_time):
    '''
    :param test_title:  测试标题
    :param pic_Nmae: 服务器上图片名字
    :param report_name: 服务器上报告名字
    :param start_time: 测试开始时间
    :return: 
    '''
    title=test_title
    picNmae=pic_Nmae
    reportname=report_name
    starttime=start_time
    agentid = Config().get('WECHART').get('agentid')
    access_token = get_access_token()
    #文本类型
    # body = {"touser":"@all",
    #         "msgtype" : "text",
    #         "agentid" : int(agentid),
    #         "text" : {
    #             "content" : "测试<a href=\"http://work.weixin.qq.com\">点击查看测试报告</a>"
    #         },
    #         "safe":0
    #         }

    #图文
    server_ip=str(Config().get('ServerInfo').get('ip'))
    port = str(Config().get('ServerInfo').get('port'))
    body = {"touser":"@all",
            "msgtype" : "news",
            "agentid" : int(agentid),
            "safe":0,
            "news": {
                "articles": [
                    {
                        "title": title,
                        "description": "报告时间:"+starttime,
                        "url":server_ip+':'+port+'/'+reportname, #html文件地址即可
                        "picurl": server_ip+':'+port+"/picture/"+picNmae  #画图，上传ftp
                    }
                ]
            }
        }

    response = requests.post(
        url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token,
        data=json.dumps(body)
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    result = response.json()
    print(result)





if __name__ == '__main__':

    sendmsg("接口/xx端UI自动化测试报告",'aaa.png','PC端UI测试报告20181106-155534.html','12345')

