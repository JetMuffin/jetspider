from redis import Redis

class BaseQueue(object):
    def __init__(self, key, db, host, port=6379):
        """Redis task queue for spider

        :type key: object
        :param server: redis server
        :param spider: spider instance
        :param key: key of redis queue
        """
        # TODO encode the url
        self.server = Redis(host, port, db)
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
    def __init__(self, key, host, db=2, port=6379):
        self.server = Redis(host, port, db)
        self.key = key

    def __len__(self):
        return self.server.llen(self.key)

    def push(self, value):
        self.server.lpush(self.key, value)

    def pop(self):
        data = self.server.rpop(self.key)
        if data:
            return data

class Subscribe(BaseQueue):
    """ subscribe mode """

    def __init__(self, key, host, db=1, port=6379):
        self.server = Redis(host, port, db)
        self.key = key
        self.ps = self.server.pubsub()
        self.ps.subscribe(self.key)


class MessageQueue(BaseQueue):

    def __init__(self, key, host, db=2, port=6379):
        self.server = Redis(host, port, db)
        self.key = key

    def pop(self):
        return self.server.blpop(self.key, 0)[0]

    def push(self, value):
        self.server.lpush(self.key, value)









