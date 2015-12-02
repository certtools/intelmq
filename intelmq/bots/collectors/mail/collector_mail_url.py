# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import sys

import imbox
from intelmq.bots.collectors.url.lib import fetch_url
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report


class MailURLCollectorBot(Bot):

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

                for body in message.body['plain']:
                    match = re.search(self.parameters.mail_url_regex, body)
                    if match:
                        url = match.group()

                        self.logger.info("Downloading report from %s" % url)
                        raw_report = fetch_url(url, timeout=60.0,
                                               chunk_size=16384)
                        self.logger.info("Report downloaded.")

                        report = Report()
                        report.add("raw", raw_report, sanitize=True)
                        report.add("feed.name",
                                   self.parameters.feed, sanitize=True)
                        report.add("feed.accuracy", self.parameters.accuracy, sanitize=True)
                        time_observation = DateTime().generate_datetime_now()
                        report.add('time.observation', time_observation,
                                   sanitize=True)
                        self.send_message(report)

                mailbox.mark_seen(uid)
                self.logger.info("Email report read")


if __name__ == "__main__":
    bot = MailURLCollectorBot(sys.argv[1])
    bot.start()
