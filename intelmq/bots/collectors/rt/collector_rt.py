# -*- coding: utf-8 -*-
import io
import re
import zipfile
from datetime import datetime, timedelta

from dateutil import parser

from intelmq.lib.bot import CollectorBot
from intelmq.lib.utils import parse_relative

try:
    import rt
except ImportError:
    rt = None
try:
    import requests
except ImportError:
    requests = None


class RTCollectorBot(CollectorBot):

    parameter_mapping = {'search_owner': 'Owner',
                         'search_queue': 'Queue',
                         'search_requestor': 'Requestor',
                         'search_status': 'Status',
                         'search_subject_like': 'Subject__like',
                         }

    def init(self):
        if requests is None:
            raise ValueError('Could not import requests. Please install it.')
        if rt is None:
            raise ValueError('Could not import rt. Please install it.')

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
            self.logger.debug('Searching for tickets newer than %r.', kwargs['Created__gt'])
        else:
            kwargs = {}

        for parameter_name, rt_name in self.parameter_mapping.items():
            parameter_value = getattr(self.parameters, parameter_name, None)
            if parameter_value:
                kwargs[rt_name] = parameter_value

        query = RT.search(order='Created', **kwargs)
        self.logger.info('%s results on search query.', len(query))

        for ticket in query:
            ticket_id = int(ticket['id'].split('/')[1])
            self.logger.debug('Process ticket %s.', ticket_id)
            content = 'attachment'
            for (att_id, att_name, _, _) in RT.get_attachments(ticket_id):
                if not self.parameters.attachment_regex:
                    break
                if re.search(self.parameters.attachment_regex, att_name):
                    self.logger.debug('Found attachment %s: %r.',
                                      att_id, att_name)
                    break
            else:
                urlmatch = False
                if self.parameters.url_regex:
                    ticket = RT.get_history(ticket_id)[0]
                    created = ticket['Created']
                    urlmatch = re.search(self.parameters.url_regex, ticket['Content'])
                if urlmatch:
                    content = 'url'
                    url = urlmatch.group(0)
                    self.logger.info('Matching URL found %r.', url)
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
                                    timeout=self.http_timeout_sec)

                response_code_class = resp.status_code // 100
                if response_code_class != 2:
                    self.logger.error('HTTP response status code for %r was %s. Skipping ticket %d.',
                                      url, resp.status_code, ticket_id)
                    if response_code_class == 4:
                        self.logger.debug('Server response: %r.', resp.text)
                        if self.parameters.set_status:
                            RT.edit_ticket(ticket_id, status=self.parameters.set_status)
                        if self.parameters.take_ticket:
                            try:
                                RT.take(ticket_id)
                            except rt.BadRequest:
                                self.logger.exception("Could not take ticket %s.", ticket_id)
                    else:
                        self.logger.info('Skipping now.')
                        continue
                self.logger.info("Report #%d downloaded.", ticket_id)
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
                    self.logger.exception("Could not take ticket %s.", ticket_id)
            if self.parameters.set_status:
                RT.edit_ticket(ticket_id, status=self.parameters.set_status)


BOT = RTCollectorBot
