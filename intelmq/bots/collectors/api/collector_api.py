# -*- coding: utf-8 -*-
"""
API Collector bot
"""
from threading import Thread

from intelmq.lib.bot import CollectorBot

try:
    import tornado.web
    from tornado.ioloop import IOLoop

    def tornadoEventLoop():
        IOLoop.instance().start()

    class Application(tornado.web.Application):
        def __init__(self, bot, *args, **kwargs):
            self.bot = bot
            super().__init__(*args, **kwargs)

    class MainHandler(tornado.web.RequestHandler):
        def post(self):
            json = self.get_argument("json")
            self.write(json)
            self.application.bot.processRequest(json)
except ImportError:
    IOLoop = None


class APICollectorBot(CollectorBot):
    def init(self):
        if IOLoop is None:
            raise ValueError("Could not import 'tornado'. Please install it.")
        app = Application(self, [
            (r"/json", MainHandler),
        ])

        self.port = getattr(self.parameters, 'port', 5000)

        app.listen(self.port)
        self.eventLoopThread = Thread(target=tornadoEventLoop)
        self.eventLoopThread.start()

    def processRequest(self, json):
        report = self.new_report()
        report.add("raw", json)
        self.send_message(report)

    def process(self):
        pass

    def shutdown(self):
        IOLoop.instance().stop()
        self.eventLoopThread.join()


BOT = APICollectorBot
