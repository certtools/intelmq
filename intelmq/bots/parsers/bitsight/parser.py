# -*- coding: utf-8 -*-
"""
Bitsight Alert Stream parser

_ts                                     Timestamp in Unix Time                  => time.source
env.remote_addr                         IP that accessed the sinkhole           => source.ip
env.remote_port                         Port that accessed the sinkhole         => source.port
env.server_addr                         Sinkhole IP                             => destination.ip
env.server_port                         Sinkhole port                           => destination.port
env.server_name                         Domain accessed by IP                   => destination.fqdn
env.request_method                      Method used by IP                       => extra.method
trojanfamily                            Malware name                            => malware.name
_geo_env_remote_addr.country_name       Country location of the IP              => source.geolocation.country
"""

import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import InvalidValue
from intelmq.lib.harmonization import DateTime


class BitsightParserBot(Bot):

    def process(self):
        report = self.receive_message()
        if report is None or not report.contains('raw'):
            self.acknowledge_message()
            return
        raw_report = json.loads(utils.base64_decode(report.get('raw')))
        extra = {}
        event = self.new_event(report)
        event.add("raw", report.get('raw'), sanitize=False)
        event.add('classification.type', 'malware')
        event.add('event_description.text', 'Sinkhole attempted connection')

        for key, value in raw_report.items():
            if key == "_ts":
                event.add('time.source', DateTime.from_timestamp(int(value)))     # Source is UTC
            if key == "trojanfamily":
                event.add('malware.name', value)
            if key == "env":
                if "remote_addr" in value:
                    event.add('source.ip', value["remote_addr"])
                if "remote_port" in value:
                    event.add('source.port', value["remote_port"])
                if "server_addr" in value:
                    event.add('destination.ip', value["server_addr"])
                if "server_port" in value:
                    event.add('destination.port', value["server_port"])
                if "server_name" in value:
                    try:
                        event.add('destination.fqdn', value["server_name"])
                    except InvalidValue:
                        pass
                if "request_method" in value:
                    extra['request_method'] = value["request_method"]
                if extra:
                    event.add('extra', extra)
            if key == "_geo_env_remote_addr":
                event.add('source.geolocation.country', value["country_name"])
        self.send_message(event)
        self.acknowledge_message()


BOT = BitsightParserBot
