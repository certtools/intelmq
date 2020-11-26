# -*- coding: utf-8 -*-
import os
import io
import re
import sys
import bz2
import pathlib
import requests

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq import RUNTIME_CONF_FILE
from intelmq.lib.utils import load_configuration, create_request_session
from intelmq.bin.intelmqctl import IntelMQController

try:
    import pyasn
    import pyasn.mrtx
except ImportError:
    pyasn = None


class ASNLookupExpertBot(Bot):

    def init(self):
        if pyasn is None:
            raise MissingDependencyError("pyasn")

        try:
            self.database = pyasn.pyasn(self.parameters.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be "
                              "accessed in %r.", self.parameters.database)
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

            info = self.database.lookup(event.get(ip_key))

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
        runtime_conf = load_configuration(RUNTIME_CONF_FILE)
        try:
            for bot in runtime_conf:
                if runtime_conf[bot]["module"] == __name__:
                    bots[bot] = runtime_conf[bot]["parameters"]["database"]

        except KeyError as e:
            sys.exit("Database update failed. Your configuration of {0} is missing key {1}.".format(bot, e))

        if not bots:
            print("Database update skipped. No bots of type {0} present in runtime.conf.".format(__name__))
            sys.exit(0)

        # we only need to import now. If there are no asn_lookup bots, this dependency does not need to be installed
        if pyasn is None:
            raise MissingDependencyError("pyasn")

        try:
            print("Searching for the latest database update...")
            session = create_request_session()
            url = "http://archive.routeviews.org/route-views4/bgpdata/"
            response = session.get(url)
            pattern = re.compile(r"href=\"(\d{4}\.\d{2})/\"")
            months = pattern.findall(response.text)
            months.sort(reverse=True)

            if not months:
                sys.exit("Database update failed. Couldn't find the latest database update.")

            url += str(months[0]) + "/RIBS/"
            response = session.get(url)
            pattern = re.compile(r"href=\"(rib\.\d{8}\.\d{4}\.bz2)\"")
            days = pattern.findall(response.text)
            days.sort(reverse=True)

            if not days:
                sys.exit("Database update failed. Couldn't find the latest database update.")

            print("Downloading the latest database update...")
            url += days[0]
            response = session.get(url)

            if response.status_code != 200:
                sys.exit("Database update failed. Server responded: {0}.\n"
                         "URL: {1}".format(response.status_code, response.url))

        except requests.exceptions.RequestException as e:
            sys.exit("Database update failed. Connection Error: {0}".format(e))

        with bz2.open(io.BytesIO(response.content)) as archive:
            print("Parsing the latest database update...")
            prefixes = pyasn.mrtx.parse_mrt_file(archive, print_progress=False, skip_record_on_error=True)

        for database_path in set(bots.values()):
            database_dir = pathlib.Path(database_path).parent
            database_dir.mkdir(parents=True, exist_ok=True)
            pyasn.mrtx.dump_prefixes_to_file(prefixes, database_path)

        print("Database updated. Reloading affected bots.")

        ctl = IntelMQController()
        for bot in bots.keys():
            ctl.bot_reload(bot)


BOT = ASNLookupExpertBot
