# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from .....lib.message import Message, MessageFactory
import intelmq.lib.test as test
from intelmq.bots.outputs.misp.output_feed import MISPFeedOutputBot

EXAMPLE_EVENT = {
    "classification.type": "infected-system",
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
        cls.use_cache = True
        cls.bot_reference = MISPFeedOutputBot
        cls.default_input_message = EXAMPLE_EVENT
        cls.sysconfig = {
            "misp_org_name": "IntelMQTestOrg",
            "misp_org_uuid": "b89da4c2-0f74-11ea-96a1-6fa873a0eb4d",
            "interval_event": "1 hour",
        }

    def setUp(self) -> None:
        super().setUp()
        self.directory = TemporaryDirectory()
        self.sysconfig["output_dir"] = self.directory.name

    def test_event(self):
        self.run_bot()

        current_event = open(f"{self.directory.name}/.current").read()
        with open(current_event) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])
        assert len(objects) == 1

    def test_accumulating_events(self):
        self.input_message = [EXAMPLE_EVENT, EXAMPLE_EVENT]
        self.run_bot(iterations=2, parameters={"bulk_save_count": 3})

        current_event = open(f"{self.directory.name}/.current").read()

        # First, the feed is empty - not enough events came
        with open(current_event) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])
        assert len(objects) == 0

        self.input_message = [EXAMPLE_EVENT]
        self.run_bot(parameters={"bulk_save_count": 3})

        # When enough events were collected, save them
        with open(current_event) as f:
            objects = json.load(f)["Event"]["Object"]
        assert len(objects) == 3

        self.input_message = [EXAMPLE_EVENT, EXAMPLE_EVENT, EXAMPLE_EVENT]
        self.run_bot(iterations=3, parameters={"bulk_save_count": 3})

        # We continue saving to the same file until interval timeout
        with open(current_event) as f:
            objects = json.load(f)["Event"]["Object"]
        assert len(objects) == 6

        # Simulating leftovers in the queue when it's time to generate new event
        Path(f"{self.directory.name}/.current").unlink()
        self.bot.cache_put(MessageFactory.from_dict(EXAMPLE_EVENT).to_dict(jsondict_as_string=True))
        self.run_bot(parameters={"bulk_save_count": 3})

        new_event = open(f"{self.directory.name}/.current").read()
        with open(new_event) as f:
            objects = json.load(f)["Event"]["Object"]
        assert len(objects) == 1

    def test_attribute_mapping(self):
        self.run_bot(
            parameters={
                "attribute_mapping": {
                    "source.ip": {},
                    "feed.name": {"comment": "event_description.text"},
                    "destination.ip": {"to_ids": False},
                    "malware.name": {"comment": "extra.non_ascii"}
                }
            }
        )

        current_event = open(f"{self.directory.name}/.current").read()
        with open(current_event) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])

        assert len(objects) == 1
        attributes = objects[0].get("Attribute")
        assert len(attributes) == 4
        source_ip = next(
            attr for attr in attributes if attr.get("object_relation") == "source.ip"
        )
        assert source_ip["value"] == "152.166.119.2"
        assert source_ip["comment"] == ""

        feed_name = next(
            attr for attr in attributes if attr.get("object_relation") == "feed.name"
        )
        assert feed_name["value"] == EXAMPLE_EVENT["feed.name"]
        assert feed_name["comment"] == EXAMPLE_EVENT["event_description.text"]

        destination_ip = next(
            attr for attr in attributes if attr.get("object_relation") == "destination.ip"
        )
        assert destination_ip["value"] == EXAMPLE_EVENT["destination.ip"]
        assert destination_ip["to_ids"] is False

        malware_name = next(
            attr for attr in attributes if attr.get("object_relation") == "malware.name"
        )
        assert malware_name["value"] == EXAMPLE_EVENT["malware.name"]
        assert malware_name["comment"] == EXAMPLE_EVENT["extra.non_ascii"]


    def tearDown(self):
        self.cache.delete(self.bot_id)
        self.directory.cleanup()
        super().tearDown()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
