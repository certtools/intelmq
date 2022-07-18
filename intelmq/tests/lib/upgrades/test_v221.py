# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest

from intelmq.lib.upgrade.v221 import feed_changes


V221_FEED = {"global": {},
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
        "columns": ["time.source", "source.url", "status", "extra.urlhaus.threat_type", "source.fqdn", "source.ip", "source.asn", "source.geolocation.cc"],
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
V221_FEED_OUT = {"global": {},
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
V221_FEED_2 = {"global": {},
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


class TestUpgradeV221(unittest.TestCase):
    def test_feed_changes(self):
        """ Test feeds_1 """
        result = feed_changes(V221_FEED, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V221_FEED_OUT, result[1])

    def test_feed_changes_2(self):
        """ Test feed_changes """
        result = feed_changes(V221_FEED_2, {}, False)
        self.assertEqual('A discontinued feed "HP Hosts File" has been found '
                         'as bot hphosts-collector. '
                         'The removed parser "HP Hosts" has been found '
                         'as bot hphosts-parser. '
                         'Remove affected bots yourself.',
                         result[0])
        self.assertEqual(V221_FEED_2, result[1])
