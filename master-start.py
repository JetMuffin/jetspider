from master.comm.rpc import MasterRPC
import sys
import logging

def usage():
    print "<Usage>: python start.py"
    sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 1:
        usage()

    try:
        rpc_proxy = MasterRPC()
    except Exception,e:
        print e
        usage()