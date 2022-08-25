#!/usr/bin/env python
"""
-------------------------------------------------------
2021-02-01 -- Christian Foerster
christian.foerster@eawag.ch
-------------------------------------------------------
"""
from pathlib import Path
from ftplib import FTP
from io import BytesIO
from hashlib import md5
from datetime import datetime


class FtpUtil:
    """basic ftp utility to work with ftp server"""

    def __init__(self, host, usr, pwd, root="/", port=21):
        self.host = host
        self.usr = usr
        self.pwd = pwd
        self.rootpath = root
        self.port = port

        self.__test_conn()

    def __login(self):
        self.ftp = FTP()
        self.ftp.connect(host=self.host, port=self.port)
        self.ftp.login(user=self.usr, passwd=self.pwd)

    def __logout(self):
        self.ftp.quit()

    def __test_conn(self):
        try:
            self.__login()
            self.__logout()

        except Exception as e:
            print(
                f"Could not connect to the ftp server "
                f"host: {self.host}, user: {self.usr}, pw: {self.pwd}, port: {self.port}."
            )
            raise e

    def ls(self, path=""):
        self.__login()
        if path == "./" or path == ".":
            path = ""
        self.ftp.cwd(f"{self.rootpath}/{path}")
        files = self.ftp.nlst()
        self.__logout()
        return files

    def get(self, path, file):
        self.__login()
        self.ftp.cwd(f"{self.rootpath}/{path}")
        bio = BytesIO()
        self.ftp.retrbinary("RETR " + file, bio.write)
        self.__logout()
        bio.seek(0)
        return bio

    def upload(self, file, destpath="", filename=None):
        if filename is None:
            filename = Path(file).name
        self.__login()
        if destpath != ".":
            self.ftp.cwd(f"{self.rootpath}/{destpath}")
        with open(file, "rb") as f:
            # use FTP's STOR command to upload the file
            self.ftp.storbinary(f"STOR {filename}", f)
        self.__logout()

    def download(self, path, file, destpath):
        self.__login()
        self.ftp.cwd(f"{self.rootpath}/{path}")
        with open(Path(destpath) / file, "wb+") as f:
            self.ftp.retrbinary("RETR " + file, f.write)
        self.__logout()

    def md5(self, path, file):
        self.__login()
        m = md5()
        self.ftp.cwd(f"{self.rootpath}/{path}")
        self.ftp.retrbinary("RETR %s" % file, m.update)
        md5_hash = m.hexdigest()
        self.__logout()

        return md5_hash

    def modification_date(self, path, file):
        self.__login()
        self.ftp.cwd(f"{self.rootpath}/{path}")
        date = self.ftp.voidcmd(f"MDTM {file}")
        self.__logout()

        return datetime.strptime(date.split()[-1], "%Y%m%d%H%M%S").strftime("%F %X")

    def remove(self, path, file):
        self.__login()
        self.ftp.delete(f"{self.rootpath}/{path}/{file}")
        self.__logout()