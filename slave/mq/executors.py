import redis
import threading

import time

from dupefilter import SimpleDupefilter
from queue import SpiderQueue
from slave.rpc.state import SlaveRPC
from slave.spiders.hhu_crawler import HHUCrawler


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
        crawler = HHUCrawler(self.task_info['start_url'], self.task_info['allowed_domain'])
        dupefilter = SimpleDupefilter(self.server, self.task_info['dupefilter_key'])

        queue.push(self.task_info['start_url'])
        while True:
            if len(queue) > 0:
                current_url = queue.pop()
                crawler.fetch(current_url)

                # if crawler successful fetch the content
                if crawler.success:
                    next_urls = crawler.parse()
                    next_urls_count = 0
                    for next_url in next_urls:
                        if not dupefilter.exists(next_url):
                            queue.push(next_url)
                            next_urls_count += 1

                    print "Crawler fetched %s and get %d urls" % (current_url, next_urls_count)
                    self.rpc_proxy.server.fetch(self.name, current_url)

            else:
                print "Wait for tasks..."
                time.sleep(3)

    def run(self):
        pass

    def close(self):
        self.queue.clear()
        self.dupefilter.clear()

