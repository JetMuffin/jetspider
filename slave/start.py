from rpc.state import SlaveRPC
import sys

def usage():
    print "<Usage>: python start.py <master-ip:port> slave_id"
    sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()

    try:
        splits = sys.argv[1].split(":")
        master_ip = splits[0]
        port = splits[1]
        rpc_proxy = SlaveRPC(sys.argv[2], master_ip, port)
        rpc_proxy.monitor()
    except Exception,e:
        print e
        usage()