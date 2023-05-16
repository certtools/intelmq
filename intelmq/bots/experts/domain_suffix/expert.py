# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
The library publicsuffixlist will be used if installed,
otherwise our own internal fallback is used.
"""
import codecs
import pathlib
import os.path
import sys

import requests.exceptions

from intelmq.lib.bot import ExpertBot
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.utils import get_bots_settings, create_request_session
from intelmq.bin.intelmqctl import IntelMQController

try:
    from publicsuffixlist import PublicSuffixList
except ImportError:
    from ._lib import PublicSuffixList


ALLOWED_FIELDS = ['fqdn', 'reverse_dns']


class DomainSuffixExpertBot(ExpertBot):
    """Extract the domain suffix from a domain and save it in the the domain_suffix field. Requires a local file with valid domain suffixes"""
    field: str = None
    suffix_file: str = None  # TODO: should be pathlib.Path
    autoupdate_cached_database: bool = True  # Activate/deactivate update-database functionality

    def init(self):
        if self.field not in ALLOWED_FIELDS:
            raise InvalidArgument('field', got=self.field, expected=ALLOWED_FIELDS)
        with codecs.open(self.suffix_file, encoding='UTF-8') as file_handle:
            self.psl = PublicSuffixList(source=file_handle, only_icann=True)

    def process(self):
        event = self.receive_message()
        for space in ('source', 'destination'):
            key = '.'.join((space, self.field))
            if key not in event:
                continue
            event['.'.join((space, 'domain_suffix'))] = self.psl.publicsuffix(domain=event[key])

        self.send_message(event)
        self.acknowledge_message()

    @staticmethod
    def check(parameters):
        if not os.path.exists(parameters.get('suffix_file', '')):
            return [["error", "File given as parameter 'suffix_file' does not exist."]]
        try:
            with codecs.open(parameters['suffix_file'], encoding='UTF-8') as database:
                PublicSuffixList(source=database, only_icann=True)
        except Exception as exc:
            return [["error", "Error reading database: %r." % exc]]

    @classmethod
    def run(cls, parsed_args=None):
        if not parsed_args:
            parsed_args = cls._create_argparser().parse_args()

        if parsed_args.update_database:
            cls.update_database(verbose=parsed_args.verbose)

        else:
            super().run(parsed_args=parsed_args)

    @classmethod
    def _create_argparser(cls):
        argparser = super()._create_argparser()
        argparser.add_argument("--update-database", action='store_true', help='downloads latest database data')
        argparser.add_argument("--verbose", action='store_true', help='be verbose')
        return argparser

    @classmethod
    def update_database(cls, verbose=False):
        bots = {}
        runtime_conf = get_bots_settings()
        try:
            for bot in runtime_conf:
                if runtime_conf[bot]["module"] == __name__ and runtime_conf[bot]['parameters'].get('autoupdate_cached_database', True):
                    bots[bot] = runtime_conf[bot]["parameters"]["suffix_file"]

        except KeyError as e:
            sys.exit(f"Database update failed. Your configuration of {bot} is missing key {e}.")

        if not bots:
            if verbose:
                print(f"Database update skipped. No bots of type {__name__} present in runtime configuration or database update disabled with parameter 'autoupdate_cached_database'.")
            sys.exit(0)

        # we only need to import now. If there are no asn_lookup bots, this dependency does not need to be installed

        try:
            session = create_request_session()
            url = "https://publicsuffix.org/list/public_suffix_list.dat"
            if verbose:
                print("Downloading the latest database update...")
            response = session.get(url)

            if not response.ok:
                sys.exit("Database update failed. Server responded: {}.\n"
                         "URL: {}".format(response.status_code, response.url))

        except requests.exceptions.RequestException as e:
            sys.exit(f"Database update failed. Connection Error: {e}")

        for database_path in set(bots.values()):
            database_dir = pathlib.Path(database_path).parent
            database_dir.mkdir(parents=True, exist_ok=True)
            with open(database_path, "wb") as database:
                database.write(response.content)

        if verbose:
            print("Database updated. Reloading affected bots.")

        ctl = IntelMQController()
        for bot in bots.keys():
            ctl.bot_reload(bot)


BOT = DomainSuffixExpertBot
