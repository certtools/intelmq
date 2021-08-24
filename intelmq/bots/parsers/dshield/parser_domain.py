# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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

import dateutil

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class DshieldDomainParserBot(Bot):
    """Parse the DShield Suspicious Domains feed"""

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():

            if row.startswith("#") or len(row) == 0 or row == "Site":
                if 'updated' in row:
                    time_str = row[row.find(': ') + 2:]
                    time = dateutil.parser.parse(time_str).isoformat()
                continue

            event = self.new_event(report)

            event.add('classification.type', 'malware-distribution')
            event.add('source.fqdn', row.strip())
            event.add('time.source', time)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = DshieldDomainParserBot
