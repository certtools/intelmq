# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os.path
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import intelmq.lib.test as test
from intelmq.bots.experts.domain_suffix import expert as domain_suffix_expert
from intelmq.bots.experts.domain_suffix.expert import DomainSuffixExpertBot


EXAMPLE_INPUT1 = {"__type": "Event",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "source.fqdn": "sub.example.com",
                  "destination.fqdn": "sub.example.net",
                  }
EXAMPLE_OUTPUT1 = {"__type": "Event",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "source.fqdn": "sub.example.com",
                   "source.domain_suffix": "example.com",
                   "destination.fqdn": "sub.example.net",
                   "destination.domain_suffix": "sub.example.net",
                   }
EXAMPLE_INPUT2 = {"__type": "Event",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "source.fqdn": "www.example.org",
                  "destination.fqdn": "www.example.net",
                  }
EXAMPLE_OUTPUT2 = {"__type": "Event",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "source.fqdn": "www.example.org",
                   "source.domain_suffix": "org",
                   "destination.fqdn": "www.example.net",
                   "destination.domain_suffix": "example.net",
                   }
IDN_INPUT = {"__type": "Event",
             "time.observation": "2015-01-01T00:00:00+00:00",
             "source.fqdn": "xn--85x722f.com.cn",
             "destination.fqdn": "xn--85x722f.xn--fiqs8s",
             }
IDN_OUTPUT = {"__type": "Event",
              "time.observation": "2015-01-01T00:00:00+00:00",
              "source.fqdn": "xn--85x722f.com.cn",
              "source.domain_suffix": "com.cn",
              "destination.fqdn": "xn--85x722f.xn--fiqs8s",
              "destination.domain_suffix": "xn--fiqs8s",
              }
WILDCARD_INPUT = {"__type": "Event",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "source.fqdn": "example.mm",
                  "destination.fqdn": "example.example.mm",
                  }
WILDCARD_OUTPUT = {"__type": "Event",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "source.fqdn": "example.mm",
                   "source.domain_suffix": "example.mm",
                   "destination.fqdn": "example.example.mm",
                   "destination.domain_suffix": "example.mm",
                   }


class TestDomainSuffixExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DomainSuffixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DomainSuffixExpertBot
        cls.sysconfig = {'suffix_file': os.path.join(os.path.dirname(__file__), 'public_suffix_list.dat'),
                         'field': 'fqdn',
                         }

    def test_event(self):
        self.input_message = EXAMPLE_INPUT1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_event2(self):
        self.input_message = EXAMPLE_INPUT2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

    def test_idn(self):
        self.input_message = IDN_INPUT
        self.run_bot()
        self.assertMessageEqual(0, IDN_OUTPUT)

    def test_wildcard(self):
        self.input_message = WILDCARD_INPUT
        self.run_bot()
        self.assertMessageEqual(0, WILDCARD_OUTPUT)


class TestDomainSuffixDatabaseUpdate(unittest.TestCase):
    def test_update_database_uses_default_suffix_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            suffix_file = Path(tmp_dir) / "domain_suffix" / "public_suffix_list.dat"
            session = SimpleNamespace(get=mock.Mock(return_value=SimpleNamespace(
                content=b"// public suffix list\ncom\n",
                ok=True,
                status_code=200,
                url="https://publicsuffix.org/list/public_suffix_list.dat",
            )))

            with mock.patch.object(DomainSuffixExpertBot, "suffix_file", str(suffix_file)), \
                    mock.patch.object(domain_suffix_expert, "get_bots_settings", return_value={
                        "domain-suffix": {
                            "module": "intelmq.bots.experts.domain_suffix.expert",
                            "parameters": {},
                        }
                    }), \
                    mock.patch.object(domain_suffix_expert, "create_request_session", return_value=session), \
                    mock.patch.object(domain_suffix_expert, "IntelMQController") as controller:
                DomainSuffixExpertBot.update_database()

            self.assertEqual(suffix_file.read_bytes(), b"// public suffix list\ncom\n")
            controller.return_value.bot_reload.assert_called_once_with("domain-suffix")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
