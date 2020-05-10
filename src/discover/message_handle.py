import json
import time
import threading

from typing import Tuple, Any


class MessageBuilder:
    def GetDiscoverMsg(self):
        return json.dumps({"method": "discover"})
    def GetMsgType(self, message)->str:
        res = json.loads(message)
        return res["method"]



class MsgHandler:
    def SendMsg(self, msg) -> int:
        pass

    def RcvMsg(self, bufsize) -> Tuple[bytes, Any]:
        pass


class DiscoverSenderMsgHander():
    def __init__(self, msg_handler):
        self.msg_handler = msg_handler
        self.msg_builder = MessageBuilder()

    def SendDiscoverMsg(self):
        self.SendMsg(self.msg_builder.GetDiscoverMsg())

    def SendMsg(self, msg):
        self.msg_handler.SendMsg(msg)
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: message send finish', {msg.encode()})


class DiscoverReceiverMsgHander(threading.Thread):
    def __init__(self, msg_handler):
        threading.Thread.__init__(self)
        # super(threading.Thread, self).__init__()
        self.msg_handler = msg_handler
        self.msg_builder = MessageBuilder()
        self.isAlive = False

    def Start(self):
        self.isAlive = True
        self.start()

    def Stop(self):
        self.isAlive = False

    def run(self):
        while self.isAlive:
            try:
                message, addr = self.msg_handler.RcvMsg(1024)
                print(
                    f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Receive data from {addr}: {message.decode()}')

                type = self.msg_builder.GetMsgType(message)
                if type == "discover":
                    print("ok")
            except Exception as e:
                print(e)
