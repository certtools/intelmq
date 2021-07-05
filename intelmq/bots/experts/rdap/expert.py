# SPDX-FileCopyrightText: 2021 Sebastian Waldbauer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot
from intelmq.lib.utils import create_request_session
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.mixins import CacheMixin

try:
    import requests
except ImportError:
    requests = None


class RDAPExpertBot(Bot, CacheMixin):
    """ Get RDAP data"""
    rdap_order: list = ['abuse', 'technical', 'administrative', 'registrant', 'registrar']
    rdap_bootstrapped_servers: dict = {}
    redis_cache_db: int = 8
    redis_cache_host: str = "127.0.0.1"  # TODO: could be ipaddress
    redis_cache_password: str = None
    redis_cache_port: int = 6379
    redis_cache_ttl: int = 86400
    overwrite: bool = True

    __rdap_directory: dict = {}
    __rdap_order_dict: dict = {}
    __session: requests.Session

    def init(self):
        if requests is None:
            raise MissingDependencyError("requests")

        self.set_request_parameters()
        self.__session = create_request_session(self)

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
            result = self.cache_get(cache_key)
            if result:
                event.add('source.abuse_contact', result, overwrite=self.overwrite)
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

                url_without_domain_suffix = url.replace(".%s" % (domain_suffix), "")
                url = "%s.%s" % (url_without_domain_suffix.split(".")[-1], domain_suffix)

                if domain_suffix in self.__rdap_directory:
                    service = self.__rdap_directory[domain_suffix]
                    if 'auth' in service:
                        if service['auth']['type'] == 'jwt':
                            self.__session.headers['Authorization'] = "Bearer %s" % (service['auth']['token'])
                        else:
                            raise NotImplementedError("Authentication type %r (configured for service %r) is not implemented" % (service['auth'], domain_suffix))

                    resp = self.__session.get("{0}domain/{1}".format(service['url'], url))

                    if resp.status_code < 200 or resp.status_code > 299:
                        if resp.status_code == 404:
                            self.logger.debug('Treating server response 404 as no data.')
                            self.send_message(event)
                            self.acknowledge_message()
                            return
                        self.logger.debug("RDAP Server '%s' responded with '%d' for domain '%s'.", service['url'], resp.status_code, url)
                        raise ValueError(f"Unable to process server's response, the returned status-code was {resp.status_code}. Enable debug logging to see more details.")

                    try:
                        resp = resp.json()
                    except ValueError:
                        self.logger.debug("Server response: %r", resp.text)
                        raise ValueError("Unable to parse server response as JSON. Enable debug logging to see more details.")
                    for entity in resp['entities']:
                        if not isinstance(entity, dict):
                            self.logger.warning("Invalid type '%s' in entities of response for domain '%s' found.", type(entity), url)
                            continue

                        if 'removed' in entity['roles']:
                            continue

                        for entrole in entity['roles']:
                            if 'entities' in entity:
                                for subentity in entity['entities']:
                                    if not isinstance(subentity, dict):
                                        self.logger.warning("Invalid type '%s' in entities of response for domain '%s' found.", type(subentity), url)
                                        continue

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
                                self.cache_set(cache_key, self.__rdap_order_dict[role]['email'], self.redis_cache_ttl)
                                event.add('source.abuse_contact', self.__rdap_order_dict[role]['email'], overwrite=self.overwrite)
                                break

                self.__session.close()

        self.send_message(event)
        self.acknowledge_message()


BOT = RDAPExpertBot
