# -*- coding: utf-8 -*-
"""
Trusted Introducer Expert

SPDX-FileCopyrightText: 2021 Intelmq Team <intelmq-team@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.mixins import HttpMixin


class TrustedIntroducerLookupExpertBot(Bot, HttpMixin):
    """ Get trusted introducer lookup data"""
    order: str = 'domain, asn'
    overwrite: bool = True

    __ti_dict: dict = {}
    __order: list = []

    def init(self):
        self.__order = [x.strip() for x in self.order.split(',')]

        for entry in self.__order:
            self.__ti_dict[entry] = {}

        resp = self.http_get(url="https://www.trusted-introducer.org/directory/teams.json")
        resp = resp.json()
        for introducer in resp:
            abuse_contact = ""
            if 'emails' not in introducer:
                continue

            for mail in introducer['emails']:
                if 'contact' in mail['usage']:
                    abuse_contact = mail['address']
                    break

            if 'domain' in self.__order:
                for domain in introducer['constituency']['domains']:
                    if '.*' in domain:  # skip wildcard tld's
                        continue

                    if '*.' in domain:
                        domain = domain.replace('*.', '')
                    self.__ti_dict['domain'][domain] = abuse_contact

            if 'asn' in self.__order:
                for asn in introducer['constituency']['asns']:
                    self.__ti_dict['asn'][asn] = abuse_contact

    def process(self):
        event = self.receive_message()

        abuse_contact = None

        for entity in self.__order:
            if abuse_contact is not None:
                break
            if entity == 'domain':
                if 'source.fqdn' in event:
                    url = event.get('source.fqdn')
                    domain_parts = url.split('.')
                    while abuse_contact is None:
                        if '.'.join(domain_parts) in self.__ti_dict['domain']:
                            abuse_contact = self.__ti_dict['domain']['.'.join(domain_parts)]
                        else:
                            if len(domain_parts) == 0:
                                break
                            domain_parts.pop(0)
            if entity == 'asn':
                if 'source.asn' in event:
                    asn = event.get('source.asn')
                    if asn in self.__ti_dict['asn']:
                        abuse_contact = self.__ti_dict['asn'][asn]

            event.add('source.abuse_contact', abuse_contact, overwrite=self.overwrite)

        self.send_message(event)
        self.acknowledge_message()


BOT = TrustedIntroducerLookupExpertBot
