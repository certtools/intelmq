# -*- coding: utf-8 -*-
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

CLASSIFICATION = {
    "c&c": "c&c",
    "scanning host": "scanner",
    "malicious host": "malware",
    "spamming": "spam",
    "malware domain": "malware",
    "malware ip": "malware",
    "malware distribution": "malware",
}


class AlienVaultParserBot(Bot):

    def process(self):
        report = self.receive_message()
        if (report is None or not report.contains("raw") or
                len(report.get("raw").strip()) == 0):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()
            if len(row) == 0:
                continue

            values = row.split("#")

            # Send one event per classification
            classification_types = list()
            if values[3].strip().find(";") > 0:
                classification_types.extend(values[3].split(";"))
            else:
                classification_types.append(values[3])

            for ctype in classification_types:

                event = Event(report)

                if ctype.lower() in CLASSIFICATION:
                    event.add('classification.type',
                              CLASSIFICATION[ctype.lower()])
                else:
                    event.add('classification.type', u"unknown")

                if len(values[6].strip()) > 0:
                    geo_coordinates = values[6].strip().split(",")
                    if len(geo_coordinates) == 2:
                        geo_latitude = geo_coordinates[0]
                        geo_longitude = geo_coordinates[1]

                event.add('source.ip', values[0].strip())
                event.add('source.geolocation.cc',
                          values[4].strip())
                event.add('source.geolocation.city',
                          values[5].strip())
                event.add('source.geolocation.latitude',
                          geo_latitude.strip())
                event.add('source.geolocation.longitude',
                          geo_longitude.strip())

                event.add("raw", row)

                self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = AlienVaultParserBot(sys.argv[1])
    bot.start()
