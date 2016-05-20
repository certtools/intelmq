# -*- coding: utf-8 -*-

"""
https://www.shadowserver.org/wiki/pmwiki.php/Services/NTP-Monitor

timestamp     Time that the IP was probed in UTC+0
ip            The IP address of the device in question
protocol      Protocol that the NTP response came on (UDP)
port          Port that the NTP response came from
hostname      Reverse DNS name of the device in question
packets       The total number of packets received from the device in question
size          The total amount of data (in bytes) received from the device in question
asn           ASN of where the device in question resides
geo           Country where the device in question resides
region        State / Province / Administrative region where the device in question resides
city          City in which the device in question resides
sector        [UNDOCUMENTED]
naics         [UNDOCUMENTED]
sic           [UNDOCUMENTED]
"""

import csv
import io
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

from intelmq.lib.exceptions import InvalidValue


class ShadowServerNTPParserBot(Bot):

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
            # TODO: clarify appropriate classification.type
            event.add('classification.type', 'exploit')

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
            if row['sector']:
                extra['sector'] = row['sector']
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])

            event.add('raw', '"'+','.join(map(str, row.items()))+'"')
            if extra:
                event.add('extra', extra)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerNTPParserBot(sys.argv[1])
    bot.start()
