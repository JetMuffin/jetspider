from rpyc import Service
from rpyc.utils.server import ThreadedServer
import logging

"""
TODO logging
"""
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/master.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

slaves = {}

class MasterRPCService(Service):
    def exposed_register(self, slave_id):
        slaves[slave_id] = ""
        print "Slave registered whith id %s"%slave_id

    def exposed_heartbeat(self, slave_id, slave_state):
        slaves[slave_id] = slave_state
        logging.info("Received heartbeat from slave %s : %s"%(slave_id, slave_state))

class MasterRPC:
    def __init__(self, port=9999, auto_register=False):
        self.server = ThreadedServer(MasterRPCService, port=port, auto_register=auto_register)
        logging.info("Start master on port %d...", port)
        self.server.start()

    def close(self):
        self.server.close()




