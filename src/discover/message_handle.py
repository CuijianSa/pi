import json
import time
import threading
from .net_util import UtilNet
import socket

class IMessageCallback:
    def OnDiscover(self):
        pass

class MessageParser:
    def __init__(self):
        self.callback_list = []

    def __del__(self):
        self.callback_list.clear()

    def GetDiscoverRequest(self):
        method = "request"
        action = "discover"
        content = []
        request_json = {"method": method, "action": action, "content": content}
        return json.dumps(request_json)

    def GetDiscoverResponse(self):
        method = "response"
        action = "discover"
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        content = [{"hostname":hostname, "ip_address":ip_address}]
        response_json = {"method":method, "action":action, "content":content}
        return json.dumps(response_json)

    def RegisterMessageCallback(self, message_callback):
        self.callback_list.append(message_callback)

    def UnregisterMessageCallback(self, message_callback):
        self.callback_list.remove(message_callback)

    def GetMessageType(self, message)->str:
        res = json.loads(message)
        return res["action"]

    def OnDiscover(self):
        for callback in self.callback_list:
            callback.OnDiscover()

    def OnUnknow(self):
            print("unkown message")

    def ParsePacket(self, message):
        type = self.GetMessageType(message)
        switch = {'discover': self.OnDiscover,
                  }
        switch.get(type, self.OnUnknow)()  # Execute the corresponding function, if not, execute the default function

class DiscoverSenderMsgHander():
    def __init__(self, util_net):
        self.util_net = util_net
        self.msg_parser = MessageParser()

    def SendDiscoverMsg(self):
        self.SendMsg(self.msg_parser.GetDiscoverRequest())

    def SendMsg(self, msg):
        self.util_net.SendMsg(msg)
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: message send finish', {msg.encode()})


class DiscoverReceiverMsgHander(threading.Thread,IMessageCallback):
    def __init__(self, util_net):
        threading.Thread.__init__(self)
        # super(threading.Thread, self).__init__()
        self.util_net = util_net
        self.msg_parser = MessageParser()
        self.isAlive = False
        self.msg_parser.RegisterMessageCallback(self)

    def __del__(self):
        self.msg_parser.UnregisterMessageCallback(self)

    def Start(self):
        self.isAlive = True
        self.start()

    def Stop(self):
        self.isAlive = False

    def run(self):
        while self.isAlive:
            try:
                message, addr = self.util_net.RcvMsg(1024)
                print(
                    f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Receive data from {addr}: {message.decode()}')

                self.msg_parser.ParsePacket(message)
            except Exception as e:
                print(e)

    # MessageHandler
    def OnDiscover(self):
        print("action:OnDiscover")
        discover_response = self.msg_parser.GetDiscoverResponse()
        print("discover_reponse:{}",{discover_response})