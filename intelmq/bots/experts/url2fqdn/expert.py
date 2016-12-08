# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import intelmq.lib.harmonization
from intelmq.lib.bot import Bot


class Url2fqdnExpertBot(Bot):

    def init(self):
        self.overwrite = getattr(self.parameters, 'overwrite', False)

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:

            key_url = key + "url"
            key_fqdn = key + "fqdn"
            if not event.contains(key_url):
                continue
            if key_fqdn in event and not self.overwrite:
                continue

            hostname = urlparse(event.get(key_url)).hostname
            if intelmq.lib.harmonization.FQDN.is_valid(hostname, sanitize=True):
                event.add(key_fqdn, hostname, sanitize=True, force=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = Url2fqdnExpertBot
