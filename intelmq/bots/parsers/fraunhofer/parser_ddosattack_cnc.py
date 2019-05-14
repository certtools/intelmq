# -*- coding: utf-8 -*-
"""
The source provides a stream/list of newline separated JSON objects. Each line
represents a single event observed by a DDoS C&C tracker, like an attack
command. This parser emits a c2server event for the C&C tracked server the
observed event originated from. If the bot receives a report with a known
C&C type but with an unknown message type, it generates a C&C event with a
feed.accuracy given by the parameter unknown_messagetype_accuracy, if set.
"""
import json
from builtins import ValueError, hasattr

from intelmq.lib.bot import ParserBot

__all__ = ['FraunhoferDdosAttackCncParserBot']


class FraunhoferDdosAttackCncParserBot(ParserBot):
    def parse_line(self, line, report):
        feed_message = json.loads(line)

        return self.__parse_cnc_server(feed_message, line, report)

    def __parse_cnc_server(self, message, line, report):
        if message['cnctype'] != 'classic_cnc':
            raise ValueError('Unable to create cnc event due to '
                             'unsupported cnctype %s.' % message['cnctype'])

        event = self.__new_event(message, line, report)
        event.add('classification.type', 'c2server')
        event.add('classification.taxonomy', 'malicious code')
        event.add('source.fqdn', message['cnc']['domain'])
        event.add('source.ip', message['cnc']['ip'])
        event.add('source.port', message['cnc']['port'])

        if message['messagetype'] != 'cnc_message' and hasattr(self.parameters, 'unknown_messagetype_accuracy'):
            event.add('feed.accuracy',
                      self.parameters.unknown_messagetype_accuracy,
                      overwrite=True)

        return event

    def __new_event(self, message, line, report):
        event = self.new_event(report)
        event.add('raw', line)
        event.add('malware.name', message['name'])
        event.add('time.source', message['ts'])
        return event


BOT = FraunhoferDdosAttackCncParserBot
