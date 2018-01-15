#this will be benkow cc parser


# -*- coding: utf-8 -*-
"""
ExampleParserBot parses data from example.com.

Document possible necessary configurations.
"""
from __future__ import unicode_literals
import sys

# imports for additional libraries and intelmq
from intelmq.lib.bot import ParserBot


class BenkowCCParserBot(ParserBot):
    def parse_line(self,line,report):
				
        event = self.new_event(report)  # copies feed.name, time.observation
        ... # implement the logic here
        event.add('source.ip', '127.0.0.1')
        event.add('extra', {"os.name": "Linux"})

				event.add("raw",line)
				yield event

BOT = BenkowCCParserBot
