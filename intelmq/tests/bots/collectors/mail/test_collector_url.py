# -*- coding: utf-8 -*-
"""
Testing Mail URL collector

TODO: Use (and generalize) the methods used in the Mail Attach Bot Test
"""
import unittest

import intelmq.lib.test as test
from intelmq.bots.collectors.mail.collector_mail_url import MailURLCollectorBot


@test.skip_exotic()
class TestMailURLCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    Test MailURLCollectorBot
    """
    @classmethod
    def set_bot(cls):
        cls.bot_reference = MailURLCollectorBot
        cls.sysconfig = {'http_url': 'http://localhost/two_files.tar.gz',
                         'extract_files': True,
                         'name': 'Example feed',
                         }
