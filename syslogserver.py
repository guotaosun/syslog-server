# -*- coding: UTF-8 -*-#
# *******************************************************************************
# 功能描述：syslogserver
#  Author: sungt
# Version 1.0.0
# Date:  2021-02-04 09:47:23
# *******************************************************************************
# Change log:
#
# *******************************************************************************
import socket
import logging
import threading
import time
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class SyslogServer(threading.Thread):
    """ This is a  ipv4 syslog server"""

    def __init__(self, dcnserver):
        threading.Thread.__init__(self, name="Syslog")
        self.daemon = True
        self.logfile = f"{syslog_file_path}/{server.log_file}"
        self.server = None
        self.ip = server.ip
        self.port = server.port
        self.stop_flag = 0

    print("start run syslog server")

    def stop(self):
        self.stop_flag = 1

    def run(self):
        if self.server is None:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            logging.debug(f"socket bound to to{self.ip} and port to {self.port}")
            print(f"Binding server ip to {self.ip} and port to {self.port}")
            self.server.bind((self.ip, self.port))
        try:
            print("write  file")
            f = open(self.logfile, "a")
            while True:
                try:
                    data, addr = self.server.recvfrom(1024)
                    stringdata = data.decode('utf-8')
                    f.write(stringdata)
                    f.flush()
                    print(stringdata)
                    print("结束写文件")
                except Exception as e:
                    print(f"syslog服务器接收出错{e}")
                    logging.error("Error while receiving message: %s" % e)
                    f.close()
                if self.stop_flag == 1:
                    print(f"syslog服务器接收到出退出命令")
                    break
        finally:
            if not f.closed:
                f.close()


class SyslogServer6(threading.Thread):
    """ This is a  syslog ipv6 server"""

    def __init__(self, server):
        threading.Thread.__init__(self, name="Syslog6")
        self.daemon = True
        self.logfile = f"{syslog_file_path}/{server.log_file}"
        self.server = None
        self.ip = server.ip
        self.port = server.port
        self.stop_flag = 0

    print("开始运行syslog ")

    def stop(self):
        self.stop_flag = 1

    def run(self):
        if self.server is None:
            self.server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, 0, 0)
            logging.debug(f"socket bound to to{self.ip} and port to {self.port}")
            print(f"Binding server ip to {self.ip} and port to {self.port}")
            self.server.bind((self.ip, self.port))

        try:
            print("写文件")
            f = open(self.logfile, "a")
            while True:
                try:
                    data, addr = self.server.recvfrom(1024)
                    stringdata = data.decode('utf-8')
                    f.write(stringdata)
                    f.flush()
                    print(stringdata)
                    print("finish write file")
                except Exception as e:
                    print(f"syslog receive message error {e}")
                    logging.error("Error while receiving message: %s" % e)
                    f.close()
                if self.stop_flag == 1:
                    print(f"syslog receive a exit command")
                    break
        finally:
            if not f.closed:
                f.close()


if __name__ == '__main__':
    logging.basicConfig(filename="debug.log", level=logging.DEBUG)
    print("Starting server...")
    server = SyslogServer6(sys_log_server4)
    server.start()
    while True:
        time.sleep(1)
