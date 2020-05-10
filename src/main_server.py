import os
from discover.discover import DiscoverServer
from discover.message_handle import DiscoverReceiverMsgHander

if __name__ == "__main__":
    ds = DiscoverServer()
    ds.InitSession()
    drm = DiscoverReceiverMsgHander(ds)
    drm.Start()
    os.system("pause");
    drm.Stop()
