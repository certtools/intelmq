"""
RPZ file output

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

from datetime import datetime
import os
from collections import defaultdict
from pathlib import Path

from intelmq.lib.bot import OutputBot

RPZ_INDICATOR_MAP = {
    "source.fqdn": "Intel::DOMAIN"
}

now = datetime.now()  # for timestamp


class RpzFileOutputBot(OutputBot):
    _file = None
    format_filename: bool = False
    hierarchical_output: bool = False
    keep_raw_field: bool = False
    message_jsondict_as_string: bool = False
    message_with_type: bool = False
    single_key: bool = False
    _is_multithreadable = False

    encoding_errors_mode = 'strict'
    file: str = "/opt/intelmq/var/lib/bots/file-output/rpz"

    cname: str = ""
    organization_name: str = ''
    rpz_domain: str = ''
    hostmaster_rpz_domain: str = ''
    rpz_email: str = ''
    ttl: int = 3600
    generate_time: str = now.strftime("%Y-%m-%d %H:%M:%S")
    ncachttl: int = 60
    serial: str = now.strftime("%y%m%d%H%M")
    refresh: int = 60
    retry: int = 60
    expire: int = 432000
    dns_record_type: str = 'CNAME'
    test_domain: str = ''

    _rpz_header = ""

    def init(self):
        self._file = None

        self.set_rpz_header()

        self.logger.debug("Opening %r file.", self.file)
        self.format_filename = getattr(self, 'format_filename', False)
        self.errors = getattr(self, 'encoding_errors_mode', 'strict')
        if not self.format_filename:
            self.open_file(self.file)
        self.logger.info("File %r is open.", self.file)

    def set_rpz_header(self):
        generate_time: str = now.strftime("%Y-%m-%d %H:%M:%S")
        self._rpz_header = f"""$TTL """ + str(self.ttl) + """
@ SOA """ + self.rpz_domain + """. """ + self.hostmaster_rpz_domain + """. """ + str(self.serial) + """ """ + str(self.refresh) + """ """ + str(self.retry) + """ """ + str(self.expire) + """ """ + str(self.ncachttl) + """
 NS localhost.
;
; """ + self.organization_name + """ Response Policy Zones (RPZ)
; Last updated: """ + str(generate_time) + """ (UTC)
;
; Terms Of Use: https://""" + self.rpz_domain + """
; For questions please contact """ + self.rpz_email + """
;\n"""

        if self.test_domain:
            self._rpz_header = self._rpz_header + self.test_domain + " " + self.dns_record_type + " " + self.cname + "\n"  # for test

    def open_file(self, filename: str = None):
        if self._file is not None:
            self._file.close()

        try:
            self._file = open(filename, mode='a+t', encoding='utf-8', errors=self.errors)
            self.add_rpz_header()
        except FileNotFoundError:  # directory does not exist
            path = Path(os.path.dirname(filename))
            try:
                path.mkdir(mode=0o755, parents=True, exist_ok=True)
            except OSError:
                self.logger.exception('Directory %r could not be created.', path)
                self.stop()
            else:
                self._file = open(filename, mode='a+t', encoding='utf-8', errors=self.errors)
                self.add_rpz_header()

    def add_rpz_header(self):
        self._file.seek(0)
        if not (len(self._file.read())):
            self._file.write(self._rpz_header)
            self._file.flush()

    def process(self):
        event = self.receive_message()
        if self.format_filename:
            ev = defaultdict(None)
            ev.update(event)
            if 'time.observation' in ev:
                try:
                    ev['time.observation'] = datetime.strptime(ev['time.observation'], '%Y-%m-%dT%H:%M:%S+00:00')
                except ValueError:
                    ev['time.observation'] = datetime.strptime(ev['time.observation'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
            if 'time.source' in ev:
                try:
                    ev['time.source'] = datetime.strptime(ev['time.source'], '%Y-%m-%dT%H:%M:%S+00:00')
                except ValueError:
                    ev['time.source'] = datetime.strptime(ev['time.source'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
            filename = self.file.format(event=ev)
            if not self.file or filename != self._file.name:
                self.open_file(filename)
        acknowledge_message = False
        for indicator_type in RPZ_INDICATOR_MAP.keys():
            if event.get(indicator_type):
                domain_url = event['source.fqdn']
                if domain_url.startswith('www.'):
                    domain_url = domain_url[len('www.'):]
                event_data = domain_url + ' ' + self.dns_record_type + ' ' + self.cname + '\n'
                event_data = event_data + 'www.' + domain_url + ' ' + self.dns_record_type + ' ' + self.cname + '\n'

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
                    self.logger.debug("Event did not have RPZ indicator types.")

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


BOT = RpzFileOutputBot
