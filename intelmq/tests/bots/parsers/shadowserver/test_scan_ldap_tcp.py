# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_ldap_tcp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open LDAP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ldap_tcp-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open LDAP',
           "classification.identifier": "open-ldap",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.configuration_naming_context": "CN=Configuration,DC=Vida,DC=net",
           "extra.current_time": "20190904080445.0Z",
           "extra.default_naming_context": "DC=Vida,DC=net",
           "extra.ds_service_name": "CN=Configuration,DC=Vida,DC=net",
           "extra.naics": 517311,
           "extra.naming_contexts": "DC=Vida,DC=net|CN=Configuration,DC=Vida,DC=net|CN=Schema,CN=Configuration,DC=Vida,DC=net|DC=DomainDnsZones,DC=Vida,DC=net|DC=ForestDnsZones,DC=Vida,DC=net",
           "extra.root_domain_naming_context": "DC=Vida,DC=net",
           "extra.schema_naming_context": "CN=Schema,CN=Configuration,DC=Vida,DC=net",
           "extra.size": 0,
           "extra.subschema_subentry": "CN=Aggregate,CN=Schema,CN=Configuration,DC=Vida,DC=net",
           "extra.supported_control": "1.2.840.113556.1.4.319|1.2.840.113556.1.4.801|1.2.840.113556.1.4.473|1.2.840.113556.1.4.528|1.2.840.113556.1.4.417|1.2.840.113556.1.4.619|1.2.840.113556.1.4.841|1.2.840.113556.1.4.529|1.2.840.113556.1.4.805|1.2.840.113556.1.4.521|1.2.840.113556.1.4.970|1.2.840.113556.1.4.1338|1.2.840.113556.1.4.474|1.2.840.113556.1.4.1339|1.2.840.113556.1.4.1340|1.2.840.113556.1.4.1413|2.16.840.1.113730.3.4.9|2.16.840.1.113730.3.4.10|1.2.840.113556.1.4.1504|1.2.840.113556.1.4.1852|1.2.840.113556.1.4.802|1.2.840.113556.1.4.1907|1.2.840.113556.1.4.1948|1.2.840.113556.1.4.1974|1.2.840.113556.1.4.1341|1.2.840.113556.1.4.2026|1.2.840.113556.1.4.2064|1.2.840.113556.1.4.20",
           "extra.tag": "ldap-tcp",
           "protocol.application": "ldap",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 6057,
           "source.geolocation.cc": "UY",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.11.149.109",
           "source.port": 389,
           "source.reverse_dns": "hostname2.test",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T08:04:41+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open LDAP',
           "classification.identifier": "open-ldap",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.configuration_naming_context": "CN=Configuration,DC=isa,DC=net,DC=uy",
           "extra.current_time": "20190904082039.0Z",
           "extra.default_naming_context": "DC=isa,DC=net,DC=uy",
           "extra.ds_service_name": "CN=Configuration,DC=isa,DC=net,DC=uy",
           "extra.naics": 517311,
           "extra.naming_contexts": "DC=isa,DC=net,DC=uy|CN=Configuration,DC=isa,DC=net,DC=uy|CN=Schema,CN=Configuration,DC=isa,DC=net,DC=uy|DC=ForestDnsZones,DC=isa,DC=net,DC=uy|DC=DomainDnsZones,DC=isa,DC=net,DC=uy",
           "extra.root_domain_naming_context": "DC=isa,DC=net,DC=uy",
           "extra.schema_naming_context": "CN=Schema,CN=Configuration,DC=isa,DC=net,DC=uy",
           "extra.size": 0,
           "extra.subschema_subentry": "CN=Aggregate,CN=Schema,CN=Configuration,DC=isa,DC=net,DC=uy",
           "extra.supported_control": "1.2.840.113556.1.4.319|1.2.840.113556.1.4.801|1.2.840.113556.1.4.473|1.2.840.113556.1.4.528|1.2.840.113556.1.4.417|1.2.840.113556.1.4.619|1.2.840.113556.1.4.841|1.2.840.113556.1.4.529|1.2.840.113556.1.4.805|1.2.840.113556.1.4.521|1.2.840.113556.1.4.970|1.2.840.113556.1.4.1338|1.2.840.113556.1.4.474|1.2.840.113556.1.4.1339|1.2.840.113556.1.4.1340|1.2.840.113556.1.4.1413|2.16.840.1.113730.3.4.9|2.16.840.1.113730.3.4.10|1.2.840.113556.1.4.1504|1.2.840.113556.1.4.1852|1.2.840.113556.1.4.802|1.2.840.113556.1.4.1907|1.2",
           "extra.tag": "ldap-tcp",
           "protocol.application": "ldap",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 6057,
           "source.geolocation.cc": "UY",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.11.114.203",
           "source.port": 389,
           "source.reverse_dns": "hostname.test",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T08:20:38+00:00"
           },
          ]

class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
