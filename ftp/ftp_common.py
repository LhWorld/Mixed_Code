# -- coding: UTF-8 --
import ftplib
import os


def upload_file(ftp_handle, file_path, remote_dir):
    try:
        ftp_handle.cwd(remote_dir)  # 重定向到指定路径
    except ftplib.error_perm:
        print('创建目录："%s"' % remote_dir)
        ftp_handle.mkd(remote_dir)  # 目录不存在则创建
        ftp_handle.cwd(remote_dir) # 重定向到ftp linux服务器上
    if (file_path.__contains__("\\")):
            file_path = file_path.replace('\\', '/') #替换linux目录格式
    file_name = os.path.basename(file_path)
    print(file_name)
    try:
        file_stream = open(file_path, 'rb')
        print("=====================upload start=====================")
        ftp_handle.storbinary("STOR " + file_name, file_stream, 8192)  #增加buffersize缓存读写数据
        print("=====================upload end======================")
        file_stream.close()
    except Exception as e:
        print(str(e))



def download_file(ftp, filename, store_dir):
    des_file_path = os.path.join(store_dir, filename)
    try:
        print("=====================download start=====================")
        ftp.retrbinary("RETR " + filename, open(des_file_path, 'wb').write, 8192) #增加buffersize缓存读写数据
        print("=====================download end======================")
    except Exception as e:
        print(str(e))
    return des_file_path


def ftp_login(ftp_dict):
    HOST = ftp_dict['host']
    PORT = ftp_dict['port']
    USER = ftp_dict['username']
    PASSWD = ftp_dict['passwd']

    ftp = ftplib.FTP()
    # ftp.set_debuglevel(2)
    try:
        ftp.set_pasv(0)  # positive mode
        ftp.connect(HOST, PORT)
        ftp.login(USER, PASSWD)
        ftp.sendcmd("OPTS UTF8 ON")
        ftp.encoding = 'gbk'
        return ftp
    except Exception as e:
        print(str(e))
        return None


def search_remote_directory(ftp_handle, store_dir):
    store_path = store_dir.replace('\\', '/')
    while store_path:
        try:
            ftp_handle.cwd(store_path)
            return store_path
        except:
            if '/' not in store_path:
                return '/'
            else:
                store_path = store_path.split("/", 1)[1]
    return '/'


def retr_files_func(ftp_handle, remote_dir, store_dir):
    try:
        remote_dir = remote_dir.replace('//', '/')
        ftp_handle.cwd(remote_dir)
        filenames = ftp_handle.nlst()
        for filename in filenames:
            download_file(ftp_handle, filename, store_dir)
    except Exception as e:
        print(str(e))
        pass


def retr_files(ftp_handle, remote_dir, store_dir):
    remote_dir = search_remote_directory(ftp_handle, remote_dir)
    retr_files_func(ftp_handle, remote_dir, store_dir)


def main():
    #  revise [host, username, passwd] for login ftp server
    ftp_dict = {
        "host": '123.206.71.237',
        "port": 21,
        "username": 'ftproot',
        "passwd": 'shangjian123'
    }
    ftp_handle = ftp_login(ftp_dict)
    if ftp_handle:
        # ftp_handle.dir()
        file_path=r"d:\新建文本文档.txt"
        remote_dir="/var/ftp/pub/test0309"
        upload_file(ftp_handle, file_path, remote_dir)
        # store_dir="d:/"
        # retr_files(ftp_handle, remote_dir, store_dir)
    ftp_handle.quit()

#
if __name__ == "__main__":
    main()
