# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta

import pytz
from dateutil import parser

from intelmq.lib.bot import Bot
from intelmq.lib.utils import parse_relative, TIMESPANS


class FilterExpertBot(Bot):

    _message_processed_verb = 'Forwarded'

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
        self.not_after = None
        self.not_before = None

        if hasattr(self.parameters, 'not_after'):
            self.not_after = self.parse_timeattr(self.parameters.not_after)
        if hasattr(self.parameters, 'not_before'):
            self.not_before = self.parse_timeattr(self.parameters.not_before)

        self.filter = True
        if not (hasattr(self.parameters, 'filter_key')):
            self.logger.info("No filter_key parameter found.")
            self.filter = False
        elif not (hasattr(self.parameters, 'filter_value')):
            self.logger.info("No filter_value parameter found.")
            self.filter = False
        elif not (hasattr(self.parameters, 'filter_action')):
            self.logger.info("No filter_action parameter found.")
            self.filter = False
        elif hasattr(self.parameters, 'filter_action') and not \
            (self.parameters.filter_action == "drop" or
             self.parameters.filter_action == "keep"):
            self.logger.info("Filter_action parameter definition unknown.")
            self.filter = False

        self.regex = False
        if hasattr(self.parameters, 'filter_regex') and self.parameters.filter_regex:
            self.regex = re.compile(self.parameters.filter_value)

        self.time_filter = self.not_after is not None or self.not_before is not None

        if not (self.filter or self.time_filter):
            raise ValueError("No relevant filter configuration found.")

    def process(self):
        event = self.receive_message()

        # time based filtering
        if self.time_filter and 'time.source' in event:
            try:
                event_time = parser.parse(str(event.get('time.source'))).replace(tzinfo=pytz.timezone('UTC'))
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

                now = datetime.now(tz=pytz.timezone('UTC'))
                if type(self.not_after) is timedelta and event_time > (now - self.not_after):
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source %r.", event.get('time.source'))
                    return
                if type(self.not_before) is timedelta and event_time < (now - self.not_before):
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source %r.", event.get('time.source'))
                    return

        # key/value based filtering
        if self.filter and self.parameters.filter_action == "drop":
            if self.doFilter(event, self.parameters.filter_key,
                             self.parameters.filter_value):
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

        if self.filter and self.parameters.filter_action == "keep":
            if self.doFilter(event, self.parameters.filter_key,
                             self.parameters.filter_value):
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
