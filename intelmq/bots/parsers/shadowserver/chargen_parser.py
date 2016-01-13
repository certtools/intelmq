# -*- coding: utf-8 -*-
"""
https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Chargen

Field 	Description
timestamp 	Time that the IP was probed in UTC+0
ip 	The IP address of the device in question
protocol 	Protocol that the DNS response came on (usually UDP)
port 	Port that the CharGen response came from
hostname 	Reverse DNS name of the device in question
tag 	will always be chargen
size 	The size of the response that was received (in bytes)
asn 	ASN of where the device in question resides
geo 	Country where the device in question resides
region 	State / Province / Administrative region where the device in question
    resides
city 	City in which the device in question resides
naics   [UNDOCUMENTED]
sic [UNDOCUMENTED]
sector  [UNDOCUMENTED]
"""
from __future__ import unicode_literals

import sys
if sys.version_info[0] == 2:
    import unicodecsv as csv
else:
    import csv
import io

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class ShadowServerChargenParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report["raw"])
        rows = csv.DictReader(io.StringIO(raw_report))

        for row in rows:
            event = Event(report)
            extra = {}

            event.add('time.source', row['timestamp']+' UTC', sanitize=True)
            event.add('source.ip', row['ip'], sanitize=True)
            event.add('protocol.transport', row['protocol'], sanitize=True)
            event.add('source.port', row['port'], sanitize=True)
            event.add('source.reverse_dns', row['hostname'], sanitize=True)
            extra['response_size'] = int(row['size'])
            event.add('source.asn', row['asn'], sanitize=True)
            event.add('source.geolocation.cc', row['geo'], sanitize=True)
            event.add('source.geolocation.city', row['city'], sanitize=True)
            event.add('source.geolocation.region', row['region'],
                      sanitize=True)
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])
            if row['sector']:
                extra['sector'] = row['sector']

            event.add('extra', extra, sanitize=True)
            event.add('classification.type', 'vulnerable service')
            event.add('classification.identifier', 'chargen')
            event.add('protocol.application', 'chargen')
            event.add('raw', '"'+','.join(map(str, row.items()))+'"',
                      sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerChargenParserBot(sys.argv[1])
    bot.start()
