# -*- coding: utf-8 -*-

import re

import requests

from intelmq.lib.bot import CollectorBot

try:
    import imbox
except ImportError:
    imbox = None


class MailURLCollectorBot(CollectorBot):

    def init(self):
        if imbox is None:
            self.logger.error('Could not import imbox. Please install it.')
            self.stop()

        # Build request
        self.set_request_parameters()

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

                for body in message.body['plain']:
                    match = re.search(self.parameters.url_regex, str(body))
                    if match:
                        url = match.group()
                        # strip leading and trailing spaces, newlines and
                        # carriage returns
                        url = url.strip()

                        self.logger.info("Downloading report from %r.", url)
                        resp = requests.get(url=url,
                                            auth=self.auth, proxies=self.proxy,
                                            headers=self.http_header,
                                            verify=self.http_verify_cert,
                                            cert=self.ssl_client_cert,
                                            timeout=self.http_timeout)

                        if resp.status_code // 100 != 2:
                            raise ValueError('HTTP response status code was {}.'
                                             ''.format(resp.status_code))

                        self.logger.info("Report downloaded.")

                        report = self.new_report()
                        report.add("raw", resp.content)
                        self.send_message(report)

                        # Only mark read if message relevant to this instance,
                        # so other instances watching this mailbox will still
                        # check it.
                        mailbox.mark_seen(uid)
                self.logger.info("Email report read.")
        mailbox.logout()


BOT = MailURLCollectorBot
