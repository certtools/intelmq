# -*- coding: utf-8 -*-
import io
import re
import requests
import sys
import zipfile

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report

import rt


class RTCollectorBot(Bot):

    def init(self):
        self.http_header = getattr(self.parameters, 'http_header', {})
        self.http_verify_cert = getattr(self.parameters, 'http_verify_cert',
                                        True)

        http_proxy = getattr(self.parameters, 'http_proxy', None)
        https_proxy = getattr(self.parameters, 'http_ssl_proxy', None)
        if http_proxy and https_proxy:
            self.proxy = {'http': http_proxy, 'https': https_proxy}
        else:
            self.proxy = None

        self.http_header['User-agent'] = self.parameters.http_user_agent

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
            content = 'attachment'
            for (att_id, att_name, _, _) in RT.get_attachments(ticket_id):
                if re.search(self.parameters.attachment_regex, att_name):
                    self.logger.debug('Found attachment {}: {!r}.'
                                      ''.format(att_id, att_name))
                    break
            else:
                text = RT.get_history(ticket_id)[0]['Content']
                urlmatch = re.search(self.parameters.url_regex, text)
                if urlmatch:
                    content = 'url'
                    url = urlmatch.group(0)
                else:
                    self.logger.debug('No matching attachment or URL found.')
                    continue
            if content == 'attachment':
                attachment = RT.get_attachment_content(ticket_id, att_id)

                if self.parameters.unzip_attachment:
                    file_obj = io.BytesIO(attachment)
                    zipped = zipfile.ZipFile(file_obj)
                    raw = zipped.read(zipped.namelist()[0])
                else:
                    raw = attachment
            else:
                resp = requests.get(url=url, proxies=self.proxy,
                                    headers=self.http_header,
                                    verify=self.http_verify_cert)

                if resp.status_code // 100 != 2:
                    self.logger.error('HTTP response status code was {}.'
                                      ''.format(resp.status_code))
                self.logger.info("Report downloaded.")
                raw = resp.text

            report = Report()
            report.add("raw", raw, sanitize=True)
            report.add("rtir_report_id", ticket_id, sanitize=True)
            report.add("feed.name", self.parameters.feed, sanitize=True)
            report.add("feed.accuracy", self.parameters.accuracy,
                       sanitize=True)
            self.send_message(report)

            if self.parameters.take_ticket:
                try:
                    RT.take(ticket_id)
                except rt.BadRequest:
                    self.logger.exception("Could not take ticket %s." % ticket_id)
            if self.parameters.set_status:
                RT.edit_ticket(ticket_id, status=self.parameters.set_status)


if __name__ == "__main__":
    bot = RTCollectorBot(sys.argv[1])
    bot.start()
