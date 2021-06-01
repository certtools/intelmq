# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import csv
import io
from intelmq.lib.bot import Bot


class CSVConverterExpertBot(Bot):
    """Convert data to CSV"""
    fieldnames: str = "time.source,classification.type,source.ip"  # TODO: could maybe be List[str]
    delimiter: str = ','

    def init(self):
        self.fieldnames = self.fieldnames.split(',')

    def process(self):
        event = self.receive_message()
        event.set_default_value('')
        out = io.StringIO()
        writer = csv.writer(out, delimiter=self.delimiter)
        row = []
        for field in self.fieldnames:
            row.append(event[field])
        writer.writerow(row)
        event['output'] = out.getvalue().rstrip()

        self.send_message(event)
        self.acknowledge_message()


BOT = CSVConverterExpertBot
