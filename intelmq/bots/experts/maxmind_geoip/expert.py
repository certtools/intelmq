# -*- coding: utf-8 -*-
"""
This product includes GeoLite2 data created by MaxMind, available from
<a href="http://www.maxmind.com">http://www.maxmind.com</a>.
"""

import io
import sys
import pathlib
import requests
import tarfile

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq import RUNTIME_CONF_FILE
from intelmq.lib.utils import load_configuration, create_request_session
from intelmq.bin.intelmqctl import IntelMQController

try:
    import geoip2.database
except ImportError:
    geoip2 = None


class GeoIPExpertBot(Bot):

    def init(self):
        if geoip2 is None:
            raise MissingDependencyError("geoip2")

        try:
            self.database = geoip2.database.Reader(self.parameters.database)
        except IOError:
            self.logger.exception("GeoIP Database does not exist or could not "
                                  "be accessed in %r.",
                                  self.parameters.database)
            self.logger.error("Read 'bots/experts/geoip/README' and follow the"
                              " procedure.")
            self.stop()
        self.overwrite = getattr(self.parameters, 'overwrite', False)
        self.registered = getattr(self.parameters, 'use_registered', False)

    def process(self):
        event = self.receive_message()

        for key in ["source.%s", "destination.%s"]:
            geo_key = key % "geolocation.%s"

            if key % "ip" not in event:
                continue

            ip = event.get(key % "ip")

            try:
                info = self.database.city(ip)

                if self.registered:
                    if info.registered_country.iso_code:
                        event.add(geo_key % "cc", info.registered_country.iso_code,
                                  overwrite=self.parameters.overwrite)
                else:
                    if info.country.iso_code:
                        event.add(geo_key % "cc", info.country.iso_code,
                                  overwrite=self.parameters.overwrite)

                if info.location.latitude:
                    event.add(geo_key % "latitude", info.location.latitude,
                              overwrite=self.parameters.overwrite)

                if info.location.longitude:
                    event.add(geo_key % "longitude", info.location.longitude,
                              overwrite=self.parameters.overwrite)

                if info.city.name:
                    event.add(geo_key % "city", info.city.name,
                              overwrite=self.parameters.overwrite)

            except geoip2.errors.AddressNotFoundError:
                pass

        self.send_message(event)
        self.acknowledge_message()

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
        license_key = None
        runtime_conf = load_configuration(RUNTIME_CONF_FILE)
        try:
            for bot in runtime_conf:
                if runtime_conf[bot]["module"] == __name__:
                    license_key = runtime_conf[bot]["parameters"]["license_key"]
                    bots[bot] = runtime_conf[bot]["parameters"]["database"]

        except KeyError as e:
            error = "Database update failed. Your configuration of {0} is missing key {1}.".format(bot, e)
            if str(e) == "'license_key'":
                error += "\n"
                error += "Since December 30, 2019 you need to register for a free license key to access GeoLite2 database.\n"
                error += "https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/"
                sys.exit(error)
            else:
                sys.exit(error)

        if not bots:
            print("Database update skipped. No bots of type {0} present in runtime.conf.".format(__name__))
            sys.exit(0)

        # we only need to import now, if there are no maxmind_geoip bots, this dependency does not need to be installed
        try:
            import maxminddb
        except ImportError:
            raise MissingDependencyError('maxminddb',
                                         additional_text="Package maxminddb should be present because it "
                                                         "is a dependency for the required geoip2 package.")

        try:
            print("Downloading the latest database update...")
            session = create_request_session()
            response = session.get("https://download.maxmind.com/app/geoip_download",
                                   params={
                                       "license_key": license_key,
                                       "edition_id": "GeoLite2-City",
                                       "suffix": "tar.gz"
                                   })
        except requests.exceptions.RequestException as e:
            sys.exit("Database update failed. Connection Error: {0}".format(e))

        if response.status_code == 401:
            sys.exit("Database update failed. Your license key is invalid.")

        if response.status_code != 200:
            sys.exit("Database update failed. Server responded: {0}.\n"
                     "URL: {1}".format(response.status_code, response.url))

        database_data = None

        try:
            with tarfile.open(fileobj=io.BytesIO(response.content), mode='r:gz') as archive:
                for member in archive.getmembers():
                    if "GeoLite2-City.mmdb" in member.name:
                        database_data = maxminddb.open_database(database=archive.extractfile(member),
                                                                mode=maxminddb.MODE_FD)
                        break

        except maxminddb.InvalidDatabaseError:
            sys.exit("Database update failed. Database file invalid.")

        if not database_data:
            sys.exit("Database update failed. Could not locate file 'GeoLite2-City.mmbd' in the downloaded archive.")

        for database_path in set(bots.values()):
            database_dir = pathlib.Path(database_path).parent
            database_dir.mkdir(parents=True, exist_ok=True)
            with open(database_path, "wb") as database:
                database.write(database_data._buffer)

        print("Database updated. Reloading affected bots.")

        ctl = IntelMQController()
        for bot in bots.keys():
            ctl.bot_reload(bot)


BOT = GeoIPExpertBot
