# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
from copy import deepcopy
import unittest
import pkg_resources
from intelmq.lib.upgrade.harmonization import harmonization
from intelmq.lib.upgrade.v210 import deprecations
from intelmq.lib.utils import load_configuration


V210 = {"global": {},
        "test-collector": {
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
V210_EXP = {"global": {},
            "test-collector": {
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

HARM = load_configuration(pkg_resources.resource_filename('intelmq',
                                                          'etc/harmonization.conf'))
V210_HARM = deepcopy(HARM)
del V210_HARM['report']['extra']


class TestUpgradeV210(unittest.TestCase):
    def test_deprecations(self):
        """ Test deprecations """
        result = deprecations(V210, {}, True)
        self.assertTrue(result[0])
        self.assertEqual(V210_EXP, result[1])

    def test_harmonization(self):
        """ Test harmonization: Addition of extra to report """
        result = harmonization({}, V210_HARM, False)
        self.assertTrue(result[0])
        self.assertEqual(HARM, result[2])
