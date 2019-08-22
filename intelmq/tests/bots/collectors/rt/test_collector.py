# -*- coding: utf-8 -*-
"""
"""
import unittest
import os

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.collectors.rt.collector_rt import RTCollectorBot

rt_url = os.getenv('INTELMQ_TEST_RT_URL')
rt_username = os.getenv('INTELMQ_TEST_RT_USERNAME')
rt_password = os.getenv('INTELMQ_TEST_RT_PASSWORD')
rt_subject = os.getenv('INTELMQ_TEST_RT_SUBJECT')
rt_ticket = os.getenv('INTELMQ_TEST_RT_TICKET')


@unittest.skipIf(not all((rt_url, rt_username, rt_password, rt_subject, rt_ticket)),
                 "Not provided all env variables needed for this test.")
class TestRTCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RTCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RTCollectorBot
        cls.sysconfig = {'uri': rt_url,
                         'user': rt_username,
                         'password': rt_password,
                         'set_status': False,
                         'take_ticket': False,
                         'search_subject_like': rt_subject,
                         'search_queue': 'Incident Reports',
                         'attachment_regex': '.*.zip',
                         'url_regex': None,
                         'unzip_attachment': True,
                         'name': 'Example feed',
                         }

    def test_report(self):
        """
        Test if Report has been produced.
        output defined inline as rt_ticket must be known and must not be None
        """
        self.run_bot(iterations=1)
        self.assertMessageEqual(0, {"__type": "Report",
              "feed.name": "Example feed",
              "feed.accuracy": 100.,
              "raw": utils.base64_encode('bar text\n'),
              "extra.file_name": "foobar",
              "extra.email_subject": "Incoming IntelMQ Test Report",
              "extra.ticket_subject": "Incoming IntelMQ Test Report",
              "extra.ticket_requestors": "wagner@cert.at",
              "extra.email_from": "wagner@cert.at",
              "extra.ticket_queue": "Incident Reports",
              "extra.ticket_status": "new",
              "extra.ticket_owner": "intelmq",
              "rtir_id": utils.lazy_int(rt_ticket),
              })


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
