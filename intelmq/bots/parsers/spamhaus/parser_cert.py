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
            elif malware == 'sshauth':
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', 'ssh')
                event.add('protocol.application', 'ssh')
            elif malware == 'telnetauth':
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', 'telnet')
                event.add('protocol.application', 'telnet')
            elif malware  == 'smtpauth':
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', 'smtp')
                event.add('protocol.application', 'smtp')
            elif malware in ['iotscan', 'iotuser']:
                event.add('classification.type', 'scanner')
                event.add('event_description.text', 'The possibly infected IoT device scanned for other vulnerable IoT devices.')
                if row_splitted[7] in ['23', '2323']:
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
            elif malware == 'l_spamlink':
                event.add('classification.type', 'spam')
                event.add('classification.identifier', 'spamlink')
                event.add('event_description.text', 'The URL appeared in a spam email sent by extra.spam_ip.')
#                event.add('protocol.application', 'http')
                ip, malware_version, malware_name = row_splitted[8].split(':')
                event.add('malware.name', malware_name)
                event.add('malware.version', malware_version)
                event.add('source.url', row_splitted[6])
                event.add('extra.spam_ip', ip)
            elif malware in ['pop', 'imap']:
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', malware)
                event.add('protocol.application', malware)
            elif malware in ['smb', 'rdp', 'iotrdp', 'iotmicrosoftds']:
                if malware.startswith('iot'):
                    malware = malware[3:]
                event.add('classification.type', 'scanner')
                event.add('classification.identifier', malware)
                event.add('protocol.application', malware)
            elif malware == 'proxyget':
                event.add('classification.type', 'other')
                event.add('classification.identifier', malware)
                event.add('event_description.text', 'The malicous client used a honeypot as proxy.')
            elif malware == 'iotlogin':
                event.add('classification.type', 'unauthorized-login')
                event.add('classification.identifier', 'iot')
                event.add('event_description.text', 'The infected iot device logged in to a honeypot.')
            elif malware == 'iotcmd':
                event.add('classification.type', 'unauthorized-command')
                event.add('classification.identifier', 'iot')
                event.add('event_description.text', 'The infected iot device logged in to a honeypot and issued malicous commands.')
            elif malware == 'iotmirai':
                event.add('classification.type', 'infected system')
                event.add('classification.identifier', 'mirai')
                event.add('malware.name', 'mirai')
            elif malware == 'ioturl':
                event.add('classification.type', 'c&c')
                event.add('classification.identifier', 'malware-generic')
            elif malware == 'automatedtest':
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', 'lookup-captcha')
                event.add('event_description.text', 'The device automatically brute-forced the Spamhaus CBL lookup.')
            elif malware == 'authspoofbadehlo':
                event.add('classification.type', 'brute-force')
                event.add('classification.identifier', 'authentication-spoof')
                event.add('protocol.application', 'smtp')
                event.add('event_description.text', 'The device spoofed SMTP authentication with a bad EHLO.')
            else:
                if malware == 'auto':
                    malware = 's_other'
                event.add('malware.name', malware)
                event.add('classification.type', 'infected system')
                event.add('source.url', row_splitted[5], raise_failure=False)

            # otherwise the same ip, ignore
            if not (malware == 'iotscan' or   # the data is wrong according to the feed provider 2018-06-15
                    ':' in row_splitted[5]):  # IP or Port in this field: also broken according to provider 2018-06-15
                event.add('destination.fqdn', row_splitted[5], raise_failure=False)
            event.add('destination.ip', row_splitted[6], raise_failure=False)
            event.add('destination.port', row_splitted[7], raise_failure=False)
            if row_splitted[8] and row_splitted[8] not in ('-', '?') and malware != 'l_spamlink':
                event.add('extra.source.local_port', int(row_splitted[8]))
            event.add('protocol.transport', row_splitted[9], raise_failure=False)
            event.add('raw', self.recover_line(row))

            yield event


BOT = SpamhausCERTParserBot
