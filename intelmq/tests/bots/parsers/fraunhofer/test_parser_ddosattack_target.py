# -*- coding: utf-8 -*-
import unittest

from intelmq.bots.parsers.fraunhofer.parser_ddosattack_target import \
    FraunhoferDdosAttackTargetParserBot
from intelmq.tests.bots.parsers.fraunhofer.ddosattack_tests_common import \
    FraunhoferDdosAttackTestCase, ddos_message, create_event


DDOS_TARGET_EVENT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    '__type': 'Event',
    'classification.type': 'ddos',
    'malware.name': 'some_malware',
    'classification.taxonomy': 'availability',
    'time.source': '2018-02-05T10:15:42+00:00',
}


class TestFraunhoferDdosAttackTargetParserBot(FraunhoferDdosAttackTestCase, unittest.TestCase):
    """
    A TestCase for a FraunhoferDdosAttackTargetParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FraunhoferDdosAttackTargetParserBot

    def test_cnc_message_with_single_ddos_target_results_in_correct_ddos_event(self):
        message = ddos_message()
        self.set_input_message(message)

        self.run_bot()

        self.assertOutputQueueLen(1)
        self.assert_ddos_event(0, message, {'destination.ip': '4.3.2.1'})

    def test_cnc_message_with_multiple_ddos_targets_results_in_multiple_ddos_events(self):
        message = ddos_message(
            targets=['4.3.2.1/32', '4.3.2.2', '4.3.2.3/24', 'sometarget.com']
        )
        self.set_input_message(message)

        self.run_bot()

        self.assertOutputQueueLen(4)
        self.assert_ddos_event(0, message, {'destination.ip': '4.3.2.1'})
        self.assert_ddos_event(1, message, {'destination.ip': '4.3.2.2'})
        self.assert_ddos_event(2, message, {'destination.network':
                                            '4.3.2.0/24'})
        self.assert_ddos_event(3, message, {'destination.fqdn':
                                            'sometarget.com'})

    def test_cnc_message_with_unknown_messagetype_results_in_no_ddos_event(self):
        message = ddos_message(
            message='content of unknown message',
            messagetype='unknown_messagetype',
        )
        self.set_input_message(message)
        self.allowed_error_count = 1

        self.run_bot()

        self.assertRegexpMatchesLog('(ValueError.*unsupported messagetype '
                                    'unknown_messagetype)')
        self.assertOutputQueueLen(0)

    def test_multiple_messages_are_parsed_correctly(self):
        single_target = ddos_message()
        multi_target = ddos_message(
            targets=['4.3.2.1/32', '4.3.2.2', '4.3.2.3/24', 'sometarget.com']
        )
        self.set_input_message(
            single_target,
            multi_target
        )

        self.run_bot(iterations=2)

        self.assertOutputQueueLen(5)
        self.assert_ddos_event(0, single_target, {'destination.ip': '4.3.2.1'})
        self.assert_ddos_event(1, multi_target, {'destination.ip': '4.3.2.1'})
        self.assert_ddos_event(2, multi_target, {'destination.ip': '4.3.2.2'})
        self.assert_ddos_event(3, multi_target, {'destination.network':
                                                 '4.3.2.0/24'})
        self.assert_ddos_event(4, multi_target, {'destination.fqdn':
                                                 'sometarget.com'})

    def assert_ddos_event(self, queue_pos, original_message, expected_fields):
        event = create_event(DDOS_TARGET_EVENT_TEMPLATE, expected_fields,
                             original_message)
        self.assertMessageEqual(queue_pos, event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
