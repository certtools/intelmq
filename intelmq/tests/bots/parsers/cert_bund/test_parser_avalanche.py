# -*- coding: utf-8 -*-
import os
import unittest

from intelmq.lib import test, utils
from intelmq.bots.parsers.cert_bund.parser_avalanche import CertBundAvalancheParserBot

# OUTPUT_0 and OUTPUT_1 may seem strange with their different "raw" keys.
# Files recieved from CERT-Bund have Unix line endings (LF);
# the bot uses Windows line endings (CRLF).
# Unless the parsing functions are rewritten to support both,
# this is neccesary to pass the tests. Changes to newlines should not
# affect the data in any way, as they do not carry any information.
#
# See issue GH-1597 for more info


with open(os.path.join(os.path.dirname(__file__), "example.csv")) as handle:
    INPUT_FILE = handle.read()

INPUT_LINES = INPUT_FILE.splitlines()

REPORT = {
    "__type": "Report",
    "feed.name": "CERT-Bund",
    "raw": utils.base64_encode(INPUT_FILE),
}

OUTPUT_0 = {
    "feed.name": "CERT-Bund",
    "source.asn": 64500,
    "source.ip": "192.0.2.1",
    "time.source": "2020-08-11T22:53:53+00:00",
    "classification.type": "malware",
    "malware.name": "andromeda",
    "source.port": 51109,
    "destination.ip": "192.0.2.2",
    "destination.port": 80,
    "destination.fqdn": "example.com",
    "protocol.transport": "tcp",
    "raw": utils.base64_encode("\r\n".join((INPUT_LINES[0], INPUT_LINES[1])) + "\n"),
    "__type": "Event",
}

OUTPUT_1 = {
    "feed.name": "CERT-Bund",
    "source.asn": 64501,
    "source.ip": "192.0.2.1",
    "time.source": "2020-08-11T18:04:47+00:00",
    "classification.type": "malware",
    "malware.name": "tinba",
    "source.port": 49402,
    "destination.ip": "192.0.2.2",
    "destination.port": 80,
    "destination.fqdn": "example.com",
    "protocol.transport": "tcp",
    "raw": utils.base64_encode("\r\n".join((INPUT_LINES[0], INPUT_LINES[2]))),
    "__type": "Event",
}


class TestCertBundAvalancheParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CertBundAvalancheParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CertBundAvalancheParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_0)
        self.assertMessageEqual(1, OUTPUT_1)


if __name__ == "__main__":
    unittest.main()
