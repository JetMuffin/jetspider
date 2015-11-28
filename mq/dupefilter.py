import redis


class BaseDupeFilter:
    def __init__(self, key, host, port=6379, db=0):
        self.server = redis.Redis(host, port, db)
        self.key = key

    def exists(self, url):
        raise NotImplementedError

    def close(self):
        self.clear()

    def clear(self):
        self.server.delete(self.key)


class SimpleDupefilter(BaseDupeFilter):
    """
        store url without any compress
    """

    def exists(self, url):
        if self.server.sismember(self.key, url):
            return True
        self.server.sadd(self.key, url)
        return False
