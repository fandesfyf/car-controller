#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/21 15:54
# @Author  : Fandes
# @FileName: socket_client.py
# @Software: PyCharm
import sys

import requests
import socket, time, json


class ControlClient:
    def __init__(self, host="127.0.0.1", port=8787):
        self.host = host
        self.port = port
        self.on_running = True
        self.reconnect()
        print('ready')

    def reconnect(self):
        try:
            print(self.host,self.port)
            self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientsocket.connect((self.host, self.port))
            self.on_running = True
        except:
            print("连接主机失败", sys.exc_info())
            self.on_running=False
        else:
            print("连接{}成功".format(self.clientsocket.family))

    def send(self, data: dict):
        if not self.on_running:
            print("尝试重新连接主机")
            self.reconnect()  # 重连
        if self.on_running:  # 重连后再判断连上了再发送
            print("send", data)
            try:
                self.clientsocket.send(json.dumps(data).encode())
            except ConnectionResetError:
                print("ConnectionResetError", sys.exc_info())
                self.clientsocket.close()
                self.on_running = False


if __name__ == '__main__':
    cl = ControlClient("192.168.19.128")
    i = 1
    while True:
        cl.send({"v": i, "t": i + 1})
        time.sleep(1)
        i += 1
