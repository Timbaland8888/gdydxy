#!/bin/env python
# -*- coding: utf-8 -*-
#function:远程关机
#Author:Timberland

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import Tkinter,wmi
import tkMessageBox
import  win32api,os,time
logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())

#远程控制win7登入
def call_remote_bat(host):
    try:
        #用wmi连接到远程win7系统
        conn = wmi.WMI(computer='127.0.0.1', user='b309\\b309-005', password="Root@123")
        cmd1 = r"net use \\%s\ipc$ 123456 /user:administrator |  " % (host)
        cmd2 = r"shutdown -m \\%s -f -s -t  0" % (host)
        os.remove('c:\\app\shutdown.bat')
        with open('c:\\app\shutdown.bat','a') as f:
            f.write(cmd1)
            f.write(cmd2)
        filename=r"c:\app\shutdown.bat"
        cmd_callbat=r"cmd /c call %s"%filename
        conn.Win32_Process.Create(CommandLine=cmd_callbat)  #执行bat文件
        print "执行成功!"

        print cmd1
        print cmd2

        return True
    except Exception,e:
        log = open(logfile, 'a')
        log.write(('%s %s call  Failed!\r\n') % (host,e))
        log.close()
        return False
    return False


if __name__=='__main__':
    result = os.popen("netstat -n| findstr 2598 ")
    host = result.read().split()[2].split(':')[0]
    # host = '172.234.243.2'
    print host
    top = Tkinter.Tk()
    top.withdraw()
    tkMessageBox.showwarning("执行关机操作", "你确定要关机！！！！")
    call_remote_bat(host)

