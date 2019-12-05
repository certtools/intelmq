"""
Tests the upgrade functions.
"""
import unittest
import pkg_resources
from copy import deepcopy

import intelmq.lib.upgrades as upgrades
from intelmq.lib.utils import load_configuration


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
V210 = {"test-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.rt.collector_rt",
    "parameters": {
        "unzip_attachment": True,
    }
},
    "test-collector2": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.rt.collector_rt",
    "parameters": {
    },
},
    "postgresql-output": {
    "group": "Output",
    "module": "intelmq.bots.outputs.postgresql.output",
    "parameters": {
        "autocommit": True,
        "database": "intelmq-events",
        "host": "localhost",
                "jsondict_as_string": True,
                "password": "<password>",
                "port": "5432",
                "sslmode": "require",
                "table": "events",
                "user": "intelmq"
    },
},
    "db-lookup": {
    "module": "intelmq.bots.experts.generic_db_lookup.expert",
    "parameters": {
        "database": "intelmq",
        "host": "localhost",
                "match_fields": {
                    "source.asn": "asn"
                },
        "overwrite": False,
        "password": "<password>",
        "port": "5432",
                "replace_fields": {
                    "contact": "source.abuse_contact",
                    "note": "comment"
                },
        "sslmode": "require",
        "table": "contacts",
        "user": "intelmq"
    }
}
}
V210_EXP = {"test-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.rt.collector_rt",
    "parameters": {
        "extract_attachment": True,
    }
},
    "test-collector2": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.rt.collector_rt",
    "parameters": {
    },
},
    "postgresql-output": {
    "group": "Output",
    "module": "intelmq.bots.outputs.sql.output",
    "parameters": {
        "autocommit": True,
        "database": "intelmq-events",
        "engine": "postgresql",
        "host": "localhost",
                "jsondict_as_string": True,
                "password": "<password>",
                "port": "5432",
                "sslmode": "require",
                "table": "events",
                "user": "intelmq"
    },
},
    "db-lookup": {
    "module": "intelmq.bots.experts.generic_db_lookup.expert",
    "parameters": {
        "engine": "postgresql",
        "database": "intelmq",
        "host": "localhost",
                "match_fields": {
                    "source.asn": "asn"
                },
        "overwrite": False,
        "password": "<password>",
        "port": "5432",
                "replace_fields": {
                    "contact": "source.abuse_contact",
                    "note": "comment"
                },
        "sslmode": "require",
        "table": "contacts",
        "user": "intelmq"
    }
}
}
V220_MISP_VERIFY_FALSE = {
"misp-collector": {
        "module": "intelmq.bots.collectors.misp.collector",
        "parameters": {
                "misp_verify": False}}}
V220_MISP_VERIFY_NULL = {
"misp-collector": {
        "module": "intelmq.bots.collectors.misp.collector",
        "parameters": {}}}
V220_MISP_VERIFY_TRUE = {
"misp-collector": {
        "module": "intelmq.bots.collectors.misp.collector",
        "parameters": {
                "misp_verify": True}}}
V220_HTTP_VERIFY_FALSE = {
"misp-collector": {
        "module": "intelmq.bots.collectors.misp.collector",
        "parameters": {
                "http_verify_cert": False}}}
DEFAULTS_HTTP_VERIFY_TRUE = {
        "http_verify_cert": True}
HARM = load_configuration(pkg_resources.resource_filename('intelmq',
                                                          'etc/harmonization.conf'))
V210_HARM = deepcopy(HARM)
del V210_HARM['report']['extra']
MISSING_REPORT = deepcopy(HARM)
del MISSING_REPORT['report']
WRONG_TYPE = deepcopy(HARM)
WRONG_TYPE['event']['source.asn']['type'] = 'String'


def generate_function(function):
    def test_function(self):
        """ Test if no errors happen for upgrade function %s. """ % function.__name__
        function({}, {}, {}, dry_run=True)
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
        result = upgrades.v110_deprecations({}, DEP_110, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(DEP_110_EXP, result[2])

    def test_v202_fixes(self):
        """ Test v202_feed_name """
        result = upgrades.v202_fixes({}, V202, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V202_EXP, result[2])

    def test_v210_deprecations(self):
        """ Test v210_deprecations """
        result = upgrades.v210_deprecations({}, V210, {}, True)
        self.assertTrue(result[0])
        self.assertEqual(V210_EXP, result[2])

    def test_v211_harmonization(self):
        """ Test v211_harmonization """
        result = upgrades.harmonization({}, {}, V210_HARM, False)
        self.assertTrue(result[0])
        self.assertEqual(HARM, result[3])

    def test_v220_configuration(self):
        """ Test v220_configuration. """
        result = upgrades.v220_configuration_1(DEFAULTS_HTTP_VERIFY_TRUE,
                                               V220_MISP_VERIFY_TRUE, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V220_MISP_VERIFY_NULL, result[2])
        result = upgrades.v220_configuration_1(DEFAULTS_HTTP_VERIFY_TRUE,
                                               V220_MISP_VERIFY_FALSE, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V220_HTTP_VERIFY_FALSE, result[2])

    def test_missing_report_harmonization(self):
        """ Test missing report in harmonization """
        result = upgrades.harmonization({}, {}, MISSING_REPORT, False)
        self.assertTrue(result[0])
        self.assertEqual(HARM, result[3])

    def test_wrong_type_harmonization(self):
        """ Test wrong type in harmonization """
        result = upgrades.harmonization({}, {}, WRONG_TYPE, False)
        self.assertTrue(result[0])
        self.assertEqual(HARM, result[3])


for name in upgrades.__all__:
    setattr(TestUpgradeLib, 'test_function_%s' % name,
            generate_function(getattr(upgrades, name)))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
