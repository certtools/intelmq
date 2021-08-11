# -*- coding: utf-8 -*-
"""
Domain validator

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import validators

import os.path
import pathlib
import sys

import requests.exceptions

from intelmq.lib.bot import Bot
from intelmq.lib.utils import get_bots_settings, create_request_session
from intelmq.bin.intelmqctl import IntelMQController


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
            if validators.domain(event[self.domain_field]) and event[self.domain_field].find('_') == -1 and \
                    event[self.domain_field].split('.')[-2:][1] in tlds_list:
                is_valid = True
            else:
                self.logger.debug(
                    f"Filtered out event with search field {self.domain_field} and event time {event[self.domain_field]} .")

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

    @classmethod
    def run(cls, parsed_args=None):
        if not parsed_args:
            parsed_args = cls._create_argparser().parse_args()

        if parsed_args.update_database:
            cls.update_database()

        else:
            super().run(parsed_args=parsed_args)

    @classmethod
    def _create_argparser(cls):
        argparser = super()._create_argparser()
        argparser.add_argument("--update-database", action='store_true', help='downloads latest database data')
        return argparser

    @classmethod
    def update_database(cls):
        bots = {}
        runtime_conf = get_bots_settings()
        try:
            for bot in runtime_conf:
                if runtime_conf[bot]["module"] == __name__:
                    bots[bot] = runtime_conf[bot]["parameters"]["suffix_file"]

        except KeyError as e:
            sys.exit("Database update failed. Your configuration of {0} is missing key {1}.".format(bot, e))

        if not bots:
            print("Database update skipped. No bots of type {0} present in runtime.conf.".format(__name__))
            sys.exit(0)

        try:
            session = create_request_session()
            url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
            print("Downloading the latest database update...")
            response = session.get(url)

            if not response.ok:
                sys.exit("Database update failed. Server responded: {0}.\n"
                         "URL: {1}".format(response.status_code, response.url))

        except requests.exceptions.RequestException as e:
            sys.exit("Database update failed. Connection Error: {0}".format(e))

        for database_path in set(bots.values()):
            database_dir = pathlib.Path(database_path).parent
            database_dir.mkdir(parents=True, exist_ok=True)
            with open(database_path, "wb") as database:
                database.write(response.content)

        print("Database updated. Reloading affected bots.")

        ctl = IntelMQController()
        for bot in bots.keys():
            ctl.bot_reload(bot)


BOT = DomainValidExpertBot
