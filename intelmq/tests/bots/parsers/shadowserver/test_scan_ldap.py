# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_ldap.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open LDAP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ldap-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open LDAP',
           "classification.identifier": "open-ldap",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.configuration_naming_context": "CN=Configuration,DC=rodwil,DC=com",
           "extra.current_time": "20190904054426.0Z",
           "extra.default_naming_context": "DC=rodwil,DC=com",
           "extra.domain_controller_functionality": 6,
           "extra.domain_functionality": 6,
           "extra.ds_service_name": "CN=Configuration,DC=rodwil,DC=com",
           "extra.forest_functionality": 6,
           "extra.highest_committed_usn": 62794,
           "extra.is_global_catalog_ready": True,
           "extra.is_synchronized": True,
           "extra.ldap_service_name": "rodwil.com:servidor$@RODWIL.COM",
           "extra.naics": 517311,
           "extra.naming_contexts": "DC=rodwil,DC=com|CN=Configuration,DC=rodwil,DC=com|CN=Schema,CN=Configuration,DC=rodwil,DC=com|DC=DomainDnsZones,DC=rodwil,DC=com|DC=ForestDnsZones,DC=rodwil,DC=com",
           "extra.root_domain_naming_context": "DC=rodwil,DC=com",
           "extra.schema_naming_context": "CN=Schema,CN=Configuration,DC=rodwil,DC=com",
           "extra.server_name": "CN=SERVIDOR,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=rodwil,DC=com",
           "extra.size": 2874,
           "extra.subschema_subentry": "CN=Aggregate,CN=Schema,CN=Configuration,DC=rodwil,DC=com",
           "extra.supported_capabilities": "1.2.840.113556.1.4.800|1.2.840.113556.1.4.1670|1.2.840.113556.1.4.1791|1.2.840.113556.1.4.1935|1.2.840.113556.1.4.2080|1.2.840.113556.1.4.2237",
           "extra.supported_control": "1.2.840.113556.1.4.319|1.2.840.113556.1.4.801|1.2.840.113556.1.4.473|1.2.840.113556.1.4.528|1.2.840.113556.1.4.417|1.2.840.113556.1.4.619|1.2.840.113556.1.4.841|1.2.840.113556.1.4.529|1.2.840.113556.1.4.805|1.2.840.113556.1.4.521|1.2.840.113556.1.4.970|1.2.840.113556.1.4.1338|1.2.840.113556.1.4.474|1.2.840.113556.1.4.1339|1.2.840.113556.1.4.1340|1.2.840.113556.1.4.1413|2.16.840.1.113730.3.4.9|2.16.840.1.113730.3.4.10|1.2.840.113556.1.4.1504|1.2.840.113556.1.4.1852|1.2.840.113556.1.4.802|1.2.840.113556.1.4.1907|1.2.840.113556.1.4.1948|1.2.840.113556.1.4.1974|1.2.840.113556.1.4.1341|1.2.840.113556.1.4.2026|1.2.840.113556.1.4.2064|1.2.840.113556.1.4.2065|1.2.840.113556.1.4.2066|1.2.840.113556.1.4.2090|1.2.840.113556.1.4.2205|1.2.840.113556.1.4.2204|1.2.840.113556.1.4.2206|1.2.840.113556.1.4.2211|1.2.840.113556.1.4.2239|1.2.840.113556.1.4.2255|1.2.840.113556.1.4.2256",
           "extra.supported_ldap_policies": "MaxPoolThreads|MaxPercentDirSyncRequests|MaxDatagramRecv|MaxReceiveBuffer|InitRecvTimeout|MaxConnections|MaxConnIdleTime|MaxPageSize|MaxBatchReturnMessages|MaxQueryDuration|MaxTempTableSize|MaxResultSetSize|MinResultSets|MaxResultSetsPerConn|MaxNotificationPerConn|MaxValRange|MaxValRangeTransitive|ThreadMemoryLimit|SystemMemoryLimitPercent",
           "extra.supported_ldap_version": "3|2",
           "extra.supported_sasl_mechanisms": "GSSAPI|GSS-SPNEGO|EXTERNAL|DIGEST-MD5",
           "extra.tag": "ldap-udp",
           "protocol.application": "ldap",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 6057,
           "source.geolocation.cc": "UY",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.11.140.210",
           "source.local_hostname": "Servidor.rodwil.com",
           "source.port": 389,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T05:40:55+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open LDAP',
           "classification.identifier": "open-ldap",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.configuration_naming_context": "CN=Configuration,DC=TAC02",
           "extra.current_time": "20190904083835.0Z",
           "extra.default_naming_context": "DC=TAC02",
           "extra.domain_controller_functionality": 3,
           "extra.domain_functionality": 0,
           "extra.ds_service_name": "CN=Configuration,DC=TAC02",
           "extra.forest_functionality": 0,
           "extra.highest_committed_usn": 5051843,
           "extra.is_global_catalog_ready": True,
           "extra.is_synchronized": True,
           "extra.ldap_service_name": "TAC02:win-a8wca1isieb$@TAC02",
           "extra.naics": 517311,
           "extra.naming_contexts": "DC=TAC02|CN=Configuration,DC=TAC02|CN=Schema,CN=Configuration,DC=TAC02|DC=ForestDnsZones,DC=TAC02|DC=DomainDnsZones,DC=TAC02",
           "extra.root_domain_naming_context": "DC=TAC02",
           "extra.schema_naming_context": "CN=Schema,CN=Configuration,DC=TAC02",
           "extra.server_name": "CN=WIN-A8WCA1ISIEB,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=TAC02",
           "extra.size": 2357,
           "extra.subschema_subentry": "CN=Aggregate,CN=Schema,CN=Configuration,DC=TAC02",
           "extra.supported_capabilities": "1.2.840.113556.1.4.800|1.2.840.113556.1.4.1670|1.2.840.113556.1.4.1791|1.2.840.113556.1.4.1935",
           "extra.supported_control": "1.2.840.113556.1.4.319|1.2.840.113556.1.4.801|1.2.840.113556.1.4.473|1.2.840.113556.1.4.528|1.2.840.113556.1.4.417|1.2.840.113556.1.4.619|1.2.840.113556.1.4.841|1.2.840.113556.1.4.529|1.2.840.113556.1.4.805|1.2.840.113556.1.4.521|1.2.840.113556.1.4.970|1.2.840.113556.1.4.1338|1.2.840.113556.1.4.474|1.2.840.113556.1.4.1339|1.2.840.113556.1.4.1340|1.2.840.113556.1.4.1413|2.16.840.1.113730.3.4.9|2.16.840.1.113730.3.4.10|1.2.840.113556.1.4.1504|1.2.840.113556.1.4.1852|1.2.840.113556.1.4.802|1.2.840.113556.1.4.1907|1.2.840.113556.1.4.1948|1.2.840.113556.1.4.1974|1.2.840.113556.1.4.1341|1.2.840.113556.1.4.2026",
           "extra.supported_ldap_policies": "MaxPoolThreads|MaxDatagramRecv|MaxReceiveBuffer|InitRecvTimeout|MaxConnections|MaxConnIdleTime|MaxPageSize|MaxQueryDuration|MaxTempTableSize|MaxResultSetSize|MaxNotificationPerConn|MaxValRange|ThreadMemoryLimit|SystemMemoryLimitPercent",
           "extra.supported_ldap_version": "3|2",
           "extra.supported_sasl_mechanisms": "GSSAPI|GSS-SPNEGO|EXTERNAL|DIGEST-MD5",
           "extra.tag": "ldap-udp",
           "protocol.application": "ldap",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 6057,
           "source.geolocation.cc": "UY",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.11.121.51",
           "source.local_hostname": "WIN-A8WCA1ISIEB.TAC02",
           "source.port": 389,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T08:38:04+00:00"
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
