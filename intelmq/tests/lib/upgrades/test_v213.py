# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest

from intelmq.lib.upgrade.v213 import deprecations, feed_changes


V213 = {"global": {},
        "mail-collector": {
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
V213_EXP = {"global": {},
            "mail-collector": {
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

V213_FEED = {"global": {},
             "zeus-collector": {
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


class TestUpgradeV213(unittest.TestCase):
    def test_deprecations(self):
        """ Test fixes """
        result = deprecations(V213, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V213_EXP, result[1])

    def test_feed_changes(self):
        """ Test feed_changes """
        result = feed_changes(V213_FEED, {}, False)
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
        self.assertEqual(V213_FEED, result[1])
