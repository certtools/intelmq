# SPDX-FileCopyrightText: 2016 jgedeon120
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
""" IntelMQ Dataplane Parser """

from intelmq.lib.bot import ParserBot

CATEGORY = {
    'dnsrd': {
        'classification.type': 'scanner',
        'protocol.application': 'dns',
        'event_description.text': 'Address has been seen performing a DNS recursion desired query to a remote host. '
                                  'The source report lists hosts that are suspicious of more than just port '
                                  'scanning. The host may be DNS server cataloging or searching for '
                                  'hosts to use for DNS-based DDoS amplification.',
    },
    'dnsrdany': {
        'classification.type': 'scanner',
        'protocol.application': 'dns',
        'event_description.text': 'Address has been seen performing a DNS recursion desired IN ANY query to a remote host. '
                                  'The source report lists hosts that are suspicious of more than just port '
                                  'scanning. The host may be DNS server cataloging or searching for '
                                  'hosts to use for DNS-based DDoS amplification.',
    },
    'dnsversion': {
        'classification.type': 'scanner',
        'protocol.application': 'dns',
        'event_description.text': 'Address has been seen initiating a DNS CH TXT version.bind operation to a remote host. '
                                  'The source report lists hosts that are suspicious of more than just port '
                                  'scanning. The host may be DNS server cataloging or searching for '
                                  'vulnerable DNS servers.',
    },
    'proto41': {
        'classification.type': 'proxy',
        'protocol.application': '6to4',
        'event_description.text': 'Address has been detected to offer open IPv6 over IPv4 tunneling. '
                                  'This could allow for the host to be used a public proxy against IPv6 '
                                  'hosts.',
    },
    'sipquery': {
        'classification.type': 'brute-force',
        'protocol.application': 'sip',
        'event_description.text': 'Address has been seen initiating a SIP OPTIONS query to a remote host. '
                                  'The source report lists hosts that are suspicious of more than just port '
                                  'scanning. The host may be SIP server cataloging or conducting various forms '
                                  'of telephony abuse.',
    },
    'sipinvitation': {
        'classification.type': 'brute-force',
        'protocol.application': 'sip',
        'event_description.text': 'Address has been seen initiating a SIP INVITE operation to a remote host. '
                                  'The source report lists hosts that are suspicious of more than just port '
                                  'scanning. The host may be SIP client cataloging or conducting various forms '
                                  'of telephony abuse.',
    },
    'sipregistration': {
        'classification.type': 'brute-force',
        'protocol.application': 'sip',
        'event_description.text': 'Address has been seen initiating a SIP REGISTER operation to a remote host. '
                                  'The source report lists hosts that are suspicious of more than just port '
                                  'scanning. The host may be SIP client cataloging or conducting various forms '
                                  'of telephony abuse.',
    },
    'smtpdata': {
        'classification.type': 'scanner',
        'protocol.application': 'smtp',
        'event_description.text': 'Address has been seen initiating a SMTP DATA operation to a remote host. '
                                  'The source report lists hosts that are suspicious of more than just port '
                                  'scanning. The host may be SMTP server cataloging or conducting various forms '
                                  'of email abuse.',
    },
    'smtpgreet': {
        'classification.type': 'scanner',
        'protocol.application': 'smtp',
        'event_description.text': 'Address has been seen initiating a SMTP HELO/EHLO operation to a remote host. '
                                  'The source report lists hosts that are suspicious of more than just port '
                                  'scanning. The host may be SMTP server cataloging or conducting various forms '
                                  'of email abuse.',
    },
    'sshclient': {
        'classification.type': 'scanner',
        'protocol.application': 'ssh',
        'event_description.text': 'Address has been seen initiating an SSH connection to a remote host. The source '
                                  'report lists hosts that are suspicious of more than just port scanning. '
                                  'The host may be SSH server cataloging or conducting authentication attack '
                                  'attempts.',
    },
    'sshpwauth': {
        'classification.type': 'brute-force',
        'protocol.application': 'ssh',
        'event_description.text': 'Address has been seen attempting to remotely login to a host using SSH password '
                                  'authentication. The source report lists hosts that are highly suspicious and '
                                  'are likely conducting malicious SSH password authentication attacks.',
    },
    'telnetlogin': {
        'classification.type': 'brute-force',
        'protocol.application': 'telnet',
        'event_description.text': 'Address has been seen initiating a telnet connection to a remote host. The source '
                                  'report lists hosts that are suspicious of more than just port scanning. '
                                  'The host may be telnet server cataloging or conducting authentication attack '
                                  'attempts.',
    },
    'vncrfb': {
        'classification.type': 'scanner',
        'protocol.application': 'vnc',
        'event_description.text': 'Address has been seen initiating a VNC remote buffer session to a remote host. The source '
                                  'report lists hosts that are suspicious of more than just port scanning. '
                                  'The host may be VNC/RFB server cataloging or conducting authentication attack '
                                  'attempts.',
    },
}


def _convert_datetime(s: str) -> str:
    return s.replace(' ', 'T', 1) + '+00:00'


FILE_FORMATS = {
    '_default': [
        ('source.asn', lambda x: x if x != 'NA' else None),
        ('source.as_name', lambda x: x.split()[0] if x != 'NA' else None),
        ('source.ip', lambda x: x),
        ('time.source', _convert_datetime),
    ],
    'proto41': [
        ('source.asn', lambda x: x if x != 'NA' else None),
        ('source.as_name', lambda x: x.split()[0] if x != 'NA' else None),
        ('source.ip', lambda x: x),
        ('extra.first_seen', _convert_datetime),
        ('time.source', _convert_datetime),
    ],
}


class DataplaneParserBot(ParserBot):
    """Parse the Dataplane feeds"""

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)
        else:
            event = self.new_event(report)

            line_contents = line.split('|')
            feed_name = line_contents[-1].strip()
            file_format = FILE_FORMATS.get(feed_name) or FILE_FORMATS['_default']

            if len(line_contents) != len(file_format) + 1:
                raise ValueError(f'Incorrect format for feed {event.get("feed.url")}, found line: "{line}"')

            if feed_name not in CATEGORY:
                raise ValueError(f'Unknown data feed {feed_name}.')

            event.update(CATEGORY[feed_name])

            for field, (field_name, converter) in zip(line_contents, file_format):
                value = converter(field.strip())
                if value is not None:
                    event.add(field_name, value)

            event.add('raw', line)
            yield event


BOT = DataplaneParserBot
