# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing asn_lookup with a faked local database
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
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
    def test_update_database_creates_missing_database_file(self):
        def dump_prefixes_to_file(prefixes, database_path):
            Path(database_path).write_text("fake database", encoding="utf-8")

        class Session:
            def get(self, url):
                if url.endswith("/RIBS/"):
                    return SimpleNamespace(
                        text='<a href="rib.20260713.0000.bz2">rib</a>',
                        status_code=200,
                        url=url,
                    )
                if url.endswith(".bz2"):
                    return SimpleNamespace(text="", content=b"BZh91AY&SY", status_code=200, url=url)
                return SimpleNamespace(
                    text='<a href="2026.07/">2026.07</a><a href="2026.06/">2026.06</a>',
                    status_code=200,
                    url=url,
                )

        pyasn = SimpleNamespace(
            mrtx=SimpleNamespace(
                parse_mrt_file=mock.Mock(return_value=["prefixes"]),
                dump_prefixes_to_file=mock.Mock(side_effect=dump_prefixes_to_file),
            )
        )

        with TemporaryDirectory() as tempdir:
            database_path = Path(tempdir) / "asn_lookup" / "ipasn.dat"
            runtime_config = {
                "asn-lookup-expert": {
                    "module": "intelmq.bots.experts.asn_lookup.expert",
                    "parameters": {"database": str(database_path)},
                }
            }
            controller = mock.Mock()

            with (
                mock.patch(
                    "intelmq.bots.experts.asn_lookup.expert.get_bots_settings",
                    return_value=runtime_config,
                ),
                mock.patch(
                    "intelmq.bots.experts.asn_lookup.expert.create_request_session",
                    return_value=Session(),
                ),
                mock.patch("intelmq.bots.experts.asn_lookup.expert.pyasn", pyasn),
                mock.patch(
                    "intelmq.bots.experts.asn_lookup.expert.IntelMQController",
                    return_value=controller,
                ),
            ):
                ASNLookupExpertBot.update_database()

            self.assertTrue(database_path.is_file())
            pyasn.mrtx.dump_prefixes_to_file.assert_called_once_with(["prefixes"], str(database_path))
            controller.bot_reload.assert_called_once_with("asn-lookup-expert")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
