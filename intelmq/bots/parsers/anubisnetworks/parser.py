# -*- coding: utf-8 -*-
"""
AnubisNetworks Cyberfeed Stream parser ::

    _ts                                     => time.source
    trojanfamily                            => malware.name

    env.remote_addr                         => source.ip
    env.remote_port                         => source.port
    env.server_addr                         => destination.ip
    env.server_port                         => destination.port
    env.server_name                         => destination.fqdn
    env.request_method                      => extra.method
    env.cookies                             => extra.cookies
    env.path_info                           => extra.path_info
    env.http_referer                        => extra.http_referer

    _origin                                 => extra._origin
    _provider                               => extra._provider
    pattern_verified                        => extra.pattern_verified

    _geo_env_remote_addr.country_code       => source.geolocation.cc
    _geo_env_remote_addr.country_name       => source.geolocation.country
    _geo_env_remote_addr.region             => source.geolocation.region
    _geo_env_remote_addr.city               => source.geolocation.city
    _geo_env_remote_addr.asn                => source.geolocation.asn
    _geo_env_remote_addr.asn_name           => source.geolocation.as_name
    _geo_env_remote_addr.longitude          => source.geolocation.longitude
    _geo_env_remote_addr.longitude          => source.geolocation.longitude
    _geo_env_remote_addr.ip + netmask       => source.network

Currently ignored and probably useful::

    btrack{id(hex),checkins(int),first(timestamp),since(int),days(int),changes(int),seen(ts),last_ip(ip),sameip(int)}
           Tracking data for devices and relations to sinkholed domains
    _geo_btrack_last_ip, _geo_env_server_addr (same fields as _geo_env_remote_addr)
    _anbtr (hex)
    env.http_xff (list of ips), X-Forwarded header as injected by proxies
    dcu_ts (timestamp)
    _geo_env_remote_addr.postal_code

"""
import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime

MAP_geo_env_remote_addr = {"country_code": 'source.geolocation.cc',
                           "country_name": 'source.geolocation.country',
                           "region": 'source.geolocation.region',
                           "city": 'source.geolocation.city',
                           "asn_name": 'source.as_name',
                           "asn": 'source.asn',
                           "longitude": 'source.geolocation.longitude',
                           "latitude": 'source.geolocation.latitude',
                           }


class AnubisNetworksParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = json.loads(utils.base64_decode(report.get('raw')))
        extra = {}
        event = self.new_event(report)
        event.change("feed.url", event["feed.url"].split("?key=")[0])
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
                    event.add('destination.fqdn', value["server_name"],
                              raise_failure=False)
                for k in ["request_method", "cookies", "path_info", "http_referer"]:
                    if k in value:
                        extra[k] = value[k]
            if key == "_geo_env_remote_addr":
                for k, v in MAP_geo_env_remote_addr.items():
                    if k in value:
                        event[v] = value[k]
                if "ip" in value and "netmask" in value:
                    event.add('source.network', '%s/%s' % (value["ip"], value["netmask"]))
            if key in ["_origin", "_provider", "pattern_verified"]:
                extra[key] = value
        if extra:
            event.add('extra', extra)
        self.send_message(event)
        self.acknowledge_message()


BOT = AnubisNetworksParserBot
