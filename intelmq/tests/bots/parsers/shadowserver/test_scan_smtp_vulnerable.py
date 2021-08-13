# SPDX-FileCopyrightText: 2021 Mikk Margus Möll <mikk@cert.ee>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_smtp_vulnerable.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Vulnerable SMTP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2021-07-08T00:00:00+00:00",
                  "extra.file_name": "2021-07-08-scan_smtp_vulnerable-test-test.csv",
                  }

EVENTS = [{'__type': 'Event',
           'feed.name': 'Vulnerable SMTP',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable-system',
           'extra.banner': '220 smtp-server.invalid ESMTP Exim 4.80 Wed, 11 Jun 2021 '
                           '10:00:00 +0300|',
           'extra.protocol': 'tcp',
           'classification.identifier': 'vulnerable-smtp',
           'extra.tag': 'smtp;21nails',
           'protocol.application': 'smtp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.reverse_dns': 'smtp-server.invalid',
           'source.asn': 12345,
           'source.geolocation.cc': 'EE',
           'source.geolocation.city': 'TALLINN',
           'source.geolocation.region': 'HARJUMAA',
           'source.ip': '1.2.3.4',
           'source.port': 25,
           'time.observation': '2021-07-08T00:00:00+00:00',
           'time.source': '2021-07-08T11:58:42+00:00'},
          {'__type': 'Event',
           'feed.name': 'Vulnerable SMTP',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable-system',
           'extra.banner': '220 smtp-out.invalid, ESMTP EXIM 4.86_2|',
           'extra.protocol': 'tcp',
           'classification.identifier': 'vulnerable-smtp',
           'extra.tag': 'smtp;21nails',
           'protocol.application': 'smtp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.reverse_dns': 'smtp-out.invalid',
           'source.asn': 23456,
           'source.geolocation.cc': 'EE',
           'source.geolocation.city': 'TALLINN',
           'source.geolocation.region': 'HARJUMAA',
           'source.ip': '5.6.7.8',
           'source.port': 25,
           'time.observation': '2021-07-08T00:00:00+00:00',
           'time.source': '2021-07-08T11:58:44+00:00'},
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
