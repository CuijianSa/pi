import socket
import struct
from .net_util import UtilNet
from typing import Tuple, Any

class DiscoverClient(UtilNet):
    def __init__(self, name="default"):
        pass
    def __del__(self):
        pass

    def SendMsg(self, msg)-> int:
        return self.sock.sendto(msg.encode(), (self.mcast_group_ip, self.mcast_group_port))
    def RcvMsg(self, bufsize)-> Tuple[bytes, Any]:
        return self.sock.recvfrom(bufsize)

    def InitSession(self, mcast_group_ip='239.255.255.252', mcast_group_port=23456):
        self.mcast_group_ip = mcast_group_ip
        self.mcast_group_port = mcast_group_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

class DiscoverServer(UtilNet):
    def __init__(self, name="default"):
        self.socket = None

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

    def SendMsg(self, msg) -> int:
        return self.sock.sendto(msg.encode(), (self.mcast_group_ip, self.mcast_group_port))

    def RcvMsg(self, bufsize) -> Tuple[bytes, Any]:
        return self.sock.recvfrom(bufsize)