# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest

from intelmq.lib.upgrade.v202 import fixes


V202 = {"global": {},
        "test-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "feed": "Feed"
    }
},
    "ripe-expert": {
    "group": "Expert",
    "module": "intelmq.bots.experts.ripe.expert",
    "parameters": {
        "query_ripe_stat_asn": True,
    },
},
    "reversedns-expert": {
    "group": "Expert",
    "module": "intelmq.bots.experts.reverse_dns.expert",
    "parameters": {
    },
},
}
V202_EXP = {"global": {},
            "test-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "name": "Feed"
    }
},
    "ripe-expert": {
    "group": "Expert",
    "module": "intelmq.bots.experts.ripe.expert",
    "parameters": {
        "query_ripe_stat_asn": True,
        "query_ripe_stat_ip": True,
    },
},
    "reversedns-expert": {
    "group": "Expert",
    "module": "intelmq.bots.experts.reverse_dns.expert",
    "parameters": {
        "overwrite": True,
    },
},
}


class TestUpgradeV202(unittest.TestCase):
    def test_fixes(self):
        """ Test fixes """
        result = fixes(V202, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V202_EXP, result[1])
