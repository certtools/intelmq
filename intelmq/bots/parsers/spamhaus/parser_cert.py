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

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import InvalidValue
from intelmq.lib.harmonization import DateTime

__all__ = ['SpamhausCERTParserBot']


class SpamhausCERTParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report["raw"])

        for row in raw_report.splitlines():
            row = row.strip()

            if not len(row) or row.startswith(';'):
                continue

            row_splitted = [field.strip() for field in row.split(',')]
            event = self.new_event(report)

            event.add('source.ip', row_splitted[0])
            event.add('source.asn', row_splitted[1].replace('AS', ''))
            event.add('source.geolocation.cc', row_splitted[2])
            event.add('time.source',
                      DateTime.from_timestamp(int(row_splitted[3])))
            event.add('malware.name', row_splitted[4].lower())
            try:
                event.add('destination.fqdn', row_splitted[5])
            except InvalidValue:
                pass  # otherwise the same ip, ignore
            event.add('destination.ip', row_splitted[6])
            event.add('destination.port', row_splitted[7])
            if row_splitted[8] and row_splitted[8] != '-':
                event.add('extra', {'destination.local_port':
                                    int(row_splitted[8])})
            event.add('protocol.transport', row_splitted[9])
            event.add('classification.type', 'botnet drone')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()


BOT = SpamhausCERTParserBot
