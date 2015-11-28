import time

import redis
from mq.queue import FIFOQueue

from mq.dupefilter import SimpleDupefilter
from slave.comm.rpc import SlaveRPC
from slave.parsers.parsers import JiebaParser
from slave.pipelines.mongodb import MongodbPipeline
from slave.spiders.crawlers import SimpleCrawler


class Executor(object):
    def __init__(self, master_address, name):
        self.master_address = master_address
        self.name = name
        self.master_ip, self.master_port = master_address.split(":")

    def run(self):
        raise NotImplementedError

    def close(self):
        self.rpc_proxy.close()


class SpiderExecutor(Executor):

    # execute task
    # spider_queue: queue of splider url
    # task_queue: queue of process task
    # crawler: web crawler instance
    # dupefilter: reduplicate fiter
    # pipeline: persistent volumn pipeline
    def fetch(self):

        spider_queue = FIFOQueue(self.task_info['redis_host'], self.task_info['redis_port'], self.task_info['spider_queue_key'])
        task_queue = FIFOQueue(self.task_info['redis_host'], self.task_info['redis_port'], self.task_info['parser_queue_key'])
        crawler = SimpleCrawler(self.task_info['start_url'], self.task_info['allowed_domain'])
        dupefilter = SimpleDupefilter(self.task_info['redis_host'], self.task_info['redis_port'], self.task_info['spider_dupefilter_key'])
        pipeline = MongodbPipeline(self.task_info['db_host'], self.task_info['db_port'], self.task_info['db_name'])

        spider_queue.push(self.task_info['start_url'])

        # TODO shutdown signal
        while True:
            if len(spider_queue) > 0:
                current_url = spider_queue.pop()
                crawler.fetch(current_url)

                # if crawler successful fetch the content
                if crawler.success:
                    item = crawler.parse()
                    next_urls = item.get('links')
                    next_urls_count = 0
                    for next_url in next_urls:
                        if not dupefilter.exists(next_url):
                            spider_queue.push(next_url)
                            next_urls_count += 1

                    # print fetch infomation
                    print "Crawler fetched %s and get %d urls" % (current_url, next_urls_count)
                    self.rpc_proxy.server.message(self.name, "Success fetched url %s."%current_url)

                    item = pipeline.insert(item, self.task_info['spider_stored_table'])
                    task_queue.push(item.get('_id'))
                    self.rpc_proxy.server.message(self.name, "Stored url %s with ID %s."%(current_url, item.get('mongo_id')))

            else:
                print "Wait for tasks..."
                time.sleep(3)

    def run(self):
        pass


class ParserExecutor(Executor):

    def collect(self):
        queue = FIFOQueue(self.task_info['redis_host'], self.task_info['redis_port'], self.task_info['parser_queue_key'])
        pipeline = MongodbPipeline(self.task_info['db_host'], self.task_info['db_port'], self.task_info['db_name'])
        parser = JiebaParser()

        # TODO shutdown signal
        while True:
            if len(queue) > 0:
                page_id = queue.pop()
                item = pipeline.find(self.task_info['spider_stored_table'], page_id)
                terms = parser.segment(item['content'])
                terms_count = len(terms)

                # update item information to db
                item['terms'] = terms
                pipeline.update(self.task_info["spider_stored_table"], page_id, item)

                # connect to master
                self.rpc_proxy.server.message(self.name, "Parse page[%s] and get %d terms" % (page_id, terms_count))
                print("Parse page[%s] and get %d terms" % (page_id, terms_count))

            else:
                print "Wait for tasks..."
                time.sleep(3)

    def run(self):
        pass

