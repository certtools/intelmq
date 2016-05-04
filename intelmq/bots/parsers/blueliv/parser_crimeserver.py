# -*- coding: utf-8 -*-
"""
"""

import json
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

TYPES = {
    'PHISHING': 'phishing',
    'MALWARE': 'malware',
    'EXPLOIT_KIT': 'exploit',
    'BACKDOOR': 'backdoor',
    'C_AND_C': 'c&c'
}


class BluelivCrimeserverParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get('raw'))

        for item in json.loads(raw_report):
            event = Event(report)
            if 'url' in item:
                event.add('source.url', item['url'])
            if 'ip' in item:
                event.add('source.ip', item['ip'])
            if 'country' in item:
                event.add('source.geolocation.cc', item['country'])
            if 'type' in item:
                event.add('classification.type', TYPES[item['type']])
            if 'firstSeenAt' in item:
                event.add('time.source', item['firstSeenAt'][:-4] + '00:00')
            event.add("raw", json.dumps(item, sort_keys=True))
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = BluelivCrimeserverParserBot(sys.argv[1])
    bot.start()
