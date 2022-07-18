# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest

from intelmq.lib.upgrade.v233 import feodotracker_browse


V233_FEODOTRACKER_BROWSE_IN = {
    "global": {},
    'Feodo-tracker-browse-parser': {
        'module': "intelmq.bots.parsers.html_table.parser",
        'parameters': {
            'columns': 'time.source,source.ip,malware.name,status,extra.SBL,source.as_name,source.geolocation.cc'.split(','),
            'type': 'c2server',
            'ignore_values': ',,,,Not listed,,',
            'skip_table_head': True,
        }
    }
}
V233_FEODOTRACKER_BROWSE_OUT = {
    "global": {},
    'Feodo-tracker-browse-parser': {
        'module': "intelmq.bots.parsers.html_table.parser",
        'parameters': {
            'columns': 'time.source,source.ip,malware.name,status,source.as_name,source.geolocation.cc',
            'type': 'c2server',
            'ignore_values': ',,,,,',
            'skip_table_head': True,
        }
    }
}


class TestUpgradeV233(unittest.TestCase):
    def test_feodotracker_browse(self):
        """ Test feodotracker_browse """
        result = feodotracker_browse(V233_FEODOTRACKER_BROWSE_IN, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V233_FEODOTRACKER_BROWSE_OUT, result[1])
