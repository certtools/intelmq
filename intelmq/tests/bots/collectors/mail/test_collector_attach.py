# -*- coding: utf-8 -*-
"""
Testing Mail Attach collector
"""
from imbox.parser import parse_email
import os
import unittest
import unittest.mock as mock

import intelmq.lib.test as test

with open(os.path.join(os.path.dirname(__file__), 'foobarzip.eml')) as handle:
    EMAIL_FOOBAR = parse_email(handle.read())


class MockedImbox():
    _connected = False

    def __init__(self, hostname, username=None, password=None, ssl=True,
                 port=None, ssl_context=None, policy=None, starttls=False):
        pass

    def messages(self, *args, **kwargs):
        yield 0, EMAIL_FOOBAR

    def mark_seen(self, uid):
        pass

    def logout(self):
        pass


from intelmq.bots.collectors.mail.collector_mail_attach import MailAttachCollectorBot


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
        with mock.patch('imbox.Imbox', new=MockedImbox):
            self.run_bot()
        self.assertMessageEqual(0, REPORT_FOOBARZIP)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
