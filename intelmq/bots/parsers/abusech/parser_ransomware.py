# -*- coding: utf-8 -*-
"""
Parser for Intelmq and Abuse.ch Ransomware feed.
"""

import csv
import io

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class AbuseCHRansomwaretrackerParserBot(Bot):
    """ Abuse.ch Ransomware Tracker Bot """

    def process(self):
        """
        The Ransomware Tracker has comments in it.
        The IP address field can also have more than one address.
        The ASN and Country code are being ignored, an expert parser can get those added.
        """

        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in csv.reader(io.StringIO(raw_report)):
            if row[0].startswith('#'):
                continue

            if '|' in row[7]:
                for ipaddr in row[7].split('|'):
                    new_row = '"' + row[0] + '","' + row[1] + '","' + row[2] + '","' + row[3] \
                              + '","' + row[4] + '","' + row[5] + '","' + row[6] + '","' + ipaddr \
                              + '","' + row[8] + '","' + row[9] + '"'

                    for nrow in csv.reader(io.StringIO(new_row)):
                        ev = Event(report)
                        ev.add('classification.identifier', nrow[2].lower())
                        ev.add('classification.type', 'c&c')
                        ev.add('time.source', nrow[0] + ' UTC', overwrite=True)
                        ev.add('status', nrow[5])
                        # in the feed sometimes a ',' is seen before srcip
                        # perhaps it is an error on feeds part
                        # however we have to deal with it
                        src_ip = nrow[7].strip(',')
                        if src_ip != '0.0.0.0':
                            ev.add('source.ip', src_ip, raise_failure=False)
                        # ev.add('source.ip', nrow[7])
                        ev.add('raw', ','.join(nrow))
                        ev.add('source.fqdn', nrow[3], raise_failure=False)
                        ev.add('source.url', nrow[4], raise_failure=False)
                        self.send_message(ev)
            else:
                event = Event(report)
                event.add('classification.identifier', row[2].lower())
                event.add('classification.type', 'c&c')
                event.add('time.source', row[0] + ' UTC')
                event.add('status', row[5])
                event.add('raw', ','.join(row))
                event.add('source.ip', row[7], raise_failure=False)
                event.add('source.fqdn', row[3], raise_failure=False)
                event.add('source.url', row[4], raise_failure=False)
                self.send_message(event)
        self.acknowledge_message()


BOT = AbuseCHRansomwaretrackerParserBot
