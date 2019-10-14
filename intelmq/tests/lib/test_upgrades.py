"""
Tests the upgrade functions.
"""
import unittest

import intelmq.lib.upgrades as upgrades


V202 = {"test-collector": {
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
V202_EXP = {"test-collector": {
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

DEP_110 = {"n6-collector": {
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
DEP_110_EXP = {"n6-collector": {
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
}}


def generate_function(function):
    def test_function(self):
        """ Test if no errors happen for upgrade function %s. """ % function.__name__
        function({}, {}, dry_run=True)
    return test_function


class TestUpgradeLib(unittest.TestCase):
    def setUp(self):
        self.allfs = upgrades.__all__
        self.modulefs = [f for f in dir(upgrades) if f.startswith('v')]
        self.mapping_list = []
        self.mapping_list_name = []
        for values in upgrades.UPGRADES.values():
            self.mapping_list.extend((x for x in values))
            self.mapping_list_name.extend((x.__name__ for x in values))

    def test_all_functions_used(self):
        self.assertEqual(len(self.mapping_list_name),
                         len(set(self.mapping_list_name)),
                         msg='Some function is assigned to multiple versions.')
        self.assertEqual(set(self.allfs),
                         set(self.mapping_list_name),
                         msg='v* functions in the module do not '
                             'match the mapping.')
        self.assertEqual(set(self.allfs), set(self.modulefs),
                         msg='v* functions in the module do not '
                             'match functions in __all__.')

    def test_v110_deprecations(self):
        """ Test v110_deprecations """
        result = upgrades.v110_deprecations({}, DEP_110, False)
        self.assertTrue(result[0])
        self.assertEqual(DEP_110_EXP, result[2])

    def test_v202_fixes(self):
        """ Test v202_feed_name """
        result = upgrades.v202_fixes({}, V202, False)
        self.assertTrue(result[0])
        self.assertEqual(V202_EXP, result[2])


for name in upgrades.__all__:
    setattr(TestUpgradeLib, 'test_function_%s' % name,
            generate_function(getattr(upgrades, name)))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
