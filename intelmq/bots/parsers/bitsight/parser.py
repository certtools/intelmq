# -*- coding: utf-8 -*-
"""
Bitsight parser

_ts					Timestamp in ????			=> time.source
env.remote_addr				IP that accessed the sinkhole		=> source.ip
env.remote_port				Port that accessed the sinkhole		=> source.port
env.server_addr				Sinkhole IP				=> destination.ip
env.server_port				Sinkhole port				=> destination.port
env.server_name				Domain accessed by IP			=> destination.fqdn
env.request_method			Method used by IP			=> extra.method
trojanfamily				Malware name				=> malware.name
_geo_env_remote_addr.country_name 	Country location of the IP		=> source.geolocation.country

"""

import json
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class BitsightParserBot(Bot):

    def process(self):
        report = self.receive_message()
        if report is None or not report.contains('raw'):
            self.acknowledge_message()
            return
        raw_report = {}
        raw_report = json.loads(utils.base64_decode(report.get('raw')))
        for key in raw_report:
            extra = {}
            event = Event(report)
            value = raw_report[key]
            if key == "_ts":
               print('ts = ' + str(value))
               #event.add('time.source', value)
            if key == "trojanfamily":
               #print('trojanfamily = ' + value)
               event.add('malware.name', value)
            if key == "env":
               #print('source.ip = ' + value["remote_addr"])
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
                   except:
                       event.add('destination.fqdn', "")
               if "request_method" in value:
                  extra['request_method'] = value["request_method"]
               if extra:
                  event.add('extra', extra)
            if key == "_geo_env_remote_addr.country_name":
               event.add('source.geolocation.country', value)
            event.add("raw", json.dumps(raw_report, sort_keys=True))
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = BitsightParserBot(sys.argv[1])
    bot.start()



