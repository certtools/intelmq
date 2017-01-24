# -*- coding: utf-8 -*-
"""
Parser for Intelmq and Abuse.ch Ransomware feed.
"""

import csv
import io

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import FQDN, URL, IPAddress
from intelmq.lib.message import Event


class AbuseCHRansomwaretrackerParserBot(Bot):
    """ Abuse.ch Ransomware Tracker Bot """

    def process(self):
        """
        The Ranswomware Tracker has comments in it.
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
                        ev.add('time.source', nrow[0] + ' UTC', force=True)
                        ev.add('status', nrow[5])
                        ev.add('source.ip', nrow[7])
                        ev.add('raw', ','.join(nrow))
                        if FQDN.is_valid(nrow[3]):
                            ev.add('source.fqdn', nrow[3])
                        if URL.is_valid(nrow[4]):
                            ev.add('source.url', nrow[4])
                        self.send_message(ev)
            else:
                event = Event(report)
                event.add('classification.identifier', row[2].lower())
                event.add('classification.type', 'c&c')
                event.add('time.source', row[0] + ' UTC')
                event.add('status', row[5])
                event.add('raw', ','.join(row))
                if IPAddress.is_valid(row[7]):
                    event.add('source.ip', row[7])
                if FQDN.is_valid(row[3]):
                    event.add('source.fqdn', row[3])
                if URL.is_valid(row[4]):
                    event.add('source.url', row[4])
                self.send_message(event)
        self.acknowledge_message()


BOT = AbuseCHRansomwaretrackerParserBot
