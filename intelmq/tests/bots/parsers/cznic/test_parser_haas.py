import unittest
import sys

from intelmq.lib import test
from intelmq.lib import utils
from intelmq.bots.parsers.cznic.parser_haas import CZNICHaasParserBot

INPUT = """[
    {
        "time": "2020-06-29T00:00:00.901916+00:00",
        "ip": "52.233.227.83",
        "country": "NL",
        "login_successful": true,
        "commands": [
            "sudo echo $UID"
        ],
        "time_closed": "2020-06-29T00:00:01.418213+00:00"
    },
    {
        "time": "2020-06-29T00:00:01.064095+00:00",
        "ip": "211.159.218.251",
        "country": "CN",
        "login_successful": false,
        "commands": [],
        "time_closed": "2020-06-29T00:00:02.076715+00:00"
    },
    {
        "time": "2020-06-29T00:00:06.548742+00:00",
        "ip": "108.162.223.108",
        "country": null,
        "login_successful": true,
        "commands": [],
        "time_closed": "2020-06-29T00:00:09.527695+00:00"
    }
]"""

OUTPUT_0 = {
    '__type': 'Event',
    'classification.type': 'unauthorized-command',
    'protocol.transport': 'tcp',
    'protocol.application': 'ssh',
    'destination.port': 22,
    'extra.commands': ['sudo echo $UID'],
    'extra.time_closed': '2020-06-29T00:00:01.418213+00:00',
    'raw': 'W3sidGltZSI6ICIyMDIwLTA2LTI5VDAwOjAwOjAwLjkwMTkxNiswMDowMCIsICJpcCI6ICI1Mi4yMzMuMjI3LjgzIiwgImNvdW50cnkiOiAiTkwiLCAibG9naW5fc3VjY2Vzc2Z1bCI6IHRydWUsICJjb21tYW5kcyI6IFsic3VkbyBlY2hvICRVSUQiXSwgInRpbWVfY2xvc2VkIjogIjIwMjAtMDYtMjlUMDA6MDA6MDEuNDE4MjEzKzAwOjAwIn1d',
    'source.geolocation.cc': 'NL',
    'source.ip': '52.233.227.83',
    'time.source': '2020-06-29T00:00:00.901916+00:00'
}

OUTPUT_1 = {
    '__type': 'Event',
    'classification.type': 'brute-force',
    'protocol.transport': 'tcp',
    'protocol.application': 'ssh',
    'destination.port': 22,
    'extra.commands': [],
    'extra.count': 1,
    'extra.time_closed': '2020-06-29T00:00:02.076715+00:00',
    'raw': 'W3sidGltZSI6ICIyMDIwLTA2LTI5VDAwOjAwOjAxLjA2NDA5NSswMDowMCIsICJpcCI6ICIyMTEuMTU5LjIxOC4yNTEiLCAiY291bnRyeSI6ICJDTiIsICJsb2dpbl9zdWNjZXNzZnVsIjogZmFsc2UsICJjb21tYW5kcyI6IFtdLCAidGltZV9jbG9zZWQiOiAiMjAyMC0wNi0yOVQwMDowMDowMi4wNzY3MTUrMDA6MDAifV0=',
    'source.geolocation.cc': 'CN',
    'source.ip': '211.159.218.251',
    'time.source': '2020-06-29T00:00:01.064095+00:00'
}

OUTPUT_2 = {
    '__type': 'Event',
    'classification.type': 'unauthorized-login',
    'protocol.transport': 'tcp',
    'protocol.application': 'ssh',
    'destination.port': 22,
    'extra.commands': [],
    'extra.time_closed': '2020-06-29T00:00:09.527695+00:00',
    'raw': 'W3sidGltZSI6ICIyMDIwLTA2LTI5VDAwOjAwOjA2LjU0ODc0MiswMDowMCIsICJpcCI6ICIxMDguMTYyLjIyMy4xMDgiLCAiY291bnRyeSI6IG51bGwsICJsb2dpbl9zdWNjZXNzZnVsIjogdHJ1ZSwgImNvbW1hbmRzIjogW10sICJ0aW1lX2Nsb3NlZCI6ICIyMDIwLTA2LTI5VDAwOjAwOjA5LjUyNzY5NSswMDowMCJ9XQ==',
    'source.ip': '108.162.223.108',
    'time.source': '2020-06-29T00:00:06.548742+00:00'
}


class TestCZNICHaasParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CZNICHaasParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CZNICHaasParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': utils.base64_encode(INPUT)}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_0)
        self.assertMessageEqual(1, OUTPUT_1)
        self.assertMessageEqual(2, OUTPUT_2)


if __name__ == '__main__':
    unittest.main()
