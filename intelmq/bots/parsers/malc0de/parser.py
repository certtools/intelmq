# SPDX-FileCopyrightText: 2016 jgedeon120
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
""" IntelMQ parser for Malc0de feeds """

import dateutil.parser

from intelmq.lib.bot import ParserBot


class Malc0deParserBot(ParserBot):
    """Parse the Malc0de IP feed in either IP Blacklist, Windows Format or Bind format"""

    WINDOWS_FORMAT = {'http://malc0de.com/bl/BOOT',
                      'https://malc0de.com/bl/BOOT'}

    BIND_FORMAT = {'http://malc0de.com/bl/ZONES',
                   'https://malc0de.com/bl/ZONES'}

    IP_BLACKLIST = {'http://malc0de.com/bl/IP_Blacklist.txt',
                    'https://malc0de.com/bl/IP_Blacklist.txt'}
    _lastgenerated = None

    def parse_line(self, line, report):

        if line.startswith('//') or len(line) == 0:
            self.tempdata.append(line)
            if '// Last updated' in line:
                self._lastgenerated = line.strip('// Last updated ')
                self._lastgenerated = dateutil.parser.parse(self._lastgenerated + 'T00:00:00+00:00').isoformat()

        else:
            event = self.new_event(report)
            if self._lastgenerated:
                event.add('time.source', self._lastgenerated)
            event.add('classification.type', 'malware-distribution')
            event.add('raw', line)

            if report['feed.url'] in Malc0deParserBot.WINDOWS_FORMAT:
                value = line.split(' ')[1]
                event.add('source.fqdn', value)
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)

            elif report['feed.url'] in Malc0deParserBot.BIND_FORMAT:
                value = line.split(' ')[1].strip('"')
                event.add('source.fqdn', value)
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)

            elif report['feed.url'] in Malc0deParserBot.IP_BLACKLIST:
                value = line.strip()
                event.add('source.ip', value)
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)

            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'])

            yield event


BOT = Malc0deParserBot
