# -*- coding: utf-8 -*-
import io
import os

from intelmq.lib.bot import Bot

from intelmq.lib.utils import base64_decode


class FileOutputBot(Bot):

    def init(self):
        self.logger.debug("Opening %r file.", self.parameters.file)
        self.file = io.open(self.parameters.file, mode='at', encoding="utf-8")
        self.logger.info("File %r is open.", self.parameters.file)
        self.single_key = getattr(self.parameters, 'single_key', None)

    def process(self):
        event = self.receive_message()
        event.set_default_value(None)
        filename = self.parameters.file.format(event=event)
        if filename != self.file.name:
            self.file.close()
            self.file = open(filename, mode='at', encoding='utf-8')

        if self.single_key:
            event_data = str(event.get(self.single_key))
            if self.single_key == 'raw':
                event_data = base64_decode(event_data)
        else:
            event_data = event.to_json(hierarchical=self.parameters.hierarchical_output)

        try:
            self.file.write(event_data)
            self.file.write("\n")
            self.file.flush()
        except FileNotFoundError:
            self.init()
        else:
            self.acknowledge_message()

    def shutdown(self):
        self.file.close()

    @staticmethod
    def check(parameters):
        if 'file' not in parameters:
            return [["error", "Parameter 'file' not given."]]
        dirname = os.path.dirname(parameters['file'])
        if not os.path.exists(dirname):
            return [["error", "Directory (%r) of parameter 'file' does not exist." % dirname]]


BOT = FileOutputBot
