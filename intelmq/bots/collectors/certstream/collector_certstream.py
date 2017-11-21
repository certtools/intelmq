# -*- coding: utf-8 -*-

"""
    A Bot to collect data from the Certificate Transparency Log (CTL)
    This bot works based on certstream libary (https://github.com/CaliDog/certstream-python)
    @author: Florian Krenn, Christoph Giese (Telekom Security)
    No parameters necessary.

"""
import json
import sys
import certstream

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report


class CertstreamCollectorBot(CollectorBot):

    def init(self):

        return

    def callback(self, message, context=None):  # callback handler for certstream events.
        CertstreamCollectorBot.send_update(message=message, self=self)

    def process(self):
        certstream.listen_for_events(self.callback)

    def send_update(self, message):

        # self.logger.debug("Received new certificate update.")
        report = Report()

        if message['message_type'] == 'heartbeat':
            return

        if message['message_type'] == 'certificate_update':
            new_report = self.new_report()
            new_report.add("feed.name", "Certstream")
            new_report.add("raw", json.dumps(message))

            self.send_message(new_report)
            self.logger.debug("Send certificate_update.")


BOT = CertstreamCollectorBot
