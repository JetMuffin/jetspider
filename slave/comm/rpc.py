import rpyc
import psutil
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')


class SlaveRPC:
    # TODO read from configuration file
    def __init__(self, name="unknown", ip="127.0.0.1", port=9999):
        self.name = name
        self.connection = rpyc.connect(ip, port)
        self.server = self.connection.root
        logging.info("Connecting master at %s:%s..." % (ip, port))

    def heartbeat(self, interval=3):
        while True:
            phymem = psutil.virtual_memory()
            state = {
                "cpu": str(psutil.cpu_percent(1)) + "%",
                "mem_used": str(int(phymem.used / 1024 / 1024)) + "MB",
                "mem_total": str(int(phymem.total / 1024 / 1024)) + "MB",
                "mem_percent": str(phymem.percent) + "%"
            }
            self.server.heartbeat(self.name, state)
            time.sleep(interval)

    def monitor(self, interval=3):
        """TODO fix bug"""
        health_thread = threading.Thread(target=self.heartbeat())
        health_thread.setDaemon(True)
        health_thread.start()

    def close(self):
        self.connection.close()
