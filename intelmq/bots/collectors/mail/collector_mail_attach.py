# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import sys
import zipfile

import imbox
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report


class MailAttachCollectorBot(Bot):

    def process(self):
        mailbox = imbox.Imbox(self.parameters.mail_host,
                              self.parameters.mail_user,
                              self.parameters.mail_password,
                              self.parameters.mail_ssl)
        emails = mailbox.messages(folder=self.parameters.mail_folder, unread=True)

        if emails:
            for uid, message in emails:

                if (self.parameters.mail_subject_regex and
                        not re.search(self.parameters.mail_subject_regex,
                                      message.subject)):
                    continue

                self.logger.info("Reading email report")

                for attach in message.attachments:
                    if not attach:
                        continue

                    # remove quote marks from filename
                    attach_name = attach['filename'][
                        1:len(attach['filename']) - 1]

                    if re.search(self.parameters.mail_attach_regex, attach_name):

                        if self.parameters.mail_attach_unzip:
                            zipped = zipfile.ZipFile(attach['content'])
                            raw_report = zipped.read(zipped.namelist()[0])
                        else:
                            raw_report = attach['content'].read()

                        report = Report()
                        report.add("raw", raw_report, sanitize=True)
                        report.add("feed.name", self.parameters.feed,
                                   sanitize=True)
                        report.add("feed.accuracy", self.parameters.accuracy, sanitize=True)
                        time_observation = DateTime().generate_datetime_now()
                        report.add('time.observation', time_observation,
                                   sanitize=True)

                        self.send_message(report)

                mailbox.mark_seen(uid)
                self.logger.info("Email report read")


if __name__ == "__main__":
    bot = MailAttachCollectorBot(sys.argv[1])
    bot.start()
