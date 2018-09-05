# -*- coding: utf-8 -*-
import datetime
import os
from pathlib import Path
from collections import defaultdict

from intelmq.lib.bot import Bot
from intelmq.lib.utils import base64_decode


class FileOutputBot(Bot):
    file = None

    def init(self):
        # needs to be done here, because in process() FileNotFoundError handling we call init(),
        # otherwise the file would not be opened again
        self.file = None

        self.logger.debug("Opening %r file.", self.parameters.file)
        self.format_filename = getattr(self.parameters, 'format_filename', False)
        self.errors = getattr(self.parameters, 'encoding_errors_mode', 'strict')
        if not self.format_filename:
            self.open_file(self.parameters.file)
        self.logger.info("File %r is open.", self.parameters.file)
        self.single_key = getattr(self.parameters, 'single_key', None)

    def open_file(self, filename: str = None):
        if self.file is not None:
            self.file.close()
        try:
            self.file = open(filename, mode='at', encoding='utf-8', errors=self.errors)
        except FileNotFoundError:  # directory does not exist
            path = Path(os.path.dirname(filename))
            try:
                path.mkdir(mode=0o755, parents=True, exist_ok=True)
            except IOError:
                self.logger.exception('Directory %r could not be created.', path)
                self.stop()
            else:
                self.file = open(filename, mode='at', encoding='utf-8', errors=self.errors)

    def process(self):
        event = self.receive_message()
        if self.format_filename:
            ev = defaultdict(None)
            ev.update(event)
            # remove once #671 is done
            if 'time.observation' in ev:
                ev['time.observation'] = datetime.datetime.strptime(ev['time.observation'],
                                                                    '%Y-%m-%dT%H:%M:%S+00:00')
            if 'time.source' in ev:
                ev['time.source'] = datetime.datetime.strptime(ev['time.source'],
                                                               '%Y-%m-%dT%H:%M:%S+00:00')
            filename = self.parameters.file.format(event=ev)
            if not self.file or filename != self.file.name:
                self.open_file(filename)

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
        if self.file:
            self.file.close()

    @staticmethod
    def check(parameters):
        if 'file' not in parameters:
            return [["error", "Parameter 'file' not given."]]
        dirname = os.path.dirname(parameters['file'])
        if not os.path.exists(dirname) and '{ev' not in dirname:
            path = Path(dirname)
            try:
                path.mkdir(mode=0o755, parents=True, exist_ok=True)
            except IOError:
                return [["error", "Directory (%r) of parameter 'file' does not exist and could not be created." % dirname]]
            else:
                return [["info", "Directory (%r) of parameter 'file' did not exist, but has now been created." % dirname]]


BOT = FileOutputBot
