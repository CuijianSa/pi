import os
from discover.discover import DiscoverReceiver

if __name__ == "__main__":
    dr = DiscoverReceiver()

    dr.InitSession()
    dr.Start()

    os.system("pause");
