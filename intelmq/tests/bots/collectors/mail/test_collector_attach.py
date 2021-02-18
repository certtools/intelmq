# -*- coding: utf-8 -*-
"""
Testing Mail Attach collector
"""
import os
import unittest
import unittest.mock as mock

import intelmq.lib.test as test

from intelmq.bots.collectors.mail.collector_mail_attach import MailAttachCollectorBot
from intelmq.lib.utils import base64_encode
if os.getenv('INTELMQ_TEST_EXOTIC'):
    from .lib import MockedZipImbox, MockedBadAttachmentImbox

REPORT_FOOBARZIP = {
                    '__type': 'Report',
                    'extra.email_from': 'wagner@cert.at',
                    'extra.email_message_id': '<07ce0153-060b-f48d-73d9-d92a20b3b3aa@cert.at>',
                    'extra.email_subject': 'foobar zip',
                    'extra.email_date': 'Tue, 3 Sep 2019 16:57:40 +0200',
                    'feed.accuracy': 100.0,
                    'feed.name': 'IMAP Feed',
                    'raw': base64_encode('bar text\n'),
                    'extra.file_name': 'foobar',
                    }


@test.skip_exotic()
class TestMailAttachCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    Test MailAttachCollectorBot
    """
    @classmethod
    def set_bot(cls):
        cls.bot_reference = MailAttachCollectorBot
        cls.sysconfig = {'mail_host': None,
                         'mail_user': None,
                         'mail_password': None,
                         'mail_ssl': None,
                         'folder': None,
                         'subject_regex': None,
                         'attach_regex': '.*zip',
                         'name': 'IMAP Feed',
                         }

    def test_extract_files(self):
        with mock.patch('imbox.Imbox', new=MockedZipImbox):
            self.run_bot(parameters={'extract_files': True})
        self.assertMessageEqual(0, REPORT_FOOBARZIP)

    def test_attach_unzip(self):
        self.allowed_warning_count = 1
        with mock.patch('imbox.Imbox', new=MockedZipImbox):
            self.run_bot(parameters={'attach_unzip': True})
        self.assertMessageEqual(0, REPORT_FOOBARZIP)

    def test_attach_no_filename(self):
        """
        https://github.com/certtools/intelmq/issues/1538
        """
        with mock.patch('imbox.Imbox', new=MockedBadAttachmentImbox):
            self.run_bot()
        self.assertOutputQueueLen(0)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
