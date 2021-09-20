#!/usr/bin/env python
"""
-------------------------------------------------------
2021-02-01 -- Christian Foerster
christian.foerster@eawag.ch
-------------------------------------------------------
"""
import os
from ftplib import FTP
from io import BytesIO
from hashlib import md5


class FtpUtil:
    """basic ftp utility to download data from the ftp server"""

    def __init__(self, host, usr, pwd, root="/"):
        self.host = host
        self.usr = usr
        self.pwd = pwd
        self.rootpath = root

        self.__test_conn()

    def __login(self):
        self.ftp = FTP(self.host)
        self.ftp.login(user=self.usr, passwd=self.pwd)

    def __logout(self):
        self.ftp.quit()

    def __test_conn(self):
        try:
            self.__login()
            self.__logout()

        except Exception as e:
            print("Connection test failed!")
            print(e)

    def ls(self, path=""):
        self.__login()
        self.ftp.cwd(f"{self.rootpath}/{path}")
        files = self.ftp.nlst()
        self.__logout()
        return files

    def get(self, sourcepath, file):
        self.__login()
        self.ftp.cwd(f"{self.rootpath}/{sourcepath}")
        bio = BytesIO()
        self.ftp.retrbinary('RETR ' + file, bio.write)
        self.__logout()
        bio.seek(0)
        return bio

    def upload(self, file, destpath=".", filename=""):
        if filename == "":
            filename = file
        self.__login()
        if destpath != ".":
            self.ftp.cwd(f"{self.rootpath}/{destpath}")
        with open(file, "rb") as f:
            # use FTP's STOR command to upload the file
            self.ftp.storbinary(f"STOR {filename}", f)
        self.__logout()

    def download(self, sourcepath, destpath, file):

        self.__login()
        self.ftp.cwd(f"{self.rootpath}/{sourcepath}")
        with open(os.path.join(destpath, file), 'wb+') as f:
            self.ftp.retrbinary('RETR ' + file, f.write)
        self.__logout()

    def md5(self, sourcepath, file):

        self.__login()
        m = md5()
        self.ftp.cwd(f"{self.rootpath}/{sourcepath}")
        self.ftp.retrbinary('RETR %s' % file, m.update)
        md5_hash = m.hexdigest()
        self.__logout()

        return md5_hash


def download_all(ftp_instance, folder, destination):
    for file in ftp_instance.ls(folder):
        ftp_instance.download(folder, destination, file)
