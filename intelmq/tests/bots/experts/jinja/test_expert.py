# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Testing jinja expert
"""

import unittest
import os

import pkg_resources

import intelmq.lib.test as test
from intelmq.bots.experts.jinja.expert import JinjaExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "192.168.0.1",
                 "destination.ip": "192.0.43.8",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "feed.url": "https://cert.at",
                 }
EXAMPLE_OUTPUT1 = {"__type": "Event",
                  "source.ip": "192.168.0.1",
                  "destination.ip": "192.0.43.8",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "feed.url": "HTTPS://CERT.AT",
                  }
EXAMPLE_OUTPUT2 = {"__type": "Event",
                  "source.ip": "192.168.0.1",
                  "destination.ip": "192.0.43.8",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.some_text": "Hello World, this is the destination ip: 192.0.43.8! And this is the source ip: 192.168.0.1!",
                  "feed.url": "https://cert.at",
                  }
EXAMPLE_OUTPUT3 = {"__type": "Event",
                  "source.ip": "192.168.0.1",
                  "destination.ip": "192.0.43.8",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.some_text": '{\n  "@timestamp": 2015-01-01T00:00:00+00:00,\n\n  "server.ip": 192.168.0.1,\n\n\n}',
                  "feed.url": "https://cert.at",
                  }


class TestJinjaExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for JinjaExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = JinjaExpertBot

    def test_jinja1(self):
        self.sysconfig = {'fields': { 'feed.url': "{{ msg['feed.url'] | upper }}" } }
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_jinja2(self):
        self.sysconfig = {'fields': { 'extra.some_text': "Hello World, this is the destination ip: {{ msg['destination.ip'] }}! And this is the source ip: {{ msg['source.ip'] }}!" } }
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

    def test_jinja_file1(self):
        self.sysconfig = {'fields': { 'extra.some_text': "file:///" + os.path.join(os.path.dirname(__file__)) + "/ecs.j2" } }
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT3)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
