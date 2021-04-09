# -*- coding: utf-8 -*-
import json
from urllib.parse import urlparse

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.utils import create_request_session
from intelmq.lib.exceptions import MissingDependencyError

try:
    import requests
except ImportError:
    requests = None


class RDAPExpertBot(Bot):
    """ Get RDAP data"""
    rdap_order: list = ['abuse', 'technical', 'administrative', 'registrant', 'registrar']
    rdap_bootstrapped_servers: dict = {}
    redis_cache_db: int = 8
    redis_cache_host: str = "127.0.0.1"  # TODO: could be ipaddress
    redis_cache_password: str = None
    redis_cache_port: int = 6379
    redis_cache_ttl: int = 86400

    __rdap_directory: dict = {}
    __rdap_order_dict: dict = {}
    __session: requests.Session

    def init(self):
        if requests is None:
            raise MissingDependencyError("requests")

        self.set_request_parameters()
        self.__session = create_request_session(self)

        self.cache = Cache(self.redis_cache_host,
                           self.redis_cache_port,
                           self.redis_cache_db,
                           self.redis_cache_ttl,
                           self.redis_cache_password
                           )

        # get overall rdap data from iana
        resp = self.__session.get('https://data.iana.org/rdap/dns.json')
        self.__session.close()
        resp = resp.json()
        for service in resp['services']:
            for tld in service[0]:
                self.__rdap_directory[tld] = {"url": service[1][0]}

        # get bootstrapped servers
        for service in self.rdap_bootstrapped_servers:
            if type(self.rdap_bootstrapped_servers[service]) is str:
                self.__rdap_directory[service] = {"url": self.rdap_bootstrapped_servers[service]}
            elif type(self.rdap_bootstrapped_servers) is dict:
                self.__rdap_directory[service] = self.rdap_bootstrapped_servers[service]

    def parse_entities(self, vcardArray) -> list:
        vcard = []
        for vcardentry in vcardArray:
            if type(vcardentry) is str:
                continue

            for vcarddata in vcardentry:
                if vcarddata[0] == 'email':
                    vcard.append(vcarddata[3])
                    break
        return vcard

    def process(self):
        event = self.receive_message()

        if 'source.fqdn' in event:
            url = event.get('source.fqdn')
            cache_key = "rdap_%s" % (url)
            result = self.cache.get(cache_key)
            if result:
                event.add('source.abuse_contact', result)
            else:
                self.__session = create_request_session(self)
                domain_parts = url.split('.')
                domain_suffix = None
                while domain_suffix is None:
                    if ".".join(domain_parts) in self.__rdap_directory:
                        domain_suffix = ".".join(domain_parts)
                    else:
                        if len(domain_parts) == 0:
                            break
                        domain_parts.pop(0)

                if domain_suffix in self.__rdap_directory:
                    service = self.__rdap_directory[domain_suffix]
                    if 'auth' in service:
                        if service['auth']['type'] is 'jwt':
                            self.__session.headers['Authorization'] = "Bearer %s" % (service['auth']['token'])

                    resp = self.__session.get("{0}domain/{1}".format(service['url'], url))
                    resp = json.loads(resp.text)
                    for entity in resp['entities']:
                        if 'removed' in entity['roles']:
                            continue

                        for entrole in entity['roles']:
                            if 'entities' in entity:
                                for subentity in entity['entities']:
                                    for subentrole in subentity['roles']:
                                        if 'vcardArray' in subentity:
                                            entity_data = self.parse_entities(subentity['vcardArray'])
                                            self.__rdap_order_dict[subentrole] = {
                                                'email': entity_data[0] if len(entity_data) > 0 else None
                                            }
                            if 'vcardArray' in entity:
                                entity_data = self.parse_entities(entity['vcardArray'])
                                self.__rdap_order_dict[entrole] = {
                                    'email': entity_data[0] if len(entity_data) > 0 else None
                                }

                    for role in self.rdap_order:
                        if role in self.__rdap_order_dict:
                            if self.__rdap_order_dict[role]['email'] is not None:
                                self.cache.set(cache_key, self.__rdap_order_dict[role]['email'], 86800)
                                event.add('source.abuse_contact', self.__rdap_order_dict[role]['email'])
                                break

                self.__session.close()

        self.send_message(event)
        self.acknowledge_message()


BOT = RDAPExpertBot
