import redis


class BaseStorage(object):
    def __init__(self, db, host, port=6379):
        self.server = redis.Redis(host, port, db)

    def set(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def delete_all(self):
        raise NotImplementedError

    def __len__(self):
        return self.server.dbsize()


class SlaveStorage(BaseStorage):
    def set(self, key, value):
        self.server.set(key, str(value))

    def get(self, key):
        value = self.server.get(key)
        if value:
            return eval(value)
        else:
            return None

    def get_all(self):
        values = []
        for key in self.server.keys():
            values.append(self.get(key))

        return values

    def delete(self, key):
        self.server.delete(key)

    def delete_all(self):
        self.server.flushdb()
