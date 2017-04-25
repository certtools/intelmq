# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta

import pytz
from dateutil import parser

from intelmq.lib.bot import Bot
from intelmq.lib.utils import parse_relative


class FilterExpertBot(Bot):

    # decide format of timefilter value and parse it
    def parse_timeattr(self, time_attr):
        try:
            absolute = parser.parse(time_attr)
        except ValueError:
            relative = timedelta(minutes=parse_relative(time_attr))
            self.logger.info("Filtering out events to (relative time) %r.", relative)
            return relative
        else:
            self.logger.info("Filtering out events to (absolute time) %r.", absolute)
            return absolute
        return None

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

        self.use_regex = False
        if hasattr(self.parameters, 'filter_regex') and self.parameters.filter_regex:
            self.use_regex = True

        if not (self.filter or self.not_after is not None or self.not_before is not None):
            raise ValueError("No relevant filter configuration found.")

    def process(self):
        event = self.receive_message()

        # time based filtering
        if 'time.source' in event:
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
                self.acknowledge_message()
                return
            else:
                self.send_message(event)
                self.acknowledge_message()
                return

        if self.filter and self.parameters.filter_action == "keep":
            if self.doFilter(event, self.parameters.filter_key,
                             self.parameters.filter_value):
                self.send_message(event)
                self.acknowledge_message()
                return
            else:
                self.acknowledge_message()
                return

        self.send_message(event)
        self.acknowledge_message()

    def doFilter(self, event, key, condition):
        if self.use_regex:
            return self.regexSearchFilter(event, key, condition)
        else:
            return self.equalsFilter(event, key, condition)

    def equalsFilter(self, event, key, value):
        return (key in event and
                event.get(key) == value)

    def regexSearchFilter(self, event, key, regex):
        if key in event:
            exp = re.compile(regex)
            return exp.search(str(event.get(key)))
        else:
            return False


BOT = FilterExpertBot
