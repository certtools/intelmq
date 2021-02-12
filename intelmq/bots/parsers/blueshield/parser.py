
"""
JSON Parser Bot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.

"""
from intelmq.lib.bot import Bot
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import base64_decode


class BlueShieldParserBot(Bot):

    def process(self):

        report = self.receive_message()
        lines = [base64_decode(report['raw'])]

        for line in lines:
           new_event = MessageFactory.unserialize(line,harmonization=self.harmonization, default_type='Event')
           event = self.new_event(report)
           event.update(new_event)
           event.add('classification.type' ,line["c"])
           event.add('source.fqdn' ,line["d"])
        
           self.send_message(event)
        self.acknowledge_message()
    
BOT = BlueShieldParserBot
