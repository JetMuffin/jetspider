import logging
from optparse import OptionParser
import sys

from comm.http import HttpClient
from rpyc import Service
from rpyc.utils.server import ThreadedServer

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='../logs/master.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

http = HttpClient()

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


# class Scheduler(Service):



def init_task(task):
    _task = DEFAULT_TASK_INFO
    for key in task.keys():
        _task[key] = task[key]
    return _task


def error(msg):
    print >> sys.stderr, msg
    print >> sys.stderr, "Use --help to show usage."
    exit(2)


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-s", "--start_url", help="start url of task", dest="start_url")
    parser.add_option("-a", "--allowed_domain", help="allowed url", dest="allowed_url")

    (options, args) = parser.parse_args()

    task = {
        "start_url": options.start_url,
        "allowed_domain": options.allowed_url,
    }

    task = init_task(task)

