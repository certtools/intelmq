
"""
JSON Parser Bot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.

"""
from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import base64_decode
import json

class BlueShieldParserBot(ParserBot):

    def parse(self, report):
        self.logger.info('Bot start processing.')
        raw_report = utils.base64_decode(report.get("raw"))
        jsondict = json.loads(raw_report)

        for line in jsondict:
            new_event = MessageFactory.unserialize(line,harmonization=self.harmonization, default_type='Event')
            event = self.new_event(report)
            event.update(new_event)
            event.add('classification.type' ,line["c"])
            event.add('source.fqdn' ,line["d"])
        
            self.send_message(event)
        self.acknowledge_message()
    
BOT = BlueShieldParserBot