# -*- coding: utf-8 -*-
"""
Cut string if length is bigger than max

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from intelmq.lib.bot import ExpertBot


class TruncateByDelimiterExpertBot(ExpertBot):
    delimiter: str = '.'
    max_length: int = 200
    field: str = 'source.fqdn'

    def process(self):
        event = self.receive_message()

        if self.field in event:
            long_string = event[self.field]
            while self.delimiter in long_string and len(long_string) > self.max_length:
                long_string = long_string.split(self.delimiter, 1)[1]
            event.change(self.field, long_string)

        self.send_message(event)
        self.acknowledge_message()


BOT = TruncateByDelimiterExpertBot
