# -*- encoding: utf-8 -*-
"""
Testing the utility functions of intelmq.

Decoding and Encoding, Logging functionality (file and stream), and log
parsing.
base64 de-/encoding is not tested yet, as we fully rely on the module.
"""
import datetime
import io
import os
import tempfile
import unittest

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

            logger.info(LINES['spare'][0])
            logger.error(LINES['spare'][1])
            logger.critical(LINES['spare'][2])
            handle.seek(0)
            file_lines = handle.readlines()

            line_format = [line.format(name) for line in LINES['long']]
            for ind, line in enumerate(file_lines):
                self.assertRegex(line.strip(), line_format[ind])

    def test_stream_logger(self):
        """Tests if a logger for a stream can be generated with log()."""

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

    def test_parse_logline(self):
        """Tests if the parse_logline() function works as expected"""
        line = ("2015-05-29 21:00:24,379 - malware-domain-list-collector - "
                "ERROR - Something went wrong")

        fields = utils.parse_logline(line)
        self.assertDictEqual({'date': '2015-05-29T21:00:24.379000',
                              'bot_id': 'malware-domain-list-collector',
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

        actual = utils.parse_logline(line, regex=utils.SYSLOG_REGEX)
        self.assertEqual({'bot_id': 'malware-domain-list-collector',
                          'date': '%d-02-22T10:17:10' % datetime.datetime.now().year,
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

    def test_parse_relative_raises(self):
        """Tests if parse_reltive correctly raises ValueError."""
        with self.assertRaises(ValueError):
            utils.parse_relative('1 hou')
        with self.assertRaises(ValueError):
            utils.parse_relative('1 minute')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
