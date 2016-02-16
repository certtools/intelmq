# -*- coding: utf-8 -*-
"""
#   DShield.org Suspicious Domain List
#
#   comments: info@dshield.org
#    updated: Tue Dec 22 04:10:10 2015 UTC
#
#    This list consists of High Level Sensitivity website URLs
#     Columns (tab delimited):
#
#      (1) site
"""
from __future__ import unicode_literals
import sys

import dateutil
from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class DshieldDomainParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.split('\n'):

            if row.startswith("#") or len(row) == 0 or row == "Site":
                if 'updated' in row:
                    time_str = row[row.find(': ') + 2:]
                    time = dateutil.parser.parse(time_str).isoformat()
                continue

            event = Event(report)

            event.add('classification.type', u'malware')
            event.add('source.fqdn', row.strip())
            event.add('time.source', time)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = DshieldDomainParserBot(sys.argv[1])
    bot.start()
