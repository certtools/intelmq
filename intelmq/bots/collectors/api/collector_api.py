# -*- coding: utf-8 -*-
"""
API Collector bot
"""
from threading import Thread

from intelmq.lib.bot import CollectorBot

try:
    import tornado.web
    from tornado.ioloop import IOLoop

    class Application(tornado.web.Application):
        def __init__(self, bot, *args, **kwargs):
            self.bot = bot
            super().__init__(*args, **kwargs)

    class MainHandler(tornado.web.RequestHandler):
        def post(self):
            json = self.request.body
            self.write(json)
            self.application.bot.processRequest(json)
except ImportError:
    IOLoop = None


class APICollectorBot(CollectorBot):
    def init(self):
        if IOLoop is None:
            raise ValueError("Could not import 'tornado'. Please install it.")

        app = Application(self, [
            (r"/api", MainHandler),
        ])

        self.port = getattr(self.parameters, 'port', 5000)
        app.listen(self.port)
        self.eventLoopThread = Thread(target=IOLoop.current().start)
        self.eventLoopThread.daemon = True
        self.eventLoopThread.start()

    def processRequest(self, json):
        report = self.new_report()
        report.add("raw", json)
        self.send_message(report)

    def process(self):
        pass

    def shutdown(self):
        IOLoop.current().stop()

BOT = APICollectorBot
