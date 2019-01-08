# -*- coding: utf-8 -*-
"""
In Version 0.9.5 the attachment filename is no longer surrounded by double quotes, see for the discussion:
https://github.com/certtools/intelmq/pull/1134
https://github.com/martinrusev/imbox/commit/7c6cc2fb5f7e39c1496d68f3d432eec19517bf8e#diff-1ae09572064c2e7c225de54ad5b49154

Uses the common mail iteration method from the lib file.
"""
import re
import zipfile

from .lib import MailCollectorBot


class MailAttachCollectorBot(MailCollectorBot):

    def process_message(self, uid, message):
        seen = False

        for attach in message.attachments:
            if not attach:
                continue

            attach_filename = attach['filename']
            if attach_filename.startswith('"'):  # for imbox versions older than 0.9.5, see also above
                attach_filename = attach_filename[1:-1]

            if re.search(self.parameters.attach_regex, attach_filename):

                self.logger.debug("Found suitable attachment %s.", attach_filename)

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
                seen = True
        self.logger.info("Email report read.")
        return seen


BOT = MailAttachCollectorBot
