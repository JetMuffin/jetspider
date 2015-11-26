from pymongo import MongoClient
import traceback

class MongodbPipeline(object):
    """
        save the data to mongodb
    """

    def __init__(self, mongo_server, mongo_port, mongo_db):

        self.mongo_server = mongo_server
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

        try:
            client = MongoClient(self.mongo_server, self.mongo_port)
            self.db = client[self.mongo_db]
        except Exception as e:
            print "ERROR(SingleMongodbPipeline): %s"%(str(e),)
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.mongo_server = crawler.settings.get('MONGODB_SERVER', 'localhost')
        cls.mongo_port = crawler.settings.getint('MONGODB_PORT', 27017)
        cls.mongo_db = crawler.settings.get('MONGODB_DB', 'spider_db')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item):
        page_detail = {
            'title': item.get('title'),
            'content': item.get('content'),
            'href': item.get('href'),
            'links': item.get('links')
        }

        result = self.db['page_detail'].insert(page_detail)
        item["mongo_id"] = str(result)

        return item

