import sys
import socket
import struct
import time
import threading


class Session:
    def __init__(self):
        pass


class DiscoverSender(Session):
    def __init__(self, name="default"):
        super().__init__()

    def __del__(self):
        pass

    def InitSession(self, mcast_group_ip='239.255.255.252', mcast_group_port=23456):
        self.mcast_group_ip = mcast_group_ip
        self.mcast_group_port = mcast_group_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def SendMsg(self, msg):
        self.sock.sendto(msg.encode(), (self.mcast_group_ip, self.mcast_group_port))
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: message send finish')


class DiscoverReceiver(Session, threading.Thread):
    def __init__(self, name="default"):
        super(Session, self).__init__()
        super(threading.Thread, self).__init__()
        self.socket = None
        self.isAlive = True

    def __del__(self):
        pass

    def InitSession(self, mcast_group_ip='239.255.255.252', mcast_group_port=23456):
        self.mcast_group_ip = mcast_group_ip
        self.mcast_group_port = mcast_group_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # if "linux" in sys.platform and not eth:
        #     self.sock.setsockopt(socket.SOL_SOCKET, 25, eth)
        # self.sock.bind((socket.gethostbyname(socket.gethostname()), mcast_group_port))
        self.sock.bind(('0.0.0.0', mcast_group_port))
        # join multicast
        mreq = struct.pack("=4sl", socket.inet_aton(mcast_group_ip), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # no block
        # self.sock.setblocking(0)

    def run(self):
        while self.isAlive:
            try:
                message, addr = self.sock.recvfrom(1024)
                print(
                    f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Receive data from {addr}: {message.decode()}')
            except Exception as e:
                print(e)

    def Start(self):
        self.start()
