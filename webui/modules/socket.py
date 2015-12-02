import tornado


class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message('Welcome to WebSocket')


class ConsoleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'console.html',
            page_title="Console | JetSpider",
        )
