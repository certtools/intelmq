# -*- coding: utf-8 -*-
import io
import re
import zipfile

import requests

from intelmq.lib.bot import CollectorBot

try:
    import rt
except ImportError:
    rt = None


class RTCollectorBot(CollectorBot):

    def init(self):
        if rt is None:
            self.logger.error('Could not import rt. Please install it.')
            self.stop()

        self.set_request_parameters()

    def process(self):
        RT = rt.Rt(self.parameters.uri, self.parameters.user,
                   self.parameters.password)
        if not RT.login():
            raise ValueError('Login failed.')

        query = RT.search(Queue=self.parameters.search_queue,
                          Subject__like=self.parameters.search_subject_like,
                          Owner=self.parameters.search_owner,
                          Status=self.parameters.search_status,
                          order='Created')
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
                ticket = RT.get_history(ticket_id)[0]
                text = ticket['Content']
                created = ticket['Created']
                urlmatch = re.search(self.parameters.url_regex, text)
                if urlmatch:
                    content = 'url'
                    url = urlmatch.group(0)
                else:
                    self.logger.debug('No matching attachment or URL found.')
                    continue
            if content == 'attachment':
                attachment = RT.get_attachment_content(ticket_id, att_id)
                created = RT.get_attachment(ticket_id, att_id)['Created']

                if self.parameters.unzip_attachment:
                    file_obj = io.BytesIO(attachment)
                    zipped = zipfile.ZipFile(file_obj)
                    raw = zipped.read(zipped.namelist()[0])
                else:
                    raw = attachment
            else:
                resp = requests.get(url=url, auth=self.auth,
                                    proxies=self.proxy,
                                    headers=self.http_header,
                                    verify=self.http_verify_cert,
                                    cert=self.ssl_client_cert,
                                    timeout=self.http_timeout)

                if resp.status_code // 100 != 2:
                    self.logger.error('HTTP response status code was {}.'
                                      ''.format(resp.status_code))
                self.logger.info("Report downloaded.")
                raw = resp.text

            report = self.new_report()
            report.add("raw", raw)
            report.add("rtir_id", ticket_id)
            report.add("time.observation", created + ' UTC', overwrite=True)
            self.send_message(report)

            if self.parameters.take_ticket:
                try:
                    RT.take(ticket_id)
                except rt.BadRequest:
                    self.logger.exception("Could not take ticket %s." % ticket_id)
            if self.parameters.set_status:
                RT.edit_ticket(ticket_id, status=self.parameters.set_status)


BOT = RTCollectorBot
