"""
RPZ file output

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import os
import tempfile
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.rpz_file.output import RpzFileOutputBot

INPUT = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'source.fqdn': 'cuhk.edu.hk.itlf.cf',
    'misp.event_uuid': '5f6dbd1d-9d04-4795-a0cd-36bd0a09d489',
    'misp.attribute_uuid': '3cd903ab-329e-444e-a0d9-fdf6dcc584d8',
    'comment': '{"date": "2020-10-19", "priority": 3, "confidence": 5, "comment": "", "context": "Phishing", "expiryDate": "2025-10-18"}',
    'event_description.text': 'Network activity',
    'event_description.url': 'https://sig01.threatreveal.com/events/view/150354',
    'classification.type': 'phishing',
    'time.source': '2020-10-20T12:57:33+00:00',
    'extra.tags': ['signatures', 'tlp:amber', 'cybercrime', 'misp-galaxy:threat-actor="cobalt dickens"'],
    'tlp': 'AMBER',
    'extra.orgc': 'bae systems',
    'extra.to_ids': True,
    'extra.first_seen': '2020-10-19',
    'extra.confidence': 'high',
    'extra.valid_to': '2025-10-18',
    'extra.elastic_index': 'cti-2020-10',
    'extra.elastic_id': 'VwVnSnUBXjJtaqsUSw8T'}

INPUT_2 = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'source.fqdn': 'pw.aparat.com.torojoonemadaretkarkonkhasteshodamdigeenqadtestzadam.filterchipedaramodarovordibekeshbiroon.dollarshode20000tomanbaskondigeh.salavatemohammadibefres.soltane-tel-injas-heh.digital',
    'misp.event_uuid': '5f6dbd1d-9d04-4795-a0cd-36bd0a09d489',
    'misp.attribute_uuid': '3cd903ab-329e-444e-a0d9-fdf6dcc584d8',
    'comment': '{"date": "2020-10-19", "priority": 3, "confidence": 5, "comment": "", "context": "Phishing", "expiryDate": "2025-10-18"}',
    'event_description.text': 'Network activity',
    'event_description.url': 'https://sig01.threatreveal.com/events/view/150354',
    'classification.type': 'phishing',
    'time.source': '2020-10-20T12:57:33+00:00',
    'extra.tags': ['signatures', 'tlp:amber', 'cybercrime', 'misp-galaxy:threat-actor="cobalt dickens"'],
    'tlp': 'AMBER',
    'extra.orgc': 'bae systems',
    'extra.to_ids': True,
    'extra.first_seen': '2020-10-19',
    'extra.confidence': 'high',
    'extra.valid_to': '2025-10-18',
    'extra.elastic_index': 'cti-2020-10',
    'extra.elastic_id': 'VwVnSnUBXjJtaqsUSw8T'}


class TestFileOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RpzFileOutputBot
        cls.os_fp, cls.filename = tempfile.mkstemp()
        cls.sysconfig = {"hierarchical_output": True,
                         "file": cls.filename,
                         "cname": 'cert.aa.'
                         }

    def test_event2(self):
        self.input_message = INPUT_2
        self.run_bot()
        filepointer = os.fdopen(self.os_fp, 'rt')
        filepointer.seek(0)
        file_lines = filepointer.readlines()
        self.assertEqual(';  Response Policy Zones (RPZ)\n', file_lines[4])
        self.assertEqual(
            'pw.aparat.com.torojoonemadaretkarkonkhasteshodamdigeenqadtestzadam.filterchipedaramodarovordibekeshbiroon.dollarshode20000tomanbaskondigeh.salavatemohammadibefres.soltane-tel-injas-heh.digital CNAME cert.aa.\n',
            file_lines[10])
        self.assertEqual(
            'www.pw.aparat.com.torojoonemadaretkarkonkhasteshodamdigeenqadtestzadam.filterchipedaramodarovordibekeshbiroon.dollarshode20000tomanbaskondigeh.salavatemohammadibefres.soltane-tel-injas-heh.digital CNAME cert.aa.\n',
            file_lines[11])
        self.assertEqual(12, len(file_lines))
        filepointer.close()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.filename)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
