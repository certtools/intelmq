# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
import psycopg2
from intelmq.bots.experts.generic_db_lookup.expert import \
    GenericDBLookupExpertBot

INPUT1 = {"__type": "Event",
          "classification.identifier": "zeus",
          "classification.type": "botnet drone",
          "source.asn": 64496,
          "source.ip": "192.0.2.1",
          "feed.name": "Example Feed",
          "time.observation": "2016-10-13T12:55:00+02"
          }
OUTPUT1 = INPUT1.copy()
OUTPUT1['source.abuse_contact'] = 'abuse@example.com'
OUTPUT1['comment'] = 'foo'

INPUT2 = INPUT1.copy()
INPUT2['source.asn'] = 42

INPUT3 = INPUT1.copy()
INPUT3['source.asn'] = 64497
OUTPUT3 = INPUT3.copy()
OUTPUT3['comment'] = 'bar'
OUTPUT3['source.abuse_contact'] = 'abuse@example.com'


@test.skip_database()
class TestGenericDBLookupExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for GenericDBLookupExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GenericDBLookupExpertBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"host": "localhost",
                         "port": 5432,
                         "database": "intelmq",
                         "user": "intelmq",
                         "password": "intelmq",
                         "sslmode": "require",
                         "table": "lookuptests",
                         "match_fields": {"source.asn": "asn"},
                         "replace_fields": {"note": "comment",
                                            "contact": "source.abuse_contact",
                                            },
                         }
        if not os.environ.get('INTELMQ_TEST_DATABASES'):
            return
        cls.con = psycopg2.connect(database=cls.sysconfig['database'],
                                   user=cls.sysconfig['user'],
                                   password=cls.sysconfig['password'],
                                   host=cls.sysconfig['host'],
                                   port=cls.sysconfig['port'],
                                   sslmode=cls.sysconfig['sslmode'],
                                   )
        cls.con.autocommit = True
        cls.cur = cls.con.cursor()
        cls.cur.execute('''CREATE TABLE lookuptests
        ("asn" BIGSERIAL UNIQUE PRIMARY KEY,
        "contact" text,
        "note" text,
        "type" text
        ) ''')
        cls.cur.execute('''INSERT INTO lookuptests ("asn", "contact", "note") VALUES
        (64496, 'abuse@example.com', 'foo')
        ''')

    def test_lookup_found(self):
        self.input_message = INPUT1
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)

    def test_lookup_novalue(self):
        self.input_message = INPUT2
        self.run_bot()
        self.assertMessageEqual(0, INPUT2)

    def test_multiple_search(self):
        self.sysconfig['match_fields'] = {"source.asn": "asn",
                                          "classification.type": "type"}
        self.cur.execute('''INSERT INTO lookuptests ("asn", "contact", "note", "type") VALUES
        (64497, 'abuse@example.com', 'bar', 'botnet drone')
        ''')
        self.input_message = INPUT3
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT3)

    @classmethod
    def tearDownClass(cls):
        if not os.environ.get('INTELMQ_TEST_DATABASES'):
            return
        cls.cur.execute('DROP TABLE IF EXISTS "lookuptests"')
        cls.cur.close()
        cls.con.close()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
