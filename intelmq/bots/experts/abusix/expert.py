# -*- coding: utf-8 -*-
'''
Reference: https://abusix.com/contactdb.html
RIPE abuse contacts resolving through DNS TXT queries

TODO: Use Python module querycontacts from abusix:
https://pypi.python.org/pypi/querycontacts/
'''
from __future__ import unicode_literals
import sys

from intelmq.bots.experts.abusix.lib import Abusix
from intelmq.lib.bot import Bot


class AbusixExpertBot(Bot):

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            if event.contains(ip_key):
                ip = event.value(ip_key)
                email = Abusix.query(ip)
                if email:
                    abuse_contact_key = key + "abuse_contact"
                    event.add(abuse_contact_key, email, force=True)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = AbusixExpertBot(sys.argv[1])
    bot.start()
