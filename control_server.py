#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/21 15:54
# @Author  : Fandes
import json
import socket
import sys
import threading
import time
import rclpy
import math
from geometry_msgs.msg import Twist, TwistStamped


class ControlServer:
    def __init__(self, host="", port=8787):
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((host, self.port))
        print("bind", host, port)
        self.serversocket.listen()
        self.client_threadlist = []
        self.on_running = True
        rclpy.init()
        self.node = rclpy.create_node('nw_chassis_control_node')
        self.pub = self.node.create_publisher(TwistStamped, 'twist_auto', 1)

    def start(self):
        print("start")
        while True:
            client_socket, client_address = self.serversocket.accept()
            th = Client(client_socket, self)
            th.start()
            print("join a client from ", client_address)
            self.client_threadlist.append(th)

    def publish(self, speed, steer):
        twist_temp = TwistStamped()
        twist_temp.twist.linear.x = float(speed)
        # base_line = 0.41
        # w = speed * math.tan(math.pi * steer/180.0) / base_line
        w = steer
        twist_temp.twist.angular.z = w
        self.pub.publish(twist_temp)
        print("publish:v={: <8} t={: <8} at {}".format(speed, steer,
                                                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


class Client(threading.Thread):
    def __init__(self, client: socket.socket, parent: ControlServer):
        super(Client, self).__init__()
        self.client = client
        self.parent = parent
        self.on_running = True
        self.heartbeatTh = threading.Thread(target=self.heartbeat)

    def run(self) -> None:
        self.heartbeatTh.start()
        while self.parent.on_running and self.on_running:
            try:
                a = self.client.recv(9999)
                if len(a) == 0:
                    break
                else:
                    d = json.loads(a.decode())
                    self.parent.publish(float(d["v"]), float(d["t"]))
                    # print(d)
            except ConnectionResetError:
                print(sys.exc_info(), 45)
                break
        self.parent.publish(.0, .0)

    def heartbeat(self):
        while self.parent.on_running:
            try:
                self.client.sendall("h".encode())  # 发送心跳连接
                time.sleep(0.5)
                # print("heartbeat")
            except:
                print(sys.exc_info(), 79)  # 如果心跳连接出现异常
                self.on_running = False
                try:
                    self.client.close()
                except:
                    print(sys.exc_info(), 81)
                break


def main():
    cs = ControlServer()
    cs.start()


if __name__ == '__main__':
    main()
