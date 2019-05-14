# -*- coding: utf-8 -*-
import unittest

from intelmq.bots.parsers.fraunhofer.parser_ddosattack_cnc import \
    FraunhoferDdosAttackCncParserBot
from intelmq.tests.bots.parsers.fraunhofer.ddosattack_tests_common import \
    FraunhoferDdosAttackTestCase, ddos_message, create_event


CNC_EVENT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    '__type': 'Event',
    'classification.type': 'c2server',
    'classification.taxonomy': 'malicious code',
    'malware.name': 'some_malware',
    'time.source': '2018-02-05T10:15:42+00:00',
}


class TestFraunhoferDdosAttackCncParserBot(FraunhoferDdosAttackTestCase, unittest.TestCase):
    """
    A TestCase for a FraunhoferDdosAttackCncParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FraunhoferDdosAttackCncParserBot

    def test_classic_cnc_message_results_correct_cnc_event(self):
        message = ddos_message()
        self.set_input_message(message)

        self.run_bot()

        self.assertOutputQueueLen(1)
        self.assert_cnc_event(0, message, {'source.ip': '1.2.3.4',
                                           'source.port': 4711})

    def test_set_fqdn_when_cnc_domain_given(self):
        message = ddos_message(domain='evil.com')
        self.set_input_message(message)

        self.run_bot()

        self.assert_cnc_event(0, message, {
            'source.fqdn': 'evil.com',
            'source.ip': '1.2.3.4',
            'source.port': 4711
        })

    def test_classic_cnc_message_with_unknown_messagetype_results_in_cnc_event_with_unknown_message_type_accuracy(self):
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
            expected_fields={'feed.accuracy': 11.0, 'source.ip': '1.2.3.4',
                             'source.port': 4711}
        )

    def test_message_with_unknown_cnc_type_results_in_no_events(self):
        message = ddos_message(
            cnc='some_cnc_information',
            cnctype='some_unknown_cnc_type',
            message='content of unknown message',
            messagetype='unknown_messagetype',
        )
        self.set_input_message(message)
        self.allowed_error_count = 1

        self.run_bot()

        self.assertRegexpMatchesLog('(ValueError.*unsupported cnctype '
                                    'some_unknown_cnc_type)')
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

        self.assertOutputQueueLen(2)
        self.assert_cnc_event(0, single_target, {'source.ip': '1.2.3.4',
                                                 'source.port': 4711})
        self.assert_cnc_event(1, unknown_message, {'source.ip': '1.2.3.4',
                                                   'source.port': 4711})

    def assert_cnc_event(self, queue_pos, original_message, expected_fields):
        event = create_event(CNC_EVENT_TEMPLATE, expected_fields,
                             original_message)
        self.assertMessageEqual(queue_pos, event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
