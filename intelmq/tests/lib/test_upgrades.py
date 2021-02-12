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
V213 = {"mail-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.mail.collector_mail_attach",
    "parameters": {
        "attach_unzip": True,
    }
},
    "mail-collector2": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.mail.collector_mail_attach",
    "parameters": {
        "attach_unzip": False,
        "extract_files": True,
    }
}
}
V213_EXP = {"mail-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.mail.collector_mail_attach",
    "parameters": {
        "extract_files": True,
    }
},
    "mail-collector2": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.mail.collector_mail_attach",
    "parameters": {
        "extract_files": True,
    },
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
WRONG_REGEX = deepcopy(HARM)
WRONG_REGEX['event']['protocol.transport']['iregex'] = 'foobar'
V213_FEED = {"zeus-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "https://zeustracker.abuse.ch/blocklist.php?download=badips",
    }
},
"bitcash-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "https://bitcash.cz/misc/log/blacklist",
    }
},
"ddos-attack-c2-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http_stream",
    "parameters": {
        "http_url": "https://feed.caad.fkie.fraunhofer.de/ddosattackfeed/",
    }
},
"ddos-attack-targets-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http_stream",
    "parameters": {
        "http_url": "https://feed.caad.fkie.fraunhofer.de/ddosattackfeed/",
    }
},
"taichung-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "https://www.tc.edu.tw/net/netflow/lkout/recent/30",
    },
},
"ransomware-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "https://ransomwaretracker.abuse.ch/feeds/csv/",
    },
},
"bambenek-dga-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "https://osint.bambenekconsulting.com/feeds/dga-feed.txt",
    },
},
"bambenek-c2dommasterlist-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt",
    },
},
"nothink-dns-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "http://www.nothink.org/honeypot_dns_attacks.txt",
    },
},
"nothink-ssh-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "http://www.nothink.org/blacklist/blacklist_ssh_day.txt",
    },
},
"nothink-parser": {
    "group": "Parser",
    "module": "intelmq.bots.parsers.nothink.parser",
},
}
V220_FEED = {
"urlvir-hosts-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "http://www.urlvir.com/export-hosts/",
    },
},
"urlvir-parser": {
    "group": "Parser",
    "module": "intelmq.bots.parsers.urlvir.parser",
},
}
V221_FEED = {
"abusech-urlhaus-columns-string-parser": {
    "parameters": {
        "column_regex_search": {},
        "columns": "time.source,source.url,status,extra.urlhaus.threat_type,source.fqdn,source.ip,source.asn,source.geolocation.cc",
        "default_url_protocol": "http://",
        "delimiter": ",",
        "filter_text": None,
        "filter_type": None,
        "skip_header": False,
        "time_format": None,
        "type": "c2server",
        "type_translation": {
            "malware_download": "malware-distribution"
        }
    },
    "module": "intelmq.bots.parsers.generic.parser_csv",
},
"abusech-urlhaus-columns-dict-parser": {
    "parameters": {
        "column_regex_search": {},
        "columns": ["time.source", "source.url","status","extra.urlhaus.threat_type","source.fqdn","source.ip","source.asn","source.geolocation.cc"],
        "default_url_protocol": "http://",
        "delimiter": ",",
        "filter_text": None,
        "filter_type": None,
        "skip_header": False,
        "time_format": None,
        "type": "c2server",
        "type_translation": {
            "malware_download": "malware-distribution"
        }
    },
    "module": "intelmq.bots.parsers.generic.parser_csv",
}
}
V221_FEED_OUT = {
"abusech-urlhaus-columns-string-parser": {
    "parameters": {
        "column_regex_search": {},
        "columns": ['time.source', 'source.url', 'status', 'classification.type|__IGNORE__', 'source.fqdn|__IGNORE__', 'source.ip', 'source.asn', 'source.geolocation.cc'],
        "default_url_protocol": "http://",
        "delimiter": ",",
        "filter_text": None,
        "filter_type": None,
        "skip_header": False,
        "time_format": None,
        "type": "c2server",
        "type_translation": {
            "malware_download": "malware-distribution"
        }
    },
    "module": "intelmq.bots.parsers.generic.parser_csv",
}
}
V221_FEED_OUT['abusech-urlhaus-columns-dict-parser'] = V221_FEED_OUT['abusech-urlhaus-columns-string-parser']
V221_FEED_2 = {
"hphosts-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "http://hosts-file.net/download/hosts.txt",
    },
},
"hphosts-parser": {
    "group": "Parser",
    "module": "intelmq.bots.parsers.hphosts.parser",
},
}
V222 = {
"shadowserver-parser": {
    "module": "intelmq.bots.parsers.shadowserver.parser",
    "parameters": {
        "feedname": "Blacklisted-IP"}}}
V222_OUT = {
"shadowserver-parser": {
    "module": "intelmq.bots.parsers.shadowserver.parser",
    "parameters": {
        "feedname": "Blocklist"}}}

V230_IN = {
"urlhaus-parser": {
    "module": "intelmq.bots.parsers.generic.parser_csv",
    "parameters": {
        "delimeter": ","
    }
}
}
V230_IN_BOTH = {
"urlhaus-parser": {
    "module": "intelmq.bots.parsers.generic.parser_csv",
    "parameters": {
        "delimeter": ",",
        "delimiter": ","
    }
}
}
V230_OUT = {
"urlhaus-parser": {
    "module": "intelmq.bots.parsers.generic.parser_csv",
    "parameters": {
        "delimiter": ","
    }
}
}


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
        result = upgrades.v220_configuration(DEFAULTS_HTTP_VERIFY_TRUE,
                                               V220_MISP_VERIFY_TRUE, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V220_MISP_VERIFY_NULL, result[2])
        result = upgrades.v220_configuration(DEFAULTS_HTTP_VERIFY_TRUE,
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

    def test_wrong_regex_harmonization(self):
        """ Test wrong regex in harmonization """
        result = upgrades.harmonization({}, {}, WRONG_REGEX, False)
        self.assertTrue(result[0])
        self.assertEqual(HARM, result[3])

    def test_v213_deprecations(self):
        """ Test v213_fixes """
        result = upgrades.v213_deprecations({}, V213, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V213_EXP, result[2])

    def test_v213_feed_changes(self):
        """ Test v213_feed_changes """
        result = upgrades.v213_feed_changes({}, V213_FEED, {}, False)
        self.assertEqual('A discontinued feed "Zeus Tracker" has been found '
                         'as bot zeus-collector. '
                         'The discontinued feed "Bitcash.cz" has been found '
                         'as bot bitcash-collector. '
                         'The discontinued feed "Fraunhofer DDos Attack" has '
                         'been found as bot ddos-attack-c2-collector, '
                         'ddos-attack-targets-collector. '
                         'The discontinued feed "Abuse.ch Ransomware Tracker" '
                         'has been found as bot ransomware-collector. '
                         'Many Bambenek feeds now require a license, see '
                         'https://osint.bambenekconsulting.com/feeds/ '
                         'potentially affected bots are '
                         'bambenek-c2dommasterlist-collector. '
                         'All Nothink Honeypot feeds are discontinued, '
                         'potentially affected bots are nothink-dns-collector, '
                         'nothink-ssh-collector. '
                         'The Nothink Parser has been removed, '
                         'affected bots are nothink-parser. '
                         'Remove affected bots yourself.',
                         result[0])
        self.assertEqual(V213_FEED, result[2])

    def test_v220_feed_changes(self):
        """ Test v213_feed_changes """
        result = upgrades.v220_feed_changes({}, V220_FEED, {}, False)
        self.assertEqual('A discontinued feed "URLVir" has been found '
                         'as bot urlvir-hosts-collector. '
                         'The removed parser "URLVir" has been found '
                         'as bot urlvir-parser. '
                         'Remove affected bots yourself.',
                         result[0])
        self.assertEqual(V220_FEED, result[2])

    def test_v221_feed_changes(self):
        """ Test v221_feeds_1 """
        result = upgrades.v221_feed_changes({}, V221_FEED, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V221_FEED_OUT, result[2])

    def test_v221_feed_changes_2(self):
        """ Test v213_feed_changes """
        result = upgrades.v221_feed_changes({}, V221_FEED_2, {}, False)
        self.assertEqual('A discontinued feed "HP Hosts File" has been found '
                         'as bot hphosts-collector. '
                         'The removed parser "HP Hosts" has been found '
                         'as bot hphosts-parser. '
                         'Remove affected bots yourself.',
                         result[0])
        self.assertEqual(V221_FEED_2, result[2])

    def test_v222_feed_changes(self):
        """ Test v222_feed_changes """
        result = upgrades.v222_feed_changes({}, V222, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V222_OUT, result[2])

    def v230_csv_parser_parameter_fix_1(self):
        """ Test v230_feed_fix """
        result = upgrades.v230_feed_fix({}, V230_IN, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V230_OUT, result[2])

        # with also the new fixed parameter
        result = upgrades.v230_feed_fix({}, V230_IN_BOTH, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V230_OUT, result[2])

        # with new parameter, no change
        result = upgrades.v230_feed_fix({}, V230_OUT, {}, False)
        self.assertIsNone(result[0])
        self.assertEqual(V230_OUT, result[2])


for name in upgrades.__all__:
    setattr(TestUpgradeLib, 'test_function_%s' % name,
            generate_function(getattr(upgrades, name)))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
