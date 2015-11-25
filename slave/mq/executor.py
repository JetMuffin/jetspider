import redis
from .queue import  SpiderQueue
from .dupefilter import SimpleDupefilter

JOB_OVER = False
class Executor(object):

    def __init__(self, server, queue_key, dupefilter_key):

        self.server = server
        self.queue_key = queue_key
        self.dupefilter_key = dupefilter_key


    def run(self, crawler):
        """execute task"""
        self.queue = SpiderQueue(self.server, self.queue_key)
        self.crawler = crawler
        self.dupefilter = SimpleDupefilter(self.server, self.dupefilter_key)
        self.queue.push(self.crawler.start_url)
        while not JOB_OVER and not self.queue.empty():
            current_url = self.queue.pop()
            self.crawler.fetch(current_url)

            # if crawler successful fetch the content
            if(self.crawler.success):
                next_urls = self.crawler.parse()
                next_urls_count = 0
                for next_url in next_urls:
                    if(not self.dupefilter.exists(next_url)):
                        self.queue.push(next_url)
                        next_urls_count += 1

                print "crawler fetched %s and get %d urls"%(current_url,next_urls_count)

    def close(self):
        self.queue.clear()
        self.dupefilter.clear()

