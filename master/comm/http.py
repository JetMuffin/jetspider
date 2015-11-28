import urllib2


class HttpClient:

    MESSAGE_API = "/apis/message"

    # Communicate with webserver
    # use REST APIs
    def __init__(self, addr="127.0.0.1"):
        self.addr = addr
        self.message_api = "http://" + self.addr + self.MESSAGE_API

    def post(self, params):
        urllib2.urlopen(self.message_api, params)

    def get(self):
        pass
