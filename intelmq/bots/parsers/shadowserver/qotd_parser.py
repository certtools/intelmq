# -*- coding: utf-8 -*-
"""
https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-QOTD

timestamp 	Time that the IP was probed in UTC+0
ip 	The IP address of the device in question
protocol 	Protocol that the DNS response came on (usually UDP)
port 	Port that the CharGen response came from
hostname 	Reverse DNS name of the device in question
tag 	will always be qotd
quote 	The quote that was sent in response
asn 	ASN of where the device in question resides
geo 	Country where the device in question resides
region 	State / Province / Administrative region where the device in question
    resides
city 	City in which the device in question resides
naics   [UNDOCUMENTED]
sic [UNDOCUMENTED]
sector  [UNDOCUMENTED]
"""
import csv
import io
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class ShadowServerQotdParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report["raw"])
        for row in csv.DictReader(io.StringIO(raw_report), dictreader=True):
            event = Event(report)
            extra = {}

            event.add('time.source', row['timestamp']+' UTC')
            event.add('source.ip', row['ip'])
            event.add('protocol.transport', row['protocol'])
            event.add('source.port', row['port'])
            event.add('source.reverse_dns', row['hostname'])
            event.add('protocol.application', row['tag'])
            extra['quote'] = row['quote']
            event.add('source.asn', row['asn'])
            event.add('source.geolocation.cc', row['geo'])
            event.add('source.geolocation.region', row['region'])
            event.add('source.geolocation.city', row['city'])
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])
            if row['sector']:
                extra['sector'] = row['sector']

            event.add('extra', extra)
            event.add('classification.type', 'vulnerable service')
            event.add('classification.identifier', 'qotd')
            event.add('raw', '"'+','.join(map(str, row.items()))+'"')

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerQotdParserBot(sys.argv[1])
    bot.start()
