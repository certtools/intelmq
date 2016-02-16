# -*- coding: utf-8 -*-
"""
TODO: Arbitrary order of decrypt and unzip
"""
from __future__ import unicode_literals

import io
import re
import sys
import zipfile

from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report

import rt

try:
    import gnupg
except ImportError:
    gnupg = None


class RTCollectorBot(Bot):

    def init(self):
        if self.parameters.gnupg_decrypt:
            if gnupg is None:
                raise ValueError('gnupg module is not available')
            self.gpg = gnupg.GPG(gnupghome=self.parameters.gnupg_homedir)

    def process(self):
        RT = rt.Rt(self.parameters.uri, self.parameters.user,
                   self.parameters.password)
        if not RT.login():
            raise ValueError('Login failed.')

        query = RT.search(Queue=self.parameters.search_queue,
                          Subject__like=self.parameters.search_subject_like,
                          Owner=self.parameters.search_owner,
                          Status=self.parameters.search_status)
        self.logger.info('{} results on search query.'.format(len(query)))

        for ticket in query:
            ticket_id = int(ticket['id'].split('/')[1])
            self.logger.debug('Process ticket {}.'.format(ticket_id))
            for (att_id, att_name, _, _) in RT.get_attachments(ticket_id):
                if re.search(self.parameters.attachment_regex, att_name):
                    self.logger.debug('Found attachment {}: {!r}.'
                                      ''.format(att_id, att_name))
                    break
            else:
                self.logger.debug('No matching attachement name found.')
                continue
            attachment = RT.get_attachment_content(ticket_id, att_id)

            if self.parameters.unzip_attachment:
                file_obj = io.BytesIO(attachment)
                zipped = zipfile.ZipFile(file_obj)
                raw = zipped.read(zipped.namelist()[0])
            else:
                raw = attachment

            if self.parameters.gnupg_decrypt:
                raw = str(self.gpg.decrypt(raw,
                                           always_trust=self.parameters.gnupg_trust,
                                           passphrase=self.parameters.gnupg_passphrase))
                self.logger.info('Successfully decrypted attachment.')

            self.logger.debug(raw)
            report = Report()
            report.add("raw", raw, sanitize=True)
            report.add("rtir_id", ticket_id, sanitize=True)
            report.add("feed.name", self.parameters.feed, sanitize=True)
            report.add("feed.accuracy", self.parameters.accuracy,
                       sanitize=True)
            time_observation = DateTime().generate_datetime_now()
            report.add('time.observation', time_observation, sanitize=True)
            self.send_message(report)

            if self.parameters.take_ticket:
                RT.edit_ticket(ticket_id, Owner=self.parameters.user)


if __name__ == "__main__":
    bot = RTCollectorBot(sys.argv[1])
    bot.start()
