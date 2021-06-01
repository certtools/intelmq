# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import re
import time

from intelmq.lib.bot import ParserBot


class DansParserBot(ParserBot):
    """Parse the MalwarePatrol Dans Guardian feed"""
    sourcetime = None

    def parse(self, report):
        report.change("feed.url", re.sub('receipt=([^&])*', '', report["feed.url"]))
        return super().parse(report)

    def parse_line(self, row, report):
        if row.startswith('#'):
            self.tempdata.append(row)
            if 'Generated at' in row:
                # This is UTC according to the feed
                self.sourcetime = time.strftime('%Y-%m-%dT%H:%M:%S+00:00',
                                                time.strptime(row.split()[3], '%Y%m%d%H%M%S'))
        else:
            event = self.new_event(report)
            if '://' not in row:
                event.add('source.url', 'http://' + row)
            else:
                event.add('source.url', row)
            event.add('classification.type', 'malware-distribution')
            event.add('time.source', self.sourcetime)
            event.add("raw", self.recover_line(row))

            yield event


BOT = DansParserBot
