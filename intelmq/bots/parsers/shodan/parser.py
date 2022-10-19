# SPDX-FileCopyrightText: 2018 by nic.at GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Shodan Stream Parser

Copyright (C) 2018 by nic.at GmbH
"""
import json

from typing import Dict, Tuple, List, Callable, Any, Optional

from intelmq.lib.bot import ParserBot
from intelmq.lib.utils import base64_decode
import intelmq.lib.harmonization as harmonization


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
        "features": "extra.ftp.features",
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
    'rsync': {
        'modules': 'extra.rsync.modules',
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


class NoValueException(Exception):
    '''
    Raised in a conversion function in case the value cannot be used,
    e.g when trying to get the first item of an empty list
    '''
    msg: Optional[str]

    def __init__(self, msg: Optional[str] = None) -> None:
        self.msg = msg

    def __repr__(self) -> str:
        return f'NoValueException({self.msg!r})'

    __str__ = __repr__


_common_keys = {  # not indicative of type
    '_id', '_shodan', 'asn', 'data', 'device', 'devicetype', 'domains', 'hash',
    'hostnames', 'html', 'ip', 'ip_str', 'isp', 'location', 'opts', 'org',
    'os', 'port', 'tags', 'timestamp', 'transport',
}


def _keys_conversion(x: Dict[str, Any]) -> List[str]:
    '''
    extracts object keys to a list, for cases where the values they map to are empty/irrelevant
    '''
    try:
        return list(x.keys())
    except AttributeError:
        raise NoValueException(f'non-dict {x!r} passed to _keys_conversion')


# in case item can be either T or List[T]
def _maybe_single_to_list(x: Any) -> List[Any]:
    '''
    converts non-list objects to lists with a single item and leaves lists as-is,
    used to harmonize fields which avoid lists when a single value is given
    '''
    return x if isinstance(x, list) else [x]


def _dict_dict_to_obj_list(x: Dict[str, Dict[str, Any]], identifier: str = 'identifier') -> List[Dict[str, Any]]:
    '''
    convert e.g
    {'OuterKey1': {'InnerKey1': 'Value1'}, 'OuterKey2': {'InnerKey2': 'Value2'}}
    to
    [{'identifier': 'OuterKey1', 'InnerKey': 'Value1}, {'identifier': 'OuterKey2', 'InnerKey': 'Value2'}}]
    '''
    out = []
    for k, v in x.items():
        if not isinstance(v, dict):
            raise NoValueException(f'expected dict, got {v!r} in _dict_dict_to_obj_list')

        v[identifier] = k
        out.append(v)

    return out


def _get_first(variable: List[Any]) -> Any:
    '''
    get first element from list, if the list has any; raise NoValueException otherwise
    '''
    try:
        return variable[0]
    except IndexError:
        raise NoValueException(f'empty list passed to _get_first')


def _get_first_fqdn(variable: List[str]) -> str:
    '''
    get first valid FQDN from a list of strings
    '''
    valid_fqdns = (hostname for hostname in variable if harmonization.FQDN.is_valid(hostname, sanitize=True))
    first = next(valid_fqdns, None)
    if first is None:
        raise NoValueException(f'no valid FQDN in {variable!r} passed to _get_first_fqdn')

    return first


CONVERSIONS: Dict[str, Callable[[Any], Any]] = {
    'ftp.features': _dict_dict_to_obj_list,
    'timestamp': lambda x: x + '+00',
    'hostnames': _get_first_fqdn,
    'domains': _get_first_fqdn,
    'coap.resources': _keys_conversion,
    'http.components': _keys_conversion,
    'mac': _keys_conversion,
    'opts.ldap.supportedControl': _maybe_single_to_list,
    'opts.ldap.supportedLDAPVersion': _maybe_single_to_list,
    'rsync.modules': _keys_conversion,
    'ssl.cert.serial': str,
    'ssl.dhparams.generator': str,
    'vulns': _dict_dict_to_obj_list,
}


class ShodanParserBot(ParserBot):
    """Parse Shodan data collected via the Shodan API"""
    ignore_errors = True
    minimal_mode = False

    def apply_mapping(self, mapping: Dict[str, Any], data: Dict[str, Any], key_path: Tuple[str, ...] = ()) -> Dict[str, Any]:
        self.logger.debug(f'Applying mapping {mapping!r} to data {data!r}.')
        event = {}
        for key in data.keys() & mapping.keys():
            value = data[key]
            if value is None:  # or mapping[key] == '__IGNORE__':  # (all commented out)
                continue

            current_key_path = key_path + (key,)
            mapping_v = mapping[key]

            if isinstance(mapping_v, dict):
                event.update(self.apply_mapping(mapping_v, value, current_key_path))
            else:
                conversion_key = '.'.join(current_key_path)
                try:
                    if conversion_key in CONVERSIONS:
                        value = CONVERSIONS[conversion_key](value)
                    event[mapping_v] = value
                except NoValueException as e:  # conversion failed, ignore this field
                    self.logger.debug(f'Error converting data under {conversion_key}: {e} .')

        return event

    def process(self) -> None:
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

            uncommon_keys = decoded.keys() - _common_keys
            event.add('extra.shodan.unique_keys', sorted(uncommon_keys))
            decoded_protocols = PROTOCOLS & uncommon_keys
            if decoded_protocols:
                event.add('protocol.application', decoded_protocols.pop())

            vulns = event.get('extra.vulns', None)
            if vulns is not None:
                event.add('extra.verified_vulns', [vuln['identifier'] for vuln in vulns if vuln['verified']])

        self.send_message(event)
        self.acknowledge_message()


BOT = ShodanParserBot
