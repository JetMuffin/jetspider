from rpyc import Service
from rpyc.utils.server import ThreadedServer
import logging
import urllib, urllib2
from websocket import create_connection

from master.comm.http import HttpClient

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='logs/master.log',
#                     filemode='w')
#
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

DEFAULT_TASK_INFO = {
    "master_addr": "127.0.0.1",
    "redis_ip": "127.0.0.1",
    "redis_port": 6379,
    "start_url": "http://www.sunzequn.com",
    "allowed_domain": "www.sunzequn.com",
    "spider_queue_key": "spider_url",
    "spider_dupefilter_key": "spider_df",
    "spider_stored_table": "page_detail",
    "parser_queue_key": "parser_task",
    "reverse_index_table": "reverse_index",
    "db_ip": "127.0.0.1",
    "db_port": 27017,
    "db_name": "spider_db",
}
task_info = {}
slaves = {}
http = HttpClient()


class MasterRPCService(Service):
    def exposed_register(self, slave_id):
        slaves[slave_id] = ""
        logging.info("Slave registered whith id %s" % slave_id)
        http.post("Slave registered whith id %s" % slave_id)

    def exposed_heartbeat(self, slave_id, slave_state):
        slaves[slave_id] = slave_state
        logging.info("Received heartbeat from slave %s : %s" % (slave_id, slave_state))
        http.post("Received heartbeat from slave %s : %s" % (slave_id, slave_state))

    def exposed_message(self, slave_id, message):
        logging.info("[%s]: %s" % (slave_id, message))
        http.post("[%s]: %s" % (slave_id, message))

class MasterRPC:
    def __init__(self, addr="127.0.0.1", port=9999, auto_register=False, task=DEFAULT_TASK_INFO):
        global task_info
        task_info = self._init_task(task)
        self.server = ThreadedServer(MasterRPCService, port=port, auto_register=auto_register)

        logging.info("Start master on port %d..." % port)
        http.post("Start master on port %d..." % port)

        print task_info
        self.server.start()

    def close(self):
        self.server.close()
