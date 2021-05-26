# -*- coding: utf-8 -*-
"""
Cut string if length is bigger than max
"""
from intelmq.lib.bot import Bot


class StringCutDelimiterExpertBot(Bot):
    string_delimiter: str = '.'
    max_length: int = 200
    field_for_cut: str = 'source.fqdn'

    def init(self):
        pass

    def process(self):
        event = self.receive_message()

        if self.field_for_cut in event:
            long_string = event[self.field_for_cut]
            while (long_string.find(self.string_delimiter) != -1) and (len(long_string) > self.max_length):
                long_string = long_string.split(self.string_delimiter, 1)[1]
            event.change(self.field_for_cut, long_string)

        self.send_message(event)
        self.acknowledge_message()


BOT = StringCutDelimiterExpertBot
