# SPDX-FileCopyrightText: 2023 James Brine
#
# SPDX-License-Identifier: AGPL-3.0-or-later

""" IntelMQ parser for jamesbrine.com.au bruteforce IP feed """

import dateutil.parser
import posixpath
from urllib.parse import urlparse

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime


class JamesBrineParserBot(ParserBot):
    """
    Parse the jamesbrine.com.au host feed (csv)

    List of source fields:
    [
        'ip_address',
        'activity' (unused),
        'date'
    ]

    """

    def parse_line(self, line, report):
    if line.startswith('#') or len(line) == 0:
        self.tempdata.append(line)

    else:
        value = line.split(',')
        event = self.new_event(report)
        event.add('source.ip', value[1])
        event.add('time.source', value[3] + ' 00:00 UTC')
        event.add('classification.type', 'blacklist')
        event.add('raw', line)
              
        yield event


BOT = JamesBrineParserBot
