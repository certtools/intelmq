# SPDX-FileCopyrightText: 2018 olekristoffer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
See README for database download.
"""

import io
import csv
import sys
import tarfile
import pathlib
import requests

from intelmq.lib.bot import Bot
from intelmq.lib.utils import get_bots_settings, create_request_session
from intelmq.bin.intelmqctl import IntelMQController


class RecordedFutureIPRiskExpertBot(Bot):
    """Adds the Risk Score from RecordedFuture IPRisk associated with source.ip or destination.ip with a local database"""
    api_token: str = "<insert Recorded Future IPRisk API token>"
    database: str = "/opt/intelmq/var/lib/bots/recordedfuture_iprisk/rfiprisk.dat"  # TODO: should be pathlib.Path
    overwrite: bool = False

    _database = dict()

    def init(self):
        self.logger.info("Loading recorded future risk list.")

        try:
            with open(self.database) as fp:
                rfreader = csv.DictReader(fp)
                for row in rfreader:
                    self._database[row['Name']] = int(row['Risk'])

        except IOError:
            raise ValueError("Recorded future risklist not defined or failed on open.")

    def process(self):
        event = self.receive_message()

        for key in ["source", "destination"]:
            if key + '.ip' in event:
                if "extra.rf_iprisk." + key not in event:
                    event.add("extra.rf_iprisk." + key, self._database.get(event.get(key + '.ip'), 0))
                elif "extra.rf_iprisk." + key in event and self.overwrite:
                    event.change("extra.rf_iprisk." + key, self._database.get(event.get(key + '.ip'), 0))

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
        api_token = None
        runtime_conf = get_bots_settings()
        try:
            for bot in runtime_conf:
                if runtime_conf[bot]["module"] == __name__:
                    api_token = runtime_conf[bot]["parameters"]["api_token"]
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
            response = session.get("https://api.recordedfuture.com/v2/ip/risklist",
                                   params={
                                       "format": "csv/splunk",
                                       "gzip": "true",
                                       "list": "large"
                                   },
                                   headers={
                                       "X-RFToken": api_token
                                   })

        except requests.exceptions.RequestException as e:
            sys.exit("Database update failed. Connection Error: {0}".format(e))

        if response.status_code == 401:
            sys.exit("Database update failed. Your API token is invalid.")

        if response.status_code != 200:
            sys.exit("Database update failed. Server responded: {0}.\n"
                     "URL: {1}".format(response.status_code, response.url))

        database_data = None

        with tarfile.open(fileobj=io.BytesIO(response.content), mode='r:gz') as archive:
            for member in archive.getmembers():
                if "rfiprisk.dat" in member.name:
                    database_data = archive.extract(member)
                    break

        if not database_data:
            sys.exit("Database update failed. Could not locate file 'rfiprisk.dat' in the downloaded archive.")

        for database_path in set(bots.values()):
            database_dir = pathlib.Path(database_path).parent
            database_dir.mkdir(parents=True, exist_ok=True)
            with open(database_path, "w") as database:
                database.write(database_data)

        if verbose:
            print("Database updated. Reloading affected bots.")

        ctl = IntelMQController()
        for bot in bots.keys():
            ctl.bot_reload(bot)


BOT = RecordedFutureIPRiskExpertBot
