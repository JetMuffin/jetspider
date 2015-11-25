import redis
from mq.executors import Executor
from spiders.hhu_crawler import HHUCrawler

start_url = "http://jetmuffin.github.io"
allowed_domain = "jetmuffin.github.io"
server = redis.Redis("127.0.0.1", 6379)
test_executor = Executor(server, "url", "df")
test_crawler = HHUCrawler(start_url, allowed_domain)
test_executor.run(test_crawler)
test_executor.close()
