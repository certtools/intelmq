# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import intelmq.lib.test as test
from intelmq.bots.outputs.misp.output_feed import MISPFeedOutputBot
from intelmq.lib.message import MessageFactory

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

    def test_additional_info(self):
        self.run_bot(parameters={"additional_info": "This is my custom info."})

        current_event = open(f"{self.directory.name}/.current").read()
        with open(current_event) as f:
            info: str = json.load(f).get("Event", {}).get("info", "")
        assert info.startswith("This is my custom info. IntelMQ event ")

    def test_additional_info_with_separator(self):
        self.run_bot(
            parameters={
                "additional_info": "Event related to {separator}.",
                "event_separator": "malware.name",
            }
        )

        current_events = json.loads(open(f"{self.directory.name}/.current").read())
        with open(current_events["salityp2p"]) as f:
            info: str = json.load(f).get("Event", {}).get("info", "")
        assert info.startswith("Event related to salityp2p. IntelMQ event ")

    def test_accumulating_events(self):
        """Ensures bot first collects events and then saves them in bulks to MISP feed,
        and also respects the event interval to create a new event periodically.
        """
        self.input_message = [EXAMPLE_EVENT, EXAMPLE_EVENT]
        self.run_bot(iterations=2, parameters={"bulk_save_count": 3})

        current_event = open(f"{self.directory.name}/.current").read()

        # The first event is always immediately dumped to the MISP feed
        # But the second wait until bulk saving size is achieved
        with open(current_event) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])
        assert len(objects) == 1

        self.input_message = [EXAMPLE_EVENT, EXAMPLE_EVENT]
        self.run_bot(iterations=2, parameters={"bulk_save_count": 3})

        # When enough events were collected, save them
        with open(current_event) as f:
            objects = json.load(f)["Event"]["Object"]
        assert len(objects) == 4

        self.input_message = [EXAMPLE_EVENT, EXAMPLE_EVENT, EXAMPLE_EVENT]
        self.run_bot(iterations=3, parameters={"bulk_save_count": 3})

        # We continue saving to the same file until interval timeout
        with open(current_event) as f:
            objects = json.load(f)["Event"]["Object"]
        assert len(objects) == 7

        # Simulating leftovers in the queue when it's time to generate new event
        Path(f"{self.directory.name}/.current").unlink()
        self.bot.cache_put(
            MessageFactory.from_dict(EXAMPLE_EVENT).to_dict(jsondict_as_string=True)
        )
        self.run_bot(parameters={"bulk_save_count": 3})

        new_event = open(f"{self.directory.name}/.current").read()
        with open(new_event) as f:
            objects = json.load(f)["Event"]["Object"]
        assert len(objects) == 2

    def test_attribute_mapping(self):
        """Tests custom attribute mapping that selects just a subset of fields to export
        and allows including custom parameters for MISPObjectAttribute, like comments."""
        self.run_bot(
            parameters={
                "attribute_mapping": {
                    "source.ip": {},
                    "feed.name": {"comment": "event_description.text"},
                    "destination.ip": {"to_ids": False},
                    "malware.name": {"comment": "extra.non_ascii"},
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
            attr
            for attr in attributes
            if attr.get("object_relation") == "destination.ip"
        )
        assert destination_ip["value"] == EXAMPLE_EVENT["destination.ip"]
        assert destination_ip["to_ids"] is False

        malware_name = next(
            attr for attr in attributes if attr.get("object_relation") == "malware.name"
        )
        assert malware_name["value"] == EXAMPLE_EVENT["malware.name"]
        assert malware_name["comment"] == EXAMPLE_EVENT["extra.non_ascii"]

    def test_attribute_mapping_omitted_when_field_is_empty(self):
        self.run_bot(
            parameters={
                "attribute_mapping": {
                    "source.ip": {},
                    "source.fqdn": {},  # not exists in the message
                }
            }
        )

        current_event = open(f"{self.directory.name}/.current").read()
        with open(current_event) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])

        assert len(objects) == 1
        attributes = objects[0].get("Attribute")
        assert len(attributes) == 1
        source_ip = next(
            attr for attr in attributes if attr.get("object_relation") == "source.ip"
        )
        assert source_ip["value"] == "152.166.119.2"

    def test_event_separation(self):
        """Tests that based on the value of the given field, incoming messages are put in separated
        MISP events."""
        self.input_message = [
            EXAMPLE_EVENT,
            {**EXAMPLE_EVENT, "malware.name": "another_malware"},
            EXAMPLE_EVENT,
        ]
        self.run_bot(iterations=3, parameters={"event_separator": "malware.name"})

        current_events = json.loads(open(f"{self.directory.name}/.current").read())
        assert len(current_events) == 2

        with open(current_events["salityp2p"]) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])
        assert len(objects) == 2
        malware_name = next(
            attr["value"]
            for attr in objects[0]["Attribute"]
            if attr.get("object_relation") == "malware.name"
        )
        assert malware_name == "salityp2p"

        with open(current_events["another_malware"]) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])
        assert len(objects) == 1
        malware_name = next(
            attr["value"]
            for attr in objects[0]["Attribute"]
            if attr.get("object_relation") == "malware.name"
        )
        assert malware_name == "another_malware"

    def test_event_separation_with_extra_and_bulk_save(self):
        self.input_message = [
            {**EXAMPLE_EVENT, "extra.some_key": "another_malware"},
            {**EXAMPLE_EVENT, "extra.some_key": "first_malware"},
            {**EXAMPLE_EVENT, "extra.some_key": "another_malware"},
        ]
        self.run_bot(
            iterations=3,
            parameters={"event_separator": "extra.some_key", "bulk_save_count": 3},
        )

        # Only the initial event is saved, the rest is cached
        current_events = json.loads(open(f"{self.directory.name}/.current").read())
        assert len(current_events) == 1
        with open(current_events["another_malware"]) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])
        assert len(objects) == 1

        self.input_message = {**EXAMPLE_EVENT, "extra.some_key": "first_malware"}
        self.run_bot(
            parameters={"event_separator": "extra.some_key", "bulk_save_count": 3},
        )

        # Now everything is saved
        current_events = json.loads(open(f"{self.directory.name}/.current").read())
        assert len(current_events) == 2
        with open(current_events["another_malware"]) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])
        assert len(objects) == 2

        with open(current_events["first_malware"]) as f:
            objects = json.load(f).get("Event", {}).get("Object", [])
        assert len(objects) == 2

    def test_tagging(self):
        """Ensures MISP events get correct MISP tags"""
        self.run_bot(
            parameters={
                "tagging": {
                    "__all__": [
                        {"name": "tlp:unclear", "colour": "#7e7eae"},
                        {"name": "source:intelmq"},
                    ]
                }
            }
        )

        current_event = open(f"{self.directory.name}/.current").read()
        with open(current_event) as f:
            tags = json.load(f).get("Event", {}).get("Tag", [])
        assert len(tags) == 2

        tlp = next(t for t in tags if t["name"] == "tlp:unclear")
        assert tlp["colour"] == "#7e7eae"

    def test_tagging_and_event_separation(self):
        """When separating events, it is possible to add different MISP tags to specific MISP
        events."""
        self.input_message = [
            EXAMPLE_EVENT,
            {**EXAMPLE_EVENT, "malware.name": "another_malware"},
        ]
        self.run_bot(
            iterations=2,
            parameters={
                "event_separator": "malware.name",
                "tagging": {
                    "__all__": [{"name": "source:intelmq"}],
                    "salityp2p": [{"name": "family:salityp2p"}],
                    "another_malware": [{"name": "family:malware_2"}],
                },
            },
        )

        current_events = json.loads(open(f"{self.directory.name}/.current").read())
        assert len(current_events) == 2

        with open(current_events["salityp2p"]) as f:
            tags = json.load(f).get("Event", {}).get("Tag", [])
        assert len(tags) == 2
        assert next(t for t in tags if t["name"] == "source:intelmq")
        assert next(t for t in tags if t["name"] == "family:salityp2p")

        with open(current_events["another_malware"]) as f:
            tags = json.load(f).get("Event", {}).get("Tag", [])
        assert len(tags) == 2
        assert next(t for t in tags if t["name"] == "source:intelmq")
        assert next(t for t in tags if t["name"] == "family:malware_2")

    def test_parameter_check_correct(self):
        result = self.bot_reference.check(
            {
                **self.sysconfig,
                "attribute_mapping": {
                    "source.ip": {},
                    "feed.name": {"comment": "event_description.text"},
                    "destination.ip": {"to_ids": False, "comment": "Possible FP"},
                    "malware.name": {"comment": "extra.non_ascii"},
                },
                "event_separator": "extra.botnet",
                "bulk_save_count": 10,
                "tagging": {
                    "__all__": [{"name": "source:feed", "colour": "#000000"}],
                    "abotnet": [{"name": "type:botnet"}],
                },
            }
        )
        assert result is None

    def test_parameter_check_errors(self):
        cases = [
            {"bulk_save_count": "not-a-number"},
            {"event_separator": "not-a-field"},
            {"attribute_mapping": "not-a-dict"},
            {"attribute_mapping": {"not-a-field": {}}},
            {"attribute_mapping": {"source.ip": "not-a-dict"}},
            {
                "tagging": {"not-all": []}
            },  # without event_separator, only __all__ is allowed
            {"tagging": {"__all__": [], "other": []}},
            {"event_separator": "malware.name", "tagging": ["not", "a", "dict"]},
            {
                "event_separator": "malware.name",
                "tagging": {"case": "must-be-list-of-dicts"},
            },
            {
                "event_separator": "malware.name",
                "tagging": {"case": ["must-be-list-of-dicts"]},
            },
            {
                "event_separator": "malware.name",
                "tagging": {"case": [{"must": "have a name"}]},
            },
        ]
        for case in cases:
            with self.subTest():
                result = self.bot_reference.check({**self.sysconfig, **case})
                assert len(list(r for r in result if r[0] == "error")) == 1

    def test_parameter_check_warnings(self):
        cases = [
            {"attribute_mapping": {"source.ip": {"not-a-feed-arg": "any"}}},
            {"tagging": {"case": [{"name": "", "not-a-feed-arg": "any"}]}},
        ]
        for case in cases:
            with self.subTest():
                result = self.bot_reference.check({**self.sysconfig, **case})
                assert len(list(r for r in result if r[0] == "warning")) == 1

    def tearDown(self):
        self.cache.delete(self.bot_id)
        self.directory.cleanup()
        super().tearDown()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
