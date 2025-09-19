# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:10:54 2019

@author: sebastian
"""
import os
from copy import deepcopy
from pathlib import Path

if os.getenv('INTELMQ_TEST_EXOTIC'):
    from imbox.parser import parse_email
    EMAIL_ZIP_FOOBAR = parse_email((Path(__file__).parent / 'foobarzip.eml').read_text())
    EMAIL_TXT_FOOBAR = parse_email((Path(__file__).parent / 'foobartxt.eml').read_text())
    EMAIL_FAKE_ATTACHMENT = parse_email((Path(__file__).parent / 'fake_attachment.eml').read_text())
    EMAIL_TEXT_ATTACHMENT = parse_email((Path(__file__).parent / 'text_attachment.eml').read_text())
    EMAIL_GPG_ATTACHMENT = parse_email((Path(__file__).parent / 'gpg_attachment.eml').read_text())
    EMAIL_TEXT_ATTACHMENT_EMPTY = parse_email((Path(__file__).parent / 'text_attachment_empty.eml').read_text())


class MockedImbox():
    def __init__(self, hostname, username=None, password=None, ssl=True,
                 port=None, ssl_context=None, policy=None, starttls=False):
        pass

    def messages(self, *args, **kwargs):
        raise NotImplementedError

    def mark_seen(self, uid):
        pass

    def logout(self):
        pass


class MockedZipImbox(MockedImbox):
    def messages(self, *args, **kwargs):
        # without deepcopy only the first read() in the attachment works
        yield 0, deepcopy(EMAIL_ZIP_FOOBAR)


class MockedTxtImbox(MockedImbox):
    def messages(self, *args, **kwargs):
        yield 0, deepcopy(EMAIL_TXT_FOOBAR)


class MockedBadAttachmentImbox(MockedImbox):
    def messages(self, *args, **kwargs):
        yield 0, deepcopy(EMAIL_FAKE_ATTACHMENT)


class MockedTextAttachmentImbox(MockedImbox):
    def messages(self, *args, **kwargs):
        yield 0, deepcopy(EMAIL_TEXT_ATTACHMENT)

class MockedGpgAttachmentImbox(MockedImbox):
    def messages(self, *args, **kwargs):
        yield 0, deepcopy(EMAIL_GPG_ATTACHMENT)

class MockedEmptyTextAttachmentImbox(MockedImbox):
    def messages(self, *args, **kwargs):
        yield 0, deepcopy(EMAIL_TEXT_ATTACHMENT_EMPTY)
