# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os
import io
import re
import sys
import bz2
import pathlib
import requests

from intelmq.lib.bot import ExpertBot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.utils import get_bots_settings, create_request_session
from intelmq.bin.intelmqctl import IntelMQController

try:
    import pyasn
    import pyasn.mrtx
except ImportError:
    pyasn = None


class ASNLookupExpertBot(ExpertBot):
    """Add ASN and netmask information from a local BGP dump"""
    database = None  # TODO: should be pathlib.Path
    autoupdate_cached_database: bool = True  # Activate/deactivate update-database functionality

    def init(self):
        if pyasn is None:
            raise MissingDependencyError("pyasn")

        try:
            self._database = pyasn.pyasn(self.database)
        except OSError:
            self.logger.error("pyasn data file does not exist or could not be "
                              "accessed in %r.", self.database)
            self.logger.error("Read 'bots/experts/asn_lookup/README' and "
                              "follow the procedure.")
            self.stop()

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:

            ip_key = key + "ip"
            asn_key = key + "asn"
            bgp_key = key + "network"

            if ip_key not in event:
                continue

            info = self._database.lookup(event.get(ip_key))

            if info:
                if info[0]:
                    event.add(asn_key, str(info[0]), overwrite=True)
                if info[1]:
                    event.add(bgp_key, str(info[1]), overwrite=True)

        self.send_message(event)
        self.acknowledge_message()

    @staticmethod
    def check(parameters):
        if not os.path.exists(parameters.get('database', '')):
            return [["error", "File given as parameter 'database' does not exist."]]
        try:
            pyasn.pyasn(parameters['database'])
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
                    bots[bot] = runtime_conf[bot]["parameters"]["database"]

        except KeyError as e:
            sys.exit(f"Database update failed. Your configuration of {bot} is missing key {e}.")

        if not bots:
            if verbose:
                print(f"Database update skipped. No bots of type {__name__} present in runtime configuration or database update disabled with parameter 'autoupdate_cached_database'.")
            sys.exit(0)

        # we only need to import now. If there are no asn_lookup bots, this dependency does not need to be installed
        if pyasn is None:
            raise MissingDependencyError("pyasn")

        try:
            if verbose:
                print("Searching for the latest database update...")
            session = create_request_session()
            base_url = "http://archive.routeviews.org/route-views4/bgpdata/"
            response = session.get(base_url)
            pattern = re.compile(r"href=\"(\d{4}\.\d{2})/\"")
            months = pattern.findall(response.text)
            months.sort(reverse=True)

            if not months:
                sys.exit("Database update failed. Couldn't find the latest database update.")

            # routeviews website creates next month's directory on 28th of the current month
            # therefore on 28th, 29th, 30th, 31st it's necessary to find the second highest month directory
            for i in range(2):
                url = base_url + str(months[i]) + "/RIBS/"
                response = session.get(url)
                pattern = re.compile(r"href=\"(rib\.\d{8}\.\d{4}\.bz2)\"")
                days = pattern.findall(response.text)
                days.sort(reverse=True)
                print(url)
                if days:
                    break

            if not days:
                sys.exit("Database update failed. Couldn't find the latest database update.")

            if verbose:
                print("Downloading the latest database update...")
            url += days[0]
            response = session.get(url)

            if response.status_code != 200:
                sys.exit("Database update failed. Server responded: {}.\n"
                         "URL: {}".format(response.status_code, response.url))

        except requests.exceptions.RequestException as e:
            sys.exit(f"Database update failed. Connection Error: {e}")

        with bz2.open(io.BytesIO(response.content)) as archive:
            if verbose:
                print("Parsing the latest database update...")
            prefixes = pyasn.mrtx.parse_mrt_file(archive, print_progress=False, skip_record_on_error=True)

        for database_path in set(bots.values()):
            database_dir = pathlib.Path(database_path).parent
            database_dir.mkdir(parents=True, exist_ok=True)
            pyasn.mrtx.dump_prefixes_to_file(prefixes, database_path)

        if verbose:
            print("Database updated. Reloading affected bots.")

        ctl = IntelMQController()
        for bot in bots.keys():
            ctl.bot_reload(bot)


BOT = ASNLookupExpertBot
