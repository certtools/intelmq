# -*- coding: utf-8 -*-

"""
Testing certbund_contact
"""

from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.certbund_contact.expert import CERTBundKontaktExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "192.168.42.23",
                 "destination.ip": "192.168.42.47",
                 "time.observation": "2016-02-26T10:11:12+00:00",
                 "feed.name": "test",
                 "raw": "",
                 "classification.type": "other"
                 }

EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "192.168.42.23",
                  "destination.ip": "192.168.42.47",
                  "time.observation": "2016-02-26T10:11:12+00:00",
                  "feed.name": "test",
                  "raw": "",
                  "classification.type": "other",
                  'extra': ('{"certbund": {'
                            '"notify_destination": ['
                            '{"email": "foo@example.com",'
                            ' "format": "CSV", "organisation": "Acme",'
                            ' "template_path": "/usr/local/templates/default",'
                            ' "ttl": 3600}], '
                            '"notify_source": ['
                            '{"email": "foo@example.com",'
                            ' "format": "CSV", "organisation": "Acme",'
                            ' "template_path": "/usr/local/templates/default",'
                            ' "ttl": 3600}]'
                            '}}'),
                  }

class CERTBundKontaktMockDBExpertBot(CERTBundKontaktExpertBot):

    """CERTBundKontaktExpertBot that does not mocks all database accesses"""

    def connect_to_database(self):
        pass

    def lookup_contact(self, class_type, class_identifier, ip, fqdn, asn):
        if ip.startswith("192.168.42."):
            return [dict(email="foo@example.com",
                         organisation="Acme",
                         template_path="/usr/local/templates/default",
                         format="CSV",
                         ttl=3600)]
        return []


class TestCERTBundKontaktMockDBExpertBot(test.BotTestCase, unittest.TestCase):

    """
    A TestCase for CERTBundKontaktExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CERTBundKontaktMockDBExpertBot
        cls.default_input_message = EXAMPLE_INPUT

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == "__main__":
    unittest.main()
