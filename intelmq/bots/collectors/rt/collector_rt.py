# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from typing import Optional

from dateutil import parser

from intelmq.lib.bot import CollectorBot
from intelmq.lib.mixins import HttpMixin
from intelmq.lib.utils import (parse_relative, file_name_from_response, unzip)
from intelmq.lib.exceptions import MissingDependencyError

try:
    import rt
except ImportError:
    rt = None


class RTCollectorBot(CollectorBot, HttpMixin):
    "Fetches attachments and URLs from an Request Tracker ticketing server"
    attachment_regex: str = "\\.csv\\.zip$"  # TODO: type could be re?
    extract_attachment: bool = True
    extract_download: bool = True
    http_password: str = None
    http_username: str = None
    password: str = "password"
    rate_limit: int = 3600
    search_not_older_than: str = None  # TODO: type could be something time,
    search_owner: str = "nobody"
    search_queue: str = "Incident Reports"
    search_requestor: Optional[str] = None
    search_status: str = "new"
    search_subject_like: str = "Report"
    set_status: str = "open"
    ssl_client_certificate: str = None  # TODO: type should be pathlib.Path
    take_ticket: bool = True
    uri: str = "http://localhost/rt/REST/1.0"
    url_regex: str = "https://dl.shadowserver.org/[a-zA-Z0-9?_-]*"  # TODO: type could be re?
    user: str = "intelmq"

    PARAMETER_MAPPING = {'search_owner': 'Owner',
                         'search_queue': 'Queue',
                         'search_requestor': 'Requestor',
                         'search_status': 'Status',
                         'search_subject_like': 'Subject__like',
                         }

    def init(self):
        if rt is None:
            raise MissingDependencyError("rt")

        if self.search_not_older_than is not None:
            try:
                self.not_older_than = parser.parse(self.search_not_older_than)
                self.not_older_than_type = 'absolute'
            except ValueError:
                try:
                    self.not_older_than_relative = timedelta(minutes=parse_relative(self.search_not_older_than))
                except ValueError:
                    self.logger.error("Parameter 'search_not_older_than' could not be parsed. "
                                      "Check your configuration.")
                    raise
                self.not_older_than_type = 'relative'
        else:
            self.not_older_than_type = False

        self._parse_extract_file_parameter('extract_attachment')
        self._parse_extract_file_parameter('extract_download')

    def process(self):
        RT = rt.Rt(self.uri, self.user,
                   self.password)
        if not RT.login():
            raise ValueError('Login failed.')

        if self.not_older_than_type:
            if self.not_older_than_type == 'relative':
                self.not_older_than = datetime.now() - self.not_older_than_relative
            kwargs = {'Created__gt': self.not_older_than.isoformat()}
            self.logger.debug('Searching for tickets newer than %r.', kwargs['Created__gt'])
        else:
            kwargs = {}

        for parameter_name, rt_name in self.PARAMETER_MAPPING.items():
            parameter_value = getattr(self, parameter_name, None)
            if parameter_value:
                kwargs[rt_name] = parameter_value

        query = RT.search(order='Created', **kwargs)
        self.logger.info('%s results on search query.', len(query))

        for ticket in query:
            ticket_id = int(ticket['id'].split('/')[1])
            self.logger.debug('Process ticket %s.', ticket_id)
            content = 'attachment'
            success = False
            if self.attachment_regex:
                for (att_id, att_name, _, _) in RT.get_attachments(ticket_id):
                    if re.search(self.attachment_regex, att_name):
                        self.logger.debug('Found attachment %s: %r.',
                                          att_id, att_name)
                        success = True
                        content = 'attachment'
                        self.extract_files = self.extract_attachment
                        break
            if not success and self.url_regex:
                ticket = RT.get_history(ticket_id)[0]
                created = ticket['Created']
                urlmatch = re.search(self.url_regex, ticket['Content'])
                if urlmatch:
                    content = 'url'
                    self.extract_files = self.extract_download

                    url = urlmatch.group(0)
                    self.logger.debug('Matching URL found %r.', url)
                    success = True
            if not success:
                self.logger.info('No matching attachment or URL found.')
                continue

            report = self.new_report()

            if content == 'attachment':
                attachment = RT.get_attachment_content(ticket_id, att_id)
                created = RT.get_attachment(ticket_id, att_id)['Created']

                raw = attachment
            else:
                resp = self.http_get(url)

                response_code_class = resp.status_code // 100
                if response_code_class != 2:
                    self.logger.error('HTTP response status code for %r was %s. Skipping ticket %d.',
                                      url, resp.status_code, ticket_id)
                    if response_code_class == 4:
                        self.logger.debug('Server response: %r.', resp.text)
                        if self.set_status:
                            RT.edit_ticket(ticket_id, status=self.set_status)
                        if self.take_ticket:
                            try:
                                RT.take(ticket_id)
                            except rt.BadRequest:
                                self.logger.exception("Could not take ticket %s.", ticket_id)
                    else:
                        self.logger.info('Skipping now.')
                        continue
                self.logger.info("Report #%d downloaded.", ticket_id)
                self.logger.debug("Downloaded content has %d bytes.", len(resp.content))
                if self.extract_download:
                    raw = resp.content
                else:
                    raw = resp.text
                report["extra.file_name"] = file_name_from_response(resp)

            report.add("rtir_id", ticket_id)
            report.add("time.observation", created + ' UTC', overwrite=True)
            """
            On RT 3.8 these fields are only available on the original ticket, not the
            first history element as in 4.4
            """
            if "Subject" not in ticket:
                ticket = RT.get_ticket(ticket_id)
            report.add("extra.email_subject", ticket["Subject"])
            report.add("extra.ticket_subject", ticket["Subject"])
            report.add("extra.email_from", ','.join(ticket["Requestors"]))
            report.add("extra.ticket_requestors", ','.join(ticket["Requestors"]))
            report.add("extra.ticket_queue", ticket["Queue"])
            report.add("extra.ticket_status", ticket["Status"])
            report.add("extra.ticket_owner", ticket["Owner"])

            if self.extract_files:
                try:
                    unzipped = unzip(raw, self.extract_files,
                                     return_names=True, logger=self.logger)
                except ValueError:
                    self.logger.error('Could not uncompress the file. Skipping for now.')
                    continue
                for file_name, raw_report in unzipped:
                    """
                    File name priority is:
                        From the archive (zip, tar.gz)
                        From the HTTP Response
                        From the Attachment name
                        For gz attachments, only the last options works
                    """
                    report_new = report.copy()
                    report_new.add("raw", raw_report)
                    report_new.add("extra.file_name", file_name, overwrite=True)
                    if "extra.file_name" not in report_new and att_name.endswith('.gz'):
                        report_new["extra.file_name"] = att_name[:-3]
                    self.send_message(report_new)
            else:
                report.add("raw", raw)
                self.send_message(report)

            if self.take_ticket:
                try:
                    RT.take(ticket_id)
                except rt.BadRequest:
                    self.logger.exception("Could not take ticket %s.", ticket_id)
            if self.set_status:
                RT.edit_ticket(ticket_id, status=self.set_status)


BOT = RTCollectorBot
