# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
In Version 0.9.5 the attachment filename is no longer surrounded by double quotes, see for the discussion:
https://github.com/certtools/intelmq/pull/1134
https://github.com/martinrusev/imbox/commit/7c6cc2fb5f7e39c1496d68f3d432eec19517bf8e#diff-1ae09572064c2e7c225de54ad5b49154

Uses the common mail iteration method from the lib file.
"""
import re
from intelmq.lib.utils import unzip
from intelmq.lib.exceptions import InvalidArgument

from ._lib import MailCollectorBot


class MailAttachCollectorBot(MailCollectorBot):
    """Monitor IMAP mailboxes and retrieve mail attachments"""
    attach_regex: str = "csv.zip"
    extract_files: bool = True
    folder: str = "INBOX"
    mail_host: str = "<host>"
    mail_password: str = "<password>"
    mail_ssl: bool = True
    mail_user: str = "<user>"
    rate_limit: int = 60
    subject_regex: str = "<subject>"

    def init(self):
        super().init()
        if self.attach_regex is None:
            raise InvalidArgument('attach_regex', expected='string')

    def process_message(self, uid, message):
        seen = False

        for attach in message.attachments:
            if not attach:
                continue

            try:
                attach_filename = attach['filename']
            except KeyError:
                # https://github.com/certtools/intelmq/issues/1538
                self.logger.debug('Skipping attachment because of missing filename.')
                continue
            if attach_filename.startswith('"'):  # for imbox versions older than 0.9.5, see also above
                attach_filename = attach_filename[1:-1]

            if re.search(self.attach_regex, attach_filename):

                self.logger.debug("Found suitable attachment %s.", attach_filename)

                report = self.new_report()

                if self.extract_files:
                    raw_reports = unzip(attach['content'].read(), self.extract_files,
                                        return_names=True, logger=self.logger)
                else:
                    raw_reports = ((attach_filename, attach['content'].read()), )

                for file_name, raw_report in raw_reports:
                    report = self.new_report()
                    report.add("raw", raw_report)
                    if file_name:
                        report.add("extra.file_name", file_name)
                    report["extra.email_subject"] = message.subject
                    report["extra.email_from"] = ','.join(x['email'] for x in message.sent_from)
                    report["extra.email_message_id"] = message.message_id
                    report["extra.email_date"] = message.date
                    self.send_message(report)

                # Only mark read if message relevant to this instance,
                # so other instances watching this mailbox will still
                # check it.
                seen = True
        self.logger.info("Email report read.")
        return seen


BOT = MailAttachCollectorBot
