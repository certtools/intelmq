# -*- coding: utf-8 -*-
"""
ATDParserBot parses data from McAfee Advanced Threat Defense.

The following information is forwarded via queue:
IP
URL
Hash
"""
from __future__ import unicode_literals
import sys

# imports for additional libraries and intelmq
from intelmq.lib.bot import Bot


class ATDParserBot(Bot):
    def process(self):
        report = self.receive_message()

        event = self.new_event(report)  # copies feed.name, time.observation
        ... # implement the logic here
        event.add('source.ip', '127.0.0.1')
        event.add('extra', {"os.name": "Linux"})

        self.send_message(event)
        self.acknowledge_message()


BOT = ATDParserBot
