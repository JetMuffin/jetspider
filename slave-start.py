import re
import sys
from optparse import OptionParser

from slave.executors import SpiderExecutor, ParserExecutor
from slave.comm.rpc import SlaveRPC
from mq.queue import Subscribe

SLAVE_TYPE = ["spider", "parser"]
def error(msg):
    print >> sys.stderr, msg
    print >> sys.stderr, "Use --help to show usage."
    exit(2)


if __name__ == "__main__":

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-m", "--master", help="address of your cluster's master", dest="master")
    parser.add_option("-n", "--name", help="give a name to your slave", dest="name")
    parser.add_option("-t", "--type", default="crawler", help="slave type: spider or parser", dest="type")

    (options, args) = parser.parse_args()

    """ Handle input Error """
    if not options.master:
        error("Wrong options: Master address required.")
    else:
        pattern = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{2,5}')
        if not pattern.match(options.master):
            error("Wrong address, your address must be such format: <ip:port>")
    if not options.name:
        error("Wrong options: Slave name required.")
    if options.type not in SLAVE_TYPE:
        error("Wrong type: your slave's type must be spider or parser.")

    (master_host, master_port) = options.master.split(':')

    """ Register to master """
    slave = {
        "name": options.name,
        "type": options.type
    }
    rpc_proxy = SlaveRPC(master_host, master_port)
    if rpc_proxy.register(slave):

        """ Monitor heartbeat """
        # TODO debug monitor
        server = Subscribe("task", "127.0.0.1")

        try:
            # while True:
            #     rpc_proxy.heartbeat(slave, interval=5)
            for msg in server.ps.listen():
                if msg['type'] == 'message':
                    print "Receive task: ", msg['data']
                    task = eval(msg['data'])
                    if(options.type == "spider"):
                        executor = SpiderExecutor(options.master, options.name, task)
                        executor.fetch()

        except KeyboardInterrupt:
            rpc_proxy.disconnect(slave)


