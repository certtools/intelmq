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

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)

        else:
            value = line.split('|')
            event = Event(report)
            event.add('time.source', value[3].strip() + '+00:00')
            if value[0].strip() != 'NA':
                event.add('source.asn', value[0].strip())
            if value[1].strip() != 'NA':
                event.add('source.as_name', value[1].split()[0])
            event.add('source.ip', value[2].strip())

            if value[4].strip() in DataplaneParserBot.CATEGORY:
                event.update(DataplaneParserBot.CATEGORY[value[4].strip()])
            else:
                raise ValueError('Unknown data feed %r.' % value[4].strip())

            event.add('raw', line)
            yield event


BOT = DataplaneParserBot
