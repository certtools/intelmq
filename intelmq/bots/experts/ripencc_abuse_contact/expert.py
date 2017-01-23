# -*- coding: utf-8 -*-
'''
Reference:
https://stat.ripe.net/docs/data_api
https://github.com/RIPE-NCC/whois/wiki/WHOIS-REST-API-abuse-contact

TODO: Load RIPE networks prefixes into memory.
TODO: Compare each IP with networks prefixes loaded.
TODO: If ip matches, query RIPE
'''

from intelmq.bots.experts.ripencc_abuse_contact import lib
from intelmq.lib.bot import Bot


class RIPENCCExpertBot(Bot):

    def init(self):
        self.query_db_asn = getattr(self.parameters, 'query_ripe_db_asn', True)
        self.query_db_ip = getattr(self.parameters, 'query_ripe_db_ip', True)
        self.query_stat_asn = getattr(self.parameters, 'query_ripe_stat', True)
        self.query_stat_ip = getattr(self.parameters, 'query_ripe_stat', True)

    def process(self):
        event = self.receive_message()

        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            abuse_key = key + "abuse_contact"
            asn_key = key + "asn"

            ip = event.get(ip_key, None)
            abuse = (event.get(abuse_key).split(',') if abuse_key in event
                     else [])
            asn = event.get(asn_key, None)
            if self.query_db_asn and asn:
                abuse.extend(lib.query_asn(asn))
            if self.query_db_ip and ip:
                abuse.extend(lib.query_ripedb(ip))
            if self.query_stat_asn and asn:
                abuse.extend(lib.query_ripestat(asn))
            if self.query_stat_ip and ip:
                abuse.extend(lib.query_ripestat(ip))

            event.add(abuse_key, ','.join(filter(None, set(abuse))), overwrite=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = RIPENCCExpertBot
