# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import psycopg2
import unittest

from intelmq import RUNTIME_CONF_FILE
import intelmq.lib.harmonization as harmonization
import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.experts.squelcher.expert import SquelcherExpertBot


INSERT_QUERY = '''
INSERT INTO {table}(
    "classification.identifier", "classification.type", notify, "source.asn",
    "source.ip", "time.source"
) VALUES (%s, %s, %s, %s, %s, LOCALTIMESTAMP + INTERVAL %s second);
'''
INPUT1 = {"__type": "Event",
          "classification.identifier": "zeus",
          "classification.type": "botnet drone",
          "notify": False,
          "source.asn": 0,
          "source.ip": "192.0.2.1",
          "time.observation": harmonization.DateTime.generate_datetime_now(),
          "feed.name": "Example Feed",
          "raw": "",
          }

INPUT2 = INPUT1.copy()
INPUT2["classification.identifier"] = "https"
INPUT2["classification.type"] = "vulnerable service"
OUTPUT2 = INPUT2.copy()
OUTPUT2["notify"] = True

INPUT3 = INPUT1.copy()
INPUT3["classification.identifier"] = "https"
INPUT3["classification.type"] = "vulnerable service"
INPUT3["source.ip"] = "192.0.2.4"
OUTPUT3 = INPUT3.copy()
OUTPUT3["notify"] = True

INPUT4 = INPUT3.copy()
INPUT4["classification.identifier"] = "openresolver"
INPUT4["notify"] = True

INPUT5 = INPUT4.copy()
INPUT5["source.ip"] = "198.51.100.5"
OUTPUT5 = INPUT5.copy()
OUTPUT5["notify"] = False

INPUT6 = INPUT4.copy()
INPUT6["source.ip"] = "198.51.100.45"
OUTPUT6 = INPUT6.copy()
OUTPUT6["notify"] = False

INPUT7 = INPUT1.copy()
INPUT7['notify'] = True
INPUT7['source.fqdn'] = 'example.com'
del INPUT7['source.ip']
OUTPUT7 = INPUT7.copy()

INPUT8 = INPUT1.copy()
del INPUT8['notify']
del INPUT8['source.asn']
OUTPUT8 = INPUT8.copy()
OUTPUT8['notify'] = False


class TestSquelcherExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for SquelcherExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SquelcherExpertBot
        cls.default_input_message = INPUT1
        try:
            cls.sysconfig = (utils.load_configuration(RUNTIME_CONF_FILE)
                             ['Expert']['Squelcher'])
        except:
            cls.sysconfig = {"configuration_path": "/opt/intelmq/etc/"
                                                   "squelcher.conf",
                             "host": "localhost",
                             "port": 5432,
                             "database": "intelmq",
                             "user": "intelmq",
                             "password": None,
                             "sslmode": "require",
                             "table": "tests",
                             }
        cls.con = psycopg2.connect(database=cls.sysconfig['database'],
                                   user=cls.sysconfig['user'],
                                   password=cls.sysconfig['password'],
                                   host=cls.sysconfig['host'],
                                   port=cls.sysconfig['port'],
                                   sslmode=cls.sysconfig['sslmode'],
                                   )
        cls.con.autocommit = True
        cls.cur = cls.con.cursor()
        cls.cur.execute("TRUNCATE TABLE {}".format(cls.sysconfig['table']))
        global INSERT_QUERY
        INSERT_QUERY = INSERT_QUERY.format(table=cls.sysconfig['table'])

    def test_ttl_1(self):
        query_data = ('zeus', 'botnet drone', True, 0, '192.0.2.1', '0')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT1
        self.run_bot()
        self.assertMessageEqual(0, INPUT1)

    def test_ttl_2(self):
        query_data = ('https', 'vulnerable service', True, 0, '192.0.2.1',
                      '- 01:45')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT2
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT2)

    def test_ttl_2h_notify(self):
        query_data = ('https', 'vulnerable service', True, 0, '192.0.2.4',
                      '- 02:45')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT3
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT3)

    def test_ttl_2h_squelch(self):
        query_data = ('https', 'vulnerable service', True, 0, '192.0.2.4',
                      '- 01:45')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT3
        self.run_bot()
        self.assertMessageEqual(0, INPUT3)

    def test_network_match(self):
        query_data = ('openresolver', 'vulnerable service', False, 0,
                      '198.51.100.5', '- 20:00')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT5
        self.run_bot()
        self.assertMessageEqual(0, INPUT5)

    def test_network_match2(self):
        query_data = ('openresolver', 'vulnerable service', False, 0,
                      '198.51.100.5', '- 25:00')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT5
        self.run_bot()
        self.assertMessageEqual(0, INPUT5)

    def test_network_match3(self):
        query_data = ('openresolver', 'vulnerable service', True, 0,
                      '198.51.100.5', '- 25:00')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT5
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT5)

    def test_address_match1(self):
        query_data = ('openresolver', 'vulnerable service', True, 0,
                      '198.51.100.45', '- 25:00')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT6
        self.run_bot()
        self.assertMessageEqual(0, INPUT6)

    def test_address_match2(self):
        query_data = ('openresolver', 'vulnerable service', True, 0,
                      '198.51.100.45', '- 20:00')
        self.cur.execute(INSERT_QUERY, query_data)
        self.input_message = INPUT6
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT6)

    def test_ttl_other_ident(self):
        self.input_message = INPUT4
        self.run_bot()
        self.assertMessageEqual(0, INPUT4)

    def test_domain(self):
        self.input_message = INPUT7
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT7)

    def test_missing_asn(self):
        self.input_message = INPUT8
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT8)

    @classmethod
    def tearDownClass(cls):
        cls.cur.execute("TRUNCATE TABLE {}".format(cls.sysconfig['table']))
        cls.cur.close()
        cls.con.close()


if __name__ == '__main__':
    unittest.main()
