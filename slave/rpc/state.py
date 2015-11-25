import rpyc
import psutil
import thread
import time
import logging

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


class SlaveRPC:
    #TODO read from configuration file
    def __init__(self, slave_id="unknown", ip="127.0.0.1", port=9999):
        self.slave_id = slave_id
        self.connection = rpyc.connect(ip, port)
        self.server = self.connection.root
        self.server.register(slave_id)
        logging.info("Connecting master at %s:%s..."%(ip, port))

    def heartbeat(self, interval=3):
        while True:
            phymem = psutil.virtual_memory()
            state = {
                "cpu" : str(psutil.cpu_percent(1)) + "%",
                "mem_used" : str(int(phymem.used/1024/1024))+"MB",
                "mem_total" : str(int(phymem.total/1024/1024))+"MB",
                "mem_percent" : str(phymem.percent) + "%"
            }
            self.server.heartbeat(self.slave_id, state)
            time.sleep(interval)

    def monitor(self, interval=3):
        thread.start_new(self.heartbeat())


    def close(self):
        self.connection.close()



