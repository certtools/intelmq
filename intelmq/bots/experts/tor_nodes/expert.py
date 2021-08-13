# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
See README for database download.
"""
import re
import sys
import pathlib
import requests

from intelmq.lib.bot import Bot
from intelmq.lib.utils import get_bots_settings, create_request_session
from intelmq.bin.intelmqctl import IntelMQController


class TorExpertBot(Bot):
    """Check if the IP address is a Tor Exit Node based on a local database of TOR nodes"""
    database: str = "/opt/intelmq/var/lib/bots/tor_nodes/tor_nodes.dat"  # TODO: pathlib.Path
    overwrite: bool = False

    _database = set()

    def init(self):
        self.logger.info("Loading TOR exit node IPs.")

        try:
            with open(self.database) as fp:
                for line in fp:
                    line = line.strip()

                    if len(line) == 0 or line[0] == "#":
                        continue

                    self._database.add(line)

        except IOError:
            raise ValueError("TOR rule not defined or failed on open.")

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:
            if key + 'ip' in event:
                if key + 'tor_node' not in event:
                    if event.get(key + 'ip') in self._database:
                        event.add(key + 'tor_node', True)
                elif key + 'tor_node' in event and self.overwrite:
                    if event.get(key + 'ip') in self._database:
                        event.change(key + 'tor_node', True)

        self.send_message(event)
        self.acknowledge_message()

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
                if runtime_conf[bot]["module"] == __name__:
                    bots[bot] = runtime_conf[bot]["parameters"]["database"]

        except KeyError as e:
            sys.exit("Database update failed. Your configuration of {0} is missing key {1}.".format(bot, e))

        if not bots:
            if verbose:
                print("Database update skipped. No bots of type {0} present in runtime.conf.".format(__name__))
            sys.exit(0)

        try:
            if verbose:
                print("Downloading the latest database update...")
            session = create_request_session()
            response = session.get("https://check.torproject.org/exit-addresses")
        except requests.exceptions.RequestException as e:
            sys.exit("Database update failed. Connection Error: {0}".format(e))

        if response.status_code != 200:
            sys.exit("Database update failed. Server responded: {0}.\n"
                     "URL: {1}".format(response.status_code, response.url))

        pattern = re.compile(r"ExitAddress ([^\s]+)")
        tor_exits = "\n".join(pattern.findall(response.text))

        for database_path in set(bots.values()):
            database_dir = pathlib.Path(database_path).parent
            database_dir.mkdir(parents=True, exist_ok=True)
            with open(database_path, "w") as database:
                database.write(tor_exits)

        if verbose:
            print("Database updated. Reloading affected bots.")

        ctl = IntelMQController()
        for bot in bots.keys():
            ctl.bot_reload(bot)


BOT = TorExpertBot
