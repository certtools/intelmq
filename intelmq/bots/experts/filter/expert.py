# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta, timezone

from dateutil import parser

from intelmq.lib.bot import ExpertBot
from intelmq.lib.utils import parse_relative, TIMESPANS


class FilterExpertBot(ExpertBot):
    """Filter events, supports named paths for splitting the message flow"""

    _message_processed_verb = 'Forwarded'
    not_after = None
    not_before = None
    filter_action: str = None
    filter_key: str = None
    filter_regex: str = None  # TODO: could be re
    filter_value: str = None

    def parse_timeattr(self, time_attr):
        """
        Parses relative or absolute time specification, decides how to parse by
        checking if the string contains any timespan identifier.

        See also https://github.com/certtools/intelmq/issues/1523
        dateutil.parser.parse detects strings like `10 hours` as absolute time.
        """
        if any([timespan in time_attr for timespan in TIMESPANS.keys()]):
            relative = timedelta(minutes=parse_relative(time_attr))
            self.logger.info("Filtering out events to (relative time) %r.", relative)
            return relative
        else:
            absolute = parser.parse(time_attr)
            self.logger.info("Filtering out events to (absolute time) %r.", absolute)
            return absolute

    def init(self):
        if self.not_after:
            self.not_after = self.parse_timeattr(self.not_after)
        if self.not_before:
            self.not_before = self.parse_timeattr(self.not_before)

        self.filter = True
        if self.filter_key is None:
            self.logger.info("No filter_key parameter found.")
            self.filter = False
        elif self.filter_value is None:
            self.logger.info("No filter_value parameter found.")
            self.filter = False
        elif self.filter_action is None:
            self.logger.info("No filter_action parameter found.")
            self.filter = False
        elif self.filter_action is not None and not \
            (self.filter_action == "drop" or
             self.filter_action == "keep"):
            self.logger.info("Filter_action parameter definition unknown.")
            self.filter = False

        self.regex = False
        if self.filter_regex is not None:
            self.regex = re.compile(self.filter_value)

        self.time_filter = self.not_after is not None or self.not_before is not None

        if not (self.filter or self.time_filter):
            raise ValueError("No relevant filter configuration found.")

    def process(self):
        event = self.receive_message()

        # time based filtering
        if self.time_filter and 'time.source' in event:
            try:
                event_time = parser.parse(str(event.get('time.source'))).replace(tzinfo=timezone.utc)
            except ValueError:
                self.logger.error("Could not parse time.source %s.", event.get('time.source'))
            else:
                if type(self.not_after) is datetime and event_time > self.not_after:
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source %s.", event.get('time.source'))
                    return
                if type(self.not_before) is datetime and event_time < self.not_before:
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source %r.", event.get('time.source'))
                    return

                now = datetime.now(tz=timezone.utc)
                if type(self.not_after) is timedelta and event_time > (now - self.not_after):
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source %r.", event.get('time.source'))
                    return
                if type(self.not_before) is timedelta and event_time < (now - self.not_before):
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source %r.", event.get('time.source'))
                    return

        # key/value based filtering
        if self.filter and self.filter_action == "drop":
            if self.doFilter(event, self.filter_key,
                             self.filter_value):
                # action == drop, filter matches
                self.send_message(event, path='action_other',
                                  path_permissive=True)
                self.send_message(event, path='filter_match',
                                  path_permissive=True)
                self.acknowledge_message()
                return
            else:
                # action == drop, filter not matches
                self.send_message(event, path='filter_no_match',
                                  path_permissive=True)
                self.send_message(event)
                self.acknowledge_message()
                return

        if self.filter and self.filter_action == "keep":
            if self.doFilter(event, self.filter_key,
                             self.filter_value):
                # action == keep, filter matches
                self.send_message(event, path='filter_match',
                                  path_permissive=True)
                self.send_message(event)
                self.acknowledge_message()
                return
            else:
                # action == keep, filter not matches
                self.send_message(event, path='action_other',
                                  path_permissive=True)
                self.send_message(event, path='filter_no_match',
                                  path_permissive=True)
                self.acknowledge_message()
                return

        self.send_message(event)
        self.acknowledge_message()

    def doFilter(self, event, key, condition):
        if self.regex:
            return self.regexSearchFilter(event, key)
        else:
            return self.equalsFilter(event, key, condition)

    def equalsFilter(self, event, key, value):
        return (key in event and
                event.get(key) == value)

    def regexSearchFilter(self, event, key):
        if key in event:
            return self.regex.search(str(event.get(key)))
        else:
            return False


BOT = FilterExpertBot
