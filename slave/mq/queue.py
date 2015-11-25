
class BaseQueue(object):

    def __init__(self, server, key):
        """Redis task queue for spider

        :param server: redis server
        :param spider: spider instance
        :param key: key of redis queue
        """
        #TODO encode the url
        self.server = server
        self.key = key

    def __len__(self):
        """Return the length of the queue"""
        raise  NotImplementedError

    def push(self, url):
        """Push an url"""
        raise NotImplementedError

    def pop(self):
        """Pop an url"""
        raise NotImplementedError

    def clear(self):
        """Clear queue"""
        self.server.delete(self.key)


class SpiderQueue(BaseQueue):
    """FIFO queue"""

    def __len__(self):
        return self.server.llen(self.key)

    def push(self, url):
        self.server.lpush(self.key, url)

    def pop(self):
        data = self.server.rpop(self.key)
        if data:
            return data

    def empty(self):
        return self.__len__() == 0