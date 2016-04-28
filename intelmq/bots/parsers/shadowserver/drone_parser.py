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
import csv
import io
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class ShadowServerDroneParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report["raw"])
        for row in csv.DictReader(io.StringIO(raw_report), dictreader=True):
            event = Event(report)
            extra = {}

            event.add('time.source', row['timestamp']+' UTC')
            event.add('source.ip', row['ip'])
            event.add('source.port', row['port'])
            event.add('source.asn', row['asn'])
            event.add('source.geolocation.cc', row['geo'])
            event.add('source.geolocation.region', row['region'])
            event.add('source.geolocation.city', row['city'])
            if row['hostname']:
                event.add('source.reverse_dns', row['hostname'])
            event.add('protocol.transport', row['type'])
            event.add('malware.name', row['infection'])
            if row['url']:
                event.add('destination.url', row['url'])
            if row['agent']:
                extra['user_agent'] = row['agent']
            event.add('destination.ip', row['cc'])
            event.add('destination.port', row['cc_port'])
            event.add('destination.asn', row['cc_asn'])
            event.add('destination.geolocation.cc', row['cc_geo'])
            if row['cc_dns']:
                event.add('destination.reverse_dns', row['cc_dns'])
            extra['connection_count'] = int(row['count'])
            if row['proxy']:
                extra['proxy'] = row['proxy']
            if row['application']:
                event.add('protocol.application', row['type'])
            extra['os.name'] = row['p0f_genre']
            extra['os.version'] = row['p0f_detail']
            if 'machine_name' in row and row['machine_name']:
                event.add('source.local_hostname', row['type'])
            if 'id' in row and row['id']:
                extra['bot_id'] = row['id']
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])

            event.add('extra', extra)
            event.add('classification.type', 'botnet drone')
            event.add('raw', '"'+','.join(map(str, row.items()))+'"')

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerDroneParserBot(sys.argv[1])
    bot.start()
