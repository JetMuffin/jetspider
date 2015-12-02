import tornado
import time
from mq.queue import MessageQueue
from tornado.websocket import WebSocketHandler


class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.write_message('Connected to socket server successful.')
        self.clients.add(self)

    def on_message(self, message):
        self.send_to_all(message)

    def send_to_all(self, message):
        for client in self.clients:
            client.write_message(message)

    def on_close(self):
        self.clients.remove(self)

class ConsoleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'console.html',
            page_title="Console",
        )
