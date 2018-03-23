# -*- coding: utf-8 -*-
import os.path
import unittest

import intelmq.lib.test as test
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

    def test_dummy(self):
        self.input_message = EXAMPLE_INPUT1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_dummy(self):
        self.input_message = EXAMPLE_INPUT2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
