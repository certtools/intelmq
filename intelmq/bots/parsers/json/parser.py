"""
JSON Parser Bot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH
"""
import sys

from intelmq.lib.bot import Bot
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import base64_decode


class JSONParserBot(Bot):

    def process(self):
        report = self.receive_message()

        event = MessageFactory.unserialize(base64_decode(report['raw']))

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = JSONParserBot(sys.argv[1])
    bot.start()
