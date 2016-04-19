# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime, timedelta

import pytz
from dateutil import parser

from intelmq.lib.bot import Bot


class FilterExpertBot(Bot):

    # number of minutes in time units
    timespans = {'hour': 60, 'day': 24 * 60, 'week': 7 * 24 * 60,
                 'month': 30 * 24 * 60, 'year': 365 * 24 * 60}

    # parse relative time attributes
    @staticmethod
    def parse_relative(relative_time):
        try:
            result = re.findall(r'^(\d+)\s+(\w+[^s])s?$', relative_time, re.UNICODE)
        except ValueError as e:
            raise ValueError("Could not apply regex to attribute \"%s\" with exception %s",
                             repr(relative_time), repr(e.args))
        if len(result) == 1 and len(result[0]) == 2 and result[0][1] in FilterExpertBot.timespans:
            return int(result[0][0]) * FilterExpertBot.timespans[result[0][1]]
        else:
            raise ValueError("Could not process result of regex for attribute " + repr(relative_time))

    # decide format of timefilter value and parse it
    def parse_timeattr(self, time_attr):
        try:
            absolute = parser.parse(time_attr)
        except ValueError:
            relative = timedelta(minutes=self.parse_relative(time_attr))
            self.logger.info("Filtering out events to (relative time) " + repr(relative))
            return relative
        else:
            self.logger.info("Filtering out events to (absolute time) " + repr(absolute))
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

        if not (self.filter or self.not_after is not None or self.not_before is not None):
            self.logger.error("No relevant filter configuration found, stopping...")
            self.stop()

    def process(self):
        event = self.receive_message()

        # time based filtering
        if event.contains('time.source'):
            try:
                event_time = parser.parse(str(event.get('time.source'))).replace(tzinfo=pytz.timezone('UTC'))
            except ValueError:
                self.logger.error("Could not parse time.source " + str(event.get('time.source')))
            else:
                if type(self.not_after) is datetime and event_time > self.not_after:
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source " + repr(event.get('time.source')))
                    return
                if type(self.not_before) is datetime and event_time < self.not_before:
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source " + repr(event.get('time.source')))
                    return

                now = datetime.now(tz=pytz.timezone('UTC'))
                if type(self.not_after) is timedelta and event_time > (now - self.not_after):
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source " + repr(event.get('time.source')))
                    return
                if type(self.not_before) is timedelta and event_time < (now - self.not_before):
                    self.acknowledge_message()
                    self.logger.debug("Filtered out event with time.source " + repr(event.get('time.source')))
                    return

        # key/value based filtering
        if self.filter and self.parameters.filter_action == "drop":
            if (event.contains(self.parameters.filter_key) and
                    event.get(self.parameters.filter_key) ==
                    self.parameters.filter_value):
                self.acknowledge_message()
                return
            else:
                self.send_message(event)
                self.acknowledge_message()
                return

        if self.filter and self.parameters.filter_action == "keep":
            if (event.contains(self.parameters.filter_key) and
                    event.get(self.parameters.filter_key) ==
                    self.parameters.filter_value):
                self.send_message(event)
                self.acknowledge_message()
                return
            else:
                self.acknowledge_message()
                return

        self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = FilterExpertBot(sys.argv[1])
    bot.start()
