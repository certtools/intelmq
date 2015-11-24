# -*- coding: utf-8 -*-
"""
https://www.shadowserver.org/wiki/pmwiki.php/Services/Botnet-Drone-Hadoop

Timestamp 	Timestamp the IP was seen in UTC+0
ip 	The IP of the device in question
port 	Source port of the IP connection
asn 	ASN where the drone resides
geo 	Country where the drone resides
region 	State or province from the Geo
city 	City from the Geo
hostname 	Reverse DNS of the IP of the drone
type 	Packet type of the connection traffic (udp/tcp)
infection 	Infection name if known
url 	Connection URL if applicable
agent 	HTTP connection agent if applicable
cc 	The Command and Control that is managing this IP
cc_port 	Server side port that the IP connected to
cc_asn 	ASN of the C&C
cc_geo 	Country of the C&C
cc_dns 	Fully qualified domain name of the C&C
count 	Number of connections from this drone IP
proxy 	If the connection went through a known proxy system
application 	Application name / Layer 7 protocol
p0f_genre 	Operating System family
p0f_detail 	Operating System version
machine_name 	Name of the compromised machine
id 	Bot ID
naics   [UNDOCUMENTED]
sic [UNDOCUMENTED]
"""
from __future__ import unicode_literals

import sys
if sys.version_info[0] == 2:
    import unicodecsv as csv
else:
    import csv
import io

import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class ShadowServerDroneParserBot(Bot):

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
            event.add('source.port', row['port'], sanitize=True)
            event.add('source.asn', row['asn'], sanitize=True)
            event.add('source.geolocation.cc', row['geo'], sanitize=True)
            event.add('source.geolocation.region', row['region'],
                      sanitize=True)
            event.add('source.geolocation.city', row['city'], sanitize=True)
            if row['hostname']:
                event.add('source.reverse_dns', row['hostname'], sanitize=True)
            event.add('protocol.transport', row['type'], sanitize=True)
            event.add('malware.name', row['infection'], sanitize=True)
            if row['url']:
                event.add('destination.url', row['url'], sanitize=True)
            if row['agent']:
                extra['user_agent'] = row['agent']
            event.add('destination.ip', row['cc'], sanitize=True)
            event.add('destination.port', row['cc_port'], sanitize=True)
            event.add('destination.asn', row['cc_asn'], sanitize=True)
            event.add('destination.geolocation.cc', row['cc_geo'],
                      sanitize=True)
            if row['cc_dns']:
                event.add('destination.reverse_dns', row['cc_dns'],
                          sanitize=True)
            extra['connection_count'] = int(row['count'])
            if row['proxy']:
                extra['proxy'] = row['proxy']
            if row['application']:
                event.add('protocol.application', row['type'], sanitize=True)
            extra['os.name'] = row['p0f_genre']
            extra['os.version'] = row['p0f_detail']
            if 'machine_name' in row and row['machine_name']:
                event.add('source.local_hostname', row['type'], sanitize=True)
            if 'id' in row and row['id']:
                extra['bot_id'] = row['id']
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])

            event.add('extra', json.dumps(extra), sanitize=True)
            event.add('classification.type', 'botnet drone')
            event.add('raw', '"'+','.join(map(str, row.items()))+'"',
                      sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerDroneParserBot(sys.argv[1])
    bot.start()
