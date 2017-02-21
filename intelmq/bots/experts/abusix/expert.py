# -*- coding: utf-8 -*-
'''
Reference: https://abusix.com/contactdb.html
RIPE abuse contacts resolving through DNS TXT queries
'''

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

        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            abuse_contact_key = key + "abuse_contact"
            if abuse_contact_key in event and not self.parameters.overwrite:
                continue
            if ip_key in event:
                ip = event.get(ip_key)
                email = self.lookup(ip)
                if email:
                    event.add(abuse_contact_key, email, overwrite=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = AbusixExpertBot
