# -*- coding: utf-8 -*-
import validators
import os.path
from intelmq.lib.bot import Bot


class DomainValidExpertBot(Bot):
    domain_field: str = 'source.fqdn'
    tlds_domains_list = '/opt/intelmq/var/lib/bots/domain_valid/tlds-alpha-by-domain.txt'

    def init(self):
        pass

    def process(self):
        event = self.receive_message()

        tlds_list = self.get_tlds_domain_list()

        is_valid = False
        if self.domain_field in event:
            if validators.domain(event[self.domain_field]) and event[self.domain_field].find('_') == -1 and event[self.domain_field].split('.')[-2:][1] in tlds_list:
                is_valid = True
            else:
                self.logger.debug(f"Filtered out event with search field {self.domain_field} and event time {event[self.domain_field]} .")

        if is_valid:
            self.send_message(event)
        self.acknowledge_message()
        return

    def get_tlds_domain_list(self):
        lines = []
        if os.path.isfile(self.tlds_domains_list):
            with open(self.tlds_domains_list) as file:
                first_line = file.readline()
                lines = [line.strip().lower() for line in file]
        else:
            self.logger.debug(f"Tld domain list file not found {self.tlds_domains_list} .")
        return lines


BOT = DomainValidExpertBot
