import redis
import threading

import time

from dupefilter import SimpleDupefilter
from queue import SpiderQueue
from slave.pipelines.mongodb import MongodbPipeline
from slave.rpc.state import SlaveRPC
from slave.spiders.crawlers import SimpleCrawler


class Executor(object):
    def __init__(self, master_address, name):
        self.master_address = master_address
        self.name = name
        self.master_ip, self.master_port = master_address.split(":")

        """ Register to master """
        self.rpc_proxy = SlaveRPC(self.name, self.master_ip, self.master_port)
        self.task_info = self.rpc_proxy.server.register(self.name)

        """ Connect to redis """
        self.server = redis.Redis(self.task_info['redis_ip'], self.task_info['redis_port'])

    def run(self):
        raise NotImplementedError

    def close(self):
        self.rpc_proxy.close()


class SpiderExecutor(Executor):

    def fetch(self):
        """execute task"""
        queue = SpiderQueue(self.server, self.task_info['queue_key'])
        crawler = SimpleCrawler(self.task_info['start_url'], self.task_info['allowed_domain'])
        dupefilter = SimpleDupefilter(self.server, self.task_info['dupefilter_key'])
        pipeline = MongodbPipeline(self.task_info['db_ip'], self.task_info['db_port'], self.task_info['db_name'])

        queue.push(self.task_info['start_url'])
        while True:
            if len(queue) > 0:
                current_url = queue.pop()
                crawler.fetch(current_url)

                # if crawler successful fetch the content
                if crawler.success:
                    item = crawler.parse()
                    next_urls = item.get('links')
                    next_urls_count = 0
                    for next_url in next_urls:
                        if not dupefilter.exists(next_url):
                            queue.push(next_url)
                            next_urls_count += 1

                    # print fetch infomation
                    print "Crawler fetched %s and get %d urls" % (current_url, next_urls_count)
                    self.rpc_proxy.server.message(self.name, "Success fetched url %s."%current_url)

                    item = pipeline.process_item(item)
                    self.rpc_proxy.server.message(self.name, "Stored url %s with ID %s."%(current_url, item.get('mongo_id')))

            else:
                print "Wait for tasks..."
                time.sleep(3)

    def run(self):
        pass

    def close(self):
        self.queue.clear()
        self.dupefilter.clear()

