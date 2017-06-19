# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.fraunhofer.parser_dga import FraunhoferDGAParserBot

EXAMPLE_REPORT = {"feed.url": "https://dgarchive.caad.fkie.fraunhofer.de/today",
                  "raw": "ewogICJiYW5qb3JpX2RnYV9hbmRlcnNlbnNpbmFpeC5jb21fMHgz"
                         "YzAzIjogWwogICAgImFuZGVyc2Vuc2luYWl4LmNvbSIsCiAgICAi"
                         "eGpzcnJzZW5zaW5haXguY29tIiwKICAgICJobHJmcnNlbnNpbmFp"
                         "eC5jb20iLAogICAgImZub3Nyc2Vuc2luYWl4LmNvbSIsCiAgICAi"
                         "MTI4LjIzOC4xOTcuMzMiLAogICAgImxiem9yc2Vuc2luYWl4LmNv"
                         "bSIsCiAgICAic2dqcHJzZW5zaW5haXguY29tIgogIF0KfQ==",
                  "__type": "Report",
                  "feed.name": "Fraunhofer DGA",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENT_TEMPL = {"feed.url": "https://dgarchive.caad.fkie.fraunhofer.de/today",
               "feed.name": "Fraunhofer DGA",
               "__type": "Event",
               "classification.type": "c&c",
               'malware.name': 'banjori',
               "time.observation": "2015-01-01T00:00:00+00:00",
               }
EXAMPLE_EVENTS_PARTS = [{'raw': 'YW5kZXJzZW5zaW5haXguY29t',
                         'source.fqdn': 'andersensinaix.com'},
                        {'raw': 'eGpzcnJzZW5zaW5haXguY29t',
                         'source.fqdn': 'xjsrrsensinaix.com'},
                        {'raw': 'aGxyZnJzZW5zaW5haXguY29t',
                         'source.fqdn': 'hlrfrsensinaix.com'},
                        {'raw': 'Zm5vc3JzZW5zaW5haXguY29t',
                         'source.fqdn': 'fnosrsensinaix.com'},
                        {'raw': 'MTI4LjIzOC4xOTcuMzM=',
                         'source.ip': '128.238.197.33'},
                        {'raw': 'bGJ6b3JzZW5zaW5haXguY29t',
                         'source.fqdn': 'lbzorsensinaix.com'},
                        {'raw': 'c2dqcHJzZW5zaW5haXguY29t',
                         'source.fqdn': 'sgjprsensinaix.com'}]


class TestFraunhoferDGAParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a FraunhoferDGAParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FraunhoferDGAParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.run_bot()
        for position, event in enumerate(EXAMPLE_EVENTS_PARTS):
            event.update(EVENT_TEMPL)
            self.assertMessageEqual(position, event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
