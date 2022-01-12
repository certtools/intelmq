# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Uses the common mail iteration method from the lib file.
"""
from typing import Union, Iterable

from ._lib import MailCollectorBot


class MailBodyCollectorBot(MailCollectorBot):
    "Monitor IMAP mailboxes and fetch mail bodies"
    content_types: Union[bool, str, Iterable[str]] = ('plain', 'html')
    folder: str = "INBOX"
    mail_host: str = "<host>"
    mail_password: str = "<password>"
    mail_ssl: bool = True
    mail_user: str = "<user>"
    rate_limit: int = 60
    subject_regex: str = "<subject>"

    def init(self):
        super().init()

        if isinstance(self.content_types, str):
            self.content_types = [x.strip() for x in self.content_types.split(',')]
        elif not self.content_types or self.content_types is True:  # empty string, null, false, true
            self.content_types = ('plain', 'html')

    def process_message(self, uid, message):
        seen = False

        for content_type in self.content_types:
            for body in message.body[content_type]:
                if not body:
                    continue

                report = self.new_report()
                report["raw"] = body
                report["extra.email_subject"] = message.subject
                report["extra.email_from"] = ','.join(x['email'] for x in message.sent_from)
                report["extra.email_message_id"] = message.message_id
                report["extra.email_date"] = message.date

                self.send_message(report)

                # at least one body has successfully been processed
                seen = True
        return seen


BOT = MailBodyCollectorBot
