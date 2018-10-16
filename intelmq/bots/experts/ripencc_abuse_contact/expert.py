# -*- coding: utf-8 -*-
'''
Reference:
https://stat.ripe.net/docs/data_api
https://github.com/RIPE-NCC/whois/wiki/WHOIS-REST-API-abuse-contact
'''
import json

try:
    import requests
except ImportError:
    requests = None

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache


STATUS_CODE_ERROR = 'HTTP status code was %s. Possible problem at the connection endpoint or network issue.'
CACHE_NO_VALUE = '__no_contact'


class RIPENCCExpertBot(Bot):
    URL_DB_IP = 'https://rest.db.ripe.net/abuse-contact/{}.json'
    URL_DB_AS = 'https://rest.db.ripe.net/abuse-contact/as{}.json'
    URL_STAT = ('https://stat.ripe.net/data/abuse-contact-finder/'
                'data.json?resource={}')

    def init(self):
        if requests is None:
            raise ValueError('Could not import requests. Please install it.')

        if hasattr(self.parameters, 'query_ripe_stat'):
            self.logger.warning("The parameter 'query_ripe_stat' is deprecated and will be "
                                "removed in 2.0. Use 'query_ripe_stat_asn' and "
                                "'query_ripe_stat_ip' instead'.")
        self.query_db_asn = getattr(self.parameters, 'query_ripe_db_asn', True)
        self.query_db_ip = getattr(self.parameters, 'query_ripe_db_ip', True)
        self.query_stat_asn = getattr(self.parameters, 'query_ripe_stat_asn',
                                      getattr(self.parameters, 'query_ripe_stat', True))
        self.query_stat_ip = getattr(self.parameters, 'query_ripe_stat_ip',
                                     getattr(self.parameters, 'query_ripe_stat', True))
        self.mode = getattr(self.parameters, 'mode', 'append')

        self.set_request_parameters()

        cache_host = getattr(self.parameters, 'redis_cache_host')
        cache_port = getattr(self.parameters, 'redis_cache_port')
        cache_db = getattr(self.parameters, 'redis_cache_db')
        cache_ttl = getattr(self.parameters, 'redis_cache_ttl')
        if cache_host and cache_port and cache_db and cache_ttl:
            self.cache = Cache(cache_host, cache_port, cache_db, cache_ttl,
                               getattr(self.parameters, "redis_cache_password",
                                       None)
                               )

    def query_ripestat(self, resource):
        cache_value = self.cache.get('stat:%s' % resource)
        if cache_value and cache_value != CACHE_NO_VALUE:
            return json.loads(cache_value)
        elif cache_value == CACHE_NO_VALUE:
            return []
        response = requests.get(self.URL_STAT.format(resource), data="",
                                proxies=self.proxy,
                                headers=self.http_header,
                                verify=self.http_verify_cert,
                                cert=self.ssl_client_cert,
                                timeout=self.http_timeout_sec)
        if response.status_code != 200:
            raise ValueError(STATUS_CODE_ERROR % response.status_code)

        try:
            reponse = response.json()
            if (reponse['data']['anti_abuse_contacts']['abuse_c']):
                contacts = [reponse['data']['anti_abuse_contacts']
                            ['abuse_c'][0]['email']]
                self.cache.set('stat:%s' % resource, json.dumps(contacts))
                return contacts
            else:
                self.cache.set('stat:%s' % resource, CACHE_NO_VALUE)
                return []
        except KeyError:
            self.cache.set('stat:%s' % resource, CACHE_NO_VALUE)
            return []

    def query_ripedb_ip(self, ip):
        cache_value = self.cache.get('dbip:%s' % ip)
        if cache_value:
            return json.loads(cache_value)
        response = requests.get(self.URL_DB_IP.format(ip), data="",
                                proxies=self.proxy,
                                headers=self.http_header,
                                verify=self.http_verify_cert,
                                cert=self.ssl_client_cert,
                                timeout=self.http_timeout_sec)
        if response.status_code != 200:
            raise ValueError(STATUS_CODE_ERROR % response.status_code)

        contacts = [response.json()['abuse-contacts']['email']]
        self.cache.set('dbip:%s' % ip, json.dumps(contacts))
        return contacts

    def query_ripedb_asn(self, asn):
        cache_value = self.cache.get('dbasn:%s' % asn)
        if cache_value and cache_value != CACHE_NO_VALUE:
            return json.loads(cache_value)
        response = requests.get(self.URL_DB_AS.format(asn), data="",
                                proxies=self.proxy,
                                headers=self.http_header,
                                verify=self.http_verify_cert,
                                cert=self.ssl_client_cert,
                                timeout=self.http_timeout_sec)
        if response.status_code != 200:
            """ If no abuse contact could be found, a 404 is given. """
            if response.status_code == 404:
                try:
                    if response.json()['message'].startswith('No abuse contact found for '):
                        self.cache.set('dbasn:%s' % asn, CACHE_NO_VALUE)
                        return []
                except ValueError:
                    pass
            raise ValueError(STATUS_CODE_ERROR % response.status_code)

        contacts = [response.json()['abuse-contacts']['email']]
        self.cache.set('dbasn:%s' % asn, json.dumps(contacts))
        return contacts

    def process(self):
        event = self.receive_message()

        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            abuse_key = key + "abuse_contact"
            asn_key = key + "asn"

            ip = event.get(ip_key, None)
            if self.mode == 'append':
                abuse = (event.get(abuse_key).split(',') if abuse_key in event
                         else [])
            else:
                abuse = []
            asn = event.get(asn_key, None)
            if self.query_db_asn and asn:
                abuse.extend(self.query_ripedb_asn(asn))
            if self.query_db_ip and ip:
                abuse.extend(self.query_ripedb_ip(ip))
            if self.query_stat_asn and asn:
                abuse.extend(self.query_ripestat(asn))
            if self.query_stat_ip and ip:
                abuse.extend(self.query_ripestat(ip))

            event.add(abuse_key, ','.join(filter(None, set(abuse))), overwrite=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = RIPENCCExpertBot
