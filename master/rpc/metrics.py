from rpyc import Service
from rpyc.utils.server import ThreadedServer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

slaves = {}
task_info = {
    "redis_ip": "127.0.0.1",
    "redis_port": 6379,
    "start_url": "http://jetmuffin.github.io",
    "allowed_domain": "jetmuffin.github.io",
    "queue_key": "spider_url",
    "dupefilter_key": "spider_df",
    "db_ip": "127.0.0.1",
    "db_port": 27017,
    "db_name": "spider_db"
}


class MasterRPCService(Service):
    def exposed_register(self, slave_id):
        slaves[slave_id] = ""
        logging.info("Slave registered whith id %s" % slave_id)
        return task_info

    def exposed_heartbeat(self, slave_id, slave_state):
        slaves[slave_id] = slave_state
        logging.info("Received heartbeat from slave %s : %s" % (slave_id, slave_state))

    def exposed_message(self, slave_id, message):
        logging.info("[%s]: %s" % (slave_id, message))


class MasterRPC:
    def __init__(self, port=9999, auto_register=False):
        self.server = ThreadedServer(MasterRPCService, port=port, auto_register=auto_register)
        logging.info("Start master on port %d...", port)
        self.server.start()

    def close(self):
        self.server.close()
