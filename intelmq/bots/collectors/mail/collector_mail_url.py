# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Uses the common mail iteration method from the lib file.
"""
import io
import re

from intelmq.lib.mixins import HttpMixin
from intelmq.lib.splitreports import generate_reports
from intelmq.lib.utils import file_name_from_response

from ._lib import MailCollectorBot


class MailURLCollectorBot(MailCollectorBot, HttpMixin):
    """Monitor IMAP mailboxes and fetch files from URLs contained in mail bodies"""
    chunk_replicate_header: bool = True
    chunk_size: int = None
    folder: str = "INBOX"
    http_password: str = None
    http_username: str = None
    mail_host: str = "<host>"
    mail_password: str = "<password>"
    mail_ssl: bool = True
    mail_user: str = "<user>"
    rate_limit: int = 60
    ssl_client_certificate: str = None  # TODO pathlib.Path
    subject_regex: str = "<subject>"
    url_regex: str = "http://"

    def init(self):
        super().init()

    def process_message(self, uid, message):
        erroneous = False  # If errors occurred this will be set to true.
        seen = False

        for body in message.body['plain']:
            match = re.search(self.url_regex, str(body.decode('utf-8') if isinstance(body, bytes) else body))
            if match:
                url = match.group()
                # strip leading and trailing spaces, newlines and
                # carriage returns
                url = url.strip()

                self.logger.info("Downloading report from %r.", url)
                try:
                    resp = self.http_get(url)
                except requests.exceptions.Timeout:
                    self.logger.error("Request timed out %i times in a row." %
                                      self.http_timeout_max_tries)
                    erroneous = True
                    # The download timed out too often, leave the Loop.
                    continue

                if resp.status_code // 100 != 2:
                    self.logger.error('HTTP response status code was {}.'
                                      ''.format(resp.status_code))
                    erroneous = True
                    continue

                if not resp.content:
                    self.logger.warning('Got empty response from server.')
                else:
                    self.logger.info("Report downloaded.")

                    template = self.new_report()
                    template["feed.url"] = url
                    template["extra.email_subject"] = message.subject
                    template["extra.email_from"] = ','.join(x['email'] for x in message.sent_from)
                    template["extra.email_message_id"] = message.message_id
                    template["extra.file_name"] = file_name_from_response(resp)
                    template["extra.email_date"] = message.date

                    for report in generate_reports(template, io.BytesIO(resp.content),
                                                   self.chunk_size,
                                                   self.chunk_replicate_header):
                        self.send_message(report)

                seen = True

        if not erroneous:
            self.logger.info("Email report read.")
        else:
            if self.error_procedure == 'pass':
                seen = True
            else:
                self.logger.error("Email report read with above errors, the report was not processed.")

        return seen


BOT = MailURLCollectorBot
