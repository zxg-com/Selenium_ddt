#coding = utf-8
"""
初始化时传入全部所需数据，message是正文，可不填，path可以传list或者str；receiver支持多人，用”;”隔开就行

邮件类。用来给指定用户发送邮件。可指定多个收件人，可带附件。

常见错误：
账户密码出错
服务器sever出错，这个可以根据你的发送人的邮箱去网站或邮箱设置中查看到
邮箱没有开通smtp服务，一般在邮箱设置中
邮件被拦截，在title、message以及发送的文件中不要带明显乱码、广告倾向的字符
sender跟loginuser不一致的问题，发送人必须是登录用户
"""
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
from utils.log import logger
from utils.config import Config,REPORT_PATH


class Email:

    def __init__(self,path=None):
        """初始化
        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """

        self.title = Config().get("EMAIL").get('title')
        self.message = Config().get("EMAIL").get('message')
        self.files = path

        self.msg = MIMEMultipart('related')

        self.server = Config().get("EMAIL").get('server')
        self.sender = Config().get("EMAIL").get('sender')
        self.receiver =Config().get("EMAIL").get('receiver')
        self.password = Config().get("EMAIL").get('password')


    def _attach_file(self, att_file):
        """将单个文件添加到附件列表中"""
        att = MIMEText(open('%s' % att_file, 'rb').read(), 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        logger.info('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # 添加附件，支持多个附件（传入list），或者单个附件（传入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)  #调用附件上传
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # 连接服务器并发送
        try:
            smtp_server = smtplib.SMTP(self.server)  # 连接sever
        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接
                logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))


if __name__ == '__main__':
    Email().send()