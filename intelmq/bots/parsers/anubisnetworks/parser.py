# -*- coding: utf-8 -*-
"""
AnubisNetworks Cyberfeed Stream parser

TODO: Refactor with JSON mapping

There is an old format and a new one - distinguishable by the test cases
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
        event = self.new_event(report)
        event.change("feed.url", event["feed.url"].split("?key=")[0])
        event.add("raw", report.get('raw'), sanitize=False)
        event.add('classification.type', 'malware')
        event.add('event_description.text', 'Sinkhole attempted connection')

        for key, value in raw_report.items():
            if key == "_ts":
                event.add('time.source', DateTime.from_timestamp(int(value)))     # Source is UTC
            elif key == "trojanfamily":
                event.add('malware.name', value)
            elif key == "env":
                for subkey, subvalue in value.items():
                    if subkey == "remote_addr":
                        event.add('source.ip', subvalue)
                    elif subkey == "remote_port":
                        event.add('source.port', subvalue)
                    elif subkey == "server_addr":
                        event.add('destination.ip', subvalue)
                    elif subkey == "server_port":
                        event.add('destination.port', subvalue)
                    elif subkey == "server_name":
                        event.add('destination.fqdn', subvalue,
                                  raise_failure=False)
                    elif subkey in ["request_method", "cookies", "path_info", "http_referer"]:
                        event['extra.%s' % subkey] = subvalue
                    else:
                        raise ValueError("Unable to parse data field env.%r. Please report this as bug." % subkey)
            elif key == "src" or key == 'dst':
                identity = 'source' if key == 'src' else 'destination'
                for subkey, subvalue in value.items():
                    if subkey == "ip":
                        event.add('%s.ip' % identity, subvalue)
                    elif subkey == "port":
                        event.add('%s.port' % identity, subvalue)
                    else:
                        raise ValueError("Unable to parse data field env.%r. Please report this as bug." % subkey)
            elif key == "_geo_env_remote_addr":
                for k, v in MAP_geo_env_remote_addr.items():
                    if k in value:
                        event[v] = value[k]
                if "ip" in value and "netmask" in value:
                    event.add('source.network', '%s/%s' % (value["ip"], value["netmask"]))
            elif key == 'qtype':
                event['extra.dns_query_type'] = value
            elif key == 'app_proto':
                event.add('protocol.application', value, overwrite=True)
            elif key == 'malw':
                for subkey, subvalue in value.items():
                    if subkey == "severity":
                        event.add('extra.malware.severity', subvalue)
                    elif subkey == "family":
                        event.add('classification.identifier', subvalue)
                    elif subkey == "variant":
                        event.add('malware.name', subvalue)
                    elif subkey == "categories":
                        event.add('extra.malware.categories', subvalue)
                    elif subkey in ["request_method", "cookies", "path_info", "http_referer"]:
                        event['extra.%s' % subkey] = subvalue
                    else:
                        raise ValueError("Unable to parse data field malw.%r. Please report this as bug." % subkey)
            elif key == 'comm':
                for subkey, subvalue in value.items():
                    if subkey == "proto":
                        event.add('protocol.application', subvalue, overwrite=True)
                    elif subkey == "method":
                        event.add('extra.communication.type', subvalue)
                    elif subkey == "http":
                        for subsubkey, subsubvalue in subvalue.items():
                            if subsubkey == 'method':
                                event.add('extra.request_method', subsubvalue)
                            elif subsubkey == 'host':
                                if not event.add('destination.fqdn', subsubvalue, raise_failure=False):
                                    # event.add('destination.ip', subsubvalue)
                                    assert raw_report['dst']['ip'] == subsubvalue
                            elif subsubkey == 'path':
                                event.add('destination.urlpath', subsubvalue)
                            elif subsubkey == 'user_agent':
                                event.add('extra.user_agent', subsubvalue)
                            elif subsubkey == 'more_headers':
                                event.add('extra.communication.headers', subsubvalue)
                            elif subsubkey in ('cookies', 'unverified_domain', 'x_forwarded_for'):
                                event.add('extra.communication.%s' % subsubkey, subsubvalue)
                            else:
                                raise ValueError("Unable to parse data field comm.http.%r. Please report this as bug." % subsubkey)
                        try:
                            event.add('destination.url',
                                      '%s://%s%s' % (value['proto'],
                                                     subvalue['host'],
                                                     subvalue['path']))
                        except KeyError:
                            pass
                    elif subkey == 'dns':
                        for subsubkey, subsubvalue in subvalue.items():
                            if subsubkey == 'name':
                                event.add('destination.fqdn', subsubvalue)
                            elif subsubkey == 'qtype':
                                event['extra.dns_query_type'] = subsubvalue
                            else:
                                raise ValueError("Unable to parse data field comm.dns.%r. Please report this as bug." % subsubkey)
                    elif subkey == "categories":
                        event.add('extra.malware.categories', subvalue)
                    elif subkey in ["request_method", "cookies", "path_info", "http_referer"]:
                        event['extra.%s' % subkey] = subvalue
                    else:
                        raise ValueError("Unable to parse data field comm.%r. Please report this as bug." % subkey)
            elif key == 'tracking':
                for subkey, subvalue in value.items():
                    if subkey == "id":
                        event.add('extra.tracking.id', subvalue)
                    elif subkey == 'last_ip':
                        event.add('extra.tracking.last.ip', subvalue)
                    elif subkey == 'first':
                        event.add('extra.first_seen', subvalue)
                    elif subkey == 'seen':
                        event.add('extra.last_seen', subvalue)
                    elif subkey == 'changes':
                        event.add('extra.tracking.changes', subvalue)
                    elif subkey == 'checkins':
                        event.add('extra.tracking.checkins', subvalue)
                    elif subkey == 'days':
                        event.add('extra.days_seen', subvalue)
                    elif subkey == 'same_ip':
                        event.add('extra.tracking.same_ip', subvalue)
                    elif subkey == 'tr':
                        event.add('extra.tracking.tr', subvalue)
                    else:
                        raise ValueError("Unable to parse data field tracking.%r. Please report this as bug." % subkey)
            elif key == '_geo_src_ip':
                event  = self.parse_geo(event, value, 'source', raw_report, key)
            elif key == '_geo_tracking_last_ip':
                event = self.parse_geo(event, value, 'tracking.last', raw_report, key)
                if value["path"] != 'tracking.last_ip':
                    raise ValueError('_geo_tracking_last_ip.path is not \'tracking.last_ip\' (%r).'
                                     ''  % subvalue)
            elif key == '_geo_comm_http_host':
                event = self.parse_geo(event, value, 'communication.http.host', raw_report, key)
                if value["path"] != 'comm.http.host':
                    raise ValueError('_geo_tracking_last_ip.path is not \'comm.http.host\' (%r).'
                                     ''  % subvalue)
            elif key.startswith('_geo_comm_http_x_forwarded_for_'):
                event = self.parse_geo(event, value,
                                       'extra.communication.http.%s' % key[15:],
                                       raw_report, '_geo_comm_http_x_forwarded_for_')
            elif key in ["_origin", "_provider", "pattern_verified", "metadata"]:
                event['extra.%s' % key] = value
            else:
                raise ValueError("Unable to parse data field %r. Please report this as bug." % key)
        self.send_message(event)
        self.acknowledge_message()

    def parse_geo(self, event, value, namespace, raw_report, orig_name):
        for subkey, subvalue in value.items():
            if subkey in ("ip", 'path'):
                pass
            elif subkey == "netmask":
                event = self.event_add_fallback(event,
                                                '%s.network' % namespace,
                                                '%s/%s' % (value['ip'], subvalue))
            elif subkey == 'country_code':
                event = self.event_add_fallback(event,
                                                '%s.geolocation.cc' % namespace,
                                                subvalue)
            elif subkey == 'country_name':
                event = self.event_add_fallback(event,
                                                '%s.geolocation.country' % namespace,
                                                subvalue)
            elif subkey in ('region_code', 'postal_code', "region", "city",
                            "latitude", "longitude", "dma_code", "area_code",
                            "metro_code"):
                event = self.event_add_fallback(event, '%s.geolocation.%s' % (namespace, subkey), subvalue)
            elif subkey == 'asn':
                event = self.event_add_fallback(event, '%s.asn' % namespace, subvalue)
            elif subkey == 'asn_name':
                event = self.event_add_fallback(event, '%s.as_name' % namespace, subvalue)
            else:
                raise ValueError("Unable to parse data field '%s.%s'. "
                                 "Please report this as bug." % (orig_name, subkey))
        return event

    def event_add_fallback(self, event, key, value):
        try:
            event[key] = value
        except KeyError:
            event['extra.%s' % key] = value
        return event


BOT = AnubisNetworksParserBot
