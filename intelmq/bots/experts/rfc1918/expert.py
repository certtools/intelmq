# *- coding: utf-8 -*-
"""
RFC 1918 Will Drop Local IP from a given record and a bit more.
  It checks for RFC1918 IPv4 Hosts
  It checks for localhost, multicast and test LANs
  It checks for Link Local and Documentation LAN in IPv6

Need only to feed the parameter "fields" to set the name of the field
parameter designed to be filtered out.
Several parameters could be used, separated by ","
It could sanitize the whole records with the "drop" parameter set to "yes"

Sources:
https://tools.ietf.org/html/rfc1918
https://tools.ietf.org/html/rfc2606
https://tools.ietf.org/html/rfc3849
https://tools.ietf.org/html/rfc4291
https://tools.ietf.org/html/rfc5737
https://en.wikipedia.org/wiki/IPv4
"""

import ipaddress
from urllib.parse import urlparse

from intelmq.lib.bot import Bot

NETWORKS = ("10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
            "169.254.0.0/16", "172.16.0.0/12", "192.0.0.0/24", "192.0.2.0/24",
            "192.88.99.0/24", "192.168.0.0/16", "198.18.0.0/15",
            "198.51.100.0/24", "203.0.113.0/24", "224.0.0.0/4", "240.0.0.0/4",
            "255.255.255.255/32", "fe80::/64", "2001:0db8::/32")
DOMAINS = ('.test', '.example', '.invalid', '.localhost', 'example.com',
           'example.net', 'example.org')


class RFC1918ExpertBot(Bot):

    def init(self):
        self.fields = self.parameters.fields.lower().strip().split(",")
        self.policy = self.parameters.policy.lower().strip().split(",")

    def is_in_net(self, ip, iprange):
        return ipaddress.ip_address(ip) in ipaddress.ip_network(iprange)

    def process(self):
        event = self.receive_message()

        for field, policy in zip(self.fields, self.policy):
            if field not in event:
                continue
            value = event.get(field)
            if field.endswith('.ip'):
                check = any(self.is_in_net(value, iprange) for iprange in NETWORKS)
            elif field.endswith('.fqdn'):
                check = any(value.endswith(domain) for domain in DOMAINS)
            elif field.endswith('.url'):
                check = any(urlparse(value).netloc.endswith(domain)
                            for domain in DOMAINS)
            if check:
                if policy == 'del':
                    self.logger.debug("Value removed from %s.", field)
                    del event[field]
                elif policy == 'drop':
                    self.acknowledge_message()
                    return
                break
        self.send_message(event)
        self.acknowledge_message()


BOT = RFC1918ExpertBot
