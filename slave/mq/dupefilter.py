import redis

# deafult values
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

class BaseDupeFilter:

    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)

        key = '%(spider)s:dupefilter'
        return cls(server, key)

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