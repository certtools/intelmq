"""
Bro file output

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import os
import tempfile
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.bro_file.output import BroFileOutputBot

INPUT = {
    "__type": "Event",
    "classification.type": "infected-system",
    "feed.url": "http://feed.url",
    "feed.accuracy": 80.0,
    "source.asn": 64496,
    "extra.elastic_id": "elasticid1",
    "source.ip": "192.0.2.1",
    "feed.name": "Example Feed",
    "source.url": "http://192.0.2.1",
}
INPUT1 = {
    "__type": "Event",
    "classification.type": "infected-system",
    "feed.url": "http://feed.url",
    "feed.accuracy": 80.0,
    "extra.elastic_id": "elasticid2",
    "source.asn": 64496,
    "feed.name": "Example Feed",
}


class TestBroFileOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BroFileOutputBot
        cls.os_fp, cls.filename = tempfile.mkstemp()
        cls.sysconfig = {"hierarchical_output": True,
                         "file": cls.filename}

    def test_event(self):
        self.input_message = INPUT
        self.run_bot()
        filepointer = os.fdopen(self.os_fp, 'rt')
        filepointer.seek(0)
        file_lines = filepointer.readlines()
        self.assertEqual(
            '#fields	indicator	indicator_type	meta.desc	meta.cif_confidence	meta.source\n',
            file_lines[0])
        self.assertEqual(
            '192.0.2.1	Intel::ADDR	infected-system	80	\n',
            file_lines[1])
        self.assertEqual(
            'http://192.0.2.1	Intel::URL	infected-system	80	\n',
            file_lines[2])
        self.assertEqual(3, len(file_lines))
        filepointer.close()

    def test_event_did_not_have_bro_indicators(self):
        self.input_message = INPUT1
        self.run_bot()
        self.assertLogMatches(pattern="source.ipEvent did not have Bro indicator types.", levelname="DEBUG")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.filename)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
