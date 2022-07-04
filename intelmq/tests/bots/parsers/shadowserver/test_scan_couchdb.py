# SPDX-FileCopyrightText: 2022 Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_couchdb.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible CouchDB Server',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-scan_couchdb-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-couchdb',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.couchdb_message' : 'Welcome',
   'extra.couchdb_version' : '1.6.1',
   'extra.server_version' : 'CouchDB/1.6.1 (Erlang OTP/18)',
   'extra.tag' : 'couchdb',
   'extra.vendor' : 'Ubuntu 16.04',
   'extra.visible_databases' : '_replicator;_users;test;shops;god',
   'feed.name' : 'Accessible CouchDB Server',
   'protocol.application' : 'couchdb',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.port' : 5984,
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-couchdb',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.couchdb_message' : 'Welcome',
   'extra.couchdb_version' : '3.2.1',
   'extra.features' : 'access-ready,partitioned,pluggable-storage-engines,reshard,scheduler',
   'extra.git_sha' : '244d428af',
   'extra.server_version' : 'CouchDB/3.2.1 (Erlang OTP/23)',
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.tag' : 'couchdb',
   'extra.vendor' : 'The Apache Software Foundation',
   'feed.name' : 'Accessible CouchDB Server',
   'protocol.application' : 'couchdb',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.port' : 5984,
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-couchdb',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.couchdb_message' : 'Welcome',
   'extra.couchdb_version' : '3.2.1',
   'extra.features' : 'access-ready,partitioned,pluggable-storage-engines,reshard,scheduler',
   'extra.git_sha' : '244d428af',
   'extra.server_version' : 'CouchDB/3.2.1 (Erlang OTP/20)',
   'extra.source.sector' : 'Retail Trade',
   'extra.tag' : 'couchdb',
   'extra.vendor' : 'The Apache Software Foundation',
   'feed.name' : 'Accessible CouchDB Server',
   'protocol.application' : 'couchdb',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.port' : 5984,
   'source.reverse_dns' : 'node03.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:02+00:00'
}
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
