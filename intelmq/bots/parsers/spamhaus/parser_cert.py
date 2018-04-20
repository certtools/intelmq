# -*- coding: utf-8 -*-
"""
Header of the File:
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
from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime

__all__ = ['SpamhausCERTParserBot']


class SpamhausCERTParserBot(ParserBot):

    def parse_line(self, row, report):
        if not len(row) or row.startswith(';'):
            self.tempdata.append(row)
        else:
            row_splitted = [field.strip() for field in row.strip().split(',')]
            event = self.new_event(report)
            event.change("feed.url", event["feed.url"].split("key=")[0])

            event.add('source.ip', row_splitted[0])
            source_asn = row_splitted[1].replace('AS', '')
            if source_asn != '?':
                event.add('source.asn', source_asn)
            event.add('source.geolocation.cc', row_splitted[2])
            event.add('time.source',
                      DateTime.from_timestamp(int(row_splitted[3])))

            malware = row_splitted[4].lower()
            if malware == 'openrelay':
                event.add('classification.type', 'vulnerable service')
                event.add('classification.identifier', 'openrelay')
                event.add('protocol.application', 'smtp')
            elif malware == 'iotrdp':
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', 'rdp')
                event.add('protocol.application', 'rdp')
            elif malware == 'sshauth':
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', 'ssh')
                event.add('protocol.application', 'ssh')
            elif malware in ('telnetauth', 'iotcmd', 'iotuser'):
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', 'telnet')
                event.add('protocol.application', 'telnet')
            elif malware == 'iotscan':
                event.add('classification.type', 'scanner')
                event.add('event_description.text', 'infected IoT device scanning for other vulnerable IoT devices')
                if row_splitted[7] == '23':
                    event.add('protocol.application', 'telnet')
                    event.add('classification.identifier', 'telnet')
                else:
                    event.add('classification.identifier', 'scanner-generic')
            elif malware == 'wpscanner':
                event.add('classification.type', 'scanner')
                event.add('classification.identifier', 'wordpress-vulnerabilities')
                event.add('event_description.text', 'scanning for wordpress vulnerabilities')
                event.add('protocol.application', 'http')
            elif malware == 'w_wplogin':
                event.add('classification.type', 'scanner')
                event.add('classification.identifier', 'wordpress-login')
                event.add('event_description.text', 'scanning for wordpress login pages')
                event.add('protocol.application', 'http')
            else:
                if malware == 'auto':
                    malware = 's_other'
                event.add('malware.name', malware)
                event.add('classification.type', 'botnet drone')

            # otherwise the same ip, ignore
            event.add('destination.fqdn', row_splitted[5], raise_failure=False)
            event.add('destination.ip', row_splitted[6], raise_failure=False)
            event.add('destination.port', row_splitted[7], raise_failure=False)
            if row_splitted[8] and row_splitted[8] not in ('-', '?'):
                try:
                    port = int(row_splitted[8])
                except ValueError:
                    event.add('destination.fqdn', row_splitted[8], raise_failure=False)
                else:
                    event.add('extra', {'destination.local_port': port})
            event.add('protocol.transport', row_splitted[9], raise_failure=False)
            event.add('raw', self.recover_line(row))

            yield event


BOT = SpamhausCERTParserBot
