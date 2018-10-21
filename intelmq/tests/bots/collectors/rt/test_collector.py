# -*- coding: utf-8 -*-
"""
"""
import os
import unittest
import random
import io

import intelmq.lib.test as test
from intelmq.bots.collectors.rt.collector_rt import RTCollectorBot

REPORT = {'__type': 'Report',
          'feed.accuracy': 100.0,
          'feed.name': 'Request Tracker',
          'rtir_id': 1,
          'raw': 'bm90IGNvbXBsZXRlbHkgZW1wdHk=',
          }

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import rt


@test.skip_internet()
@test.skip_exotic()
class TestRTCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RtCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RTCollectorBot
        cls.sysconfig = {"attachment_regex": "^test\\.csv$",
                         "feed": "Request Tracker",
                         "password": "administrateur",
                         "search_not_older_than": None,
                         "search_owner": "support",
                         "search_queue": "Service commercial",
                         "search_status": "resolved",
                         "search_subject_like": "test",
                         "set_status": False,
                         "take_ticket": False,
                         "unzip_attachment": False,
                         "uri": "http://demo.request-tracker.fr/REST/1.0",
                         "url_regex": "http://[^ \n]+",
                         "user": "administrateur",
                         }

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.sysconfig['search_subject_like'] = 'test %s' % random.randint(0, 100000)
        attachment = io.StringIO("not completely empty")

        instance = rt.Rt(self.sysconfig['uri'])
        instance.login(login=self.sysconfig['user'], password=self.sysconfig['password'])
        ticket_id = instance.create_ticket(Queue=self.sysconfig['search_queue'], Subject=self.sysconfig['search_subject_like'], Owner=self.sysconfig['search_owner'], Status=self.sysconfig['search_status'], files=[('test.csv', attachment, 'text/csv')])

        self.run_bot()
        REPORT['rtir_id'] = ticket_id
        self.assertMessageEqual(0, REPORT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
