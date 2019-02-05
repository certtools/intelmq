# -*- coding: utf-8 -*-
import re
import io
import imaplib

try:
    import imbox
except ImportError:
    imbox = None
try:
    import requests
except ImportError:
    requests = None

from intelmq.lib.bot import CollectorBot
from intelmq.lib.splitreports import generate_reports


class MailURLCollectorBot(CollectorBot):

    def init(self):
        if imbox is None:
            raise ValueError('Could not import imbox. Please install it.')
        if requests is None:
            raise ValueError('Could not import requests. Please install it.')

        # Build request
        self.set_request_parameters()

        self.chunk_size = getattr(self.parameters, 'chunk_size', None)
        self.chunk_replicate_header = getattr(self.parameters,
                                              'chunk_replicate_header', None)

    def connect_mailbox(self):
        self.logger.debug("Connecting to %s.", self.parameters.mail_host)
        mailbox = imbox.Imbox(self.parameters.mail_host,
                              self.parameters.mail_user,
                              self.parameters.mail_password,
                              self.parameters.mail_ssl)
        return mailbox

    def process(self):
        mailbox = self.connect_mailbox()
        emails = mailbox.messages(folder=self.parameters.folder, unread=True,
                                  sent_to=getattr(self.parameters, "sent_to", None),
                                  sent_from=getattr(self.parameters, "sent_from", None))

        if emails:
            for uid, message in emails:

                if (self.parameters.subject_regex and
                        not re.search(self.parameters.subject_regex,
                                      re.sub(r"\r\n\s", " ", message.subject))):
                    self.logger.debug("Message with date %s skipped because subject %r does not match.",
                                      message.date, message.subject)
                    continue

                erroneous = False  # If errors occurred this will be set to true.

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

                        # Only mark read if message relevant to this instance,
                        # so other instances watching this mailbox will still
                        # check it.
                        try:
                            mailbox.mark_seen(uid)
                        except imaplib.abort:
                            # Disconnect, see https://github.com/certtools/intelmq/issues/852
                            mailbox = self.connect_mailbox()
                            mailbox.mark_seen(uid)

                if not erroneous:
                    self.logger.info("Email report read.")
                else:
                    if self.parameters.error_procedure == 'pass':
                        try:
                            mailbox.mark_seen(uid)
                        except imaplib.abort:
                            mailbox = self.connect_mailbox()
                            mailbox.mark_seen(uid)
                        self.logger.error("Download of report failed with above error, marked Email as read "
                                          "(according to `error_procedure` parameter).")
                    else:
                        self.logger.error("Email report read with above errors, the report was not processed.")
        else:
            self.logger.debug("No unread mails to check.")
        mailbox.logout()


BOT = MailURLCollectorBot
