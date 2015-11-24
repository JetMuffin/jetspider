from rpyc import Service
from rpyc.utils.server import ThreadedServer
import logging

slaves = {}

class MasterRPCService(Service):
    def exposed_register(self, slave_id):
        slaves[slave_id] = ""
        print "Slave registered whith id %s"%slave_id

    def exposed_heartbeat(self, slave_id, slave_state):
        slaves[slave_id] = slave_state
        print "Received heartbeat from slave %s : %s"%(slave_id, slave_state)

class MasterRPC:
    def __init__(self, port=9999, auto_register=False):
        self.server = ThreadedServer(MasterRPCService, port=port, auto_register=auto_register)
        self.server.start()

    def close(self):
        self.server.close()

if __name__ == "__main__":
    test = MasterRPC()


