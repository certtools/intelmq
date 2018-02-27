# -*- coding: utf-8 -*-
"""
The source provides a stream/list of newline separated JSON objects. Each line
represents a single event observed by a DDoS C&C tracker, like an attack
command. If the bot receives a report with a known C&C type but with an unknown
message type, it generates a C&C event with a feed.accuracy given by the
parameter unknown_messagetype_accuracy, if set.
"""
import json

from intelmq.lib.bot import ParserBot

__all__ = ['FraunhoferDdosAttackParserBot']


class FraunhoferDdosAttackParserBot(ParserBot):
    def parse_line(self, line, report):
        feed_message = json.loads(line)

        yield from self.__parse_cnc_server(feed_message, line, report)
        yield from self.__parse_ddos_targets(feed_message, line, report)

    def __parse_cnc_server(self, message, line, report):
        if message['cnctype'] != 'classic_cnc':
            self.logger.info('Unable to create cnc event due to '
                             'unsupported cnctype %s.', message['cnctype'])
            return None

        event = self.__new_event(message, line, report)
        event.add('classification.type', 'c&c')
        event.add('source.fqdn', message['cnc']['domain'])
        event.add('source.ip', message['cnc']['ip'])
        event.add('source.port', message['cnc']['port'])

        if message['messagetype'] != 'cnc_message' and hasattr(self.parameters, 'unknown_messagetype_accuracy'):
            event.add('feed.accuracy', self.parameters.unknown_messagetype_accuracy, overwrite=True)

        yield event

    def __parse_ddos_targets(self, message, line, report):
        if message['messagetype'] != 'cnc_message':
            self.logger.info('Unable to create ddos events due to '
                             'unsupported messagetype %s.',
                             message['messagetype'])
            return None

        for target_address in message['message']['targets']:
            event = self.__new_event(message, line, report)
            event.add('classification.type', 'ddos')
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


BOT = FraunhoferDdosAttackParserBot
