# SPDX-FileCopyrightText: 2019 Brajneesh kumar
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot


class FormatFieldExpertBot(Bot):
    """Perform string method operations on column values"""
    new_value       = ""
    old_value       = ""
    replace_column  = ""
    replace_count   = 1
    strip_columns   = ""
    split_separator = ','
    strip_chars     = ' '
    split_column    = None

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
