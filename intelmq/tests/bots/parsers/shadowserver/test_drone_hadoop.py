# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'drone-hadoop.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

with open(os.path.join(os.path.dirname(__file__),
                       'drone-hadoop_RECONSTRUCTED.csv')) as handle:
    RECONSTRUCTED_FILE = handle.read()
RECONSTRUCTED_LINES = RECONSTRUCTED_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Botnet Drone Hadoop",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'US',
           'destination.ip': '74.208.164.166',
           'destination.port': 80,
           'extra': '{"connection_count": 1, "os.name": "Windows", "os.version": "2000 SP4, XP SP1+"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[1], ''])),
           'source.asn': 7543,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'MELBOURNE',
           'source.geolocation.region': 'VICTORIA',
           'source.ip': '210.23.139.130',
           'source.port': 3218,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:05+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 16265,
           'destination.fqdn': '015.maxided.com',
           'destination.geolocation.cc': 'NL',
           'destination.ip': '94.75.228.147',
           'extra': '{"connection_count": 1, "os.name": "WINXP"}',
           'malware.name': 'spyeye',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[2], ''])),
           'source.asn': 9556,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'ADELAIDE',
           'source.geolocation.region': 'SOUTH AUSTRALIA',
           'source.ip': '115.166.54.44',
           'source.reverse_dns': '115-166-54-44.ip.adam.com.au',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:08+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'DE',
           'destination.ip': '87.106.24.200',
           'destination.port': 80,
           'extra': '{"os.name": "Windows", "os.version": "XP SP1+, 2000 SP3 (2)"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[3], ''])),
           'source.asn': 9822,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'PERTH',
           'source.geolocation.region': 'WESTERN AUSTRALIA',
           'source.ip': '116.212.205.74',
           'source.port': 48986,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:10+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'DE',
           'destination.ip': '87.106.24.200',
           'destination.port': 443,
           'extra': '{"connection_count": 1, "os.name": "Windows", "os.version": "2000 SP4, XP SP1+"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[4], ''])),
           'source.asn': 1221,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'DEVONPORT',
           'source.geolocation.region': 'TASMANIA',
           'source.ip': '58.169.82.113',
           'source.port': 2423,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:15+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'US',
           'destination.ip': '74.208.164.166',
           'destination.port': 443,
           'extra': '{"connection_count": 1, "os.name": "Windows", "os.version": "2000 SP4, XP SP1+"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[5], ''])),
           'source.asn': 4804,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'BRISBANE',
           'source.geolocation.region': 'QUEENSLAND',
           'source.ip': '114.78.17.48',
           'source.port': 2769,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:26+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'DE',
           'destination.ip': '87.106.24.200',
           'destination.port': 443,
           'extra': '{"os.name": "Windows", "os.version": "2000 SP4, XP SP1+"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[6], ''])),
           'source.asn': 1221,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'MELBOURNE',
           'source.geolocation.region': 'VICTORIA',
           'source.ip': '124.190.16.11',
           'source.port': 4095,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:28+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'DE',
           'destination.ip': '87.106.24.200',
           'destination.port': 443,
           'extra': '{"connection_count": 1, "os.name": "Windows", "os.version": "XP/2000 (RFC1323+, w+, tstamp+)"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[7], ''])),
           'source.asn': 1221,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'PERTH',
           'source.geolocation.region': 'WESTERN AUSTRALIA',
           'source.ip': '124.182.36.33',
           'source.port': 60837,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:29+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'US',
           'destination.ip': '74.208.164.166',
           'destination.port': 80,
           'extra': '{"connection_count": 1, "os.name": "Windows", "os.version": "XP SP1+, 2000 SP3 (2)"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[8], ''])),
           'source.asn': 9822,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'PERTH',
           'source.geolocation.region': 'WESTERN AUSTRALIA',
           'source.ip': '116.212.205.74',
           'source.port': 23321,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:33+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'US',
           'destination.ip': '74.208.164.166',
           'destination.port': 443,
           'extra': '{"connection_count": 1, "os.name": "Windows", "os.version": "2000 SP4, XP SP1+"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[9], ''])),
           'source.asn': 1221,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'MELBOURNE',
           'source.geolocation.region': 'VICTORIA',
           'source.ip': '124.190.16.11',
           'source.port': 4089,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:36+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'DE',
           'destination.ip': '87.106.24.200',
           'destination.port': 443,
           'extra': '{"connection_count": 1, "os.name": "Windows", "os.version": "2000 SP4, XP SP1+"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[10], ''])),
           'source.asn': 1221,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'SYDNEY',
           'source.geolocation.region': 'NEW SOUTH WALES',
           'source.ip': '165.228.93.207',
           'source.port': 27105,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:37+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Botnet Drone Hadoop',
           'classification.taxonomy': 'Malicious Code',
           'classification.type': 'botnet drone',
           'classification.identifier': 'botnet',
           'destination.asn': 8560,
           'destination.geolocation.cc': 'DE',
           'destination.ip': '87.106.24.200',
           'destination.port': 443,
           'destination.url': 'https://115-166-54-44.ip.adam.com.au/index.php',
           'protocol.application': 'https',
           'extra': '{"connection_count": 1, "os.name": "Windows", "os.version": "2000 SP4, XP SP1+"}',
           'malware.name': 'sinkhole',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[11], ''])),
           'source.asn': 1221,
           'source.geolocation.cc': 'AU',
           'source.geolocation.city': 'SYDNEY',
           'source.geolocation.region': 'NEW SOUTH WALES',
           'source.ip': '165.228.93.207',
           'source.port': 27105,
           'source.reverse_dns': '115-166-54-44.ip.adam.com.au',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2011-04-23T00:00:37+00:00'}]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Botnet-Drone-Hadoop'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


TESTING_OVERWRITE_FEEDNAME = 'My-Botnet-Drone-Hadoop'


class TestOverwriteShadowserverParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT.copy()
        cls.default_input_message['feed.name'] = TESTING_OVERWRITE_FEEDNAME
        cls.sysconfig = {'feedname': 'Botnet-Drone-Hadoop',
                         'overwrite': True}

    def test_bot_name(self):
        "Do **not** test that our second test has the same name as the bot."

    def test_overwrite(self):
        """ Test if overwrite parameter works. """

        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            event = EVENT.copy()
            event['feed.name'] = 'Botnet-Drone-Hadoop'
            self.assertMessageEqual(i, event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
