# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot


class FormatFieldExpertBot(Bot):
    strip_columns = None
    strip_chars     = ' '
    split_column    = None
    split_separator = ','
    replace_column  = None
    old_value       = None
    new_value       = None
    replace_count   = 1

    def init(self):
        if type(self.strip_columns) is str:
            self.strip_columns = [column.strip() for column in self.strip_columns.split(",")]

    def process(self):
        event = self.receive_message()

        if self.strip_columns:
            for column in self.strip_columns:
                value = event.get(column, None)
                if value:
                    event.add(column, value.strip(self.strip_chars), overwrite=True)

        if self.replace_column:
            value = event.get(self.replace_column, None)
            if value:
                event.add(self.replace_column, value.replace(self.old_value, self.new_value, self.replace_count), overwrite=True)

        if self.split_column:
            value = event.get(self.split_column, None)
            if value:
                event.add(self.split_column, value.split(self.split_separator), overwrite=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = FormatFieldExpertBot
