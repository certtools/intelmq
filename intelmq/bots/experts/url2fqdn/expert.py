# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import re
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from intelmq.lib.bot import Bot


class Url2fqdnExpertBot(Bot):

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for key in ["source.", "destination."]:

            key_url = key + "url"
            key_fqdn = key + "fqdn"
            if not event.contains(key_url):
                continue

            hostname = urlparse(event.value(key_url)).hostname
            if not re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$").match(hostname):
                event.add(key_fqdn, hostname, sanitize=True,
                          force=True)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = Url2fqdnExpertBot(sys.argv[1])
    bot.start()
