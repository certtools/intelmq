# -*- coding: utf-8 -*-
"""
API Collector bot
"""
import logging
from tornado.ioloop import IOLoop
import tornado.web
from threading import Thread

from intelmq.lib.bot import CollectorBot

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

class APICollectorBot(CollectorBot):
    def init(self):
        app = Application(self, [
            (r"/json", MainHandler),
        ])

        self.port = getattr(self.parameters, 'port', 5000)

        app.listen(self.port)
        self.eventLoopThread = Thread(target=tornadoEventLoop)
        self.eventLoopThread.start()

    def processRequest(self, json):
        response = {'json': json}

        report = self.new_report()
        report.add("raw", json)
        self.send_message(report)

    def process(self):
        pass

    def shutdown(self):
        IOLoop.instance().stop()
        self.eventLoopThread.join()

BOT = APICollectorBot
