# -*- coding: utf-8 -*-
import csv
import io
from intelmq.lib.bot import Bot


class CSVConverterExpertBot(Bot):

    def init(self):
        self.fieldnames = self.parameters.fieldnames.split(',')
        self.delimiter = getattr(self.parameters, 'delimiter', ',')

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
