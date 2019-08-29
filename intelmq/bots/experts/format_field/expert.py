# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot


class FormatFieldExpertBot(Bot):

    def init(self):
        self.strip_columns   = getattr(self.parameters, 'strip_columns', None)
        if type(self.strip_columns) is str:
            self.strip_columns = [column.strip() for column in self.strip_columns.split(",")]
        self.strip_chars     = getattr(self.parameters, 'strip_chars', ' ')
        self.split_column    = getattr(self.parameters, 'split_column', None)
        self.split_separator = getattr(self.parameters, 'split_separator', ',')
        self.replace_column  = getattr(self.parameters, 'replace_column', None)
        self.old_value       = getattr(self.parameters, 'old_value', None)
        self.new_value       = getattr(self.parameters, 'new_value', None)
        self.replace_count   = getattr(self.parameters, 'replace_count', 1)

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
