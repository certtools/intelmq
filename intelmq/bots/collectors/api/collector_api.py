# -*- coding: utf-8 -*-
"""
API Collector bot
"""
from threading import Thread

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import tornado.web
    from tornado.ioloop import IOLoop
except ImportError:
    IOLoop = None
else:
    class Application(tornado.web.Application):
        def __init__(self, request_handler, *args, **kwargs):
            self.request_handler = request_handler
            super().__init__(*args, **kwargs)

    class MainHandler(tornado.web.RequestHandler):
        def post(self):
            data = self.request.body
            self.application.request_handler(data)


class APICollectorBot(CollectorBot):
    collector_empty_process = True
    is_multithreadable = False

    def init(self):
        if IOLoop is None:
            raise MissingDependencyError("tornado")

        app = Application(self.request_handler, [
            ("/intelmq/push", MainHandler),
        ])

        self.port = getattr(self.parameters, 'port', 5000)
        self.server = app.listen(self.port)
        self.eventLoopThread = Thread(target=IOLoop.current().start)
        self.eventLoopThread.daemon = True
        self.eventLoopThread.start()

    def request_handler(self, data):
        report = self.new_report()
        report.add("raw", data)
        self.send_message(report)

    def process(self):
        pass

    def shutdown(self):
        if self.server:
            # Closes the server and the socket, prevents address already in use
            self.server.stop()
        if IOLoop.current():
            IOLoop.current().stop()


BOT = APICollectorBot
