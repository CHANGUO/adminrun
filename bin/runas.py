#! /bin/env python
# coding:utf-8

import os
import time
import subprocess
import configparser
import sys

"""..\lsrunase.exe /user:colipu /password:zg98huYbsA== /domain: /command:"C:\Program Files\Internet Explorer\iexplore.exe http://www.google.be" /runpath:c:\\\\"""
"""‪C:\\Users\\chenwei01\\Desktop\\sogou_pinyin_102a.exe    'rem start C:\Windows\System32\cmd.exe"""

LSRUNASE_PATH = r'..\execute\lsrunase.exe /user:{0} /password:{1} /domain:{2} /command:"{3}" /runpath:{4}'


#生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



def get_conf():

    file_path = os.path.abspath(os.path.join(os.getcwd(), '..\\conf\\configure.ini'))
    conf = configparser.ConfigParser()
    conf.read(file_path, encoding='utf-8')
    return conf


def run_as_exe(username: str, password, domain, command, path):

    try:
        cmd = LSRUNASE_PATH.format(username, password, domain, command, path)
        print(cmd)
        p = subprocess.Popen(cmd, subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        print(stdout, stderr)
    except Exception as e:
        print("exception:" + str(e))


def main():
    conf = get_conf()
    username = conf.get("account", "username")
    password = conf.get("account", "password")
    domain = conf.get("account", "domain")
    path = os.path.abspath(os.path.join(os.getcwd(), '..\\execute'))
    print(path)
    run_as_exe(username, password, domain, 'boot.bat notepad.exe', path)
    pass


if __name__ == '__main__':
    main()
