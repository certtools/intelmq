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

    def init(self):
        if imbox is None:
            raise MissingDependencyError("imbox")

        if getattr(self.parameters, 'attach_unzip', None) and not self.extract_files:
            self.extract_files = True
            self.logger.warning("The parameter 'attach_unzip' is deprecated and will "
                                "be removed in version 4.0. Use 'extract_files' instead.")

    def connect_mailbox(self):
        self.logger.debug("Connecting to %s.", self.parameters.mail_host)
        ca_file = getattr(self.parameters, 'ssl_ca_certificate', None)
        ssl_custom_context = ssl.create_default_context(cafile=ca_file)
        mailbox = imbox.Imbox(self.parameters.mail_host,
                              self.parameters.mail_user,
                              self.parameters.mail_password,
                              self.parameters.mail_ssl,
                              # imbox itself uses ports 143/993 as default depending on SSL setting
                              port=getattr(self.parameters, 'mail_port', None),
                              ssl_context=ssl_custom_context)
        return mailbox

    def process(self):
        mailbox = self.connect_mailbox()
        emails = mailbox.messages(folder=self.parameters.folder, unread=True,
                                  sent_to=getattr(self.parameters, "sent_to", None),
                                  sent_from=getattr(self.parameters, "sent_from", None))

        if emails:
            for uid, message in emails:

                if (self.parameters.subject_regex and
                        not re.search(self.parameters.subject_regex,
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
