import redis

class BaseStorage(object):
    def __init__(self, key, db, host, port=6379):
        self.server = redis.Redis(host, port, db)


