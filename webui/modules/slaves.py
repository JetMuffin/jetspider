import tornado.web
from mq.storage import SlaveStorage

class SlaveHandler(tornado.web.RequestHandler):
    def get(self):
        slave_storage = SlaveStorage(3, "127.0.0.1", "6379")
        slaves = slave_storage.get_all()
        print slaves
        self.render(
            'slaves.html',
            slaves=slaves,
            page_title="Slaves | JetSpider",
        )