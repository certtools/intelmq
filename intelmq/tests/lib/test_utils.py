# -*- encoding: utf-8 -*-
"""
Testing the utility functions of intelmq.

Decoding and Encoding, Logging functionality (file and stream), and log
parsing.
base64 de-/encoding is not tested yet, as we fully rely on the module.
"""
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
                      u'Lorem ipsum dolor sit amet'],
           'unicode': [b'\xc2\xa9\xc2\xab\xc2\xbb \xc2\xa4\xc2\xbc',
                       u'©«» ¤¼']}


class TestUtils(unittest.TestCase):

    def test_decode_byte(self):
        """Tests if the decode can handle bytes."""
        self.assertEqual(SAMPLES['normal'][1],
                         utils.decode(SAMPLES['normal'][0]))

    def test_decode_unicode(self):
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

    def test_file_logger(self):
        """Tests if a logger for a file can be generated with log()."""

        with tempfile.NamedTemporaryFile() as handle:
            filename = handle.name
            name = os.path.split(filename)[-1]
            logger = utils.log(tempfile.tempdir, name)

            logger.info(LINES['spare'][0])
            logger.error(LINES['spare'][1])
            logger.critical(LINES['spare'][2])

            handle.seek(0)
            file_lines = handle.readlines()

            line_format = [line.format(name) for line in LINES['long']]
            for ind, line in enumerate(file_lines):
                self.assertRegexpMatches(line, line_format[ind])

    def test_stream_logger(self):
        """Tests if a logger for a stream can be generated with log()."""

        stream = io.BytesIO()
        with tempfile.NamedTemporaryFile() as handle:
            filename = handle.name
            name = os.path.split(filename)[-1]
            logger = utils.log(tempfile.tempdir, name, stream=stream)

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
        self.assertDictEqual({'asctime': '2015-05-29 21:00:24,379',
                              'name': 'malware-domain-list-collector',
                              'levelname': 'ERROR',
                              'message': 'Something went wrong'},
                             fields)


if __name__ == "__main__":
    unittest.main()
