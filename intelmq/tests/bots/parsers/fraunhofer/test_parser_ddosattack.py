# -*- coding: utf-8 -*-
import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.fraunhofer.parser_ddosattack import \
    FraunhoferDdosAttackParserBot
from intelmq.lib import utils

UNKNOWN_CNC_TYPE = json.dumps({
    'cnc': 'some_cnc_information',
    'cnctype': 'some_unknown_cnc_type',
    'message': 'some_message',
    'messagetype': 'some_unknown_message_type',
    'name': 'some_malware',
    'ts': '2018-02-05T10:15:42Z'
})
UNKNOWN_MESSAGETYPE = json.dumps({
    'cnc': {
        'domain': None,
        'ip': '1.2.3.4',
        'port': 4711
    },
    'cnctype': 'classic_cnc',
    'message': 'content of unknown message',
    'messagetype': 'unknown_messagetype',
    'name': 'some_malware',
    'ts': '2018-02-05T10:15:42Z'
})
SINGLE_DDOS_TARGET = json.dumps({
    'cnc': {
        'domain': None,
        'ip': '1.2.3.4',
        'port': 4711
    },
    'cnctype': 'classic_cnc',
    'message': {
        'attack': 'someattack',
        'duration': 20,
        'flags': {
            'len': '1024'
        },
        'targets': [
            '4.3.2.1/32'
        ]
    },
    'messagetype': 'cnc_message',
    'name': 'some_malware',
    'ts': '2018-02-05T10:15:42Z'
})
MULTIPLE_DDOS_TARGETS = json.dumps({
    'cnc': {
        'domain': None,
        'ip': '1.2.3.4',
        'port': 4711
    },
    'cnctype': 'classic_cnc',
    'message': {
        'attack': 'someattack',
        'duration': 20,
        'flags': {
            'len': '1024'
        },
        'targets': [
            '4.3.2.1/32',
            '4.3.2.2',
            '4.3.2.3/24',
            'sometarget.com'
        ]
    },
    'messagetype': 'cnc_message',
    'name': 'some_malware',
    'ts': '2018-02-05T10:15:42Z'
})

CNC_EVENT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    '__type': 'Event',
    'classification.type': 'c&c',
    'malware.name': 'some_malware',
    'time.source': '2018-02-05T10:15:42+00:00',
}
DDOS_TARGET_EVENT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    '__type': 'Event',
    'classification.type': 'ddos',
    'malware.name': 'some_malware',
    'time.source': '2018-02-05T10:15:42+00:00',
}
REPORT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    '__type': 'Report',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    'time.observation': '2018-01-01T00:00:00+00:00',
}


def new_report_from_template(raw_data):
    report = dict(REPORT_TEMPLATE)
    report['raw'] = utils.base64_encode(raw_data)
    return report


def new_event_from_template(template, fields, original_message):
    event = dict(template)
    event['raw'] = utils.base64_encode(original_message)
    event.update(fields)
    return event


class TestFraunhoferDdosAttackParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a FraunhoferDdosAttackParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FraunhoferDdosAttackParserBot

    def test_classic_cnc_message_with_single_ddos_target_results_in_two_events(self):
        self.input_message = new_report_from_template(SINGLE_DDOS_TARGET)

        self.run_bot()

        self.assertOutputQueueLen(2)
        self.assert_cnc_event(0, SINGLE_DDOS_TARGET,
                              {'source.ip': '1.2.3.4', 'source.port': 4711})
        self.assert_ddos_event(1, SINGLE_DDOS_TARGET,
                               {'destination.ip': '4.3.2.1'})

    def test_classic_cnc_message_with_multiple_ddos_targets_results_in_multiple_ddos_events(self):
        self.input_message = new_report_from_template(MULTIPLE_DDOS_TARGETS)

        self.run_bot()

        self.assertOutputQueueLen(5)
        self.assert_cnc_event(0, MULTIPLE_DDOS_TARGETS,
                              {'source.ip': '1.2.3.4', 'source.port': 4711})
        self.assert_ddos_event(1, MULTIPLE_DDOS_TARGETS,
                               {'destination.ip': '4.3.2.1'})
        self.assert_ddos_event(2, MULTIPLE_DDOS_TARGETS,
                               {'destination.ip': '4.3.2.2'})
        self.assert_ddos_event(3, MULTIPLE_DDOS_TARGETS,
                               {'destination.network': '4.3.2.0/24'})
        self.assert_ddos_event(4, MULTIPLE_DDOS_TARGETS,
                               {'destination.fqdn': 'sometarget.com'})

    def test_classic_cnc_message_with_unknown_messagetype_results_only_in_cnc_event(self):
        self.input_message = new_report_from_template(UNKNOWN_MESSAGETYPE)

        self.run_bot()

        self.assertOutputQueueLen(1)
        self.assert_cnc_event(0, UNKNOWN_MESSAGETYPE,
                              {'source.ip': '1.2.3.4', 'source.port': 4711})

    def test_classic_cnc_message_with_unknown_messagetype_sets_feed_accuracy_to_given_value(self):
        self.input_message = new_report_from_template(UNKNOWN_MESSAGETYPE)
        self.sysconfig = {'unknown_messagetype_accuracy': 11.0}

        self.run_bot()

        self.assertOutputQueueLen(1)
        self.assert_cnc_event(0, UNKNOWN_MESSAGETYPE,
                              {'feed.accuracy': 11.0, 'source.ip': '1.2.3.4', 'source.port': 4711})

    def test_message_with_unknown_cnc_type_results_in_no_events(self):
        self.input_message = new_report_from_template(UNKNOWN_CNC_TYPE)

        self.run_bot()

        self.assertOutputQueueLen(0)

    def test_multiple_messages_are_parsed_correctly(self):
        self.input_message = [
            new_report_from_template(SINGLE_DDOS_TARGET),
            new_report_from_template(UNKNOWN_MESSAGETYPE)]

        self.run_bot(iterations=2)

        self.assertOutputQueueLen(3)
        self.assert_cnc_event(0, SINGLE_DDOS_TARGET,
                              {'source.ip': '1.2.3.4', 'source.port': 4711})
        self.assert_ddos_event(1, SINGLE_DDOS_TARGET,
                               {'destination.ip': '4.3.2.1'})
        self.assert_cnc_event(2, UNKNOWN_MESSAGETYPE,
                              {'source.ip': '1.2.3.4', 'source.port': 4711})

    def assert_cnc_event(self, queue_pos, original_message, expected_fields):
        event = new_event_from_template(CNC_EVENT_TEMPLATE, expected_fields,
                                        original_message)
        self.assertMessageEqual(queue_pos, event)

    def assert_ddos_event(self, queue_pos, original_message, expected_fields):
        event = new_event_from_template(DDOS_TARGET_EVENT_TEMPLATE,
                                        expected_fields, original_message)
        self.assertMessageEqual(queue_pos, event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
