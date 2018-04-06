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

EXAMPLE_OUTPUT = {
    "__type": "Event",
    "source.ip": "192.168.42.23",
    "destination.ip": "192.168.42.47",
    "time.observation": "2016-02-26T10:11:12+00:00",
    "feed.name": "test",
    "classification.type": "other",
    'extra': ('{"certbund": {"source_contacts": {'
              '"matches": ['
              '{"address": "192.168.42.0/24", "field": "ip",'
              ' "managed": "automatic", "organisations": [0]'
              '}, '
              '{"field": "fqdn", "managed": "manual", "organisations": [1]}'
              '], '
              '"organisations": ['
              '{"annotations": [{"type": "tag", "value": "daily"}],'
              ' "contacts": ['
              '{"email": "someone@example.com", "managed": "automatic"}'
              '],'
              ' "id": 0, "managed": "automatic",'
              ' "name": "Some Organisation", "sector": null'
              '}, '
              '{"annotations": [{"type": "tag", "value": ""}],'
              ' "contacts": ['
              '{"email": "other@example.com", "managed": "manual"}'
              '],'
              ' "id": 1, "managed": "manual", "name": "Another Organisation",'
              ' "sector": "IT"}]}}}'),
    }

class CERTBundKontaktMockDBExpertBot(CERTBundKontaktExpertBot):

    """CERTBundKontaktExpertBot that does not mocks all database accesses"""

    def connect_to_database(self):
        pass

    def lookup_contact(self, ip, fqdn, asn, country_code):
        if ip.startswith("192.168.42."):
            return {"matches": [{"field": "ip", "managed": "automatic",
                                 "address": "192.168.42.0/24",
                                 "organisations": [0]},
                                {"field": "fqdn", "managed": "manual",
                                 "organisations": [1]}],
                    "organisations": [
                        {"id": 0,
                         "name": "Some Organisation",
                         "managed": "automatic",
                         "sector": None,
                         "annotations": [{"type": "tag", "value": "daily"}],
                         "contacts": [{
                             "email": "someone@example.com",
                             "managed": "automatic",
                             }],
                         },
                        {"id": 1,
                         "name": "Another Organisation",
                         "managed": "manual",
                         "sector": "IT",
                         "annotations": [{"type": "tag", "value": ""}],
                         "contacts": [{
                             "email": "other@example.com",
                             "managed": "manual",
                             }],
                         }]
                    }
        return {"matches": [], "organisations": []}


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
