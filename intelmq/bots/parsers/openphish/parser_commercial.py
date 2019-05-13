# -*- coding: utf-8 -*-

import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class OpenPhishCommercialParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():

            row = row.strip()
            if row == "":
                continue

            json_row = json.loads(row)
            event = self.new_event(report)

            keys_to_harmonize = {
                'ip': 'source.ip',
                'url': 'source.url',
                'asn': 'source.asn',
                'host': 'source.fqdn',
                'isotime': 'time.source',
                'asn_name': 'source.as_name',
                'country_code': 'source.geolocation.cc'
            }

            for source_key in json_row:
                if source_key in keys_to_harmonize:
                    if json_row.get(source_key, None):
                        event_key = keys_to_harmonize[source_key]
                        if source_key == 'asn':
                            event.add('source.asn', int(json_row['asn'][2:]))  # It comes as "AS11111"
                        else:
                            event.add(event_key, json_row[source_key])
                else:
                    if json_row[source_key]:
                        event['extra.%s' % source_key] = json_row[source_key]

            event.add('raw', row)
            event.add('classification.type', 'phishing')

            self.send_message(event)
        self.acknowledge_message()


BOT = OpenPhishCommercialParserBot
