# -*- coding: utf-8 -*-
import re
import zipfile

from intelmq.lib.bot import CollectorBot

try:
    import imbox
except ImportError:
    imbox = None


class MailAttachCollectorBot(CollectorBot):

    def init(self):
        if imbox is None:
            self.logger.error('Could not import imbox. Please install it.')
            self.stop()

    def process(self):
        mailbox = imbox.Imbox(self.parameters.mail_host,
                              self.parameters.mail_user,
                              self.parameters.mail_password,
                              self.parameters.mail_ssl)
        emails = mailbox.messages(folder=self.parameters.folder, unread=True)

        if emails:
            for uid, message in emails:

                if (self.parameters.subject_regex and
                        not re.search(self.parameters.subject_regex,
                                      re.sub("\r\n\s", " ", message.subject))):
                    continue

                for attach in message.attachments:
                    if not attach:
                        continue

                    # remove quote marks from filename
                    attach_name = attach['filename'][
                        1:len(attach['filename']) - 1]

                    if re.search(self.parameters.attach_regex, attach_name):

                        if self.parameters.attach_unzip:
                            zipped = zipfile.ZipFile(attach['content'])
                            raw_report = zipped.read(zipped.namelist()[0])
                        else:
                            raw_report = attach['content'].read()

                        report = self.new_report()
                        report.add("raw", raw_report)

                        self.send_message(report)

                        # Only mark read if message relevant to this instance,
                        # so other instances watching this mailbox will still
                        # check it.
                        mailbox.mark_seen(uid)
                self.logger.debug("Email report read.")
        mailbox.logout()


BOT = MailAttachCollectorBot
