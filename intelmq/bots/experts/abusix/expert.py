# -*- coding: utf-8 -*-
'''
Reference: https://abusix.com/contactdb.html
RIPE abuse contacts resolving through DNS TXT queries
'''
from __future__ import unicode_literals, absolute_import
import sys

from intelmq.bots.experts.abusix.lib import Abusix
from intelmq.lib.bot import Bot

try:
    import querycontacts
except ImportError:
    querycontacts = None


class AbusixExpertBot(Bot):

    def init(self):
        if querycontacts:
            qf = querycontacts.ContactFinder()
            self.lookup = lambda t: ', '.join(qf.find(t))
        else:
            self.lookup = Abusix.query

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            if event.contains(ip_key):
                ip = event.get(ip_key)
                email = self.lookup(ip)
                if email:
                    abuse_contact_key = key + "abuse_contact"
                    event.add(abuse_contact_key, email, force=True)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = AbusixExpertBot(sys.argv[1])
    bot.start()
