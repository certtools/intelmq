#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:10:54 2019

@author: sebastian
"""
import os

if os.getenv('INTELMQ_TEST_EXOTIC'):
    from imbox.parser import parse_email
    with open(os.path.join(os.path.dirname(__file__), 'foobarzip.eml')) as handle:
        EMAIL_ZIP_FOOBAR = parse_email(handle.read())
    with open(os.path.join(os.path.dirname(__file__), 'foobartxt.eml')) as handle:
        EMAIL_TXT_FOOBAR = parse_email(handle.read())


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
        yield 0, EMAIL_ZIP_FOOBAR


class MockedTxtImbox(MockedImbox):
    def messages(self, *args, **kwargs):
        yield 0, EMAIL_TXT_FOOBAR
