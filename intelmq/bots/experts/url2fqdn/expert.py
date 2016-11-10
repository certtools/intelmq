# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import intelmq.lib.harmonization
from intelmq.lib.bot import Bot


class Url2fqdnExpertBot(Bot):

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:

            key_url = key + "url"
            key_fqdn = key + "fqdn"
            if not event.contains(key_url):
                continue

            hostname = urlparse(event.get(key_url)).hostname
            if intelmq.lib.harmonization.FQDN.is_valid(hostname, sanitize=True):
                event.add(key_fqdn, hostname, sanitize=True, force=True)

        self.send_message(event)
        self.acknowledge_message()
