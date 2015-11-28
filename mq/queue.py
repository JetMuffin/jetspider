import redis


class BaseQueue(object):
    def __init__(self, key, host, port=6379, db=0):
        """Redis task queue for spider

        :type key: object
        :param server: redis server
        :param spider: spider instance
        :param key: key of redis queue
        """
        # TODO encode the url
        self.server = redis.Redis(host, port, db)
        self.key = key

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, url):
        """Push an url"""
        raise NotImplementedError

    def pop(self):
        """Pop an url"""
        raise NotImplementedError

    def clear(self):
        """Clear queue"""
        self.server.delete(self.key)


class FIFOQueue(BaseQueue):
    """FIFO queue"""

    def __len__(self):
        return self.server.llen(self.key)

    def push(self, url):
        self.server.lpush(self.key, url)

    def pop(self):
        data = self.server.rpop(self.key)
        if data:
            return data
