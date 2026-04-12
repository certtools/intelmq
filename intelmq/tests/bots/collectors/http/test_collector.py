# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing HTTP collector
"""
import datetime
import os
import unittest

import requests_mock

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.http.collector_http import HTTPCollectorBot

OUTPUT = [
    {
        "__type": "Report",
        "feed.name": "Example feed",
        "feed.accuracy": 100.,
        "feed.url": "http://localhost/two_files.tar.gz",
        "raw": utils.base64_encode('bar text\n'),
        "extra.file_name": "bar",
    },
    {
        "__type": "Report",
        "feed.name": "Example feed",
        "feed.accuracy": 100.,
        "feed.url": "http://localhost/two_files.tar.gz",
        "raw": utils.base64_encode('foo text\n'),
        "extra.file_name": "foo",
    },
    {
        "__type": "Report",
        "feed.name": "Example feed",
        "feed.accuracy": 100.,
        "feed.url": "http://localhost/foobar.txt",
        "raw": utils.base64_encode("bar text\n"),
    }
]


ASSET_PATH = os.path.join(os.path.dirname(__file__), '../../../assets/')


def prepare_mocker(mocker):
    for filename in os.listdir(ASSET_PATH):
        with open(os.path.join(ASSET_PATH, filename), 'rb') as f:
            mocker.get('http://localhost/%s' % filename, content=f.read())



@requests_mock.Mocker()
class TestHTTPCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HTTPCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTTPCollectorBot
        cls.sysconfig = {'http_url': 'http://localhost/two_files.tar.gz',
                         'extract_files': True,
                         'name': 'Example feed',
                         }

    def test_targz_twofiles(self, mocker):
        """ Test tar.gz archive with two files inside. """
        self.input_message = None
        prepare_mocker(mocker)
        self.run_bot(iterations=1)

        self.assertMessageEqual(0, OUTPUT[0])
        self.assertMessageEqual(1, OUTPUT[1])

    def test_formatting(self, mocker):
        """ Test formatting URLs. """
        self.input_message = None
        self.allowed_warning_count = 1  # message has empty raw
        url = 'http://localhost/%s.txt' % datetime.datetime.now().year
        mocker.get(url, text='')

        self.run_bot(parameters={'http_url': 'http://localhost/{time[%Y]}.txt',
                                 'extract_files': None,
                                 'name': 'Example feed',
                                 'http_url_formatting': True,
                                 },
                     iterations=1)
        self.assertLogMatches('Downloading report from %r.' % url,
                              'INFO')

    def test_gzip(self, mocker):
        """
        Test with a gzipped file.
        """
        prepare_mocker(mocker)
        self.run_bot(parameters={'http_url': 'http://localhost/foobar.gz',
                                 'extract_files': True,
                                 'name': 'Example feed',
                                 },
                     iterations=1)

        output = OUTPUT[0].copy()
        output['feed.url'] = 'http://localhost/foobar.gz'
        del output['extra.file_name']
        self.assertMessageEqual(0, output)
        self.assertLogMatches(r'Report downloaded \(29B\).', 'INFO')

    def test_zip_auto(self, mocker):
        """
        Test automatic unzipping
        """
        prepare_mocker(mocker)
        self.run_bot(parameters={'http_url': 'http://localhost/two_files.zip',
                                 'name': 'Example feed',
                                 },
                     iterations=1)

        output0 = OUTPUT[0].copy()
        output0['feed.url'] = 'http://localhost/two_files.zip'
        output1 = OUTPUT[1].copy()
        output1['feed.url'] = 'http://localhost/two_files.zip'
        self.assertMessageEqual(0, output0)
        self.assertMessageEqual(1, output1)

    def test_zip(self, mocker):
        """
        Test unzipping with explicit extract_files
        """
        prepare_mocker(mocker)
        self.run_bot(parameters={'http_url': 'http://localhost/two_files.zip',
                                 'extract_files': ['bar', 'foo'],
                                 'name': 'Example feed',
                                 },
                     iterations=1)

        output0 = OUTPUT[0].copy()
        output0['feed.url'] = 'http://localhost/two_files.zip'
        output1 = OUTPUT[1].copy()
        output1['feed.url'] = 'http://localhost/two_files.zip'
        self.assertMessageEqual(0, output0)
        self.assertMessageEqual(1, output1)

    def test_zip_subdirs(self, mocker):
        """
        Test unzipping when the zip has subdirectories
        """
        prepare_mocker(mocker)
        self.run_bot(parameters={'http_url': 'http://localhost/subdir.zip',
                                 'name': 'Example feed',
                                 },
                     iterations=1)

        output0 = OUTPUT[0].copy()
        output0['feed.url'] = 'http://localhost/subdir.zip'
        output0['extra.file_name'] = 'subdir/bar'
        output1 = OUTPUT[1].copy()
        output1['feed.url'] = 'http://localhost/subdir.zip'
        output1['extra.file_name'] = 'subdir/foo'
        self.assertMessageEqual(0, output0)
        self.assertMessageEqual(1, output1)

    @test.skip_exotic()
    def test_pgp(self, mocker):
        """
        Test with PGP signature
        """
        prepare_mocker(mocker)
        self.run_bot(
            parameters={
                "http_url": "http://localhost/foobar.txt",
                "name": "Example feed",
                "extract_files": False,
                "verify_gpg_signatures": True,
                "signature_url": "http://localhost/foobar.txt.asc"
            },
            iterations=1
        )
        self.assertMessageEqual(0, OUTPUT[2])

    def test_debug_request_response_log(self, mocker):
        """
        Test if the request and response is logged in case of errors as DEBUG
        """
        mocker.get(self.sysconfig['http_url'], status_code=400,
                   headers={'some': 'header'},
                   text='Should be in logs')
        self.run_bot(allowed_error_count=1,
                     parameters={'logging_level': 'DEBUG'})
        self.assertLogMatches(r"Request headers: .*\.", 'DEBUG')
        self.assertLogMatches("Request body: None.", 'DEBUG')
        self.assertLogMatches("Response headers: {'some': 'header'}.", 'DEBUG')
        self.assertLogMatches("Response body: 'Should be in logs'.", 'DEBUG')

    def test_chunking(self, mocker):
        """
        Test file chunking
        """
        prepare_mocker(mocker)
        self.run_bot(allowed_error_count=1,
                     parameters={
                        'http_url': 'http://localhost/multiline.txt',
                        'chunk_size': 3,
                        'chunk_replicate_header': False,
                        'extract_files': None,
                        })
        self.assertOutputQueueLen(4)


@requests_mock.Mocker()
class TestHTTPCollectorBotAuthentication(test.BotTestCase, unittest.TestCase):
    """
    HttpMixin setup is called a initialization
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTTPCollectorBot
        cls.sysconfig = {'http_url': 'http://localhost/foobar',
                         'name': 'Example feed',
                         'http_username': '',
                         'http_password': '',
                         'logging_level': 'DEBUG'
                         }

    def test_empty_auth(self, mocker):
        """
        Test that no Authorization is set when username and password are empty strings.
        """
        def check_authorization_header(request):
            print(f'check_authorization_header: {request.headers}')  # show the erroneos headers when the test fails
            return 'Authorization' not in request.headers
        # generates a mock address if the Authorization header is empty, otherwise the test fails
        captured = mocker.register_uri('GET', self.sysconfig['http_url'],
                            text='Foo Bar',
                            additional_matcher=check_authorization_header)
        self.run_bot()

    def test_auth_only_username_or_password(self, mocker):
        """
        Test that no Authorization is set only the username is given and password is missing
        """
        def check_authorization_header(request):
            print(f'check_authorization_header: {request.headers}')  # show the erroneos headers when the test fails
            return 'Authorization' not in request.headers
        # generates a mock address if the Authorization header is empty, otherwise the test fails
        captured = mocker.register_uri('GET', self.sysconfig['http_url'],
                            text='Foo Bar',
                            additional_matcher=check_authorization_header)
        log_line = "Either 'http_username' or 'http_password' are given, but for HTTP Authentication, both must be set\."
        self.run_bot(parameters={'http_username': 'username'}, allowed_warning_count=1)
        self.assertLogMatches(log_line, 'WARNING')
        self.run_bot(parameters={'http_password': 'password'}, allowed_warning_count=1)
        self.assertLogMatches(log_line, 'WARNING')

    def test_auth(self, mocker):
        """
        Test the Authorization header when username and password are set.
        """
        def check_authorization_header(request):
            print(f'check_authorization_header: {request.headers}')  # show the erroneos headers when the test fails
            return request.headers['Authorization'] == 'Basic dXNlcjpwYXNzd29yZA=='
        # generates a mock address if the Authorization header is correct, otherwise the test fails
        captured = mocker.register_uri('GET', self.sysconfig['http_url'],
                            text='Foo Bar',
                            additional_matcher=check_authorization_header)
        self.run_bot(parameters={'http_username': 'user',
                                 'http_password': 'password'})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
