# -*- coding: utf-8 -*-
""" IntelMQ Dataplane Parser """

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class DataplaneParserBot(ParserBot):
    CATEGORY = {
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
        'sshclient': {
            'classification.type': 'scanner',
            'protocol.application': 'ssh',
            'event_description.text': 'Address has been seen initiating an SSH connection to a remote host. The source '
                                      'report lists hosts that are suspicious of more than just port scanning.  '
                                      'The host may be SSH server cataloging or conducting authentication attack '
                                      'attempts.',
        },
        'sshpwauth': {
            'classification.type': 'brute-force',
            'protocol.application': 'ssh',
            'event_description.text': 'Address has been seen attempting to remotely login to a host using SSH password '
                                      'authentication. The source report lists hosts that are highly suspicious and '
                                      'are likely conducting malicious SSH password authentication attacks.',
        }
    }

    FILE_FORMAT = [
        ('source.asn', lambda x: x if x != 'NA' else None),
        ('source.as_name', lambda x: x.split()[0] if x != 'NA' else None),
        ('source.ip', lambda x: x),
        ('time.source', lambda x: x + '+00:00'),
    ]

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)
        else:
            event = Event(report)

            line_contents = line.split('|')
            if len(line_contents) != len(self.FILE_FORMAT) + 1:
                raise ValueError('Incorrect format for feed {}, found line: "{}"'.format(event.get('feed.url'), line))

            if line_contents[-1].strip() in self.CATEGORY:
                event.update(self.CATEGORY[line_contents[-1].strip()])
            else:
                raise ValueError('Unknown data feed {}.'.format(line_contents[-1].strip()))

            for field, setter in zip(line_contents, self.FILE_FORMAT):
                value = setter[1](field.strip())
                if value is not None:
                    event.add(setter[0], value)

            event.add('raw', line)
            yield event


BOT = DataplaneParserBot
