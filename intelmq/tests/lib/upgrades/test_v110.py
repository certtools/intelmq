# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest
from intelmq.lib.upgrade.v110 import deprecations


DEP_110 = {"global": {},
           "n6-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.n6.collector_stomp",
    "parameters": {
        "feed": "Feed",
    },
},
    "cymru-full-bogons-parser": {
    "group": "Parser",
    "module": "intelmq.bots.parsers.cymru_full_bogons.parser",
    "parameters": {
    },
},
    "ripe-expert": {
    "group": "Expert",
    "module": "intelmq.bots.experts.ripencc_abuse_contact.expert",
    "parameters": {
        "query_ripe_stat": True,
    },
}
}

DEP_110_EXP = {"global": {},
               "n6-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.stomp.collector",
    "parameters": {
        "name": "Feed",
    },
},
    "cymru-full-bogons-parser": {
    "group": "Parser",
    "module": "intelmq.bots.parsers.cymru.parser_full_bogons",
    "parameters": {
    }},
    "ripe-expert": {
    "group": "Expert",
    "module": "intelmq.bots.experts.ripe.expert",
    "parameters": {
        "query_ripe_stat_asn": True,
        "query_ripe_stat_ip": True,
    },
}
}


class TestUpgradeV110(unittest.TestCase):
    def test_deprecations(self):
        """ Test deprecations """
        result = deprecations(DEP_110, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(DEP_110_EXP, result[1])
