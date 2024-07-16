# SPDX-FileCopyrightText: 2019 Sebastian Wagner, 2024 CERT.at GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import datetime
import json
import re
from pathlib import Path
from uuid import uuid4


from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.message import Event, Message, MessageFactory
from intelmq.lib.mixins import CacheMixin
from intelmq.lib.utils import parse_relative

try:
    from pymisp import (
        MISPEvent,
        MISPObject,
        MISPOrganisation,
        MISPTag,
        MISPObjectAttribute,
        NewAttributeError,
    )
    from pymisp.tools import feed_meta_generator
except ImportError:
    MISPEvent = None

DEFAULT_KEY = "default"


class MISPFeedOutputBot(OutputBot, CacheMixin):
    """Generate an output in the MISP Feed format"""

    interval_event: str = "1 hour"
    misp_org_name = None
    misp_org_uuid = None
    output_dir: str = (
        "/opt/intelmq/var/lib/bots/mispfeed-output"  # TODO: should be path
    )
    # Enables regenerating the MISP feed after collecting given number of messages
    bulk_save_count: int = None

    # Additional information to be added to the MISP event description
    additional_info: str = None

    # An optional field used to create multiple MISP events from incoming messages
    event_separator: str = None

    # Optional non-standard mapping of message fields to MISP object attributes
    # The structure is like:
    # {<IDF_field_name = MIPS_object_relation>: {<dict of additional parameters for MISPObjectAttribute>}}
    # For example:
    #   {"source.ip": {"comment": "This is the source of the event"}}
    #        will include only the "source.ip" field in the MISP object attributes,
    #        and set the comment
    attribute_mapping: dict = None

    # Optional definition to add tags to the MISP event. It should be a dict where keys are
    # '__all__' (to add tags for every event) or, if the event_separator is used, the separator
    # values. For each key, there should be a list of dicts defining parameters for the MISPTag
    # object, but only the "name" is required to set.
    # For example:
    #   {"__all__": [{"name": "tag1"}, {"name": "tag2"}]}
    #       will add two tags to every event
    #   {"infostealer": [{"name": "type:infostealer"}], "__all__": [{"name": "tag1"}]}
    #       will add two tags to every event separated by "infostealer", and
    #       one tag to every other event
    tagging: dict = None

    # Delaying reloading would delay saving eventually long-awaiting messages
    _sighup_delay = False
    _is_multithreadable: bool = False

    @staticmethod
    def check_output_dir(dirname):
        output_dir = Path(dirname)
        if not output_dir.exists():
            output_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
            return True

    def init(self):
        if MISPEvent is None:
            raise MissingDependencyError("pymisp", version=">=2.4.117.3")

        self.current_events = {}
        self.current_files = {}

        self.misp_org = MISPOrganisation()
        self.misp_org.name = self.misp_org_name
        self.misp_org.uuid = self.misp_org_uuid

        self.output_dir = Path(self.output_dir)
        MISPFeedOutputBot.check_output_dir(self.output_dir)

        if self.interval_event is None:
            self.timedelta = datetime.timedelta(hours=1)
        else:
            self.timedelta = datetime.timedelta(
                minutes=parse_relative(self.interval_event)
            )

        self.min_time_current = datetime.datetime.max
        self.max_time_current = datetime.datetime.min

        if (self.output_dir / ".current").exists():
            try:
                with (self.output_dir / ".current").open() as f:
                    current = f.read()

                if not self.event_separator:
                    self.current_files[DEFAULT_KEY] = Path(current)
                else:
                    self.current_files = {
                        k: Path(v) for k, v in json.loads(current).items()
                    }

                for key, path in self.current_files.items():
                    self._load_event(path, key)
            except Exception:
                self.logger.exception(
                    "Loading current events %s failed. Skipping it.", self.current_files
                )
                self.current_events = {}

        if not self.current_files or self.max_time_current < datetime.datetime.now():
            self.min_time_current = datetime.datetime.now()
            self.max_time_current = self.min_time_current + self.timedelta
            self.current_events = {}

        self._tagging_objects = {}
        if self.tagging:
            for key, tag_list in self.tagging.items():
                self._tagging_objects[key] = list()
                for kw in tag_list:
                    # For some reason, PyMISP do not uses classmethod, and from_dict requires
                    # unpacking. So this is really the way to initialize tag objects.
                    tag = MISPTag()
                    tag.from_dict(**kw)
                    self._tagging_objects[key].append(tag)

        # Ensure we do generate feed on reload / restart, so awaiting messages won't wait forever
        if self.cache_length() and not getattr(self, "testing", False):
            self.logger.debug(
                "Found %s awaiting messages. Generating feed.", self.cache_length()
            )
            self._generate_misp_feed()

    def _load_event(self, file_path: Path, key: str):
        if file_path.exists():
            self.current_events[key] = MISPEvent()
            self.current_events[key].load_file(file_path)

            last_min_time, last_max_time = re.findall(
                "IntelMQ event (.*) - (.*)", self.current_events[key].info
            )[0]
            last_min_time = datetime.datetime.strptime(
                last_min_time, "%Y-%m-%dT%H:%M:%S.%f"
            )
            last_max_time = datetime.datetime.strptime(
                last_max_time, "%Y-%m-%dT%H:%M:%S.%f"
            )

            self.min_time_current = min(last_min_time, self.min_time_current)
            self.max_time_current = max(last_max_time, self.max_time_current)

    def process(self):
        if datetime.datetime.now() > self.max_time_current:
            self.min_time_current = datetime.datetime.now()
            self.max_time_current = self.min_time_current + self.timedelta

            self._generate_misp_feed()

        event = self.receive_message().to_dict(jsondict_as_string=True)

        cache_size = None
        if self.bulk_save_count:
            cache_size = self.cache_put(event)

        if cache_size is None:
            self._generate_misp_feed(event)
        elif not self.current_events:
            # Always create the first event so we can keep track of the interval.
            self._generate_misp_feed()
        elif cache_size >= self.bulk_save_count:
            self._generate_misp_feed()

        self.acknowledge_message()

    def _generate_new_misp_event(self, key):
        self.current_events[key] = MISPEvent()

        tags: list[MISPTag] = []
        if "__all__" in self._tagging_objects:
            tags.extend(self._tagging_objects["__all__"])
        if key in self._tagging_objects:
            tags.extend(self._tagging_objects[key])
        self.current_events[key].tags = tags

        info = "IntelMQ event {begin} - {end}" "".format(
            begin=self.min_time_current.isoformat(),
            end=self.max_time_current.isoformat(),
        )
        if self.additional_info:
            info = f"{self.additional_info.format(separator=key)} {info}"

        self.current_events[key].info = info
        self.current_events[key].set_date(datetime.date.today())
        self.current_events[key].Orgc = self.misp_org
        self.current_events[key].uuid = str(uuid4())
        self.current_files[key] = (
            self.output_dir / f"{self.current_events[key].uuid}.json"
        )
        with (self.output_dir / ".current").open("w") as f:
            if not self.event_separator:
                f.write(str(self.current_files[key]))
            else:
                json.dump({k: str(v) for k, v in self.current_files.items()}, f)
        return self.current_events[key]

    def _add_message_to_misp_event(self, message: dict):
        # For proper handling of nested fields, we need the object
        message_obj = MessageFactory.from_dict(
            message, harmonization=self.harmonization, default_type="Event"
        )
        if not self.event_separator:
            key = DEFAULT_KEY
        else:
            key = message_obj.get(self.event_separator) or DEFAULT_KEY

        if key in self.current_events:
            event = self.current_events[key]
        else:
            event = self._generate_new_misp_event(key)

        obj = event.add_object(name="intelmq_event")
        # For caching and default mapping, the serialized version is the right format to work on.
        # However, for any custom mapping the Message object is more sufficient as it handles
        # subfields.
        if not self.attribute_mapping:
            self._default_mapping(obj, message)
        else:
            self._custom_mapping(obj, message_obj)

    def _default_mapping(self, obj: "MISPObject", message: dict):
        for object_relation, value in message.items():
            try:
                obj.add_attribute(object_relation, value=value)
            except NewAttributeError:
                # This entry isn't listed in the harmonization file, ignoring.
                if object_relation != "__type":
                    self.logger.warning(
                        "Object relation %s not exists in MISP definition, ignoring",
                        object_relation,
                    )

    def _extract_misp_attribute_kwargs(self, message: dict, definition: dict) -> dict:
        """Creates the a dict with arguments to create a MISPObjectAttribute."""
        result = {}
        for parameter, value in definition.items():
            # Check if the value is a harmonization key or a static value
            if isinstance(value, str) and (
                value in self.harmonization["event"]
                or value.split(".", 1)[0] in self.harmonization["event"]
            ):
                result[parameter] = message.get(value)
            else:
                result[parameter] = value
        return result

    def _custom_mapping(self, obj: "MISPObject", message: Message):
        """Map the IntelMQ event to the MISP Object using the custom mapping definition."""
        for object_relation, definition in self.attribute_mapping.items():
            if object_relation in message:
                obj.add_attribute(
                    object_relation,
                    value=message[object_relation],
                    **self._extract_misp_attribute_kwargs(message, definition),
                )
                # In case of custom mapping, we want to fail if it produces incorrect values

    def _generate_misp_feed(self, message: dict = None):
        if message:
            self._add_message_to_misp_event(message)

        message = self.cache_pop()
        while message:
            self._add_message_to_misp_event(message)
            message = self.cache_pop()

        for key, event in self.current_events.items():
            feed_output = event.to_feed(with_meta=False)
            with self.current_files[key].open("w") as f:
                json.dump(feed_output, f)

        feed_meta_generator(self.output_dir)

    @staticmethod
    def check(parameters):
        results = []
        if "output_dir" not in parameters:
            results.append(["error", "Parameter 'output_dir' not given."])
        else:
            try:
                created = MISPFeedOutputBot.check_output_dir(parameters["output_dir"])
            except OSError:
                results.append(
                    [
                        "error",
                        "Directory %r of parameter 'output_dir' does not exist and could not be created."
                        % parameters["output_dir"],
                    ]
                )
            else:
                if created:
                    results.append(
                        [
                            "info",
                            "Directory %r of parameter 'output_dir' did not exist, but has now been created."
                            "" % parameters["output_dir"],
                        ]
                    )

        bulk_save_count = parameters.get("bulk_save_count")
        if bulk_save_count and not isinstance(bulk_save_count, int):
            results.append(
                ["error", "Parameter 'bulk_save_count' has to be int if set."]
            )

        sanity_event = Event({})
        event_separator = parameters.get("event_separator")
        if (
            event_separator
            and not sanity_event._Message__is_valid_key(event_separator)[0]
        ):
            results.append(
                [
                    "error",
                    f"Value {event_separator} in 'event_separator' is not a valid event key.",
                ]
            )

        not_feed_field_warning = (
            "Parameter '{parameter}' of {context} looks like not being a field exportable to"
            " MISP Feed. It may be a valid PyMISP parameter, but won't be exported to the feed."
            " Please ensure it's intended and consult PyMISP documentation at https://pymisp.readthedocs.io/"
            " for valid parameters for the {object}."
        )
        attribute_mapping = parameters.get("attribute_mapping")
        if attribute_mapping:
            if not isinstance(attribute_mapping, dict):
                results.append(
                    ["error", "Parameter 'attribute_mapping has to be a dictionary."]
                )
            else:
                for key, value in attribute_mapping.items():
                    if not sanity_event._Message__is_valid_key(key)[0]:
                        results.append(
                            [
                                "error",
                                f"The key '{key}' in attribute_mapping is not a valid IDF field.",
                            ]
                        )
                    if not isinstance(value, dict):
                        results.append(
                            [
                                "error",
                                f"The config attribute_mapping['{key}'] should be a "
                                "dict with parameters for MISPObjectAttribute.",
                            ]
                        )
                    else:
                        for parameter in value.keys():
                            if parameter not in MISPObjectAttribute._fields_for_feed:
                                results.append(
                                    [
                                        "warning",
                                        not_feed_field_warning.format(
                                            parameter=parameter,
                                            context=f"attribute_mapping['{key}']",
                                            object="MISPObjectAttribute",
                                        ),
                                    ]
                                )

        tagging = parameters.get("tagging")
        if tagging:
            tagging_error = (
                "should be a list of dictionaries with parameters for the MISPTag object."
                " Please consult PyMISP documentation at https://pymisp.readthedocs.io/"
                " to find valid fields."
            )
            if not isinstance(tagging, dict):
                results.append(
                    [
                        "error",
                        (
                            "Parameter 'tagging' has to be a dictionary with keys as '__all__' "
                            "or possible 'event_separator' values. Each dictionary value "
                            + tagging_error,
                        ),
                    ]
                )
            else:
                if not event_separator and (
                    "__all__" not in tagging or len(tagging.keys()) > 1
                ):
                    results.append(
                        [
                            "error",
                            (
                                "Tagging configuration expects custom values, but the 'event_separator'"
                                " parameter is not set. If you want to just tag all events, use only"
                                " the '__all__' key."
                            ),
                        ]
                    )
                for key, value in tagging.items():
                    if not isinstance(value, list):
                        results.append(
                            [
                                "error",
                                f"The config tagging['{key}'] {tagging_error}",
                            ]
                        )
                    else:
                        for tag in value:
                            if not isinstance(tag, dict):
                                results.append(
                                    [
                                        "error",
                                        f"The config tagging['{key}'] {tagging_error}",
                                    ]
                                )
                            else:
                                if "name" not in tag:
                                    results.append(
                                        [
                                            "error",
                                            f"The config tagging['{key}'] contains a tag without 'name'.",
                                        ]
                                    )
                                for parameter in tag.keys():
                                    if parameter not in MISPTag._fields_for_feed:
                                        results.append(
                                            [
                                                "warning",
                                                not_feed_field_warning.format(
                                                    parameter=parameter,
                                                    context=f"tagging['{key}']",
                                                    object="MISPTag",
                                                ),
                                            ]
                                        )

        return results or None


BOT = MISPFeedOutputBot
