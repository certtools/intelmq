# -*- coding: utf-8 -*-
import unittest
import sys
from tempfile import TemporaryDirectory

import intelmq.lib.test as test
from intelmq.bots.outputs.misp.output_feed import MISPFeedOutputBot

EXAMPLE_EVENT = {"classification.type": "malware",
                 "destination.port": 9796,
                 "feed.accuracy": 100.0,
                 "destination.ip": "52.18.196.169",
                 "malware.name": "salityp2p",
                 "event_description.text": "Sinkhole attempted connection",
                 "time.source": "2016-04-19T23:16:08+00:00",
                 "source.ip": "152.166.119.2",
                 "feed.url": "http://alerts.bitsighttech.com:8080/stream?",
                 "source.geolocation.country": "Dominican Republic",
                 "time.observation": "2016-04-19T23:16:08+00:00",
                 "source.port": 65118,
                 "__type": "Event",
                 "feed.name": "BitSight",
                 "extra.non_ascii": "ççãããã\x80\ua000 \164 \x80\x80 abcd \165\166",
                 "raw": "eyJ0cm9qYW5mYW1pbHkiOiJTYWxpdHlwMnAiLCJlbnYiOnsic"
                 "mVtb3RlX2FkZHIiOiIxNTIuMTY2LjExOS4yIiwicmVtb3RlX3"
                 "BvcnQiOiI2NTExOCIsInNlcnZlcl9hZGRyIjoiNTIuMTguMTk"
                 "2LjE2OSIsInNlcnZlcl9wb3J0IjoiOTc5NiJ9LCJfdHMiOjE0"
                 "NjExMDc3NjgsIl9nZW9fZW52X3JlbW90ZV9hZGRyIjp7ImNvd"
                 "W50cnlfbmFtZSI6IkRvbWluaWNhbiBSZXB1YmxpYyJ9fQ==",
                 "__type": "Event",
                 }


@test.skip_exotic()
class TestMISPFeedOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MISPFeedOutputBot
        cls.default_input_message = EXAMPLE_EVENT
        cls.directory = TemporaryDirectory()
        cls.sysconfig = {"misp_org_name": 'IntelMQTestOrg',
                         "misp_org_uuid": "b89da4c2-0f74-11ea-96a1-6fa873a0eb4d",
                         "output_dir": cls.directory.name,
                         "interval_event": '1 hour'}

    def test_event(self):
        self.run_bot()

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
