"""
Bro file output

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import datetime
import os
from collections import defaultdict
from pathlib import Path

from intelmq.lib.bot import OutputBot

BRO_INDICATOR_MAP = {
    "source.ip": "Intel::ADDR",
    "source.fqdn": "Intel::DOMAIN",
    "source.url": "Intel::URL"
}

BRO_HEADER = "#fields\tindicator\tindicator_type\tmeta.desc\tmeta.cif_confidence\tmeta.source\n"


class BroFileOutputBot(OutputBot):
    _file = None
    encoding_errors_mode = 'strict'
    file: str = "/opt/intelmq/var/lib/bots/file-output/bro"
    format_filename: bool = False
    hierarchical_output: bool = False
    keep_raw_field: bool = False
    message_jsondict_as_string: bool = False
    message_with_type: bool = False
    single_key: bool = False
    is_multithreadable = False

    def init(self):
        # needs to be done here, because in process() FileNotFoundError handling we call init(),
        # otherwise the file would not be opened again
        self._file = None

        self.logger.debug("Opening %r file.", self.file)
        if not self.format_filename:
            self.open_file(self.file)
        self.logger.info("File %r is open.", self.file)

    def open_file(self, filename: str = None):
        if self._file is not None:
            self._file.close()
        try:
            self._file = open(filename, mode='a+t', encoding='utf-8', errors=self.encoding_errors_mode)
            self.add_bro_header()
        except FileNotFoundError:  # directory does not exist
            path = Path(os.path.dirname(filename))
            try:
                path.mkdir(mode=0o755, parents=True, exist_ok=True)
            except OSError:
                self.logger.exception('Directory %r could not be created.', path)
                self.stop()
            else:
                self._file = open(filename, mode='a+t', encoding='utf-8', errors=self.encoding_errors_mode)
                self.add_bro_header()

    def add_bro_header(self):
        self._file.seek(0)
        if self._file.readline() != BRO_HEADER:
            self._file.write(BRO_HEADER)
            self._file.flush()

    def process(self):
        event = self.receive_message()
        if self.format_filename:
            ev = defaultdict(None)
            ev.update(event)
            if 'time.observation' in ev:
                try:
                    ev['time.observation'] = datetime.datetime.strptime(ev['time.observation'],
                                                                        '%Y-%m-%dT%H:%M:%S+00:00')
                except ValueError:
                    ev['time.observation'] = datetime.datetime.strptime(ev['time.observation'],
                                                                        '%Y-%m-%dT%H:%M:%S.%f+00:00')
            if 'time.source' in ev:
                try:
                    ev['time.source'] = datetime.datetime.strptime(ev['time.source'],
                                                                   '%Y-%m-%dT%H:%M:%S+00:00')
                except ValueError:
                    ev['time.source'] = datetime.datetime.strptime(ev['time.source'],
                                                                   '%Y-%m-%dT%H:%M:%S.%f+00:00')
            filename = self.file.format(event=ev)
            if not self.file or filename != self._file.name:
                self.open_file(filename)
        acknowledge_message = False
        for indicator_type in BRO_INDICATOR_MAP.keys():
            if event.get(indicator_type):
                event_data = ''
                event_data += event[indicator_type] + '\t'
                event_data += BRO_INDICATOR_MAP[indicator_type] + '\t'
                if "extra.tags" in event and "apt" in event["extra.tags"]:
                    event_data += 'apt' + '\t'
                else:
                    event_data += event['classification.type'] + '\t'
                event_data += str(int(event['feed.accuracy'])) + '\t'
                if 'extra.orgc' in event:
                    event_data += event['extra.orgc']
                elif 'feed.provider' in event:
                    event_data += event['feed.provider']
                event_data += '\n'
                try:
                    self._file.write(event_data)
                    self._file.flush()
                except FileNotFoundError:
                    self.init()
                else:
                    if not acknowledge_message:
                        self.acknowledge_message()
                        acknowledge_message = True
            else:
                if not acknowledge_message:
                    self.acknowledge_message()
                    acknowledge_message = True
                    self.logger.debug(str(indicator_type) + "Event did not have Bro indicator types.")

    def shutdown(self):
        if self._file:
            self._file.close()

    @staticmethod
    def check(parameters):
        if 'file' not in parameters:
            return [["error", "Parameter 'file' not given."]]
        dirname = os.path.dirname(parameters['file'])
        if not os.path.exists(dirname) and '{ev' not in dirname:
            path = Path(dirname)
            try:
                path.mkdir(mode=0o755, parents=True, exist_ok=True)
            except OSError:
                return [
                    ["error", "Directory (%r) of parameter 'file' does not exist and could not be created." % dirname]]
            else:
                return [
                    ["info", "Directory (%r) of parameter 'file' did not exist, but has now been created." % dirname]]


BOT = BroFileOutputBot
