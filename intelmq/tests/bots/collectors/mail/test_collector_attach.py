# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing Mail Attach collector
"""
import os
from shutil import copytree
from tempfile import mkdtemp
import unittest
import unittest.mock as mock

import intelmq.lib.test as test

from intelmq.bots.collectors.mail.collector_mail_attach import MailAttachCollectorBot
from intelmq.lib.utils import base64_encode
from intelmq.lib.exceptions import PipelineError
if os.getenv('INTELMQ_TEST_EXOTIC'):
    from .lib import MockedZipImbox, MockedBadAttachmentImbox, MockedTextAttachmentImbox, MockedGpgAttachmentImbox, MockedEmptyTextAttachmentImbox

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
REPORT_FOOBARTXT = REPORT_FOOBARZIP.copy()
REPORT_FOOBARTXT['extra.file_name'] = 'foobar.txt'
REPORT_FOOBARGPG = REPORT_FOOBARZIP.copy()
REPORT_FOOBARGPG['extra.file_name'] = 'foobar.txt.gpg'


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
                         'name': 'IMAP Feed'
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

    def test_text_attachment(self):
        """
        https://github.com/certtools/intelmq/pull/2021
        """
        with mock.patch('imbox.Imbox', new=MockedTextAttachmentImbox):
            self.run_bot(parameters={'attach_regex': '.*.txt$',
                                     'extract_files': False})
        self.assertMessageEqual(0, REPORT_FOOBARTXT)

    def test_text_attachment_empty(self):
        # without allow_empty, the parsing fails
        with mock.patch('imbox.Imbox', new=MockedEmptyTextAttachmentImbox), self.assertRaises(PipelineError):
            self.run_bot(parameters={'attach_regex': '.*.txt$',
                                     'extract_files': False,
                                     'allow_empty': False})

        with mock.patch('imbox.Imbox', new=MockedEmptyTextAttachmentImbox):
            self.run_bot(parameters={'attach_regex': '.*.txt$',
                                     'extract_files': False,
                                     'allow_empty': True})
        self.assertOutputQueueLen(0)


    def _make_ring(self):
        temp_gnupg_dir = mkdtemp(prefix="gnupg-temp-")
        copytree(os.environ.get('GPG_RING_PATH'), temp_gnupg_dir, dirs_exist_ok=True)
        return temp_gnupg_dir


    def test_gpg_attachment(self):
        """
        Attachment is GPG encrypted.
        """
        with mock.patch('imbox.Imbox', new=MockedGpgAttachmentImbox):
            self.run_bot(parameters={'attach_regex': '.*.gpg$',
                                     'extract_files': False,
                                     'decrypt_openpgp': True,
                                     'gpg_home': self._make_ring(),
                                     'openpgp_passphrase': 'test'})
        self.assertMessageEqual(0, REPORT_FOOBARGPG)

    def test_gpg_wrong_passphrase(self):
        """
        Attachment is GPG encrypted. But we have wrong passphrase.
        """
        with mock.patch('imbox.Imbox', new=MockedGpgAttachmentImbox):
            self.run_bot(parameters={'attach_regex': '.*.gpg$',
                                     'extract_files': False,
                                     'decrypt_openpgp': True,
                                     'gpg_home': self._make_ring(),
                                     'openpgp_passphrase': 'WRONG',
                                     }, allowed_error_count=1)
        self.assertLogMatches("Could not decrypt")
        self.assertOutputQueueLen(0)

    def test_gpg_not_encrypted(self):
        """
        We want to decrypt an attachment that is not encrypted.
        """
        with mock.patch('imbox.Imbox', new=MockedTextAttachmentImbox):
            self.run_bot(parameters={'attach_regex': '.*.txt$',
                                     'extract_files': False,
                                     'decrypt_openpgp': True,
                                     'gpg_home': self._make_ring(),
                                     'openpgp_passphrase': 'test',
                                     }, allowed_error_count=1)
        self.assertLogMatches("Could not decrypt")
        self.assertOutputQueueLen(0)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
