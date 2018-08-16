# -*- coding: utf-8 -*-

"""
    A Bot to collect data from the Certificate Transparency Log (CTL)
    This bot works based on certstream libary (https://github.com/CaliDog/certstream-python)
    @author: Florian Krenn, Christoph Giese (Telekom Security)
    No parameters necessary.

"""
import json

from intelmq.lib.bot import CollectorBot

try:
    from certstream.core import CertStreamClient
except ImportError:
    CertStreamClient = None


class CertstreamCollectorBot(CollectorBot):
    def init(self):
        if CertStreamClient is None:
            raise ValueError("Could not import library 'certstream'. Please install it.")

    def callback(self, message, context=None):  # callback handler for certstream events.
        CertstreamCollectorBot.send_update(message=message, self=self)

    def process(self):
        c = CertStreamClient(self.callback, skip_heartbeats=True, on_open=None, on_error=None)
        c.run_forever()

    def send_update(self, message):

        if message['message_type'] == 'heartbeat':
            return

        elif message['message_type'] == 'certificate_update':
            new_report = self.new_report()
            new_report.add("raw", json.dumps(message))

            self.send_message(new_report)

        else:
            raise ValueError('Unhandled message_type %r.' % message['message_type'])


BOT = CertstreamCollectorBot
