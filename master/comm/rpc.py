from rpyc import Service
from rpyc.utils.server import ThreadedServer
import logging

from mq.queue import MessageQueue
from mq.storage import SlaveStorage

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



class MasterRPCService(Service):
    def exposed_register(self, slave_id, slave_info):
        if (not slaves.get(slave_id)):
            slaves.set(slave_id, slave_info)
            logging.info("Slave registered with id %s" % slave_id)
            message_queue.push("Slave registered with id %s" % slave_id)
            return True
        else:
            return False

            # http.post("Slave registered whith id %s" % slave_id)

    def exposed_disconnect(self, slave_id):
        slaves.delete(slave_id)
        logging.info("[%s] lost connection." % slave_id)
        message_queue.push("[%s] lost connection." % slave_id)

    def exposed_heartbeat(self, slave_id, slave_state):
        slave_info = slaves.get(slave_id)
        slave_info['state'] = slave_state
        slaves.set(slave_id, slave_info)

        # logging.info("Received heartbeat from slave %s : %s" % (slave_id, slave_state))
        # http.post("Received heartbeat from slave %s : %s" % (slave_id, slave_state))

    def exposed_message(self, slave_id, message):
        logging.info("[%s]: %s" % (slave_id, message))
        # http.post("[%s]: %s" % (slave_id, message))


class MasterRPC:
    def __init__(self, redis_host, redis_port=6379, slaves_db=3, port=8780, auto_register=False):
        global slaves, message_queue
        slaves = SlaveStorage(slaves_db, redis_host, redis_port)
        message_queue = MessageQueue(host=redis_host, key="message_queue")
        self.server = ThreadedServer(MasterRPCService, port=port, auto_register=auto_register)

        logging.info("Start master on port %d..." % port)
        message_queue.push("Start master on port %d..." % port)
        # http.post("Start master on port %d..." % port)

        self.server.start()

    def close(self):
        self.server.close()


