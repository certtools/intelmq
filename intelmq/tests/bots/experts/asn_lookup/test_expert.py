# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing asn_lookup with a faked local database
"""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pkg_resources

import intelmq.lib.test as test
from intelmq.bots.experts.asn_lookup.expert import ASNLookupExpertBot

ASN_DB = pkg_resources.resource_filename('intelmq', 'tests/bots/experts/asn_lookup/ipasn.dat')
EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 "destination.ip": "192.0.43.8",  # iana.org
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "source.asn": 15133,
                  "source.network": "93.184.216.0/24",
                  "destination.ip": "192.0.43.8",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "destination.asn": 40528,
                  "destination.network": "192.0.43.0/24",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:500:88:200::7",  # iana.org
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:500:88:200::7",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "source.asn": 16876,
                   "source.network": "2001:500:88::/48",
                   }

@test.skip_exotic()
class TestASNLookupExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ASNLookupExpertBot
        cls.sysconfig = {'database': ASN_DB}

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)


class TestASNLookupUpdateDatabase(unittest.TestCase):
    """
    update_database() must not reject a database file that doesn't exist yet
    (first-time setup): the file is created by the update itself, only an
    existing-but-unwritable file (or a path that isn't a plain file) should
    be rejected.
    """

    def _run_with_fake_bots(self, database_path):
        settings = {
            'bot-1': {
                'module': 'intelmq.bots.experts.asn_lookup.expert',
                'parameters': {'database': str(database_path)},
            }
        }
        with mock.patch(
            'intelmq.bots.experts.asn_lookup.expert.get_bots_settings',
            return_value=settings,
        ):
            with mock.patch(
                'intelmq.bots.experts.asn_lookup.expert.pyasn',
                new=mock.Mock(),
            ):
                with mock.patch(
                    'intelmq.bots.experts.asn_lookup.expert.create_request_session',
                    side_effect=RuntimeError('reached the network step'),
                ):
                    with self.assertRaises((RuntimeError, SystemExit)) as ctx:
                        ASNLookupExpertBot.update_database(verbose=False)
        return ctx.exception

    def test_missing_database_file_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / 'does-not-exist-yet' / 'ipasn.dat'
            exc = self._run_with_fake_bots(database_path)
        # Got past the file check and reached the (mocked) network step,
        # instead of raising ValueError('Database file does not exist...').
        self.assertIsInstance(exc, RuntimeError)

    def test_existing_unwritable_database_file_still_rejected(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / 'ipasn.dat'
            database_path.touch()
            database_path.chmod(0o400)
            try:
                with self.assertRaises(ValueError) as ctx:
                    self._run_with_fake_bots(database_path)
                self.assertIn('not writeable', str(ctx.exception))
            finally:
                database_path.chmod(0o600)

    def test_existing_directory_as_database_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / 'ipasn.dat'
            database_path.mkdir()
            with self.assertRaises(ValueError) as ctx:
                self._run_with_fake_bots(database_path)
            self.assertIn('not a file', str(ctx.exception))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
