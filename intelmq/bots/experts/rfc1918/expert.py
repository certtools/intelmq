# *- coding: utf-8 -*-
"""
RFC 1918 Will Drop Local IP from a given record and a bit more.
  It checks for RFC1918 IPv4 Hosts
  It checks for localhost, multicast and test LANs
  It checks for Link Local and Documentation LAN in IPv6
  It checks for RFC538 ASNs

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
https://en.wikipedia.org/wiki/Autonomous_system_(Internet)
"""

import ipaddress
from urllib.parse import urlparse

from intelmq.lib.bot import Bot

NETWORKS = ("10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
            "169.254.0.0/16", "172.16.0.0/12", "192.0.0.0/24", "192.0.2.0/24",
            "192.88.99.0/24", "192.168.0.0/16", "198.18.0.0/15",
            "198.51.100.0/24", "203.0.113.0/24", "224.0.0.0/4", "240.0.0.0/4",
            "255.255.255.255/32", "fe80::/64", "2001:0db8::/32")
DOMAINS = ("example.com", "example.net", "example.org")
# Also contains TLDs
SUBDOMAINS = (".test", ".example", ".invalid", ".localhost", ".example.com",
              ".example.net", ".example.org")
ASN16 = tuple(range(64496, 64512))
ASN32 = tuple(range(65536, 65552))
ASNS = ASN16 + ASN32


class RFC1918ExpertBot(Bot):

    def init(self):
        self.fields = self.parameters.fields.lower().strip().split(",")
        self.policy = self.parameters.policy.lower().strip().split(",")

        if len(self.fields) != len(self.policy):
            raise ValueError("Length of parameters 'fields' (%d) and 'policy' (%d) is unequal."
                             "" % (len(self.fields), len(self.policy)))

        self.ip_networks = [ipaddress.ip_network(iprange) for iprange in NETWORKS]

    @staticmethod
    def check(parameters):
        fields = len(parameters.get("fields", "").split(","))
        policy = len(parameters.get("policy", "").split(","))
        if fields != policy:
            return [["error",
                     "Length of parameters 'fields' (%d) and 'policy' (%d) is unequal."
                     "" % (fields, policy)]]

    def is_in_net(self, ip):
        return any(ip in iprange for iprange in self.ip_networks)

    def is_in_domains(self, value):
        return value in DOMAINS

    def is_subdomain(self, value):
        return any(value.endswith(domain) for domain in SUBDOMAINS)

    def process(self):
        event = self.receive_message()

        for field, policy in zip(self.fields, self.policy):
            netcheck = False
            if field not in event:
                self.logger.debug("Field %r not present.", field)
                continue
            value = event.get(field)
            if field.endswith(".ip"):
                ip = ipaddress.ip_address(value)
                netcheck = self.is_in_net(ip)
                if netcheck:
                    self.logger.debug("Field %r (%r) matched IP address check.", field, value)
            elif field.endswith(".fqdn"):
                netcheck = self.is_in_domains(value) or self.is_subdomain(value)
                if netcheck:
                    self.logger.debug("Field %r (%r) matched Domain/TLD check.", field, value)
            elif field.endswith(".url"):
                netloc = urlparse(value).netloc
                try:
                    ip = ipaddress.ip_address(netloc)
                except ValueError:
                    netcheck = self.is_in_domains(netloc) or self.is_subdomain(netloc)
                    if netcheck:
                        self.logger.debug("Field %r (%r) matched Domain/TLD check.", field, value)
                else:
                    netcheck = self.is_in_net(ip)
                    if netcheck:
                        self.logger.debug("Field %r (%r) matched IP address check.", field, value)
            elif field.endswith(".asn"):
                netcheck = value in ASNS
                if netcheck:
                    self.logger.debug("Field %r (%r) matched ASN check.", field, value)
            if netcheck:
                if policy == "del":
                    self.logger.debug("Value removed from %s.", field)
                    del event[field]
                elif policy == "drop":
                    self.logger.debug("Dropping event.")
                    self.acknowledge_message()
                    return
                break
        self.send_message(event)
        self.acknowledge_message()


BOT = RFC1918ExpertBot
