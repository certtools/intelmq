# SPDX-FileCopyrightText: 2018 by nic.at GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Shodan Stream Parser

Copyright (C) 2018 by nic.at GmbH
"""
import json

from intelmq.lib.bot import Bot
from intelmq.lib.utils import base64_decode

MAPPING = {
    'hash': 'extra.shodan.event_hash',
    # 'ip': '__IGNORE__',  # using ip_str
    'hostnames': 'source.reverse_dns',  # TODO: multiple hostname
    'org': 'event_description.target',
    'data': 'extra.data',
    'port': 'source.port',
    'transport': 'protocol.transport',
    'isp': 'extra.isp',
    'platform': 'extra.platform',
    'product': 'extra.product',
    'device': 'extra.device',
    'devicetype': 'extra.devicetype',
    'info': 'extra.info',
    'mac': 'extra.mac',
    'version': 'extra.version',
    'vulns': 'extra.vulns',
    "ftp": {
            "features": {
                "AUTH": {
                    "parameters": "extra.ftp.auth.parameters",
                },
                "AVBL": {
                    "parameters": "extra.ftp.avbl.parameters",
                },
                "CCC": {
                    "parameters": "extra.ftp.ccc.parameters",
                },
                "COMB": {
                    "parameters": "extra.ftp.comb.parameters",
                },
                "CSID": {
                    "parameters": "extra.ftp.csid.parameters",
                },
                "DSIZ": {
                    "parameters": "extra.ftp.dsiz.parameters",
                },
                "EPRT": {
                    "parameters": "extra.ftp.eprt.parameters",
                },
                "EPSV": {
                    "parameters": "extra.ftp.epsv.parameters",
                },
                "ESTA": {
                    "parameters": "extra.ftp.esta.parameters",
                },
                "ESTP": {
                    "parameters": "extra.ftp.estp.parameters",
                },
                "HELP": {
                    "parameters": "extra.ftp.help.parameters",
                },
                "HOST": {
                    "parameters": "extra.ftp.host.parameters",
                },
                "IDLE": {
                    "parameters": "extra.ftp.idle.parameters",
                },
                "LANG": {
                    "parameters": "extra.ftp.lang.parameters",
                },
                "MFCT": {
                    "parameters": "extra.ftp.mfct.parameters",
                },
                "MFF": {
                    "parameters": "extra.ftp.mff.parameters",
                },
                "MODE": {
                    "parameters": "extra.ftp.mode.parameters",
                },
                "OPTS": {
                    "parameters": "extra.ftp.opts.parameters",
                },
                "PASV": {
                    "parameters": "extra.ftp.pasv.parameters",
                },
                "PBSZ": {
                    "parameters": "extra.ftp.pbsz.parameters",
                },
                "PRET": {
                    "parameters": "extra.ftp.pret.parameters",
                },
                "PROT": {
                    "parameters": "extra.ftp.prot.parameters",
                },
                "RANG": {
                    "parameters": "extra.ftp.rang.parameters",
                },
                "RMDA": {
                    "parameters": "extra.ftp.rmda.parameters",
                },
                "SITE": {
                    "parameters": "extra.ftp.site.parameters",
                },
                "SPSV": {
                    "parameters": "extra.ftp.spsv.parameters",
                },
                "SSCN": {
                    "parameters": "extra.ftp.sscn.parameters",
                },
                "STAT": {
                    "parameters": "extra.ftp.stat.parameters",
                },
                "STORD": {
                    "parameters": "extra.ftp.stord.parameters",
                },
                "THMB": {
                    "parameters": "extra.ftp.thmb.parameters",
                },
                "TVFS": {
                    "parameters": "extra.ftp.tvfs.parameters",
                },
                "XCRC": {
                    "parameters": "extra.ftp.xcrc.parameters",
                },
                "XMD5": {
                    "parameters": "extra.ftp.xmd5.parameters",
                },
                "XSHA1": {
                    "parameters": "extra.ftp.xsha1.parameters",
                },
                "XSHA256": {
                    "parameters": "extra.ftp.xsha256.parameters",
                },
                "XSHA512": {
                    "parameters": "extra.ftp.xsha512.parameters",
                },
                "MLST": {
                    "parameters": 'extra.ftp.features.mlst',
                },
                "UTF8": {
                    "parameters": 'extra.ftp.utf8.parameters',
                },
                "REST": {
                    "parameters": 'extra.ftp.rest.parameters',
                },
                "CLNT": {
                    "parameters": 'extra.ftp.clnt.parameters',
                },
                "MLSD": {
                    "parameters": 'extra.ftp.mlsd.parameters',
                },
                "MFMT": {
                    "parameters": 'extra.ftp.mfmt.parameters',
                },
                "MDTM": {
                    "parameters": 'extra.ftp.mdtm.parameters',
                },
                "SIZE": {
                    "parameters": 'extra.ftp.size.parameters',
                }
            },
        "anonymous": 'extra.ftp.anonymous',
        # "features_hash": '__IGNORE__',
    },
    'http': {
        # 'robots_hash': '__IGNORE__',
        # 'redirects': unknown,
        # 'securitytxt': unknown,
        'title': 'extra.http.html.title',
        # 'sitemap_hash': '__IGNORE__',
        # 'robots': '__IGNORE__',
        # 'favicon': '__IGNORE__',
        # 'host': '__IGNORE__',
        'html': 'extra.http.html.data',
        'location': 'extra.http.location',
        'components': 'extra.http.components',
        # 'securitytxt_hash': unknown,
        'server': 'extra.http.server',
        # 'sitemap': unknown,
        'host': 'extra.http.host',
        'waf': 'extra.http.waf',
    },
    "isakmp": {
        "initiator_spi": "extra.isakmp.initiator_spi",
        "responder_spi": "extra.isakmp.responder_spi",
        "msg_id": "extra.isakmp.msg_id",
        "next_payload": "extra.isakmp.next_payload",
        "exchange_type": "extra.isakmp.exchange_type",
        "length": "extra.isakmp.length",
        "version": "extra.isakmp.version",
        "flags": {
            "encryption": "extra.isakmp.encryption",
            "authentication": "extra.isakmp.authentication",
            "commit": "extra.isakmp.commit",
        },
        # "aggressive": {  # same as above
        # "initiator_spi": "extra.isakmp.initiator_spi",
        # "responder_spi": "extra.isakmp.responder_spi",  # can be zeros
        # "msg_id": "extra.isakmp.msg_id",
        # "next_payload": "extra.isakmp.next_payload",
        # "exchange_type": "extra.isakmp.exchange_type",
        # "length": "extra.isakmp.length",
        # "version": "extra.isakmp.version",
        # "flags": {
        # "encryption": "extra.isakmp.encryption",
        # "authentication": "extra.isakmp.authentication",
        # "commit": "extra.isakmp.commit",
        # },
        #              "vendor_ids": [] unknown
        # },
        #            "vendor_ids": [] unknown
    },
    'asn': 'source.asn',
    # 'html': '__IGNORE__',  # use http.html
    'location': {
        # 'country_code3': '__IGNORE__',  # using country_code
        'city': 'source.geolocation.city',
        'region_code': 'extra.region_code',
        'postal_code': 'extra.postal_code',
        'longitude': 'source.geolocation.longitude',
        'country_code': 'source.geolocation.cc',
        'latitude': 'source.geolocation.latitude',
        # 'country_name': '__IGNORE__',  # using country_code
        'area_code': 'extra.area_code',
        'dma_code': 'extra.dma_code',
    },
    'timestamp': 'time.source',
    'domains': 'source.fqdn',  # TODO: multiple domains
    'ip_str': 'source.ip',
    'os': 'extra.os_name',
    # '_shodan': '__IGNORE__',  # for now
    'opts': {
        'amqp': {
            'mechanisms': 'extra.amqp.mechanism',
            'server_properties': {
                'capabilities': {
                    'basic.nack': 'extra.amqp.capabilities.nack',
                    'consumer_cancel_notify': 'extra.amqp.capabilities.consumer_cancel_notify',
                    'exchange_exchange_bindings': 'extra.amqp.capabilities.exchange_exchange_bindings',
                    'publisher_confirms': 'extra.amqp.capabilities.publisher_confirms',
                    'copyright': 'extra.amqp.copyright',
                    'information': 'extra.amqp.information',
                    'platform': 'extra.amqp.platform',
                    'product': 'extra.amqp.product',
                    'version': 'extra.amqp.version',
                },
            },
        },
        'dhcp': {
            'broadcast': 'extra.dhcp.broadcast',
            'chaddr': 'extra.dhcp.chaddr',
            'ciaddr': 'extra.dhcp.ciaddr',
            'file': 'extra.dhcp.file',
            'giaddr': 'extra.dhcp.giaddr',
            'siaddr': 'extra.dhcp.siaddr',
            'sname': 'extra.dhcp.sname',
            'yiaddr': 'extra.dhcp.yiaddr',
        },
        'heartbleed': 'extra.heartbleed',
        'ip': 'extra.ip',
        'ldap': {
            'configurationNamingContext': 'extra.ldap.configurationnamingcontext',
            'defaultNamingContext': 'extra.ldap.defaultnamingcontext',
            'dnsHostName': 'extra.ldap.dnshostname',
            'dsServiceName': 'extra.ldap.dsservicename',
            'errorMessage': 'extra.ldap.errormessage',
            'ldapServiceName': 'extra.ldap.ldapservicename',
            'namingContexts': 'extra.ldap.namingcontexts',
            'resultCode': 'extra.ldap.resultcode',
            'rootDomainNamingContext': 'extra.ldap.rootdomainnamingcontext',
            'schemaNamingContext': 'extra.ldap.schemanamingcontext',
            'serverName': 'extra.ldap.servername',
            'subschemaSubentry': 'extra.ldap.subschemasubentry',
            'supportedCapabilities': 'extra.ldap.supportedcapabilities',
            'supportedControl': 'extra.ldap.supportedcontrol',
            'supportedExtension': 'extra.ldap.supportedextension',
            'supportedLDAPPolicies': 'extra.ldap.supportedldappolicies',
            'supportedLDAPVersion': 'extra.ldap.supportedldapversion',
            'supportedSASLMechanisms': 'extra.ldap.supportedsaslmechanisms',
        },
        'raw': 'extra.raw',
        'text': 'extra.text',
    },
    'tags': 'extra.tags',
    'telnet': {
        'do': 'extra.telnet.do',
        'dont': 'extra.telnet.dont',
        'will': 'extra.telnet.will',
        'wont': 'extra.telnet.wont',
    },
    'afp': {
        'machine_type': 'extra.afp.machine_type',
        'network_addresses': 'extra.afp.network_addresses',
        'uams': 'extra.afp.uams',
        'utf8_server_name': 'extra.afp.server_name',
    },
    'checkpoint': {
        'firewall_host': 'extra.checkpoint.firewall_host',
        'smartcenter_host': 'extra.checkpoint.smartcenter_host',
    },
    'coap': {
        'resources': 'extra.coap.resources',
    },
    'dns': {
        'recursive': 'extra.dns.recursive',
        'resolver_hostname': 'extra.dns.resolver_hostname',
        'resolver_id': 'extra.dns.resolver_id',
        'software': 'extra.dns.software',
    },
    'elastic': {
        'cluster': {
            'cluster_name': 'extra.elastic.cluster.cluster_name',
            'status': 'extra.elastic.cluster.status',
        },
    },
    'etcd': {
        'api': 'extra.etcd.api',
        'clientURLs': 'extra.etcd.clienturls',
        'name': 'extra.etcd.name',
        'peerURLs': 'extra.etcd.peerurls',
        'state': 'extra.etcd.state',
        'version': 'extra.etcd.version',
    },
    'ethernetip': {
        'device_type': 'extra.ethernetip.device_type',
        'ip': 'extra.ethernetip.ip',
        'product_name': 'extra.ethernetip.product_name',
        'revision_major': 'extra.ethernetip.revision_major',
        'revision_minor': 'extra.ethernetip.revision_minor',
        'serial': 'extra.ethernetip.serial',
        'vendor_id': 'extra.ethernetip.vendor_id',
        'version': 'extra.ethernetip.version',
    },
    'hp_ilo': {
        'ilo_firmware': 'extra.hp_ilo.ilo_firmware',
        'ilo_serial_number': 'extra.hp_ilo.ilo_serial_number',
        'ilo_type': 'extra.hp_ilo.ilo_type',
        'server_type': 'extra.hp_ilo.server_type',
    },
    'influxdb': {
        'bind_address': 'extra.influxdb.bind_address',
        'build': 'extra.influxdb.build',
        'databases': 'extra.influxdb.databases',
        'go_arch': 'extra.influxdb.go_arch',
        'go_os': 'extra.influxdb.go_os',
        'version': 'extra.influxdb.version',
    },
    'knx': {
        'device': {
            'friendly_name': 'extra.knx.device.friendly_name',
            'knx_address': 'extra.knx.device.knx_address',
            'mac': 'extra.knx.device.mac',
            'multicast_address': 'extra.knx.device.multicast_address',
            'serial': 'extra.knx.device.serial',
        },
        'supported_services': {
            'core': 'extra.knx.supported_services.core',
            'device_management': 'extra.knx.supported_services.device_management',
            'routing': 'extra.knx.supported_services.routing',
            'tunneling': 'extra.knx.supported_services.tunneling',
        },
    },
    'lantronix': {
        'gateway': 'extra.lantronix.gateway',
        'ip': 'extra.lantronix.ip',
        'mac': 'extra.lantronix.mac',
        'type': 'extra.lantronix.type',
        'version': 'extra.lantronix.version',
    },
    'mongodb': {
        'authentication': 'extra.mongodb.authentication',
        'buildInfo': {
            'buildEnvironment': {
                'target_arch': 'extra.mongodb.target_arch',
                'target_os': 'extra.mongodb.target_os',
            },
            'openssl': {
                'compiled': 'extra.mongodb.openssl.compiled',
                'running': 'extra.mongodb.openssl.running',
            },
            'debug': 'extra.mongodb.debug',
            'gitVersion': 'extra.mongodb.gitversion',
            'version': 'extra.mongodb.version',
        },
    },
    'mssql': {
        'dns_computer_name': 'extra.mssql.dns_computer_name',
        'dns_domain_name': 'extra.mssql.dns_domain_name',
        'dns_forest_name': 'extra.mssql.dns_forest_name',
        'netbios_computer_name': 'extra.mssql.netbios_computer_name',
        'netbios_domain_name': 'extra.mssql.netbios_domain_name',
        'os_version': 'extra.mssql.os_version',
        'target_realm': 'extra.mssql.target_realm',
    },
    'netbios': {
        'mac': 'extra.netbios.mac',
        'networks': 'extra.netbios.networks',
        'server_name': 'extra.netbios.server_name',
    },
    'ntp': {
        'digest': 'extra.ntp.digest',
        'host': 'extra.ntp.host',
        'processor': 'extra.ntp.processor',
        'stratum': 'extra.ntp.stratum',
        'system': 'extra.ntp.system',
        'version': 'extra.ntp.version',
    },
    'redis': {
        'keys': {
            'data': 'extra.redis.keys.data',
        },
        'replication': {
            'master_host': 'extra.redis.replication.master_host',
            'role': 'extra.redis.replication.role',
        },
        'server': {
            'os': 'extra.redis.server.os',
            'redis_mode': 'extra.redis.mode',
            'redis_version': 'extra.redis.version',
            'tcp_port': 'extra.redis.server.tcp_port',
        },
    },
    'smb': {
        'anonymous': 'extra.smb.anonymous',
        'capabilities': 'extra.smb.capabilities',
        'os': 'extra.smb.os',
        'smb_version': 'extra.smb.smb_version',
        'software': 'extra.smb.software',
    },
    'snmp': {
        'contact': 'extra.snmp.contact',
        'description': 'extra.snmp.description',
        'location': 'extra.snmp.location',
        'name': 'extra.snmp.name',
        'objectid': 'extra.snmp.objectid',
        'ordescr': 'extra.snmp.ordescr',
    },
    'ssh': {
        'cipher': 'extra.ssh.cipher',
        'fingerprint': 'extra.ssh.fingerprint',
        'mac': 'extra.ssh.mac',
        'type': 'extra.ssh.type',
    },
    'ssl': {
        'cert': {
            'expired': 'extra.ssl.cert.expired',
            'issuer': {
                'C': 'extra.ssl.cert.issuer.c',
                'O': 'extra.ssl.cert.issuer.c',
                'OU': 'extra.ssl.cert.issuer.ou',
                'CN': 'extra.ssl.cert.issuer.cn',
            },
            'pubkey': {
                'bits': 'extra.ssl.cert.pubkey.bits',
                'type': 'extra.ssl.cert.pubkey.type',
            },
            'serial': 'extra.ssl.cert.serial',
            'subject': {
                'C': 'extra.ssl.cert.subject.c',
                'O': 'extra.ssl.cert.subject.c',
                'OU': 'extra.ssl.cert.subject.ou',
                'CN': 'extra.ssl.cert.subject.cn',
            },
            'version': 'extra.ssl.cert.version',
        },
        'cipher': {
            'bits': 'extra.ssl.cipher.bits',
            'name': 'extra.ssl.cipher.name',
            'version': 'extra.ssl.cipher.version',
        },
        'dhparams': {
            'bits': 'extra.ssl.dhparams.bits',
            'fingerprint': 'extra.ssl.dhparams.fingerprint',
            'generator': 'extra.ssl.dhparams.generator',
            'prime': 'extra.ssl.dhparams.prime',
            'public_key': 'extra.ssl.dhparams.public_key',
        },
    },
    'ubiquiti': {
        'hostname': 'extra.ubiquiti.hostname',
        'ip': 'extra.ubiquiti.ip',
        'ip_alt': 'extra.ubiquiti.ip_alt',
        'mac': 'extra.ubiquiti.mac',
        'mac_alt': 'extra.ubiquiti.mac_alt',
        'product': 'extra.ubiquiti.product',
        'version': 'extra.ubiquiti.version',
    },
    'unitronics_pcom': {
        'hardware_version': 'extra.unitronics_pcom.hardware_version',
        'model': 'extra.unitronics_pcom.model',
        'os_build': 'extra.unitronics_pcom.os_build',
        'os_version': 'extra.unitronics_pcom.os_version',
        'plc_name': 'extra.unitronics_pcom.plc_name',
        'plc_unique_id': 'extra.unitronics_pcom.plc_unique_id',
        'uid_master': 'extra.unitronics_pcom.uid_master',
    },
    'upnp': {
        'device_type': 'extra.upnp.device_type',
        'friendly_name': 'extra.upnp.friendly_name',
        'manufacturer': 'extra.upnp.manufacturer',
        'model_description': 'extra.upnp.model_description',
        'model_name': 'extra.upnp.model_name',
        'model_number': 'extra.upnp.model_number',
        'serial_number': 'extra.upnp.serial_number',
        'udn': 'extra.upnp.udn',
        'upc': 'extra.upnp.upc',
    },
    'vmware': {
        'api_type': 'extra.vmware.api_type',
        'api_version': 'extra.vmware.api_version',
        'build': 'extra.vmware.build',
        'full_name': 'extra.vmware.full_name',
        'name': 'extra.vmware.name',
        'os_type': 'extra.vmware.os_type',
        'product_line_id': 'extra.vmware.product_line_id',
        'vendor': 'extra.vmware.vendor',
        'version': 'extra.vmware.version',
    },
}

MAPPING_MINIMAL = {
    'source.ip': "ip_str",
    'source.asn': "asn",
    'source.port': "port",
    'protocol.transport': "transport",
    'event_description.target': "org",
    'extra.data': 'data',
    'extra.html_title': 'title',
    'extra.tags': 'tags',
}

PROTOCOLS = {
    'ftp',
    'http',
    'isakmp',
    'afp',
    'bgp',
    'coap',
    'dns',
    'ethernetip',
    'hp_ilo',
    'iscsi',
    'knx',
    'lantronix',
    'minecraft',
    'mqtt',
    'msrpc',
    'netbios',
    'ntp',
    'redis',
    'rip',
    'rsync',
    'smb',
    'snmp',
    'ssh',
    'telnet',
    'unitronics_pcom',
    'upnp',
}


def _keys_conversion(x):
    return list(x.keys())


# in case item can be either T or List[T]
def _maybe_single_to_list(x):
    if isinstance(x, list):
        return x
    return [x]


CONVERSIONS = {
    'timestamp': lambda x: x + '+00',
    'hostnames': lambda x: x[0],
    'domains': lambda x: x[0],
    'coap.resources': _keys_conversion,
    'http.components': _keys_conversion,
    'mac': _keys_conversion,
    'opts.ldap.supportedControl': _maybe_single_to_list,
    'opts.ldap.supportedLDAPVersion': _maybe_single_to_list,
}


class ShodanParserBot(Bot):
    """Parse Shodan data collected via the Shodan API"""
    ignore_errors = True
    minimal_mode = False

    _common_keys = {  # not indicative of type
        '_id', '_shodan', 'asn', 'data', 'device', 'devicetype', 'domains', 'hash',
        'hostnames', 'html', 'ip', 'ip_str', 'isp', 'location', 'opts', 'org',
        'os', 'port', 'tags', 'timestamp', 'transport',
    }

    def apply_mapping(self, mapping, data, key_path=()):
        self.logger.debug('Applying mapping %r to data %r.', mapping, data)
        event = {}
        for key, value in data.items():
            current_key_path = key_path + (key,)
            conversion_key = '.'.join(current_key_path)
            try:
                if value and mapping[key] != '__IGNORE__':
                    if isinstance(mapping[key], dict):
                        update = self.apply_mapping(mapping[key], value, current_key_path)
                        if update:
                            event.update(update)
                    else:
                        if conversion_key in CONVERSIONS:
                            value = CONVERSIONS[conversion_key](value)
                        event[mapping[key]] = value
            except KeyError:
                if not self.ignore_errors:
                    raise
        return event

    def process(self):
        report = self.receive_message()
        raw = base64_decode(report['raw'])
        decoded = json.loads(raw)

        event = self.new_event(report)
        event['raw'] = raw
        if self.minimal_mode:
            for intelmqkey, shodankey in MAPPING_MINIMAL.items():
                try:
                    if decoded[shodankey]:
                        event[intelmqkey] = decoded[shodankey]
                except KeyError:
                    pass
            try:
                event['source.geolocation.cc'] = decoded["location"]["country_code"]
            except KeyError:
                pass
            event['time.source'] = CONVERSIONS['timestamp'](decoded["timestamp"])

            event['extra.shodan'] = decoded
            event['classification.type'] = 'other'
            event['classification.identifier'] = 'network-scan'
        else:
            event.update(self.apply_mapping(MAPPING, decoded))
            event.add('classification.type', 'other')
            event.add('classification.identifier', 'shodan-scan')

            uncommon_keys = decoded.keys() - self._common_keys
            event.add('extra.shodan.unique_keys', sorted(uncommon_keys))
            decoded_protocols = PROTOCOLS & uncommon_keys
            if decoded_protocols:
                event.add('protocol.application', decoded_protocols.pop())

            if event.get('extra.vulns', []):
                event.add('extra.verified_vulns', [k for k, v in decoded['vulns'].items() if v['verified']])

        self.send_message(event)
        self.acknowledge_message()


BOT = ShodanParserBot
