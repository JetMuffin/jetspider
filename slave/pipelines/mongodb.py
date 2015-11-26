from pymongo import MongoClient
from bson import ObjectId
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
            print "ERROR(SingleMongodbPipeline): %s" % (str(e),)
            traceback.print_exc()

    def insert(self, item, table):
        """
            insert an item into table
            :param item:
            :param table:
        """
        result = self.db[table].insert(item)
        item["mongo_id"] = str(result)
        return item

    def find(self, table, object_id):
        """
            use object_id to find item
            :param table:
            :param object_id:
        """
        item = self.db[table].find_one({'_id': ObjectId(object_id)})
        return item

    def update(self, table, object_id, new_item):
        """
            update item by object_id
            :param table:
            :param object_id:
            :param new_item:
        """
        self.db[table].update({'_id': ObjectId(object_id)}, {"$set": new_item})

    def delete(self, table, object_id):
        """
            delete item by object_id
            :param table:
            :param object_id:
        """
        self.db[table].delete_one({'_id': ObjectId(object_id)})

    def remove(self, table):
        """
            remove all items of table
            :param table:
        """
        self.db[table].remove()

