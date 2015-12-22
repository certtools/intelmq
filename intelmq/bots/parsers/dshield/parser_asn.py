# -*- coding: utf-8 -*-
"""
# created: Tue, 22 Dec 2015 12:19:03 +0000#
# Source IP is 0 padded so each byte is three digits long
# Reports: number of packets received
# Targets: number of target IPs that reported packets from this source.
# First Seen: First time we saw a packet from this source
# Last Seen: Last time we saw a packet from this source
# Updated: Last time the record was updated.
#
# IPs are removed if they have not been seen in 30 days.
#
# source IP <tab> Reports <tab> Targets <tab> First Seen <tab> Last Seen <tab> Updated <CR>
"""
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class DShieldASNParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):

            if row.startswith('#'):
                continue

            values = row.split("\t")

            if len(values) < 6:
                continue    # raise an error

            source_ip = '.'.join(map(str, map(int, values[0].split('.'))))
            reports = int(values[1])
            targets = int(values[2])
#            first_seen = values[3]  # often missing
            last_seen = values[4]
            updated = values[5]

            url = report['feed.url']
            asn = int(url[url.rfind('?as=')+4:])

            event = Event(report)

            event.add('source.ip', source_ip, sanitize=True)
            event.add('source.asn', asn, sanitize=True)
            event.add('classification.type', 'brute-force')
            event.add("time.source", updated+'+0', sanitize=True)
            event.add("raw", row, sanitize=True)
            event.add("extra", {'reports': reports, 'targets': targets,
                                'last_seen': last_seen}, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DShieldASNParserBot(sys.argv[1])
    bot.start()
