from discover.discover import DiscoverClient
from discover.message_handle import DiscoverSenderMsgHander

if __name__ == "__main__":
    dc = DiscoverClient()
    dc.InitSession()
    dsm = DiscoverSenderMsgHander(dc)
    dsm.SendDiscoverMsg()
