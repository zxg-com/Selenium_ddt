
from ftplib import FTP
from utils.config import REPORT_PATH


def upload(remotepath, localpath):
    '''
    :param remotepath: 远程路径
    :param localpath: 本地路径
    :return: 
    '''
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect("47.94.81.110",21)
    ftp.login()
    print(ftp.nlst() )
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR %s' % remotepath, fp, bufsize)
    fp.close()
    ftp.quit()
    ftp.welcome()


if __name__ == '__main__':
    fileName="a.html"
    upload(fileName,REPORT_PATH+"/"+fileName)










