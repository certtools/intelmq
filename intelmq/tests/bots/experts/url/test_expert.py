# SPDX-FileCopyrightText: 2023 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.url.expert import URLExpertBot

INPUT = {
    "test_extracting_ip": {
        "__type": "Event",
        "source.url": "http://5.5.5.5/index.html",
        "time.observation": "2015-01-01T00:00:00+00:00"
    },
    "test_extracting_fqdn": {
        "__type": "Event",
        "source.url": "https://admin@www.example.com:8443/index.html",
        "time.observation": "2015-01-01T00:00:00+00:00"
    },
    "test_skip_fields": {
        "__type": "Event",
        "source.url": "http://www.example.com:8000/",
        "time.observation": "2015-01-01T00:00:00+00:00"
    },
    "test_overwrite": {
        "source.url": "https://admin@www.example.com:8443/index.html",
        "time.observation": "2015-01-01T00:00:00+00:00",
        "source.port": 80,
        "source.ip": "5.5.5.5",
        "source.urlpath": "/index.html",
        "protocol.application": "http",
        "protocol.transport": "tcp",
        "__type": "Event"
    },
    "test_source_priority": {
        "__type": "Event",
        "source.url": "http://5.5.5.5/index.html",
        "destination.url": "https://admin@www.example.com:8443/backdoor.html",
        "time.observation": "2015-01-01T00:00:00+00:00"
    }

}

OUTPUT = {
    "test_extracting_ip": {
        "source.url": "http://5.5.5.5/index.html",
        "time.observation": "2015-01-01T00:00:00+00:00",
        "source.port": 80,
        "source.ip": "5.5.5.5",
        "source.urlpath": "/index.html",
        "protocol.application": "http",
        "protocol.transport": "tcp",
        "__type": "Event"
    },
    "test_extracting_fqdn": {
        "source.url": "https://admin@www.example.com:8443/index.html",
        "time.observation": "2015-01-01T00:00:00+00:00",
        "source.fqdn": "www.example.com",
        "source.port": 8443,
        "source.urlpath": "/index.html",
        "source.account": "admin",
        "protocol.application": "http",
        "__type": "Event"
    },
    "test_skip_fields": {
        "__type": "Event",
        "source.url": "http://www.example.com:8000/",
        "time.observation": "2015-01-01T00:00:00+00:00"
    },
    "test_overwrite": {
        "source.url": "https://admin@www.example.com:8443/index.html",
        "time.observation": "2015-01-01T00:00:00+00:00",
        "source.fqdn": "www.example.com",
        "source.ip": "5.5.5.5",
        "source.port": 8443,
        "source.urlpath": "/index.html",
        "source.account": "admin",
        "protocol.application": "http",
        "protocol.transport": "tcp",
        "__type": "Event"
    },
    "test_source_priority": {
        "source.url": "http://5.5.5.5/index.html",
        "destination.url": "https://admin@www.example.com:8443/backdoor.html",
        "time.observation": "2015-01-01T00:00:00+00:00",
        "source.port": 80,
        "source.ip": "5.5.5.5",
        "source.urlpath": "/index.html",
        "protocol.application": "http",
        "protocol.transport": "tcp",
        "__type": "Event",
        'destination.account': 'admin',
        'destination.fqdn': 'www.example.com',
        'destination.port': 8443,
        'destination.urlpath': '/backdoor.html',
    }

}


class TestURLExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for URLExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URLExpertBot

    def test_extracting_ip(self):
        """
        Tests extracting ip, default port, urlpath, transport protocol and application protocol
        """
        self.input_message = INPUT["test_extracting_ip"]
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT["test_extracting_ip"])

    def test_extracting_fqdn(self):
        """
        Tests extracting fqdn, explicit port, account, transport protocol and application protocol
        """
        self.input_message = INPUT["test_extracting_fqdn"]
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT["test_extracting_fqdn"])

    def test_skip_fields(self):
        """
        Tests skip_fields parameter (by skipping everything).
        """
        self.input_message = INPUT["test_skip_fields"]
        self.run_bot(parameters={"skip_fields": ["source.fqdn",
                                                 "source.ip",
                                                 "source.port",
                                                 "source.urlpath",
                                                 "source.account",
                                                 "destination.fqdn",
                                                 "destination.ip",
                                                 "destination.port",
                                                 "destination.urlpath",
                                                 "destination.account",
                                                 "protocol.application",
                                                 "protocol.transport"]})
        self.assertMessageEqual(0, OUTPUT["test_skip_fields"])

    def test_overwrite(self):
        """
        Tests overwrite parameter.
        """
        self.input_message = INPUT["test_overwrite"]
        self.run_bot(parameters={"overwrite": True})
        self.assertMessageEqual(0, OUTPUT["test_overwrite"])

    def test_source_priority(self):
        """
        Tests source.url (over destination.url) priority when extracting transport protocol and application protocol.
        """
        self.input_message = INPUT["test_source_priority"]
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT["test_source_priority"])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
