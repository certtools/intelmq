# -*- coding: utf-8 -*-
"""
; Bots filtered by last 1 hours, prepared for <CERTNAME> on UTC = ...
; Copyright © 2015 The Spamhaus Project Ltd. All rights reserved.
; No re-distribution or public access allowed without Spamhaus permission.
; Fields description:
;
; 1 - Infected IP
; 2 - ASN
; 3 - Country Code
; 4 - Lastseen Timestamp (in UTC)
; 5 - Bot Name
;   Command & Control (C&C) information, if available:
; 6 - C&C Domain
; 7 - Remote IP (connecting to)
; 8 - Remote Port (connecting to)
; 9 - Local Port
; 10 - Protocol
;   Additional fields may be added in the future without notice
;
; ip, asn, country, lastseen, botname, domain, remote_ip, remote_port,
local_port, protocol
"""
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import InvalidValue
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Event
import json


__all__ = ['SpamhausCERTParserBot']


class SpamhausCERTParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report["raw"])

        for row in raw_report.splitlines():
            row = row.strip()

            if not len(row) or row.startswith(';'):
                continue

            row_splitted = [field.strip() for field in row.split(',')]
            event = Event(report)

            event.add('source.ip', row_splitted[0], sanitize=True)
            event.add('source.asn', row_splitted[1].replace('AS', ''),
                      sanitize=True)
            event.add('source.geolocation.cc', row_splitted[2], sanitize=True)
            event.add('time.source',
                      DateTime.from_timestamp(int(row_splitted[3])),
                      sanitize=True)
            event.add('malware.name', row_splitted[4].lower(), sanitize=True)
            try:
                event.add('destination.fqdn', row_splitted[5], sanitize=True)
            except InvalidValue:
                pass  # otherwise the same ip, ignore
            event.add('destination.ip', row_splitted[6], sanitize=True)
            event.add('destination.port', row_splitted[7], sanitize=True)
            if row_splitted[8] and row_splitted[8] != '-':
                event.add('extra',
                          json.dumps({'destination.local_port':
                                      int(row_splitted[8])}),
                          sanitize=True)
            event.add('protocol.transport', row_splitted[9], sanitize=True)
            event.add('classification.type', u'botnet drone')
            event.add('raw', row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = SpamhausCERTParserBot(sys.argv[1])
    bot.start()
