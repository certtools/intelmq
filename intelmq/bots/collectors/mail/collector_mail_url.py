# -*- coding: utf-8 -*-
import re
import io
import requests

try:
    import imbox
except ImportError:
    imbox = None

from intelmq.lib.bot import CollectorBot
from intelmq.lib.splitreports import generate_reports


class MailURLCollectorBot(CollectorBot):

    def init(self):
        if imbox is None:
            self.logger.error('Could not import imbox. Please install it.')
            self.stop()

        # Build request
        self.set_request_parameters()

        self.chunk_size = getattr(self.parameters, 'chunk_size', None)
        self.chunk_replicate_header = getattr(self.parameters,
                                              'chunk_replicate_header', None)

    def process(self):
        mailbox = imbox.Imbox(self.parameters.mail_host,
                              self.parameters.mail_user,
                              self.parameters.mail_password,
                              self.parameters.mail_ssl)
        emails = mailbox.messages(folder=self.parameters.folder, unread=True)

        if emails:
            for uid, message in emails:

                if (self.parameters.subject_regex and
                        not re.search(self.parameters.subject_regex,
                                      re.sub("\r\n\s", " ", message.subject))):
                    continue

                erroneous = False  # If errors occured this will be set to true.

                for body in message.body['plain']:
                    match = re.search(self.parameters.url_regex, str(body))
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
                            raise ValueError('HTTP response status code was {}.'
                                             ''.format(resp.status_code))

                        self.logger.info("Report downloaded.")

                        template = self.new_report()

                        for report in generate_reports(template, io.BytesIO(resp.content),
                                                       self.chunk_size,
                                                       self.chunk_replicate_header):
                            self.send_message(report)

                        # Only mark read if message relevant to this instance,
                        # so other instances watching this mailbox will still
                        # check it.
                        mailbox.mark_seen(uid)

                if not erroneous:
                    self.logger.info("Email report read.")
                else:
                    self.logger.error("Email report read with errors, the report was not processed.")

        mailbox.logout()


BOT = MailURLCollectorBot
