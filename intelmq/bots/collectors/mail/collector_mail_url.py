# -*- coding: utf-8 -*-
"""
Uses the common mail iteration method from the lib file.
"""
import io
import re

from intelmq.lib.splitreports import generate_reports

from .lib import MailCollectorBot

try:
    import requests
except ImportError:
    requests = None


class MailURLCollectorBot(MailCollectorBot):

    def init(self):
        super().init()
        if requests is None:
            raise ValueError('Could not import requests. Please install it.')

        # Build request
        self.set_request_parameters()

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
                timeoutretries = 0
                resp = None
                while timeoutretries < self.http_timeout_max_tries and resp is None:
                    try:
                        resp = requests.get(url=url,
                                            auth=self.auth, proxies=self.proxy,
                                            headers=self.http_header,
                                            verify=self.http_verify_cert,
                                            cert=self.ssl_client_cert,
                                            timeout=self.http_timeout_sec)

                    except requests.exceptions.Timeout:
                        timeoutretries += 1
                        self.logger.warn("Timeout whilst downloading the report.")

                if resp is None and timeoutretries >= self.http_timeout_max_tries:
                    self.logger.error("Request timed out %i times in a row. " %
                                      timeoutretries)
                    erroneous = True
                    # The download timed out too often, leave the Loop.
                    continue

                if resp.status_code // 100 != 2:
                    self.logger.error('HTTP response status code was {}.'
                                      ''.format(resp.status_code))
                    erroneous = True
                    continue

                if not resp.content:
                    self.logger.warning('Got empty reponse from server.')
                else:
                    self.logger.info("Report downloaded.")

                    template = self.new_report()

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
