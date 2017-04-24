# -*- coding: utf-8 -*-
import io
import re
import zipfile
from datetime import datetime, timedelta

import requests
from dateutil import parser

from intelmq.lib.bot import CollectorBot
from intelmq.lib.utils import parse_relative

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

        if getattr(self.parameters, 'search_not_older_than', None):
            try:
                self.not_older_than = parser.parse(self.parameters.search_not_older_than)
                self.not_older_than_type = 'absolute'
            except ValueError:
                try:
                    self.not_older_than_relative = timedelta(minutes=parse_relative(self.parameters.search_not_older_than))
                except ValueError:
                    self.logger.error("Parameter 'search_not_older_than' could not be parsed. "
                                      "Check your configuration.")
                    raise
                self.not_older_than_type = 'relative'
        else:
            self.not_older_than_type = False

    def process(self):
        RT = rt.Rt(self.parameters.uri, self.parameters.user,
                   self.parameters.password)
        if not RT.login():
            raise ValueError('Login failed.')

        if self.not_older_than_type:
            if self.not_older_than_type == 'relative':
                self.not_older_than = datetime.now() - self.not_older_than_relative
            kwargs = {'Created__gt': self.not_older_than.isoformat()}
            self.logger.debug('Searching for tickets newer than %r.' % kwargs['Created__gt'])
        else:
            kwargs = {}

        query = RT.search(Queue=self.parameters.search_queue,
                          Subject__like=self.parameters.search_subject_like,
                          Owner=self.parameters.search_owner,
                          Status=self.parameters.search_status,
                          order='Created', **kwargs)
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
                created = ticket['Created']
                urlmatch = re.search(self.parameters.url_regex, ticket['Content'])
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

                response_code_class = resp.status_code // 100
                if response_code_class != 2:
                    self.logger.error('HTTP response status code for {!r} was {}.'
                                      ''.format(url, resp.status_code))
                    if response_code_class == 4:
                        self.logger.debug('Server response: {!r}.'.format(resp.text))
                        self.logger.warning('Setting status of unprocessable ticket.')
                        if self.parameters.set_status:
                            RT.edit_ticket(ticket_id, status=self.parameters.set_status)
                    else:
                        self.logger.info('Skipping now.')
                        continue
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
