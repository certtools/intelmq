# SPDX-FileCopyrightText: 2023 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.turris.parser import TurrisGreylistParserBot
from intelmq.lib import utils

INPUT = """\
# For the terms of use see https://view.sentinel.turris.cz/greylist-data/LICENSE.txt
Address,Tags
159.203.8.168,http
103.155.105.100,"ftp,http"
117.247.161.208,telnet
103.185.234.2,telnet
152.32.236.101,"ftp,http,port_scan,smtp,telnet"
61.219.175.42,telnet
"""

OUTPUT = [
    {
        "protocol.transport": "tcp",
        "protocol.application": "http",
        "classification.type": "brute-force",
        "destination.port": 80,
        "raw": "QWRkcmVzcyxUYWdzCjE1OS4yMDMuOC4xNjgsaHR0cA==",
        "source.ip": "159.203.8.168",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "ftp",
        "classification.type": "brute-force",
        "destination.port": 21,
        "raw": "QWRkcmVzcyxUYWdzCjEwMy4xNTUuMTA1LjEwMCwiZnRwLGh0dHAi",
        "source.ip": "103.155.105.100",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "http",
        "classification.type": "brute-force",
        "destination.port": 80,
        "raw": "QWRkcmVzcyxUYWdzCjEwMy4xNTUuMTA1LjEwMCwiZnRwLGh0dHAi",
        "source.ip": "103.155.105.100",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "telnet",
        "classification.type": "brute-force",
        "destination.port": 23,
        "raw": "QWRkcmVzcyxUYWdzCjExNy4yNDcuMTYxLjIwOCx0ZWxuZXQ=",
        "source.ip": "117.247.161.208",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "telnet",
        "classification.type": "brute-force",
        "destination.port": 23,
        "raw": "QWRkcmVzcyxUYWdzCjEwMy4xODUuMjM0LjIsdGVsbmV0",
        "source.ip": "103.185.234.2",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "ftp",
        "classification.type": "brute-force",
        "destination.port": 21,
        "raw": "QWRkcmVzcyxUYWdzCjE1Mi4zMi4yMzYuMTAxLCJmdHAsaHR0cCxwb3J0X3NjYW4sc210cCx0ZWxuZXQi",
        "source.ip": "152.32.236.101",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "http",
        "classification.type": "brute-force",
        "destination.port": 80,
        "raw": "QWRkcmVzcyxUYWdzCjE1Mi4zMi4yMzYuMTAxLCJmdHAsaHR0cCxwb3J0X3NjYW4sc210cCx0ZWxuZXQi",
        "source.ip": "152.32.236.101",
        "__type": "Event"
    },
    {
        "classification.type": "scanner",
        "raw": "QWRkcmVzcyxUYWdzCjE1Mi4zMi4yMzYuMTAxLCJmdHAsaHR0cCxwb3J0X3NjYW4sc210cCx0ZWxuZXQi",
        "source.ip": "152.32.236.101",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "smtp",
        "classification.type": "brute-force",
        "raw": "QWRkcmVzcyxUYWdzCjE1Mi4zMi4yMzYuMTAxLCJmdHAsaHR0cCxwb3J0X3NjYW4sc210cCx0ZWxuZXQi",
        "source.ip": "152.32.236.101",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "telnet",
        "classification.type": "brute-force",
        "destination.port": 23,
        "raw": "QWRkcmVzcyxUYWdzCjE1Mi4zMi4yMzYuMTAxLCJmdHAsaHR0cCxwb3J0X3NjYW4sc210cCx0ZWxuZXQi",
        "source.ip": "152.32.236.101",
        "__type": "Event"
    },
    {
        "protocol.transport": "tcp",
        "protocol.application": "telnet",
        "classification.type": "brute-force",
        "destination.port": 23,
        "raw": "QWRkcmVzcyxUYWdzCjYxLjIxOS4xNzUuNDIsdGVsbmV0",
        "source.ip": "61.219.175.42",
        "__type": "Event"
    }
]


class TestTurrisGreylistParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TurrisGreylistParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TurrisGreylistParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': utils.base64_encode(INPUT)}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT[0])
        self.assertMessageEqual(1, OUTPUT[1])
        self.assertMessageEqual(2, OUTPUT[2])
        self.assertMessageEqual(3, OUTPUT[3])
        self.assertMessageEqual(4, OUTPUT[4])
        self.assertMessageEqual(5, OUTPUT[5])
        self.assertMessageEqual(6, OUTPUT[6])
        self.assertMessageEqual(7, OUTPUT[7])
        self.assertMessageEqual(8, OUTPUT[8])
        self.assertMessageEqual(9, OUTPUT[9])
        self.assertMessageEqual(10, OUTPUT[10])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
