"""
JSON Parser Bot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH
"""
from intelmq.lib.bot import Bot
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import base64_decode


class JSONParserBot(Bot):

    def process(self):
        report = self.receive_message()
        if getattr(self.parameters, 'splitlines', False):
            lines = base64_decode(report['raw']).splitlines()
        else:
            lines = [base64_decode(report['raw'])]

        for line in lines:
            new_event = MessageFactory.unserialize(line,
                                                   harmonization=self.harmonization,
                                                   default_type='Event')
            event = self.new_event(report)
            dict.update(event, new_event)
            if 'raw' not in event:
                event['raw'] = line
            self.send_message(event)
        self.acknowledge_message()


BOT = JSONParserBot
