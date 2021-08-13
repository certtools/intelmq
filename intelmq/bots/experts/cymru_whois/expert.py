# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import json

from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import IPAddress
from intelmq.lib.mixins import CacheMixin

from ._lib import Cymru

CACHE_KEY = "%d_%s"


class CymruExpertBot(Bot, CacheMixin):
    """Add ASN, netmask, AS name, country, registry and allocation time from the Cymru Whois DNS service"""
    overwrite = False
    redis_cache_db: int = 5
    redis_cache_host: str = "127.0.0.1"  # TODO: could be ipaddress
    redis_cache_password: str = None
    redis_cache_port: int = 6379
    redis_cache_ttl: int = 86400

    def process(self):
        event = self.receive_message()

        keys = ["source.%s", "destination.%s"]

        for key in keys:
            ip_key = key % "ip"

            if ip_key not in event:
                continue

            address = event.get(ip_key)
            cache_key = CACHE_KEY % (IPAddress.version(address), address)
            result_json = self.cache_get(cache_key)

            if result_json:
                result = json.loads(result_json)
            else:
                result = Cymru.query(address)
                if not result:
                    self.logger.info('Got no result from Cymru for IP address %r.',
                                     address)
                result_json = json.dumps(result)
                self.cache_set(cache_key, result_json)

            if not result:
                continue

            for result_key, result_value in result.items():
                if result_key == 'registry' and result_value == 'other':
                    continue
                event.add(key % result_key, result_value, overwrite=self.overwrite)

        self.send_message(event)
        self.acknowledge_message()


BOT = CymruExpertBot
