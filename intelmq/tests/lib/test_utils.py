# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- encoding: utf-8 -*-
"""
Testing the utility functions of intelmq.

Decoding and Encoding, Logging functionality (file and stream), and log
parsing.
base64 de-/encoding is not tested yet, as we fully rely on the module.
"""
import contextlib
import datetime
import io
import os
import tempfile
import unittest
import unittest.mock
import requests
import pkg_resources
import pprint

import cerberus
import json

import termstyle

from intelmq.tests.test_conf import CerberusTests
import intelmq.lib.utils as utils

LINES = {'spare': ['Lorem', 'ipsum', 'dolor'],
         'short': ['{}: Lorem', '{}: ipsum',
                   '{}: dolor'],
         'long': [r'\A[-0-9]{{10}} [0-9:]{{8}},\d{{3}} - {} - INFO - Lorem\Z',
                  r'\A[-0-9]{{10}} [0-9:]{{8}},\d{{3}} - {} - ERROR - ipsum\Z',
                  r'\A[-0-9]{{10}} [0-9:]{{8}},\d{{3}} - {} - CRITICAL - dolor\Z'],
         }
SAMPLES = {'normal': [b'Lorem ipsum dolor sit amet',
                      'Lorem ipsum dolor sit amet'],
           'unicode': [b'\xc2\xa9\xc2\xab\xc2\xbb \xc2\xa4\xc2\xbc',
                       '©«» ¤¼']}


def new_get_runtime() -> dict:
    runtime_conf = utils.load_configuration(pkg_resources.resource_filename('intelmq', 'etc/runtime.yaml'))
    if 'global' not in runtime_conf:
        runtime_conf['global'] = {}
    runtime_conf['global']['http_proxy'] = 'http://localhost:8080'
    runtime_conf['global']['https_proxy'] = 'http://localhost:8080'
    runtime_conf['cymru-whois-expert']['parameters']['http_proxy'] = 'http://localhost:8081'
    return runtime_conf


class TestUtils(unittest.TestCase):

    def test_decode_byte(self):
        """Tests if the decode can handle bytes."""
        self.assertEqual(SAMPLES['normal'][1],
                         utils.decode(SAMPLES['normal'][0]))

    def test_decode_bytes_unicode(self):
        """Tests if the decode can handle bytes."""
        self.assertEqual(SAMPLES['unicode'][1],
                         utils.decode(SAMPLES['unicode'][0]))

    def test_encode_byte(self):
        """Tests if the decode can handle bytes."""
        self.assertEqual(SAMPLES['normal'][0],
                         utils.encode(SAMPLES['normal'][1]))

    def test_encode_unicode(self):
        """Tests if the decode can handle bytes."""
        self.assertEqual(SAMPLES['unicode'][0],
                         utils.encode(SAMPLES['unicode'][1]))

    def test_decode_ascii(self):
        """ Test ASCII decoding enforcement. """
        self.assertEqual('fobar',
                         utils.decode(b'fo\xe4bar', encodings=('ascii', ),
                                      force=True))

    def test_decode_unicode(self):
        """ Test decoding with unicode string. """
        self.assertEqual('foobar', utils.decode('foobar'))

    def test_encode_bytes(self):
        """ Test encoding with bytes string. """
        self.assertEqual('foobar', utils.decode(b'foobar'))

    def test_encode_force(self):
        """ Test ASCII encoding enforcement. """
        self.assertEqual(b'fobar',
                         utils.encode('fo\xe4bar', encodings=('ascii', ),
                                      force=True))

    def test_file_logger(self):
        """Tests if a logger for a file can be generated with log()."""

        with tempfile.NamedTemporaryFile(suffix=".log", mode='w+') as handle:
            filename = handle.name
            name = os.path.splitext(os.path.split(filename)[-1])[0]
            logger = utils.log(name, log_path=tempfile.tempdir,
                               stream=io.StringIO())

            logger.info(termstyle.green(LINES['spare'][0]))
            logger.error(LINES['spare'][1])
            logger.critical(LINES['spare'][2])
            handle.seek(0)
            file_lines = handle.readlines()

            line_format = [line.format(name) for line in LINES['long']]
            for ind, line in enumerate(file_lines):
                self.assertRegex(line.strip(), line_format[ind])

    def test_stream_logger_given(self):
        """
        Tests if a logger for a stream can be generated with log()
        if the stream is explicitly given.
        """

        stream = io.StringIO()
        with tempfile.NamedTemporaryFile() as handle:
            filename = handle.name
            name = os.path.split(filename)[-1]
            logger = utils.log(name, log_path=tempfile.tempdir, stream=stream)

            logger.info(LINES['spare'][0])
            logger.error(LINES['spare'][1])
            logger.critical(LINES['spare'][2])

            stream_lines = stream.getvalue().splitlines()

            line_format = [line.format(name) for line in LINES['short']]
            self.assertSequenceEqual(line_format, stream_lines)

    def test_stream_logger(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            with contextlib.redirect_stderr(stderr):
                logger = utils.log('test-bot', log_path=None)
                logger.info(LINES['spare'][0])
                logger.error(LINES['spare'][1])
                logger.critical(LINES['spare'][2])
        line_format = [line.format('test-bot') for line in LINES['short']]
        self.assertEqual(stdout.getvalue(), line_format[0] + '\n')
        self.assertEqual(stderr.getvalue(),
                         '\n'.join((termstyle.red(line_format[1]),
                                    termstyle.red(line_format[2]))) + '\n')

    def test_parse_logline(self):
        """Tests if the parse_logline() function works as expected"""
        line = ("2015-05-29 21:00:24,379 - malware-domain-list-collector - "
                "ERROR - Something went wrong")
        thread = ("2015-05-29 21:00:24,379 - malware-domain-list-collector.4 - "
                  "ERROR - Something went wrong")

        fields = utils.parse_logline(line)
        self.assertDictEqual({'date': '2015-05-29T21:00:24.379000',
                              'bot_id': 'malware-domain-list-collector',
                              'thread_id': None,
                              'log_level': 'ERROR',
                              'message': 'Something went wrong'},
                             fields)
        fields = utils.parse_logline(thread)
        self.assertDictEqual({'date': '2015-05-29T21:00:24.379000',
                              'bot_id': 'malware-domain-list-collector',
                              'thread_id': 4,
                              'log_level': 'ERROR',
                              'message': 'Something went wrong'},
                             fields)

    def test_parse_logline_invalid(self):
        """Tests if the parse_logline() function returns the line. """
        line = ("    report = self.receive_message()\n  File"
                " \"/usr/local/lib/python3.4/dist-packages/intelmq-1.0.0"
                "-py3.4.egg/intelmq/lib/bot.py\", line 259, in"
                " receive_message")

        actual = utils.parse_logline(line)
        self.assertEqual(line, actual)

    def test_parse_logline_syslog(self):
        """Tests if the parse_logline() function parses syslog correctly. """
        line = ("Feb 22 10:17:10 host malware-domain-list-collector: ERROR "
                "Something went wrong")
        thread = ("Feb 22 10:17:10 host malware-domain-list-collector.4: ERROR "
                "Something went wrong")

        actual = utils.parse_logline(line, regex=utils.SYSLOG_REGEX)
        self.assertEqual({'bot_id': 'malware-domain-list-collector',
                          'date': '%d-02-22T10:17:10' % datetime.datetime.now().year,
                          'thread_id': None,
                          'log_level': 'ERROR',
                          'message': 'Something went wrong'}, actual)
        actual = utils.parse_logline(thread, regex=utils.SYSLOG_REGEX)
        self.assertEqual({'bot_id': 'malware-domain-list-collector',
                          'date': '%d-02-22T10:17:10' % datetime.datetime.now().year,
                          'thread_id': 4,
                          'log_level': 'ERROR',
                          'message': 'Something went wrong'}, actual)

    def test_error_message_from_exc(self):
        """Tests if error_message_from_exc correctly returns the error message."""
        exc = IndexError('This is a test')
        self.assertEqual(utils.error_message_from_exc(exc), 'This is a test')

    def test_parse_relative(self):
        """Tests if parse_reltive returns the correct timespan."""
        self.assertEqual(utils.parse_relative('1 hour'), 60)
        self.assertEqual(utils.parse_relative('2\tyears'), 1051200)
        self.assertEqual(utils.parse_relative('5 minutes'), 5)
        self.assertEqual(utils.parse_relative('10 seconds'), 1 / 60 * 10)

    def test_parse_relative_raises(self):
        """Tests if parse_reltive correctly raises ValueError."""
        with self.assertRaises(ValueError):
            utils.parse_relative('1 hou')
        with self.assertRaises(ValueError):
            utils.parse_relative('1 µs')

    def test_seconds_to_human(self):
        """ Test seconds_to_human """
        self.assertEqual(utils.seconds_to_human(60), '1m')
        self.assertEqual(utils.seconds_to_human(3600), '1h')
        self.assertEqual(utils.seconds_to_human(86401), '1d 1s')
        self.assertEqual(utils.seconds_to_human(64.2), '1m 4s')
        self.assertEqual(utils.seconds_to_human(64.2, precision=1),
                         '1.0m 4.2s')

    def test_version_smaller(self):
        """ Test version_smaller """
        self.assertTrue(utils.version_smaller((1, 0, 0), (1, 1, 0)))
        self.assertTrue(utils.version_smaller((1, 0, 0), (1, 0, 1, 'alpha')))
        self.assertFalse(utils.version_smaller((1, 0, 0, 'beta', 3), (1, 0, 0, 'alpha', 0)))
        self.assertFalse(utils.version_smaller((1, 0, 0), (1, 0, 0, 'alpha', 99)))
        self.assertFalse(utils.version_smaller((1, 0, 0), (1, 0, 0, 'beta')))

    def test_unzip_tar_gz(self):
        """ Test the unzip function with a tar gz file. """
        filename = os.path.join(os.path.dirname(__file__), '../assets/two_files.tar.gz')
        with open(filename, 'rb') as fh:
            result = utils.unzip(fh.read(), extract_files=True)
        self.assertEqual(tuple(result), (b'bar text\n', b'foo text\n'))

    def test_unzip_tar_gz_return_names(self):
        """ Test the unzip function with a tar gz file and return_names. """
        filename = os.path.join(os.path.dirname(__file__), '../assets/two_files.tar.gz')
        with open(filename, 'rb') as fh:
            result = utils.unzip(fh.read(), extract_files=True, return_names=True)
        self.assertEqual(tuple(result), (('bar', b'bar text\n'),
                                         ('foo', b'foo text\n')))

    def test_unzip_gz(self):
        """ Test the unzip function with a gz file. """
        filename = os.path.join(os.path.dirname(__file__), '../assets/foobar.gz')
        with open(filename, 'rb') as fh:
            result = utils.unzip(fh.read(), extract_files=True)
        self.assertEqual(result, (b'bar text\n', ))

    def test_unzip_gz_name(self):
        """ Test the unzip function with a gz file. """
        filename = os.path.join(os.path.dirname(__file__), '../assets/foobar.gz')
        with open(filename, 'rb') as fh:
            result = utils.unzip(fh.read(), extract_files=True, return_names=True)
        self.assertEqual(result, ((None, b'bar text\n'), ))

    def test_unzip_zip(self):
        """ Test the unzip function with a zip file. """
        filename = os.path.join(os.path.dirname(__file__), '../assets/two_files.zip')
        with open(filename, 'rb') as fh:
            result = utils.unzip(fh.read(), extract_files=True)
        self.assertEqual(tuple(result), (b'bar text\n', b'foo text\n'))

    def test_unzip_zip_return_names(self):
        """ Test the unzip function with a zip file and return_names. """
        filename = os.path.join(os.path.dirname(__file__), '../assets/two_files.zip')
        with open(filename, 'rb') as fh:
            result = utils.unzip(fh.read(), extract_files=True, return_names=True)
        self.assertEqual(tuple(result), (('bar', b'bar text\n'),
                                         ('foo', b'foo text\n')))

    def test_file_name_from_response(self):
        """ test file_name_from_response """
        response = requests.Response()
        response.headers['Content-Disposition'] = 'attachment; filename=2019-09-09-drone_brute_force-austria-geo.csv'
        self.assertEqual(utils.file_name_from_response(response),
                         '2019-09-09-drone_brute_force-austria-geo.csv')

    def test_list_all_bots(self):
        """ test list_all_bots """
        bots_list = utils.list_all_bots()
        test = CerberusTests()
        with open(os.path.join(os.path.dirname(__file__), '../assets/bots.schema.json')) as handle:
            schema = json.loads(test.convert_cerberus_schema(handle.read()))

        v = cerberus.Validator(schema)

        self.assertTrue(v.validate(bots_list),
                        msg='Invalid BOTS list:\n%s' % pprint.pformat(v.errors))

    def test_get_bots_settings(self):
        with unittest.mock.patch.object(utils, "get_runtime", new_get_runtime):
            runtime = utils.get_bots_settings()
        self.assertEqual(runtime['cymru-whois-expert']['parameters']['http_proxy'], 'http://localhost:8081')
        self.assertEqual(runtime['deduplicator-expert']['parameters']['http_proxy'], 'http://localhost:8080')

        with unittest.mock.patch.object(utils, "get_runtime", new_get_runtime):
            cymru = utils.get_bots_settings('cymru-whois-expert')
        self.assertEqual(cymru['parameters']['http_proxy'], 'http://localhost:8081')

        with unittest.mock.patch.object(utils, "get_runtime", new_get_runtime):
            deduplicator = utils.get_bots_settings('deduplicator-expert')
        self.assertEqual(deduplicator['parameters']['http_proxy'], 'http://localhost:8080')

    def test_get_global_settings(self):
        with unittest.mock.patch.object(utils, "get_runtime", new_get_runtime):
            defaults = utils.get_global_settings()
        self.assertEqual(defaults['http_proxy'], 'http://localhost:8080')
        self.assertEqual(defaults['https_proxy'], 'http://localhost:8080')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
