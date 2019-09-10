# -*- coding: utf-8 -*-
"""
Testing Mail Attach collector
"""
import os
import unittest
import unittest.mock as mock

import intelmq.lib.test as test

from intelmq.bots.collectors.mail.collector_mail_attach import MailAttachCollectorBot
if os.getenv('INTELMQ_TEST_EXOTIC'):
    from .lib import MockedZipImbox

REPORT_FOOBARZIP = {
                    '__type': 'Report',
                    'extra.email_from': 'wagner@cert.at',
                    'extra.email_message_id': '<07ce0153-060b-f48d-73d9-d92a20b3b3aa@cert.at>',
                    'extra.email_subject': 'foobar zip',
                    'feed.accuracy': 100.0,
                    'feed.name': 'IMAP Feed',
                    'raw': 'UEsDBAoAAAAAAG93AU+n9EgFCQAAAAkAAAAGABwAZm9vYmFyVVQJAAMx4kJdMeJCXXV4CwABBOgDAAAEZAAAAGJhciB0ZXh0ClBLAQIeAwoAAAAAAG93AU+n9EgFCQAAAAkAAAAGABgAAAAAAAEAAACkgQAAAABmb29iYXJVVAUAAzHiQl11eAsAAQToAwAABGQAAABQSwUGAAAAAAEAAQBMAAAASQAAAAAA',
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

    def test_one(self):
        with mock.patch('imbox.Imbox', new=MockedZipImbox):
            self.run_bot()
        self.assertMessageEqual(0, REPORT_FOOBARZIP)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
