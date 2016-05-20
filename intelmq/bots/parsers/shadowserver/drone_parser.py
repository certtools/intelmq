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
cc_ip 	The Command and Control that is managing this IP
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

from intelmq.lib.exceptions import InvalidValue


class ShadowServerDroneParserBot(Bot):

    mapping = [
        ("destination.asn"            , "cc_asn"),
        ("destination.geolocation.cc" , "cc_geo"),
        ("destination.ip"             , "cc_ip"),
        ("destination.port"           , "cc_port"),
        ("destination.reverse_dns"    , "cc_dns"),
        ("destination.url"            , "url"),
        ("malware.name"               , "infection"),
        ("protocol.application"       , "application"),
        ("protocol.transport"         , "type"),
        ("source.asn"                 , "asn"),
        ("source.geolocation.cc"      , "geo"),
        ("source.geolocation.city"    , "city"),
        ("source.geolocation.region"  , "region"),
        ("source.local_hostname"      , "machine_name"),
        ("source.reverse_dns"         , "hostname"),
    ]

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report["raw"])
        for row in csv.DictReader(io.StringIO(raw_report)):

            event = Event(report)
            extra = {}

            # Required fields which must not fail
            event.add('time.source', row['timestamp']+' UTC')
            event.add('source.ip', row['ip'])
            event.add('source.port', row['port'])
            event.add('classification.type', 'botnet drone')

            # Add events
            for item in self.mapping:
                intelmq_key, shadow_key = item[:2]
                if len(item) > 2:
                    conv = item[2]
                else:
                    conv = None
                value = row.get(shadow_key)
                raw_value = value
                if raw_value is not None:
                    if conv is not None:
                        value = conv(raw_value)
                    else:
                        value = raw_value
                    try:
                        event.add(intelmq_key, value)
                    except InvalidValue:
                        self.logger.warn(
                                'Could not add event "{}";'\
                                ' adding it to extras...'.format(shadow_key)
                        )
                        extra[shadow_key] = raw_value

            # Add extras
            if row['agent']:
                extra['user_agent'] = row['agent']
            if row['count']:
                extra['connection_count'] = int(row['count'])
            if row['proxy']:
                extra['proxy'] = row['proxy']
            extra['os.name'] = row['p0f_genre']
            extra['os.version'] = row['p0f_detail']
            if 'id' in row and row['id']:
                extra['bot_id'] = row['id']
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])

            event.add('raw', '"'+','.join(map(str, row.items()))+'"')
            event.add('extra', extra)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerDroneParserBot(sys.argv[1])
    bot.start()
