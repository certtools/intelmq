# -*- coding: utf-8 -*-
'''
Reference:
https://stat.ripe.net/docs/data_api
https://github.com/RIPE-NCC/whois/wiki/WHOIS-REST-API-abuse-contact
'''

import json
import warnings

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.exceptions import MissingDependencyError

try:
    import requests
except ImportError:
    requests = None


STATUS_CODE_ERROR = 'HTTP status code was {}. Possible problem at the connection endpoint or network issue.'
CACHE_NO_VALUE = '__no_contact'


def clean_string(s):
    '''Clean RIPE reply specifics for splittable string replies'''
    values = set(s.split(','))
    values.discard('')
    return values


def clean_geo(geo_data):
    '''Clean RIPE reply specifics for geolocation query'''
    if 'country' in geo_data and geo_data['country'] == '?':
        del geo_data['country']
    return geo_data


class RIPEExpertBot(Bot):
    QUERY = {
        'db_ip': 'https://rest.db.ripe.net/abuse-contact/{}.json',
        'db_asn': 'https://rest.db.ripe.net/abuse-contact/as{}.json',
        'stat': 'https://stat.ripe.net/data/abuse-contact-finder/data.json?resource={}',
        'stat_geolocation': 'https://stat.ripe.net/data/maxmind-geo-lite/data.json?resource={}',
    }

    REPLY_TO_DATA = {
        'db_ip': lambda x: clean_string(x['abuse-contacts']['email']),
        'db_asn': lambda x: clean_string(x['abuse-contacts']['email']),
        'stat': lambda x: clean_string(x['data']['anti_abuse_contacts']['abuse_c'][0]['email']),
        'stat_geolocation': lambda x: clean_geo(x['data']['located_resources'][0]['locations'][0]),
    }

    GEOLOCATION_REPLY_TO_INTERNAL = {
        ('cc', 'country'),
        ('latitude', 'latitude'),
        ('longitude', 'longitude'),
        ('city', 'city')
    }

    def init(self):
        if requests is None:
            raise MissingDependencyError("requests")

        self.__mode = getattr(self.parameters, 'mode', 'append')
        self.__query = {
            "db_asn": getattr(self.parameters, 'query_ripe_db_asn', True),
            "db_ip": getattr(self.parameters, 'query_ripe_db_ip', True),
            "stat_asn": getattr(self.parameters, 'query_ripe_stat_asn', True),
            "stat_ip": getattr(self.parameters, 'query_ripe_stat_ip', True),
            "stat_geo": getattr(self.parameters, 'query_ripe_stat_geolocation', True)
        }

        self.__initialize_http_session()
        self.__initialize_cache()

    def __initialize_http_session(self):
        self.set_request_parameters()
        self.http_session = utils.create_request_session(self)

    def __initialize_cache(self):
        cache_host = getattr(self.parameters, 'redis_cache_host')
        cache_port = getattr(self.parameters, 'redis_cache_port')
        cache_db = getattr(self.parameters, 'redis_cache_db')
        cache_ttl = getattr(self.parameters, 'redis_cache_ttl')
        if cache_host and cache_port and cache_db and cache_ttl:
            self.__cache = Cache(cache_host, cache_port, cache_db, cache_ttl,
                                 getattr(self.parameters, "redis_cache_password", None))

    def process(self):
        event = self.receive_message()
        for target in {'source.', 'destination.'}:
            abuse_key = target + "abuse_contact"
            abuse = set(event.get(abuse_key).split(',')) if self.__mode == 'append' and abuse_key in event else set()

            asn = event.get(target + "asn", None)
            if asn:
                if self.__query['stat_asn']:
                    abuse.update(self.__perform_cached_query('stat', asn))
                if self.__query['db_asn']:
                    abuse.update(self.__perform_cached_query('db_asn', asn))

            ip = event.get(target + "ip", None)
            if ip:
                if self.__query['stat_ip']:
                    abuse.update(self.__perform_cached_query('stat', ip))
                if self.__query['db_ip']:
                    abuse.update(self.__perform_cached_query('db_ip', ip))
                if self.__query['stat_geo']:
                    info = self.__perform_cached_query('stat_geolocation', ip)

                    should_overwrite = self.__mode == 'replace'

                    for local_key, ripe_key in self.GEOLOCATION_REPLY_TO_INTERNAL:
                        if ripe_key in info:
                            event.add(target + "geolocation." + local_key, info[ripe_key], overwrite=should_overwrite)

            event.add(abuse_key, ','.join(abuse), overwrite=True)
        self.send_message(event)
        self.acknowledge_message()

    def __perform_cached_query(self, type, resource):
        cached_value = self.__cache.get('{}:{}'.format(type, resource))
        if cached_value:
            if cached_value == CACHE_NO_VALUE:
                return {}
            else:
                return json.loads(cached_value)
        else:
            response = self.http_session.get(self.QUERY[type].format(resource),
                                             data="", timeout=self.http_timeout_sec)

            if response.status_code != 200:
                if type == 'db_asn' and response.status_code == 404:
                    """ If no abuse contact could be found, a 404 is given. """
                    try:
                        if response.json()['message'].startswith('No abuse contact found for '):
                            self.__cache.set('{}:{}'.format(type, resource), CACHE_NO_VALUE)
                            return {}
                    except ValueError:
                        pass
                raise ValueError(STATUS_CODE_ERROR.format(response.status_code))
            try:
                response_data = response.json()

                # geolocation was marked as under maintenance by this, see
                # https://lists.cert.at/pipermail/intelmq-users/2020-March/000140.html
                status = response_data.get('data_call_status', '')
                if status.startswith('maintenance'):
                    warnings.warn('The API call %s is currently under maintenance. '
                                  'Response: %r. This warning is only given once per bot run.'
                                  '' % (type, status))

                data = self.REPLY_TO_DATA[type](response_data)
                self.__cache.set('{}:{}'.format(type, resource),
                                 (json.dumps(list(data) if isinstance(data, set) else data) if data else CACHE_NO_VALUE))
                return data
            except (KeyError, IndexError):
                self.__cache.set('{}:{}'.format(type, resource), CACHE_NO_VALUE)

            return {}


BOT = RIPEExpertBot
