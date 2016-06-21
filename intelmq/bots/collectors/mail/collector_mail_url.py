# -*- coding: utf-8 -*-

import re
import sys

try:
    import imbox
except ImportError:
    imbox = None
import requests

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report


class MailURLCollectorBot(Bot):

    def init(self):
        if imbox is None:
            self.logger.error('Could not import imbox. Please install it.')
            self.stop()

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
                                      message.subject)):
                    continue

                self.logger.info("Reading email report")

                for body in message.body['plain']:
                    match = re.search(self.parameters.url_regex, str(body))
                    if match:
                        url = match.group()
                        url = url.strip()     # strip leading and trailing spaces, newlines and carriage returns

                        # Build request
                        self.http_header = getattr(self.parameters,
                                'http_header', {})
                        self.http_verify_cert = getattr(self.parameters,
                                                        'http_verify_cert', True)

                        if hasattr(self.parameters, 'http_user') and hasattr(
                                self.parameters, 'http_password'):
                            self.auth = (self.parameters.http_user,
                                         self.parameters.http_password)
                        else:
                            self.auth = None

                        http_proxy = getattr(self.parameters, 'http_proxy', None)
                        https_proxy = getattr(self.parameters,
                                              'http_ssl_proxy', None)
                        if http_proxy and https_proxy:
                            self.proxy = {'http': http_proxy, 'https': https_proxy}
                        else:
                            self.proxy = None

                        self.http_header['User-agent'] = self.parameters.http_user_agent

                        self.logger.info("Downloading report from %s" % url)
                        resp = requests.get(url=url,
                                            auth=self.auth, proxies=self.proxy,
                                            headers=self.http_header,
                                            verify=self.http_verify_cert)

                        if resp.status_code // 100 != 2:
                            raise ValueError('HTTP response status code was {}.'
                                             ''.format(resp.status_code))

                        self.logger.info("Report downloaded.")

                        report = Report()
                        report.add("raw", resp.content)
                        report.add("feed.name",
                                   self.parameters.feed)
                        report.add("feed.accuracy", self.parameters.accuracy)
                        self.send_message(report)

                        # Only mark read if message relevant to this instance,
                        # so other instances watching this mailbox will still
                        # check it.
                        mailbox.mark_seen(uid)
                self.logger.info("Email report read")


if __name__ == "__main__":
    bot = MailURLCollectorBot(sys.argv[1])
    bot.start()
