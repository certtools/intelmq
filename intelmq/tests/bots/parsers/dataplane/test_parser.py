# SPDX-FileCopyrightText: 2016 jgedeon120
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.dataplane.parser import DataplaneParserBot, CATEGORY

feed_name_map = {
    'dnsrd': 'DNS Recursion Desired',
    'dnsrdany': 'DNS Recursion Desired IN ANY',
    'dnsversion': 'DNS CH TXT version.bind',
    'proto41': 'Protocol 41',
    'sipquery': 'SIP Query',
    'sipinvitation': 'SIP Invitation',
    'sipregistration': 'SIP Registration',
    'smtpdata': 'SMTP DATA',
    'smtpgreet': 'SMTP HELO/EHLO',
    'sshclient': 'SSH Client',
    'sshpwauth': 'SSH Password Authentication',
    'telnetlogin': 'Telnet Login',
    'vncrfb': 'VNC/RFB Login',
}

feed_names = list(feed_name_map)

file_data = {}

REPORTS = {}
for feed_name in feed_names:
    report = {
        'feed.url': f'https://dataplane.org/{feed_name}.txt',
        'feed.name': feed_name_map[feed_name],
        '__type': 'Report',
        'time.observation': '2021-09-01T06:27:26+00:00',
    }

    with open(os.path.join(os.path.dirname(__file__), f'{feed_name}.txt')) as fd:
        report['raw'] = utils.base64_encode(fd.read())

    REPORTS[feed_name] = report


EVENTS = {feed_name: report.copy() for feed_name, report in REPORTS.items()}

for feed_name, event in EVENTS.items():
    event.update(CATEGORY[feed_name])
    event['__type'] = 'Event'

EVENTS['dnsrd'].update({
    'raw': 'MTc0ICAgICAgICAgIHwgIENPR0VOVC0xNzQgICAgICAgICAgICAgICAgICAgICAgfCAgMTg1LjE0Mi4yMzYuMzUgICB8ICAyMDIxLTA4LTMxIDEwOjA3OjEwICB8ICBkbnNyZA==',
    'source.as_name': 'COGENT-174',
    'source.asn': 174,
    'source.ip': '185.142.236.35',
    'time.source': '2021-08-31T10:07:10+00:00',
})

EVENTS['dnsrdany'].update({
    'raw': 'MjA5ICAgICAgICAgIHwgIENFTlRVUllMSU5LLVVTLUxFR0FDWS1RV0VTVCAgICAgfCAgNjMuMjI0LjI1MC4yMTUgICB8ICAyMDIxLTA4LTMwIDA3OjA4OjAwICB8ICBkbnNyZGFueQ==',
    'source.as_name': 'CENTURYLINK-US-LEGACY-QWEST',
    'source.asn': 209,
    'source.ip': '63.224.250.215',
    'time.source': '2021-08-30T07:08:00+00:00',
})

EVENTS['dnsversion'].update({
    'raw': 'MTc0ICAgICAgICAgIHwgIENPR0VOVC0xNzQgICAgICAgICAgICAgICAgICAgICAgfCAgMTg1LjE0Mi4yMzYuMzUgICB8ICAyMDIxLTA4LTMxIDEwOjA3OjA5ICB8ICBkbnN2ZXJzaW9u',
    'source.as_name': 'COGENT-174',
    'source.asn': 174,
    'source.ip': '185.142.236.35',
    'time.source': '2021-08-31T10:07:09+00:00',
})

EVENTS['proto41'].update({
    'extra.first_seen': '2021-08-28T05:00:18+00:00',
    'raw': 'MSAgICAgICAgICAgIHwgIExWTFQtMSAgICAgICAgICAgICAgICAgICAgICAgICAgfCAgNDUuNi4xOTIuMSAgICAgICB8ICAyMDIxLTA4LTI4IDA1OjAwOjE4ICB8ICAyMDIxLTA4LTI4IDA1OjAwOjE4ICB8ICBwcm90bzQx',
    'source.as_name': 'LVLT-1',
    'source.asn': 1,
    'source.ip': '45.6.192.1',
    'time.source': '2021-08-28T05:00:18+00:00',
})

EVENTS['sipquery'].update({
    'raw': 'MjA5ICAgICAgICAgIHwgIENFTlRVUllMSU5LLVVTLUxFR0FDWS1RV0VTVCAtICAgfCAgICAgIDY1LjE1Ny40Mi42ICB8ICAyMDE2LTEyLTA1IDE0OjAxOjIxICB8ICBzaXBxdWVyeQ==',
    'source.as_name': 'CENTURYLINK-US-LEGACY-QWEST',
    'source.asn': 209,
    'source.ip': '65.157.42.6',
    'time.source': '2016-12-05T14:01:21+00:00',
})

EVENTS['sipinvitation'].update({
    'raw': 'ODU2MCAgICAgICAgIHwgIE9ORUFORE9ORS1BUyBCcmF1ZXJzdHJhc3NlIDQ4LCAgfCAgIDc0LjIwOC4xNDkuMjMxICB8ICAyMDE2LTEyLTA1IDE2OjA4OjI5ICB8ICBzaXBpbnZpdGF0aW9u',
    'source.as_name': 'ONEANDONE-AS',
    'source.asn': 8560,
    'source.ip': '74.208.149.231',
    'time.source': '2016-12-05T16:08:29+00:00',
})

EVENTS['sipregistration'].update({
    'raw': 'ODU2MCAgICAgICAgIHwgIE9ORUFORE9ORS1BUyBCcmF1ZXJzdHJhc3NlIDQ4LCAgfCAgIDc0LjIwOC4xNTIuMjA4ICB8ICAyMDE2LTEyLTA0IDIzOjE0OjAxICB8ICBzaXByZWdpc3RyYXRpb24=',
    'source.as_name': 'ONEANDONE-AS',
    'source.asn': 8560,
    'source.ip': '74.208.152.208',
    'time.source': '2016-12-04T23:14:01+00:00',
})

EVENTS['smtpdata'].update({
    'raw': 'MzIxNiAgICAgICAgIHwgIFNPVkFNLUFTIFBKU0MgIlZpbXBlbGNvbSIgICAgICAgfCAgMjEzLjIzNC4yMDcuMTg4ICB8ICAyMDIxLTA4LTMxIDEzOjUyOjQ2ICB8ICBzbXRwZGF0YQ==',
    'source.as_name': 'SOVAM-AS',
    'source.asn': 3216,
    'source.ip': '213.234.207.188',
    'time.source': '2021-08-31T13:52:46+00:00',
})

EVENTS['smtpgreet'].update({
    'raw': 'MTc0ICAgICAgICAgIHwgIENPR0VOVC0xNzQgICAgICAgICAgICAgICAgICAgICAgfCAgMTg1LjE0Mi4yMzYuMzQgICB8ICAyMDIxLTA5LTAyIDE2OjA4OjM4ICB8ICBzbXRwZ3JlZXQ=',
    'source.as_name': 'COGENT-174',
    'source.asn': 174,
    'source.ip': '185.142.236.34',
    'time.source': '2021-09-02T16:08:38+00:00',
})

EVENTS['telnetlogin'].update({
    'raw': 'MSAgICAgICAgICAgIHwgIExWTFQtMSAgICAgICAgICAgICAgICAgICAgICAgICAgfCAgMjQuMjIwLjc3LjQ2ICAgICB8ICAyMDIxLTA4LTMxIDIzOjUwOjQ2ICB8ICB0ZWxuZXRsb2dpbg==',
    'source.as_name': 'LVLT-1',
    'source.asn': 1,
    'source.ip': '24.220.77.46',
    'time.source': '2021-08-31T23:50:46+00:00',
})

EVENTS['vncrfb'].update({
    'raw': 'MyAgICAgICAgICAgIHwgIE1JVC1HQVRFV0FZUyAgICAgICAgICAgICAgICAgICAgfCAgMTI4LjMxLjAuMTMgICAgICB8ICAyMDIxLTA5LTAzIDEwOjAzOjAzICB8ICB2bmNyZmI=',
    'source.as_name': 'MIT-GATEWAYS',
    'source.asn': 3,
    'source.ip': '128.31.0.13',
    'time.source': '2021-09-03T10:03:03+00:00',
})

SSH_CLIENT_EVENT = [{'feed.url': 'https://dataplane.org/sshclient.txt',
                     'feed.name': 'SSH Client',
                     '__type': 'Event',
                     'time.observation': '2016-12-07T06:27:26+00:00',
                     'raw': 'TkEgICAgICAgICAgIHwgIE5BICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfCAgICAgICA1LjE1Ny43LjgyICB8ICAyMDE2LTEyLTAxIDIwOjQxOjA5ICB8ICBzc2hjbGllbnQ=',
                     'event_description.text': 'Address has been seen initiating an SSH connection to a remote host. The source '
                                               'report lists hosts that are suspicious of more than just port scanning. The host '
                                               'may be SSH server cataloging or conducting authentication attack attempts.',
                     'source.ip': '5.157.7.82',
                     'time.source': '2016-12-01T20:41:09+00:00',
                     'protocol.application': 'ssh',
                     'classification.type': 'scanner',
                     },
                    {'feed.url': 'https://dataplane.org/sshclient.txt',
                     'feed.name': 'SSH Client',
                     '__type': 'Event',
                     'time.observation': '2016-12-07T06:27:26+00:00',
                     'raw': 'Mzk0NDcyICAgICAgIHwgIFNXT0ktQVNOIC0gU1dPSSwgVVMgICAgICAgICAgICAgfCAgMTA0LjI0MS4yMzIuMjM4ICB8ICAyMDE2LTEyLTA1IDAxOjQ5OjE5ICB8ICBzc2hjbGllbnQ=',
                     'event_description.text': 'Address has been seen initiating an SSH connection to a remote host. The source '
                                               'report lists hosts that are suspicious of more than just port scanning. The host '
                                               'may be SSH server cataloging or conducting authentication attack attempts.',
                     'source.asn': 394472,
                     'source.ip': '104.241.232.238',
                     'source.as_name': 'SWOI-ASN',
                     'time.source': '2016-12-05T01:49:19+00:00',
                     'protocol.application': 'ssh',
                     'classification.type': 'scanner',
                     }]

SSH_AUTH_EVENT = [{'feed.url': 'https://dataplane.org/sshpwauth.txt',
                   'feed.name': 'SSH Password Authentication',
                   '__type': 'Event',
                   'time.observation': '2016-12-07T06:27:26+00:00',
                   'raw': 'TkEgICAgICAgICAgIHwgIE5BICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfCAgMTcwLjIzOS4xMDQuMTgzICB8ICAyMDE2LTEyLTAxIDA0OjI2OjQ4ICB8ICBzc2hwd2F1dGg=',
                   'event_description.text': 'Address has been seen attempting to remotely login to a host using SSH password '
                                             'authentication. The source report lists hosts that are highly suspicious and '
                                             'are likely conducting malicious SSH password authentication attacks.',
                   'source.ip': '170.239.104.183',
                   'time.source': '2016-12-01T04:26:48+00:00',
                   'protocol.application': 'ssh',
                   'classification.type': 'brute-force',
                   },
                  {'feed.url': 'https://dataplane.org/sshpwauth.txt',
                   'feed.name': 'SSH Password Authentication',
                   '__type': 'Event',
                   'time.observation': '2016-12-07T06:27:26+00:00',
                   'raw': 'NDEzNCAgICAgICAgIHwgIENISU5BTkVULUJBQ0tCT05FIE5vLjMxLEppbi1ybyAgfCAgIDExNy4yMS4yMjQuMTIxICB8ICAyMDE2LTEyLTA2IDAyOjM1OjM4ICB8ICBzc2hwd2F1dGg=',
                   'event_description.text': 'Address has been seen attempting to remotely login to a host using SSH password '
                                             'authentication. The source report lists hosts that are highly suspicious and '
                                             'are likely conducting malicious SSH password authentication attacks.',
                   'source.asn': 4134,
                   'source.ip': '117.21.224.121',
                   'source.as_name': 'CHINANET-BACKBONE',
                   'time.source': '2016-12-06T02:35:38+00:00',
                   'protocol.application': 'ssh',
                   'classification.type': 'brute-force',
                   }]


class TestDataplaneParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for the DataplaneParserBot """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DataplaneParserBot

    def test_feeds(self):
        for feed_name in set(feed_names) - {'sshclient', 'sshpwauth'}:
            self.input_message = REPORTS[feed_name]
            self.run_bot()
            self.assertMessageEqual(0, EVENTS[feed_name])

    def test_ssh_client(self):
        self.input_message = REPORTS['sshclient']
        self.allowed_error_count = 1
        self.run_bot()
        self.allowed_error_count = 0
        self.assertLogMatches('.*Incorrect format for feed https://dataplane.org/sshclient.txt.*', 'ERROR')
        self.assertMessageEqual(0, SSH_CLIENT_EVENT[0])
        self.assertMessageEqual(1, SSH_CLIENT_EVENT[1])

    def test_ssh_auth(self):
        self.input_message = REPORTS['sshpwauth']
        self.run_bot()
        self.assertMessageEqual(0, SSH_AUTH_EVENT[0])
        self.assertMessageEqual(1, SSH_AUTH_EVENT[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
