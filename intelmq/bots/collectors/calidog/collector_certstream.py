# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

"""
    A Bot to collect data from the Certificate Transparency Log (CTL)
    This bot works based on certstream library (https://github.com/CaliDog/certstream-python)
    @author: Florian Krenn, Christoph Giese (Telekom Security)
    No parameters necessary.

"""
import json

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    from certstream.core import CertStreamClient
except ImportError:
    CertStreamClient = None


class CertstreamCollectorBot(CollectorBot):
    """Collect information from CertStream certificate transparency logs"""

    def init(self):
        if CertStreamClient is None:
            raise MissingDependencyError("certstream")

    def callback(self, message, context=None):  # callback handler for certstream events.
        CertstreamCollectorBot.send_update(message=message, self=self)

    def process(self):
        c = CertStreamClient(self.callback, skip_heartbeats=True, on_open=None, on_error=None, url='wss://certstream.calidog.io/')
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
