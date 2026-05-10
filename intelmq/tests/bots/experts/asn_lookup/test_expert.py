# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing asn_lookup with a faked local database
"""

import bz2
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pkg_resources

import intelmq.lib.test as test
from intelmq.bots.experts.asn_lookup import expert as asn_lookup_expert
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


class TestASNLookupDatabaseUpdate(unittest.TestCase):
    def test_update_database_creates_missing_database_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            database_path = Path(tmp_dir) / "asn_lookup" / "ipasn.dat"

            responses = [
                SimpleNamespace(text='href="2026.05/"', status_code=200, url="months"),
                SimpleNamespace(text='href="rib.20260509.0000.bz2"', status_code=200, url="ribs"),
                SimpleNamespace(content=bz2.compress(b"rib"), status_code=200, url="rib"),
            ]
            session = SimpleNamespace(get=mock.Mock(side_effect=responses))

            def dump_prefixes_to_file(prefixes, target_path):
                Path(target_path).write_text("created", encoding="utf-8")

            mocked_pyasn = SimpleNamespace(
                mrtx=SimpleNamespace(
                    parse_mrt_file=mock.Mock(return_value=["prefixes"]),
                    dump_prefixes_to_file=mock.Mock(side_effect=dump_prefixes_to_file),
                )
            )

            with mock.patch.object(asn_lookup_expert, "pyasn", mocked_pyasn), \
                    mock.patch.object(asn_lookup_expert, "get_bots_settings", return_value={
                        "asn-lookup": {
                            "module": "intelmq.bots.experts.asn_lookup.expert",
                            "parameters": {"database": str(database_path)},
                        }
                    }), \
                    mock.patch.object(asn_lookup_expert, "create_request_session", return_value=session), \
                    mock.patch.object(asn_lookup_expert, "IntelMQController") as controller:
                ASNLookupExpertBot.update_database()

            self.assertTrue(database_path.is_file())
            self.assertEqual(database_path.read_text(encoding="utf-8"), "created")
            controller.return_value.bot_reload.assert_called_once_with("asn-lookup")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
