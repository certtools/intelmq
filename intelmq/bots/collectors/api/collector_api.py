# SPDX-FileCopyrightText: 2018 tavi.poldma
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
API Collector bot
"""
from threading import Thread
from typing import Optional
import os
import socket

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import tornado.web
    from tornado.ioloop import IOLoop
    from tornado.netutil import bind_unix_socket
    from tornado.httpserver import HTTPServer
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
    """Collect data by exposing a HTTP API interface"""
    name: str = "API"
    port: int = 5000
    __collector_empty_process: bool = True
    provider: str = "APICollector"
    __is_multithreadable: bool = False
    use_socket = False
    socket_path = '/tmp/imq_api_default_socket'
    _server: Optional['HTTPServer'] = None
    _unix_socket: Optional[socket.socket] = None
    _eventLoopThread: Optional[Thread] = None

    def init(self):
        if IOLoop is None:
            raise MissingDependencyError("tornado")

        app = Application(self.request_handler, [
            ("/intelmq/push", MainHandler),
        ])

        if self.use_socket:
            self.server = HTTPServer(app)
            self._unix_socket = bind_unix_socket(self.socket_path)
            self.server.add_socket(self._unix_socket)
        else:
            self.server = app.listen(self.port)

        self._eventLoopThread = Thread(target=IOLoop.current().start)
        self._eventLoopThread.daemon = True
        self._eventLoopThread.start()

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

        loop = IOLoop.current()
        if loop:
            loop.add_callback(loop.stop)
            if self._eventLoopThread:
                self._eventLoopThread.join()


BOT = APICollectorBot
