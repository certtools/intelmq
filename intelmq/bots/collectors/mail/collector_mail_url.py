# -*- coding: utf-8 -*-
"""
Uses the common mail iteration method from the lib file.
"""
import io
import re

from intelmq.lib.splitreports import generate_reports
from intelmq.lib.utils import create_request_session, file_name_from_response

from .lib import MailCollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import requests
except ImportError:
    requests = None


class MailURLCollectorBot(MailCollectorBot):

    def init(self):
        super().init()
        if requests is None:
            raise MissingDependencyError("requests")

        # Build request
        self.set_request_parameters()
        self.session = create_request_session(self)

        self.chunk_size = getattr(self.parameters, 'chunk_size', None)
        self.chunk_replicate_header = getattr(self.parameters,
                                              'chunk_replicate_header', None)

    def process_message(self, uid, message):
        erroneous = False  # If errors occurred this will be set to true.
        seen = False

        for body in message.body['plain']:
            match = re.search(self.parameters.url_regex, str(body.decode('utf-8') if isinstance(body, bytes) else body))
            if match:
                url = match.group()
                # strip leading and trailing spaces, newlines and
                # carriage returns
                url = url.strip()

                self.logger.info("Downloading report from %r.", url)
                try:
                    resp = self.session.get(url=url)
                except requests.exceptions.Timeout:
                    self.logger.error("Request timed out %i times in a row." %
                                      self.http_timeout_max_tries)
                    erroneous = True
                    # The download timed out too often, leave the Loop.
                    continue

                if resp.status_code // 100 != 2:
                    self.logger.error('HTTP response status code was {}.'
                                      ''.format(resp.status_code))
                    erroneous = True
                    continue

                if not resp.content:
                    self.logger.warning('Got empty response from server.')
                else:
                    self.logger.info("Report downloaded.")

                    template = self.new_report()
                    template["feed.url"] = url
                    template["extra.email_subject"] = message.subject
                    template["extra.email_from"] = ','.join(x['email'] for x in message.sent_from)
                    template["extra.email_message_id"] = message.message_id
                    template["extra.file_name"] = file_name_from_response(resp)
                    template["extra.email_date"] = message.date

                    for report in generate_reports(template, io.BytesIO(resp.content),
                                                   self.chunk_size,
                                                   self.chunk_replicate_header):
                        self.send_message(report)

                seen = True

        if not erroneous:
            self.logger.info("Email report read.")
        else:
            if self.parameters.error_procedure == 'pass':
                seen = True
            else:
                self.logger.error("Email report read with above errors, the report was not processed.")

        return seen


BOT = MailURLCollectorBot
