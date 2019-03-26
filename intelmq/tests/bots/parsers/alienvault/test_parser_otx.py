# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.alienvault.parser_otx import AlienVaultOTXParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'test_parser_otx.data'), encoding='utf-8') as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "AlienVault OTX",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-09-02T14:17:58+00:00"
                  }
EXAMPLE_EVENT = {
    "__type": "Event",
    "extra.author": "AlienVault",
    "extra.time_updated": "2015-09-02T09:22:22.97+00:00",
    "extra.pulse_key": "55e6bfb14637f22cb605746e",
    "extra.pulse": "The Spy Kittens Are Back: Rocket Kitten 2",
    "extra.tags": ['spy kittens', 'rocket kitten', 'ghole', 'spearphishing', 'Social engineering', 'TSPY_WOOLERG', 'apt', 'trendmicro'],
    "comment": """Our findings show that Rocket Kitten is still active, retains
a growing level of persistence, and acts ever more aggressively in terms of
attack method. We also found that recent publications on the group’s activity
have done nothing to change their behavior or reduce their activity. They don’t
seem to bother to have to “disappear.” With this paper, we feel fairly certain
that Rocket Kitten’s prime targets are not companies and political
organizations as entire bodies but individuals that operate in strategically
interesting fields such as diplomacy, foreign policy research, and
defense-related businesses. We believe the espionage factor and political
context make their attacks unique and very different from traditional targeted
attacks.""".replace('\n', ' '),
    "feed.name": "AlienVault OTX",
    "classification.type": "blacklist",
    "source.url": "http://107.6.172.54/woolen/",
    "raw": "eyJfaWQiOiAiNTVlNmJmYjE0NjM3ZjIyY2I2MDU3NDY2IiwgImNyZWF0ZWQiOiAiMj"
           "AxNS0wOS0wMlQwOToyMTo1My4wOTMiLCAiZGVzY3JpcHRpb24iOiAiIiwgImluZGlj"
           "YXRvciI6ICJodHRwOi8vMTA3LjYuMTcyLjU0L3dvb2xlbi8iLCAidHlwZSI6ICJVUk"
           "wifQ==",
    "time.source": "2015-09-02T09:21:53+00:00",
    "time.observation": "2015-09-02T14:17:58+00:00",
}

EXAMPLE_EVENT_2 = {
  '__type': 'Event',
  'classification.type': 'blacklist',
  'comment': 'Active users of mobile banking apps should be aware of a new '
             'Android banking malware campaign targeting customers of large '
             'banks in the United States, Germany, France, Australia, Turkey, '
             'Poland, and Austria. This banking malware can steal login '
             'credentials from 94 different mobile banking apps. Due to its '
             'ability to intercept SMS communications, the malware is also '
             'able to bypass SMS-based two-factor authentication. '
             'Additionally, it also contains modules to target some popular '
             'social media apps.',
  'extra.adversary': '',
  'extra.tags': ['skype', 'flash player', 'android', 'banker'],
  'extra.pulse_key': '581b9aef324bc542d6b1fd84',
  'extra.targeted_countries': ['United States', 'Germany', 'France', 'Australia', 'Turkey', 'Poland', 'Austria'],
  'extra.industries': ['banking'],
  'extra.time_updated': '2016-11-03T20:15:43.26+00:00',
  'extra.author': 'AlienVault',
  'extra.pulse': 'Android banking malware masquerades as Flash Player',
  'feed.name': 'AlienVault OTX',
  'malware.hash.sha256': 'e5df30b41b0c50594c2b77c1d5d6916a9ce925f792c563f692426c2d50aa2524',
  'raw': 'eyJhY2Nlc3NfZ3JvdXBzIjogW10sICJhY2Nlc3NfcmVhc29uIjogIiIsICJhY2Nlc3NfdHlwZSI6ICJwdWJsaWMiLCAiY29udGVudCI6ICIiLCAiY3JlYXRlZCI6ICIyMDE2LTExLTAzVDIwOjE1OjQ0IiwgImRlc2NyaXB0aW9uIjogIiIsICJleHBpcmF0aW9uIjogbnVsbCwgImlkIjogMTI2NTM1NCwgImluZGljYXRvciI6ICJlNWRmMzBiNDFiMGM1MDU5NGMyYjc3YzFkNWQ2OTE2YTljZTkyNWY3OTJjNTYzZjY5MjQyNmMyZDUwYWEyNTI0IiwgImlzX2FjdGl2ZSI6IDEsICJvYnNlcnZhdGlvbnMiOiAzLCAicm9sZSI6IG51bGwsICJ0aXRsZSI6ICIiLCAidHlwZSI6ICJGaWxlSGFzaC1TSEEyNTYifQ==',
  'time.source': '2016-11-03T20:01:00+00:00',
  "tlp": "GREEN",
  }

EXAMPLE_EVENT_3 = {
  '__type': 'Event',
   'classification.type': 'blacklist',
   'comment': 'Myanmar is a country currently engaged in an important '
              'political process. A pro-democracy reform took place \n'
              'in 2011 which has helped the government create an atmopshere '
              'conducive to investor interest. The country is \n'
              'resource rich, with a variety of natural resources and a steady '
              'labor supply. Despite recent progress, the \n'
              'country is subject to ongoing conflict with ethnic rebels and '
              'an ongoing civil war. Analysts suggest that both \n'
              'China and the United States are vying for greater influence in '
              'Myanmar, with China in particular having \n'
              'geopolitical interest due to sea passages, port deals, and fuel '
              'pipelines that are important to its goals. \n'
              'Geopolitical analysts have suggested that the United States may '
              'have its own interests that involve thwarting \n'
              'Chinese ambitions in the region. APT groups from multiple '
              'countries - including China - have been known to target '
              'organizations of strategic interest with aggressive '
              'malware-based espionage campaigns.',
  'extra.pulse_key': '55e557fa4637f21c54c1bb0d',
  'extra.tags': ['plugx', 'Myanmar', 'rat', 'Strategic\tWeb\tCompromise'],
  'extra.author': 'AlienVault',
  'extra.time_updated': '2015-09-01T07:47:06.00+00:00',
  'extra.pulse': 'PlugX Threat\tActivity in Myanmar',
  'feed.name': 'AlienVault OTX',
  'raw': 'eyJfaWQiOiAiNTVlNTU3ZmE0NjM3ZjIxYzU0YzFiYWY4IiwgImNyZWF0ZWQiOiAiMjAxNS0wOS0wMVQwNzo0NzowNi4wNzMiLCAiZGVzY3JpcHRpb24iOiAiIiwgImluZGljYXRvciI6ICJodHRwOi8vd3d3LnVlY215YW5tYXIub3JnL2RtZG9jdW1lbnRzL2ludml0YXRpb25zLnJhciIsICJ0eXBlIjogIlVSTCJ9',
  'source.url': 'http://www.uecmyanmar.org/dmdocuments/invitations.rar',
  'time.source': '2015-09-01T07:47:06+00:00',
  }

EXAMPLE_EVENT_4 = {
  '__type': 'Event',
  'classification.type': 'blacklist',
  'comment': 'HIDDEN COBRA – North Korean Malicious Cyber Activity',
  'extra.adversary': '',
  'extra.pulse_key': '5942175dd78f563d01abc79c',
  'extra.pulse': 'Alert (TA17-164A)',
  'extra.author': 'bschlaps',
  'extra.industries': [],
  'extra.tags': [],
  'extra.time_updated': '2017-06-15T05:17:12.18+00:00',
  'feed.name': 'AlienVault OTX',
  'raw': 'eyJhY2Nlc3NfZ3JvdXBzIjogW10sICJhY2Nlc3NfcmVhc29uIjogIiIsICJhY2Nlc3NfdHlwZSI6ICJwdWJsaWMiLCAiY29udGVudCI6ICIiLCAiY3JlYXRlZCI6ICIyMDE3LTA2LTE1VDA1OjEzOjAyIiwgImRlc2NyaXB0aW9uIjogIiIsICJleHBpcmF0aW9uIjogbnVsbCwgImlkIjogMTM1Nzk4OSwgImluZGljYXRvciI6ICIxMzQuMTE5LjM2LjEzNSIsICJpc19hY3RpdmUiOiAxLCAib2JzZXJ2YXRpb25zIjogMTEsICJwdWxzZV9rZXkiOiAiNTk0MjE3NWRkNzhmNTYzZDAxYWJjNzljIiwgInJvbGUiOiBudWxsLCAidGl0bGUiOiAiIiwgInR5cGUiOiAiSVB2NCJ9',
  'source.ip': '134.119.36.135',
  'time.source': '2017-06-15T05:01:00+00:00',
  "tlp": "WHITE",
  }

EXAMPLE_EVENT_URI_1 = {
    "__type": "Event",
    "extra.author": "bschlaps",
    'extra.adversary': '',
    'extra.industries': [],
    'extra.tags': [],
    "extra.pulse": "Alert (TA17-164A)",
    "extra.pulse_key": "5942175dd78f563d01abc79c",
    "extra.time_updated": "2017-06-15T05:17:12.18+00:00",
    "comment": "HIDDEN COBRA – North Korean Malicious Cyber Activity",
    "feed.name": "AlienVault OTX",
    "classification.type": "blacklist",
    "source.url": "http://107.6.172.54/woolen/",
    "raw": "eyJfaWQiOiAiNTVlNmJmYjE0NjM3ZjIyY2I2"
           "MDU3NDY2IiwgImNyZWF0ZWQiOiAiMjAxNS0wO"
           "S0wMlQwOToyMTo1My4wOTMiLCAiZGVzY3JpcH"
           "Rpb24iOiAiIiwgImluZGljYXRvciI6ICJodHR"
           "wOi8vMTA3LjYuMTcyLjU0L3dvb2xlbi8iLCAidHlwZSI6ICJVUkkifQ==",
    "time.source": "2015-09-02T09:21:53+00:00",
    "time.observation": "2015-09-02T14:17:58+00:00",
    "tlp": "WHITE",
}

EXAMPLE_EVENT_URI_2 = {
    "__type": "Event",
    "extra.author": "bschlaps",
    'extra.adversary': '',
    'extra.industries': [],
    'extra.tags': [],
    "extra.pulse": "Alert (TA17-164A)",
    "extra.pulse_key": "5942175dd78f563d01abc79c",
    "extra.time_updated": "2017-06-15T05:17:12.18+00:00",
    "comment": "HIDDEN COBRA – North Korean Malicious Cyber Activity",
    "feed.name": "AlienVault OTX",
    "classification.type": "blacklist",
    "source.urlpath": "/woolen/",
    "raw": "eyJfaWQiOiAiNTVlNmJmYjE0NjM3ZjIyY2I2MDU3NDY2IiwgImNyZWF0ZWQiOiAiMjAxNS"
           "0wOS0wMlQwOToyMTo1My4wOTMiLCAiZGVzY3JpcHRpb24iOiAiIiwgImluZGljYXRvciI6"
           "ICIvd29vbGVuLyIsICJ0eXBlIjogIlVSSSJ9",
    "time.source": "2015-09-02T09:21:53+00:00",
    "time.observation": "2015-09-02T14:17:58+00:00",
    "tlp": "WHITE",
}


class TestAlienVaultOTXParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AlienVaultOTXParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AlienVaultOTXParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)
        self.assertMessageEqual(11, EXAMPLE_EVENT_2)
        self.assertMessageEqual(70, EXAMPLE_EVENT_3)
        self.assertMessageEqual(91, EXAMPLE_EVENT_4)
        self.assertMessageEqual(93, EXAMPLE_EVENT_URI_1)
        self.assertMessageEqual(94, EXAMPLE_EVENT_URI_2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
