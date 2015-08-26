# -*- coding: utf-8 -*-
'''
Reference:
https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=1.1.1.1

TODO:
Load RIPE networks prefixes into memory.
Compare each IP with networks prefixes loaded.
If ip matchs, query RIPE
IPv6
'''
from __future__ import unicode_literals
import sys

from intelmq.bots.experts.ripencc_abuse_contact.lib import RIPENCC
from intelmq.lib.bot import Bot


class RIPENCCExpertBot(Bot):

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            if event.contains(ip_key):
                ip = event.value(ip_key)
                email = RIPENCC.query(ip)
                if email:
                    event.add(key + "abuse_contact", email, sanitize=True)

        self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = RIPENCCExpertBot(sys.argv[1])
    bot.start()
