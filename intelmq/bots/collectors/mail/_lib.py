# SPDX-FileCopyrightText: 2021 Sebastian Waldbauer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import imaplib
import re
import ssl

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import imbox
except ImportError:
    imbox = None


class MailCollectorBot(CollectorBot):
    attach_unzip = None
    mail_host = None
    ssl_ca_certificate = None
    mail_user = None
    mail_password = None
    mail_ssl = None
    mail_port = None
    mail_starttls = False
    folder = None
    sent_to = None
    sent_from = None
    subject_regex = None

    def init(self):
        if imbox is None:
            raise MissingDependencyError("imbox")

        if self.attach_unzip is not None and not self.extract_files:
            self.extract_files = True
            self.logger.warning("The parameter 'attach_unzip' is deprecated and will "
                                "be removed in version 4.0. Use 'extract_files' instead.")

    def connect_mailbox(self):
        self.logger.debug("Connecting to %s.", self.mail_host)
        ca_file = self.ssl_ca_certificate
        ssl_custom_context = ssl.create_default_context(cafile=ca_file)
        mailbox = imbox.Imbox(self.mail_host,
                              self.mail_user,
                              self.mail_password,
                              self.mail_ssl,
                              # imbox itself uses ports 143/993 as default depending on SSL setting
                              port=self.mail_port,
                              starttls=self.mail_starttls,
                              ssl_context=ssl_custom_context)
        return mailbox

    def process(self):
        mailbox = self.connect_mailbox()
        emails = mailbox.messages(folder=self.folder, unread=True,
                                  sent_to=self.sent_to,
                                  sent_from=self.sent_from)

        if emails:
            for uid, message in emails:

                if (self.subject_regex and
                        not re.search(self.subject_regex,
                                      re.sub(r"\r\n\s", " ", message.subject))):
                    self.logger.debug("Message with date %s skipped because subject %r does not match.",
                                      message.date, message.subject)
                    continue

                if self.process_message(uid, message):
                    try:
                        mailbox.mark_seen(uid)
                    except imaplib.abort:
                        # Disconnect, see https://github.com/certtools/intelmq/issues/852
                        mailbox = self.connect_mailbox()
                        mailbox.mark_seen(uid)
        else:
            self.logger.debug("No unread mails to check.")
        mailbox.logout()

    def process_message(self, uid, message) -> bool:
        """
        Returns:
            seen: Mark the message as seen or not
        """
        raise NotImplementedError
