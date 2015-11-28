from optparse import OptionParser

from master.comm.rpc import MasterRPC
import sys
import logging

def error(msg):
    print >> sys.stderr, msg
    print >> sys.stderr, "Use --help to show usage."
    exit(2)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-m", "--mq", help="address of message queue", dest="mq")
    (options, args) = parser.parse_args()

    (redis_host, redis_port) = options.mq.split(':')
    rpc_proxy = MasterRPC(redis_host, redis_port)




