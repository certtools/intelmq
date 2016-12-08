# -*- coding: utf-8 -*-
"""
#   primary URL: http://feeds.dshield.org/block.txt
#     PGP Sign.: http://feeds.dshield.org/block.txt.asc
#
#    updated: Tue Dec 15 15:33:38 2015 UTC
#
#    This list summarizes the top 20 attacking class C (/24) subnets
#   over the last three days. The number of 'attacks' indicates the
#   number of targets reporting scans from this subnet.
#
#    Columns (tab delimited):
#    (1) start of netblock
#    (2) end of netblock
#    (3) subnet (/24 for class C)
#    (4) number of targets scanned
#    (5) name of Network
#    (6) Country
#    (7) contact email address
"""


import dateutil

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class DshieldBlockParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():

            row = row.strip()

            if row.startswith("#") or len(row) == 0 or row.startswith('Start'):
                if 'updated' in row:
                    time_str = row[row.find(': ') + 2:]
                    time = dateutil.parser.parse(time_str).isoformat()
                continue

            values = row.split("\t")

            if len(values) < 3:
                continue    # raise an error

            network_ip = values[0]
            network_mask = values[2]
            network = '%s/%s' % (network_ip, network_mask)

            extra = {}
            event = self.new_event(report)

            if len(values) > 3:
                extra['attacks'] = int(values[3])
            if len(values) > 4:
                extra['network_name'] = values[4]
            if len(values) > 5:
                event['source.geolocation.cc'] = values[5]
            if len(values) > 6:
                event['source.abuse_contact'] = values[6]

            if extra:
                event.add('extra', extra)

            event.add('time.source', time)
            event.add('source.network', network)
            event.add('classification.type', 'blacklist')
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = DshieldBlockParserBot
