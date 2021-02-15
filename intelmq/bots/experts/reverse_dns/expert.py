# -*- coding: utf-8 -*-

from datetime import datetime

import dns.exception
import dns.resolver
import dns.reversename

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.harmonization import IPAddress

MINIMUM_BGP_PREFIX_IPV4 = 24
MINIMUM_BGP_PREFIX_IPV6 = 128
DNS_EXCEPTION_VALUE = "__dns-exception"


class InvalidPTRResult(ValueError):
    pass


class ReverseDnsExpertBot(Bot):
    """Get the correspondent domain name for source and destination IP address"""
    cache_ttl_invalid_response: int = 60
    overwrite: bool = False
    redis_cache_db: int = 7
    redis_cache_host: str = "127.0.0.1"  # TODO: should be ipaddress
    redis_cache_password: str = None
    redis_cache_port: int = 6379
    redis_cache_ttl: int = 86400

    def init(self):
        self.cache = Cache(self.redis_cache_host,
                           self.redis_cache_port,
                           self.redis_cache_db,
                           self.redis_cache_ttl,
                           self.redis_cache_password
                           )

        if not hasattr(self, 'overwrite'):
            self.logger.warning("Parameter 'overwrite' is not given, assuming 'True'. "
                                "Please set it explicitly, default will change to "
                                "'False' in version 3.0.0'.")

    def process(self):
        event = self.receive_message()

        keys = ["source.%s", "destination.%s"]

        for key in keys:
            ip_key = key % "ip"

            if ip_key not in event:
                continue
            if key % 'reverse_dns' in event and not self.overwrite:
                continue

            ip = event.get(ip_key)
            ip_version = IPAddress.version(ip)
            ip_integer = IPAddress.to_int(ip)

            if ip_version == 4:
                minimum = MINIMUM_BGP_PREFIX_IPV4

            elif ip_version == 6:
                minimum = MINIMUM_BGP_PREFIX_IPV6

            cache_key = bin(ip_integer)[2: minimum + 2]
            cachevalue = self.cache.get(cache_key)

            result = None
            if cachevalue == DNS_EXCEPTION_VALUE:
                continue
            elif cachevalue:
                result = cachevalue
            else:
                rev_name = dns.reversename.from_address(ip)
                try:
                    results = dns.resolver.query(rev_name, "PTR")
                    expiration = results.expiration
                    for result in results:
                        # use first valid result
                        if event.is_valid('source.reverse_dns', str(result)):
                            break
                    else:
                        raise InvalidPTRResult
                except (dns.exception.DNSException, InvalidPTRResult) as e:
                    # Set default TTL for 'DNS query name does not exist' error
                    ttl = None if isinstance(e, dns.resolver.NXDOMAIN) else self.cache_ttl_invalid_response
                    self.cache.set(cache_key, DNS_EXCEPTION_VALUE, ttl)
                    result = None

                else:
                    ttl = datetime.fromtimestamp(expiration) - datetime.now()
                    self.cache.set(cache_key, str(result),
                                   ttl=int(ttl.total_seconds()))

            if result is not None:
                event.add(key % 'reverse_dns', str(result), overwrite=self.overwrite)

        self.send_message(event)
        self.acknowledge_message()


BOT = ReverseDnsExpertBot
