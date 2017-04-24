# -*- coding: utf-8 -*-
'''
Reference:
https://stat.ripe.net/docs/data_api
https://github.com/RIPE-NCC/whois/wiki/WHOIS-REST-API-abuse-contact

TODO: Load RIPE networks prefixes into memory.
TODO: Compare each IP with networks prefixes loaded.
TODO: If ip matches, query RIPE
'''
import requests

from intelmq.lib.bot import Bot


URL_STAT = ('https://stat.ripe.net/data/abuse-contact-finder/'
            'data.json?resource={}')
URL_DB_IP = 'http://rest.db.ripe.net/abuse-contact/{}.json'
URL_DB_AS = 'http://rest.db.ripe.net/abuse-contact/as{}.json'


class RIPENCCExpertBot(Bot):

    def init(self):
        self.query_db_asn = getattr(self.parameters, 'query_ripe_db_asn', True)
        self.query_db_ip = getattr(self.parameters, 'query_ripe_db_ip', True)
        self.query_stat_asn = getattr(self.parameters, 'query_ripe_stat', True)
        self.query_stat_ip = getattr(self.parameters, 'query_ripe_stat', True)

        self.set_request_parameters()

    def query_ripestat(self, resource):
        response = requests.get(URL_STAT.format(resource), data="",
                                proxies=self.proxy,
                                headers=self.http_header,
                                verify=self.http_verify_cert,
                                cert=self.ssl_client_cert,
                                timeout=self.http_timeout)
        if response.status_code != 200:
            raise ValueError('HTTP response status code was {}.'
                             ''.format(response.status_code))

        try:
            if (response.json()['data']['anti_abuse_contacts']['abuse_c']):
                return [response.json()['data']['anti_abuse_contacts']
                        ['abuse_c'][0]['email']]
            else:
                return []
        except:
            return []

    def query_ripedb(self, ip=None, asn=None):
        response = requests.get(URL_DB_IP.format(ip), data="",
                                proxies=self.proxy,
                                headers=self.http_header,
                                verify=self.http_verify_cert,
                                cert=self.ssl_client_cert,
                                timeout=self.http_timeout)
        if response.status_code != 200:
            return []

        return [response.json()['abuse-contacts']['email']]

    def query_asn(self, asn):
        response = requests.get(URL_DB_AS.format(asn), data="",
                                proxies=self.proxy,
                                headers=self.http_header,
                                verify=self.http_verify_cert,
                                cert=self.ssl_client_cert,
                                timeout=self.http_timeout)
        if response.status_code != 200:
            return []

        return [response.json()['abuse-contacts']['email']]

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
                abuse.extend(self.query_asn(asn))
            if self.query_db_ip and ip:
                abuse.extend(self.query_ripedb(ip))
            if self.query_stat_asn and asn:
                abuse.extend(self.query_ripestat(asn))
            if self.query_stat_ip and ip:
                abuse.extend(self.query_ripestat(ip))

            event.add(abuse_key, ','.join(filter(None, set(abuse))), overwrite=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = RIPENCCExpertBot
