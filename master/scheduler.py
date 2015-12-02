import logging
from optparse import OptionParser
import sys
from comm.http import HttpClient
from rpyc import Service
from rpyc.utils.server import ThreadedServer
from redis import Redis

class Scheduler(object):
    task = {}
    DEFAULT_TASK_INFO = {
        "master_addr": "127.0.0.1",
        "redis_host": "127.0.0.1",
        "redis_port": 6379,
        "start_url": "http://www.sunzequn.com",
        "allowed_domain": "www.sunzequn.com",
        "spider_queue_key": "spider_url",
        "spider_dupefilter_key": "spider_df",
        "spider_stored_table": "page_detail",
        "parser_queue_key": "parser_task",
        "reverse_index_table": "reverse_index",
        "db_host": "127.0.0.1",
        "db_port": 27017,
        "db_name": "spider_db",
    }

    def __init__(self, task):
        self.task = self.init_task(task)

    def init_task(self, task):
        _task = self.DEFAULT_TASK_INFO
        for key in task.keys():
            _task[key] = task[key]
        return _task

    def run(self):
        redis_server = Redis("127.0.0.1", "6379")
        redis_server.publish("task", self.task)
        print self.task
