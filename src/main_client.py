from discover.discover import DiscoverSender

if __name__ == "__main__":
    ds = DiscoverSender()
    ds.InitSession()
    ds.SendMsg("hello")
