#! /bin/env python
# coding:utf-8

import os
import time
import subprocess
import configparser
import sys
import logging as log
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
file_path = None
log.basicConfig(level=log.INFO)


# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_conf():

    # file_path = os.path.abspath(os.path.join(os.getcwd(), '..\\conf\\configure.ini'))
    file_path = resource_path(os.path.join("conf", "configure.ini"))
    conf = configparser.ConfigParser()
    conf.read(file_path, encoding='utf-8')
    return conf


def run_as_exe(run_path, username: str, password, domain, command, path, count: int):

    try:
        LSRUNASE_PATH = r'{0} /user:{1} /password:{2} /domain:{3} /command:"{4}" /runpath:{5}'
        result = "正在试用管理员打开软件"
        cmd = LSRUNASE_PATH.format(run_path, username, password, domain, command, path)
        print(cmd)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        stdout, stdin = p.communicate()

        print(stdout.decode("gbk"))
        if stdout:
            if stdout.decode("gbk").find("密码不正确。") > -1:
                if count >= 1:
                    print("试用password2密码！！")
                    result = "试用password2 重新打开软件"
                    run_as_exe(run_path, username, get_conf().get("account", "password2"), domain, command, path, 0)
            else:
                result = stdout.decode("gbk")

        messagebox.showinfo('提示', result)
    except Exception as e:
        print("exception:" + str(e))


def send_cmd():
    # 定义传入 用户名与密码 1=username 2=password 1=command
    args = sys.argv
    command = "cmd"

    if args.__len__() >= 2:
        command = args[1]
    if args.__len__() >= 3:
        username = args[2]
        password = args[3]
    else:
        # 初始化配置文件
        conf = get_conf()
        username = conf.get("account", "username")
        password = conf.get("account", "password")
        domain = conf.get("account", "domain")

    if file_path is not None:
        command = file_path

    command = command.replace(" ", "$")
    log.info("Command=%s ", command)
    runas_path = resource_path(os.path.join("execute", "lsrunase.exe"))
    # path = os.path.abspath(os.path.join(os.getcwd(), '..\\execute'))
    # path = resource_path(os.path.join("execute", ""))
    boot = resource_path(os.path.join("execute", "boot.bat"))
    boot = boot + " " + command
    run_as_exe(runas_path, username, password, domain, boot, "c:\\", 1)
    pass


def clicked():
    file = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))

    if file.__len__() > 0:
        global file_path
        file_path = str(file[0])
        if file_path.__contains__('exe'):
            print("exe filepath: %s" % file_path)


def ui_init():
    window = Tk()
    # 设置默认图标
    window.iconbitmap(resource_path(os.path.join("conf", "logo.ico")))
    window.title('请选择需要使用管理员的程序路径,程序安装包不能存放在桌面!最好放在非C盘位置')
    window.geometry('450x450')
    btn = Button(window, text="选择程序路径", command=clicked)
    btn.grid(column=0, row=0)
    sent_btn = Button(window, text="运行程序", command=send_cmd)
    sent_btn.grid(column=1, row=0)
    set_label = Label(window, text="程序安装包不能存放在桌面!最好放在非C盘位置", foreground="red")
    set_label.grid(column=2, row=1)
    window.mainloop()


if __name__ == '__main__':
    # main()
    # time.sleep(3)
    # sys.exit(0)
    ui_init()
