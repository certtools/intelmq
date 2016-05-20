# -*- coding: utf-8 -*-

"""
https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Memcached

timestamp         	 Time that the IP was probed in UTC+0
ip                	 The IP address of the device in question
protocol          	 Protocol that the Memcached response came on (always TCP)
port              	 Port that the Memcached response came from (usually 11211/TCP)
hostname          	 Reverse DNS name of the device in question
tag               	 will always be memcached
version           	 Memcached version number
asn               	 ASN of where the device in question resides
geo               	 Country where the device in question resides
region            	 State / Province / Administrative region where the device in question resides
city              	 City in which the device in question resides
naics             	 North American Industry Classification System Code
sic               	 Standard Industrial Classification System Code
pid               	 Process ID (PID) of the running Memcached server instance
pointer_size      	 the system architecture (32 or 64 bits)
uptime            	 Number of seconds since Memcached server start
time              	 The current time and date (in UTC) that Memcached thinks it is at the time the server was probed
curr_connections  	 The current number of client connections to the Memcached server
total_connections 	 The total number of client connections to the Memcached server since it was last restarted
sector            	 [UNDOCUMENTED]
"""

import csv
import io
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

from intelmq.lib.exceptions import InvalidValue


class ShadowServerOpenMemcachedParserBot(Bot):

    mapping = [
        ("protocol.transport"         , "protocol"),
        ("source.reverse_dns"         , "hostname"),
        ("source.asn"                 , "asn"),
        ("source.geolocation.cc"      , "geo"),
        ("source.geolocation.region"  , "region"),
        ("source.geolocation.city"    , "city"),
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
            event.add('classification.type', 'vulnerable service')

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
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])
            # documented extra fields
            for field in [
                    "tag"               ,
                    "version"           ,
                    "naics"             ,
                    "sic"               ,
                    "pid"               ,
                    "pointer_size"      ,
                    "uptime"            ,
                    "time"              ,
                    "curr_connections"  ,
                    "total_connections" ,
                    "sector"            ,
                    ]:
                if field in row:
                    extra[field] = row[field]

            event.add('raw', '"'+','.join(map(str, row.items()))+'"')
            if extra:
                event.add('extra', extra)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerOpenMemcachedParserBot(sys.argv[1])
    bot.start()
