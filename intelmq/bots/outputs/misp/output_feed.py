# SPDX-FileCopyrightText: 2019 Sebastian Wagner
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
from intelmq.lib.mixins import CacheMixin
from intelmq.lib.utils import parse_relative

try:
    from pymisp import MISPEvent, MISPOrganisation, NewAttributeError
    from pymisp.tools import feed_meta_generator
except ImportError:
    # catching SyntaxError because of https://github.com/MISP/PyMISP/issues/501
    MISPEvent = None
    import_fail_reason = "import"


class MISPFeedOutputBot(OutputBot, CacheMixin):
    """Generate an output in the MISP Feed format"""

    interval_event: str = "1 hour"
    delay_save_event_count: int = None
    misp_org_name = None
    misp_org_uuid = None
    output_dir: str = "/opt/intelmq/var/lib/bots/mispfeed-output"  # TODO: should be path
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

        self.current_event = None

        self.misp_org = MISPOrganisation()
        self.misp_org.name = self.misp_org_name
        self.misp_org.uuid = self.misp_org_uuid

        self.output_dir = Path(self.output_dir)
        MISPFeedOutputBot.check_output_dir(self.output_dir)

        if self.interval_event is None:
            self.timedelta = datetime.timedelta(hours=1)
        else:
            self.timedelta = datetime.timedelta(minutes=parse_relative(self.interval_event))

        if (self.output_dir / '.current').exists():
            try:
                with (self.output_dir / '.current').open() as f:
                    self.current_file = Path(f.read())

                if self.current_file.exists():
                    self.current_event = MISPEvent()
                    self.current_event.load_file(self.current_file)

                    last_min_time, last_max_time = re.findall(
                        "IntelMQ event (.*) - (.*)", self.current_event.info
                    )[0]
                    last_min_time = datetime.datetime.strptime(
                        last_min_time, "%Y-%m-%dT%H:%M:%S.%f"
                    )
                    last_max_time = datetime.datetime.strptime(
                        last_max_time, "%Y-%m-%dT%H:%M:%S.%f"
                    )
                    if last_max_time < datetime.datetime.now():
                        self.min_time_current = datetime.datetime.now()
                        self.max_time_current = self.min_time_current + self.timedelta
                        self.current_event = None
                    else:
                        self.min_time_current = last_min_time
                        self.max_time_current = last_max_time
            except:
                self.logger.exception(
                    "Loading current event %s failed. Skipping it.", self.current_event
                )
                self.current_event = None
        else:
            self.min_time_current = datetime.datetime.now()
            self.max_time_current = self.min_time_current + self.timedelta

    def process(self):
        if not self.current_event or datetime.datetime.now() > self.max_time_current:
            self.min_time_current = datetime.datetime.now()
            self.max_time_current = self.min_time_current + self.timedelta
            self.current_event = MISPEvent()
            self.current_event.info = "IntelMQ event {begin} - {end}" "".format(
                begin=self.min_time_current.isoformat(),
                end=self.max_time_current.isoformat(),
            )
            self.current_event.set_date(datetime.date.today())
            self.current_event.Orgc = self.misp_org
            self.current_event.uuid = str(uuid4())
            self.current_file = self.output_dir / f"{self.current_event.uuid}.json"
            with (self.output_dir / ".current").open("w") as f:
                f.write(str(self.current_file))

            # On startup or when timeout occurs, clean the queue to ensure we do not
            # keep events forever because there was not enough generated
            self._generate_feed()

        event = self.receive_message().to_dict(jsondict_as_string=True)

        cache_size = None
        if self.delay_save_event_count:
            cache_size = self.cache_put(event)

        if cache_size is None:
            self._generate_feed(event)
        elif cache_size >= self.delay_save_event_count:
            self._generate_feed()

        self.acknowledge_message()

    def _add_message_to_feed(self, message: dict):
        obj = self.current_event.add_object(name="intelmq_event")
        for object_relation, value in message.items():
            try:
                obj.add_attribute(object_relation, value=value)
            except NewAttributeError:
                # This entry isn't listed in the harmonization file, ignoring.
                pass

    def _generate_feed(self, message: dict = None):
        if message:
            self._add_message_to_feed(message)

        while message := self.cache_pop():
            self._add_message_to_feed(message)

        feed_output = self.current_event.to_feed(with_meta=False)
        with self.current_file.open("w") as f:
            json.dump(feed_output, f)

        feed_meta_generator(self.output_dir)

    @staticmethod
    def check(parameters):
        if 'output_dir' not in parameters:
            return [["error", "Parameter 'output_dir' not given."]]
        try:
            created = MISPFeedOutputBot.check_output_dir(parameters['output_dir'])
        except OSError:
            return [["error",
                     "Directory %r of parameter 'output_dir' does not exist and could not be created." % parameters['output_dir']]]
        else:
            if created:
                return [["info",
                         "Directory %r of parameter 'output_dir' did not exist, but has now been created."
                         "" % parameters['output_dir']]]


BOT = MISPFeedOutputBot
