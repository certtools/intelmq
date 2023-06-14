# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
rt_attachment_ticket = os.getenv('INTELMQ_TEST_RT_ATTACHMENT_TICKET')
rt_url_ticket = os.getenv('INTELMQ_TEST_RT_URL_TICKET')

REPORT = {"__type": "Report",
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
              "rtir_id": utils.lazy_int(0 if not rt_attachment_ticket else rt_attachment_ticket),
              }
REPORT_URL1 = REPORT.copy()
REPORT_URL1['rtir_id'] = utils.lazy_int(0 if not rt_url_ticket else rt_url_ticket)
REPORT_URL1['extra.file_name'] = 'bar'
REPORT_URL2 = REPORT_URL1.copy()
REPORT_URL2['extra.file_name'] = 'foo'
REPORT_URL2['raw'] = 'Zm9vIHRleHQK'


@unittest.skipIf(not all((rt_url, rt_username, rt_password, rt_subject)),
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
                         'search_status': 'new',
                         'attachment_regex': '.*.zip',
                         'url_regex': None,
                         'name': 'Example feed',
                         'extract_attachment': True,
                         }

    @unittest.skipIf(not rt_attachment_ticket,
                     'Not Ticket ID for attachment test given')
    def test_attachment_zip(self):
        """
        Test a zipped attachment
        """
        self.run_bot(iterations=1)
        self.assertMessageEqual(0, REPORT)

    @unittest.skipIf(not rt_attachment_ticket,
                     'Not Ticket ID for attachment test given')
    def test_attachment_gz(self):
        """
        Test a gzipped attachment
        """
        self.prepare_bot(parameters={'attachment_regex': r'.*\.gz'})
        self.run_bot(iterations=1, prepare=False)
        self.assertMessageEqual(0, REPORT)

    @unittest.skipIf(not rt_url_ticket,
                     'Not Ticket ID for URL test given')
    def test_url_zip(self):
        """
        Test a zipped URL
        """
        self.prepare_bot(parameters={'attachment_regex': None,
                                     'url_regex': r'http://localhost/.*\.zip',
                                     'extract_download': True})
        self.run_bot(iterations=1, prepare=False)
        self.assertMessageEqual(0, REPORT_URL1)
        self.assertMessageEqual(1, REPORT_URL2)


class TestRTRawQuery(unittest.TestCase):
    def test_simple(self):
        kwargs = {
            'Status': 'active',
            'Subject__like': 'Report',
            'Subject__notlike': 'except',
            'Created__gt': '2023-01-01',
            'Queue': 'IR',
        }

        raw_query = RTCollectorBot._convert_to_raw_query(kwargs)

        expected_query = ("(Status=\'active\')"
                          " AND (Subject LIKE \'Report\')"
                          " AND (Subject NOT LIKE \'except\')"
                          " AND (Created>\'2023-01-01\')")

        self.assertEqual(raw_query, {"Queue": "IR", "raw_query": expected_query})

    def test_multiple_values(self):
        kwargs = {
            'Status': 'active',
            'Subject__like': ['Report', 'Report 2'],
            'Subject__notlike': ['except', 'except2'],
            'Created__gt': '2023-01-01',
            'Queue': 'IR',
        }

        raw_query = RTCollectorBot._convert_to_raw_query(kwargs)

        expected_query = ("(Status=\'active\')"
                          " AND (Subject LIKE \'Report\')"
                          " AND (Subject LIKE \'Report 2\')"
                          " AND (Subject NOT LIKE \'except\')"
                          " AND (Subject NOT LIKE \'except2\')"
                          " AND (Created>\'2023-01-01\')")

        self.assertEqual(raw_query, {"Queue": "IR", "raw_query": expected_query})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
