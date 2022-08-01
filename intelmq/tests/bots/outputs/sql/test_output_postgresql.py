# SPDX-FileCopyrightText: 2019 Sebastian Wagner, 2022 Intevation GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import json
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.sql.output import SQLOutputBot

if os.environ.get('INTELMQ_TEST_DATABASES'):
    import psycopg2
    import psycopg2.extras


INPUT1 = {"__type": "Event",
          "classification.identifier": "zeus",
          "classification.type": "infected-system",
          "source.asn": 64496,
          "source.ip": "192.0.2.1",
          "feed.name": "Example Feed",
          }
OUTPUT1 = INPUT1.copy()
del OUTPUT1['__type']
INPUT_EXTRA = {"__type": "Event",
               "classification.type": "vulnerable-system",
               "extra.asn": 64496,
               "extra.ip": "192.0.2.1",
               }
INPUT_NULL = {"__type": "Event",
              "classification.type": "undetermined",
              "extra.payload": '{"text": "M41\u0012)3U>\bxӾ6\u0000\u0013M6M6M4M4]4y]4ӭ4"}',
              }


@test.skip_database()
class TestSQLOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SQLOutputBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"engine": "postgresql",
                         "host": "localhost",
                         "port": 5432,
                         "database": "intelmq",
                         "user": "intelmq",
                         "password": "intelmq",
                         "sslmode": "allow",
                         "table": "tests"}
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
        cls.cur = cls.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def test_event(self):
        self.run_bot()
        self.cur.execute('SELECT "classification.identifier", "classification.type", "source.asn",'
                         ' "source.ip", "feed.name" FROM tests WHERE "source.asn" = 64496')
        self.assertEqual(self.cur.rowcount, 1)
        from_db = {k: v for k, v in self.cur.fetchone().items() if v is not None}
        self.assertDictEqual(from_db, OUTPUT1)

    def test_extra(self):
        """
        Test if extra.* fields are saved as one column according to jsondict_as_string parameter.
        jsondict_as_string is True by default.
        """
        self.input_message = INPUT_EXTRA
        self.run_bot()
        self.cur.execute('SELECT "extra" FROM tests WHERE "classification.type" = \'vulnerable-system\'')
        self.assertEqual(self.cur.rowcount, 1)
        from_db = {k: v for k, v in self.cur.fetchone().items() if v is not None}
        self.assertEqual(from_db['extra'], {"asn": 64496, "ip": "192.0.2.1"})

    def test_extra_nullbyte(self):
        """
        Test a Nullbyte in an extra-field
        https://github.com/certtools/intelmq/issues/2203
        """
        self.input_message = INPUT_NULL
        self.run_bot()
        self.cur.execute('SELECT "extra" FROM tests WHERE "classification.type" = \'undetermined\'')
        self.assertEqual(self.cur.rowcount, 1)
        from_db = {k: v for k, v in self.cur.fetchone().items() if v is not None}
        self.assertEqual(from_db['extra'], {"payload": '{"text": "M41\u0012)3U>\bxӾ6\\u0000\u0013M6M6M4M4]4y]4ӭ4"}'})

    @classmethod
    def tearDownClass(cls):
        if not os.environ.get('INTELMQ_TEST_DATABASES'):
            return
        cls.cur.execute('TRUNCATE "tests"')
        cls.cur.close()
        cls.con.close()


@test.skip_database()
class TestPostgreSQLOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SQLOutputBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"engine": "postgresql",
                         "host": "localhost",
                         "port": 5432,
                         "database": "intelmq",
                         "user": "intelmq",
                         "password": "intelmq",
                         "sslmode": "allow",
                         "table": "tests"}
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
        cls.cur = cls.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def test_event(self):
        self.allowed_warning_count = 1
        self.run_bot()
        self.cur.execute('SELECT "classification.identifier", "classification.type", "source.asn",'
                         ' "source.ip", "feed.name" FROM tests WHERE "source.asn" = 64496')
        self.assertEqual(self.cur.rowcount, 1)
        from_db = {k: v for k, v in self.cur.fetchone().items() if v is not None}
        self.assertDictEqual(from_db, OUTPUT1)

    def test_prepare_null(self):
        """ Test if a null character in extra is correctly removed. https://github.com/certtools/intelmq/issues/2203 """
        values = [json.dumps({"special": "foo\x00bar"})]
        self.prepare_bot(prepare_source_queue=False)
        output = self.bot.prepare_values(values)
        self.assertEqual(output, ['{"special": "foo\\\\u0000bar"}'])

    @classmethod
    def tearDownClass(cls):
        if not os.environ.get('INTELMQ_TEST_DATABASES'):
            return
        cls.cur.execute('TRUNCATE "tests"')
        cls.cur.close()
        cls.con.close()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
