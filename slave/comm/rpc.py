import rpyc
import psutil
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

class SlaveRPC:
    # TODO read from configuration file
    def __init__(self, ip="127.0.0.1", port=8781):
        self.connection = rpyc.connect(ip, port)
        self.server = self.connection.root
        logging.info("Connecting master at %s:%s..." % (ip, port))

    def register(self, slave):
        if self.server.register(slave['name'], slave):
            logging.info("Register to master with name %s successful." % slave['name'])
            return True
        else:
            logging.info("Slave name %s has been used, please change another one." % slave['name'])
            return False

    def disconnect(self, slave):
        self.server.disconnect(slave['name'])
        logging.info("Disconnect from master...")

    def heartbeat(self, slave, interval=3):
        while True:
            phymem = psutil.virtual_memory()
            state = {
                "cpu": str(psutil.cpu_percent(1)) + "%",
                "mem_used": str(int(phymem.used / 1024 / 1024)) + "MB",
                "mem_total": str(int(phymem.total / 1024 / 1024)) + "MB",
                "mem_percent": str(phymem.percent) + "%"
            }
            self.server.heartbeat(slave['name'], state)
            time.sleep(interval)

    def close(self):
        self.connection.close()
