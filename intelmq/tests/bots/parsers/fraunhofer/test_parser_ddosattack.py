# -*- coding: utf-8 -*-
import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.fraunhofer.parser_ddosattack import \
    FraunhoferDdosAttackParserBot
from intelmq.lib import utils

CNC_EVENT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    '__type': 'Event',
    'classification.type': 'c&c',
    'classification.taxonomy': 'malicious code',
    'malware.name': 'some_malware',
    'time.source': '2018-02-05T10:15:42+00:00',
}
DDOS_TARGET_EVENT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    '__type': 'Event',
    'classification.type': 'ddos',
    'malware.name': 'some_malware',
    'classification.taxonomy': 'availability',
    'time.source': '2018-02-05T10:15:42+00:00',
}
REPORT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    '__type': 'Report',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    'time.observation': '2018-01-01T00:00:00+00:00',
}


class TestFraunhoferDdosAttackParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a FraunhoferDdosAttackParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FraunhoferDdosAttackParserBot

    def test_classic_cnc_message_with_single_ddos_target_results_in_two_events(self):
        message = ddos_message()
        self.set_input_message(message)

        self.run_bot()

        self.assertOutputQueueLen(2)
        self.assert_cnc_event(0, message, {'source.ip': '1.2.3.4', 'source.port': 4711})
        self.assert_ddos_event(1, message, {'destination.ip': '4.3.2.1'})

    def test_set_fqdn_when_cnc_domain_given(self):
        message = ddos_message(domain='evil.com')
        self.set_input_message(message)

        self.run_bot()

        self.assert_cnc_event(0, message, {
            'source.fqdn': 'evil.com',
            'source.ip': '1.2.3.4',
            'source.port': 4711
        })

    def test_classic_cnc_message_with_multiple_ddos_targets_results_in_multiple_ddos_events(self):
        message = ddos_message(
            targets=['4.3.2.1/32', '4.3.2.2', '4.3.2.3/24', 'sometarget.com']
        )
        self.set_input_message(message)

        self.run_bot()

        self.assertOutputQueueLen(5)
        self.assert_cnc_event(0, message, {'source.ip': '1.2.3.4', 'source.port': 4711})
        self.assert_ddos_event(1, message, {'destination.ip': '4.3.2.1'})
        self.assert_ddos_event(2, message, {'destination.ip': '4.3.2.2'})
        self.assert_ddos_event(3, message, {'destination.network': '4.3.2.0/24'})
        self.assert_ddos_event(4, message, {'destination.fqdn': 'sometarget.com'})

    def test_classic_cnc_message_with_unknown_messagetype_results_only_in_cnc_event(self):
        self.sysconfig = {'unknown_messagetype_accuracy': 11.0}
        message = ddos_message(
            message='content of unknown message',
            messagetype='unknown_messagetype',
        )
        self.set_input_message(message)

        self.run_bot()

        self.assertOutputQueueLen(1)
        self.assert_cnc_event(
            queue_pos=0,
            original_message=message,
            expected_fields={'feed.accuracy': 11.0, 'source.ip': '1.2.3.4', 'source.port': 4711}
        )

    def test_message_with_unknown_cnc_type_results_in_no_events(self):
        message = ddos_message(
            cnc='some_cnc_information',
            cnctype='some_unknown_cnc_type',
            message='content of unknown message',
            messagetype='unknown_messagetype',
        )
        self.set_input_message(message)

        self.run_bot()

        self.assertOutputQueueLen(0)

    def test_multiple_messages_are_parsed_correctly(self):
        single_target = ddos_message()
        unknown_message = ddos_message(
            message='content of unknown message',
            messagetype='unknown_messagetype',
        )
        self.set_input_message(
            single_target,
            unknown_message
        )

        self.run_bot(iterations=2)

        self.assertOutputQueueLen(3)
        self.assert_cnc_event(0, single_target, {'source.ip': '1.2.3.4', 'source.port': 4711})
        self.assert_ddos_event(1, single_target, {'destination.ip': '4.3.2.1'})
        self.assert_cnc_event(2, unknown_message, {'source.ip': '1.2.3.4', 'source.port': 4711})

    def set_input_message(self, *message):
        self.input_message = [create_report(m) for m in message]

    def assert_cnc_event(self, queue_pos, original_message, expected_fields):
        event = create_event(CNC_EVENT_TEMPLATE, expected_fields, original_message)
        self.assertMessageEqual(queue_pos, event)

    def assert_ddos_event(self, queue_pos, original_message, expected_fields):
        event = create_event(DDOS_TARGET_EVENT_TEMPLATE, expected_fields, original_message)
        self.assertMessageEqual(queue_pos, event)


def create_report(raw_data):
    report = dict(REPORT_TEMPLATE)
    report['raw'] = utils.base64_encode(json.dumps(raw_data))
    return report


def create_event(template, fields, original_message):
    event = dict(template)
    event['raw'] = utils.base64_encode(json.dumps(original_message))
    event.update(fields)
    return event


def ddos_message(domain=None, targets=None, **kwargs):
    message = {
        'cnc': {
            'domain': domain,
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
            'targets': targets or ['4.3.2.1/32']
        },
        'messagetype': 'cnc_message',
        'name': 'some_malware',
        'ts': '2018-02-05T10:15:42Z'
    }
    message.update(kwargs)
    return message


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
