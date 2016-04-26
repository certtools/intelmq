# -*- coding: utf-8 -*-
"""
https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-SNMP

timestamp 	Time that the IP was probed in UTC+0
ip 	The IP address of the device in question
protocol 	Protocol that the DNS response came on (usually UDP)
port 	Port that the SNMP response came from
hostname 	Reverse DNS name of the device in question
sysdesc 	System Description as obtained from OID 1.3.6.1.2.1.1.1
sysname 	System Name as obtained from OID 1.3.6.1.2.1.1.5
asn 	ASN of where the device in question resides
geo 	Country where the device in question resides
region 	State / Province / Administrative region where the device in question
    resides
city 	City in which the device in question resides
version 	The SNMP probe version that the IP responded to (usually 2)
naics   [UNDOCUMENTED]
sic [UNDOCUMENTED]
vector  [UNDOCUMENTED]
"""
import csv
import io
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class ShadowServerSNMPParserBot(Bot):

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
            extra['sysdesc'] = row['sysdesc']
            extra['sysname'] = row['sysname']
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
            event.add('protocol.application', 'snmp')
            event.add('classification.type', 'vulnerable service')
            event.add('classification.identifier', 'snmp')
            event.add('raw', '"'+','.join(map(str, row.items()))+'"')

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerSNMPParserBot(sys.argv[1])
    bot.start()
