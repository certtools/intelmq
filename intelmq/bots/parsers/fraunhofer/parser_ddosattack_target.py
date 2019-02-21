# -*- coding: utf-8 -*-
"""
The source provides a stream/list of newline separated JSON objects. Each line
represents a single event observed by a DDoS C&C tracker, like an attack
command. This parser emits a ddos event for every target detected in the
observed event.
"""
import json
from builtins import ValueError

from intelmq.lib.bot import ParserBot

__all__ = ['FraunhoferDdosAttackTargetParserBot']


class FraunhoferDdosAttackTargetParserBot(ParserBot):
    def parse_line(self, line, report):
        feed_message = json.loads(line)

        yield from self.__parse_ddos_targets(feed_message, line, report)

    def __parse_ddos_targets(self, message, line, report):
        if message['messagetype'] != 'cnc_message':
            raise ValueError('Unable to create ddos events due to '
                             'unsupported messagetype %s.' % message['messagetype'])

        for target_address in message['message']['targets']:
            event = self.__new_event(message, line, report)
            event.add('classification.type', 'ddos')
            event.add('classification.taxonomy', 'availability')
            if not event.add('destination.ip', target_address, raise_failure=False):
                if not event.add('destination.network', target_address, raise_failure=False):
                    event.add('destination.fqdn', target_address)
            yield event

    def __new_event(self, message, line, report):
        event = self.new_event(report)
        event.add('raw', line)
        event.add('malware.name', message['name'])
        event.add('time.source', message['ts'])
        return event


BOT = FraunhoferDdosAttackTargetParserBot
