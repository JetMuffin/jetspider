import tornado


class TaskHandler(tornado.web.RequestHandler):
    def post(self):
        db_addr = self.get_argument("db_addr")
        start_url = self.get_argument("start_url")
        allowed_domain = self.get_argument("allowed_domain")

        print db_addr, start_url, allowed_domain