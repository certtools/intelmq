# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
from copy import deepcopy
import unittest

import pkg_resources

from intelmq.lib.upgrade.harmonization import harmonization
from intelmq.lib.utils import load_configuration


HARM = load_configuration(pkg_resources.resource_filename('intelmq',
                                                          'etc/harmonization.conf'))
MISSING_REPORT = deepcopy(HARM)
del MISSING_REPORT['report']
WRONG_TYPE = deepcopy(HARM)
WRONG_TYPE['event']['source.asn']['type'] = 'String'
WRONG_REGEX = deepcopy(HARM)
WRONG_REGEX['event']['protocol.transport']['iregex'] = 'foobar'


class TestUpgradeHarmonization(unittest.TestCase):
    def test_missing_report_harmonization(self):
        """ Test missing report in harmonization """
        result = harmonization({}, MISSING_REPORT, False)
        self.assertTrue(result[0])
        self.assertEqual(HARM, result[2])

    def test_wrong_type_harmonization(self):
        """ Test wrong type in harmonization """
        result = harmonization({}, WRONG_TYPE, False)
        self.assertTrue(result[0])
        self.assertEqual(HARM, result[2])

    def test_wrong_regex_harmonization(self):
        """ Test wrong regex in harmonization """
        result = harmonization({}, WRONG_REGEX, False)
        self.assertTrue(result[0])
        self.assertEqual(HARM, result[2])
