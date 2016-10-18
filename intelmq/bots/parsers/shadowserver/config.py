# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

This is a configuration File for the shadowserver parser

Mappings are "straight forward" each mapping is a dict
of at least three keys:
 1) required fields:
    the parser will work this keys first.
 2) optional fields:
    the parser will try to interpret these values.
    if it fails, the value is written to the extra field
 3) constant fields:
    Some information about an event may not be explicitly stated in a
    feed because it is implicit in the nature of the feed. For instance
    a feed that is exclusively about HTTP may not have a field for the
    protocol because it's always TCP.

The first value is the IntelMQ key,
the second value is the row in the shadowserver csv.


Reference material:
    * when setting the classification.* fields, please use the taxonomy from
    [eCSIRT II](https://www.trusted-introducer.org/Incident-Classification-Taxonomy.pdf)
    Also to be found on the
    [ENISA page](https://www.enisa.europa.eu/topics/csirt-cert-services/community-projects/existing-taxonomies)

    * please respect the Data harmonisation ontology: https://github.com/certtools/intelmq/blob/master/docs/Data-Harmonization.md


TODOs:
    There is a bunch of inline todos.
    Most of them show lines of code were the mapping  has to be validated

    @ Check-Implementation Tags for parser configs.
    dmth thinks it's not sufficient. Some CERT-Expertise is needed to
    check if the mappings are correct.

"""


def get_feed(feedname):
    # TODO should this be case insensitive?
    feed_idx = {
        "Botnet-Drone-Hadoop": botnet_drone_hadoop,
        "Open-Memcached": open_memcached,
        "Ssl-Scan": ssl_scan,  # a.k.a POODLE
        "Ssl-Freak-Scan": ssl_freak_scan,  # Only differs in a few extra fields
        "NTP-Monitor": ntp_monitor,
        "NTP-Version": ntp_version,
        "DNS-open-resolvers": dns_open_resolvers,  # TODO Check implementation.
        "Open-Elasticsearch": open_elasticsearch,
        "Open-NetBIOS": open_netbios,
        "Open-MongoDB": open_mongodb,
        "Open-MSSQL": open_mssql,  # TODO Check implementation.
        "Open-SNMP": open_snmp,
        "Open-SSDP": open_ssdp,  # TODO Check implementation.
        "Open-IPMI": open_ipmi,  # TODO VERIFY THIS FEED, as dmth did not have example data
        "Open-Portmapper": open_portmapper,
        "Open-Redis": open_redis,
        "Microsoft-Sinkhole": microsoft_sinkhole,
        "Open-TFTP": open_tftp,
        "Open-Chargen": open_chargen,
        "Open-QOTD": open_qotd,
        "Sinkhole-HTTP-Drone": sinkhole_http_drone,  # TODO Check implementation. Especially the TOR-Converter
        "Open-mDNS": open_mdns,  # TODO Check implementation.
        "Open-XDMCP": open_xdmcp,
        "Open-NATPMP": open_natpmp,
        "Compromised-Website": compromised_website,
        "Open-Netis": open_netis,
        "Sandbox-URL": sandbox_url,
        "Spam-URL": spam_url,
        "Open-Proxy": open_proxy,
        "Sinkhole-HTTP-Referer": sinkhole_http_referer,
        "Vulnerable-ISAKMP": vulnerable_isakmp,
        "Botnet-CCIP": botnet_ccip,
        "Accessible-RDP": accessible_rdp,
    }

    return feed_idx.get(feedname)


def add_UTC_to_timestamp(value):
    return value + ' UTC'


def convert_bool(value):
    if value.lower() in ('yes', 'true', 'enabled'):
        return True
    elif value.lower() in ('no', 'false', 'disabled'):
        return False


def validate_to_none(value):
    if value == '0' or not len(value):
        return None
    return value


def convert_int(value):
    """ Returns an int or None for empty strings. """
    if not value:
        return None
    else:
        return int(value)


def convert_host_and_url(value, row):
    """
    URLs are split into hostname and path, we can also guess the protocol here.
    """
    if row['http_host'] and row['url']:
        return 'http://' + row['http_host'] + row['url']
    return value


def invalidate_zero(value):
    """ Returns an int or None for empty strings or '0'. """
    if not value:
        return None
    elif int(value) != 0:
        return int(value)


# TODO this function is a wild guess...
def set_tor_node(value):
    if value:
        return True
    else:
        return None


def validate_ip(value):
    """Remove "invalid" IP."""
    if value == '0.0.0.0':
        return None
    return value

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-mDNS
open_mdns = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # This will be 'mdns' in constant fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'mdns_name', validate_to_none),
        ('extra.', 'mdns_ipv4', validate_to_none),
        ('extra.', 'mdns_ipv6', validate_to_none),
        ('extra.', 'services', validate_to_none),
        ('extra.', 'workstation_name', validate_to_none),
        ('extra.', 'workstation_ipv4', validate_to_none),
        ('extra.', 'workstation_ipv6', validate_to_none),
        ('extra.', 'workstation_info', validate_to_none),
        ('extra.', 'http_name', validate_to_none),
        ('extra.', 'http_ipv4', validate_to_none),
        ('extra.', 'http_ipv6', validate_to_none),
        ('extra.', 'http_ptr', validate_to_none),
        ('extra.', 'http_info', validate_to_none),
        ('extra.', 'http_target', validate_to_none),
        ('extra.', 'http_port', validate_to_none),
    ],
    'constant_fields': {
        'protocol.transport': 'udp',
        'protocol.application': 'mdns',
        'classification.type': 'vulnerable service',
        'feed.code': 'shadowserver-openmdns',
        'classification.identifier': 'openmdns',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Chargen
open_chargen = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('response_size', 'size', convert_int),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openchargen',
        'feed.code': 'shadowserver-openchargen',
        'feed.name': 'shadowserver',
        'protocol.application': 'chargen',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-TFTP
open_tftp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'size', convert_int),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # opcode
        # errocode
        # error
        # errormessage
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'opentftp',
        'feed.code': 'shadowserver-opentftp',
        'feed.name': 'shadowserver',
        'protocol.application': 'tftp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Sinkhole-HTTP-Drone
sinkhole_http_drone = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'src_port')
    ],
    'optional_fields': [
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('malware.name', 'type'),
        ('source.tor_node', 'tor', set_tor_node),
        ('source.reverse_dns', 'hostname'),
        ('destination.port', 'dst_port'),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.asn', 'dst_asn'),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.fqdn', 'http_host'),
        # Other known fields which will go into "extra"
        ('user_agent', 'http_agent'),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # http_referer
        # http_referer_ip
        # http_referer_asn
        # http_referer_geo
    ],
    'constant_fields': {
        # The feed does not include explicit information about the
        # protocol, but since it is about HTTP the protocol is always
        # tcp.
        'protocol.transport': 'tcp',
        'classification.type': 'botnet drone',
        'classification.taxonomy': 'Malicious Code',
        'classification.identifier': 'botnet',
        'feed.code': 'shadowserver-sinkhole-http-drone',
        'feed.name': 'shadowserver',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Microsoft-Sinkhole
# Format should be same as sinkhole-http-drone
microsoft_sinkhole = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'src_port')
    ],
    'optional_fields': [
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('malware.name', 'type'),
        ('source.tor_node', 'tor', set_tor_node),
        ('source.reverse_dns', 'hostname'),
        ('destination.port', 'dst_port'),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.fqdn', 'http_host'),
        ('destination.asn', 'dst_asn'),
        ('destination.geolocation.cc', 'dst_geo'),
        ('user_agent', 'http_agent'),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('destination.url', 'url', convert_host_and_url, True),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http_referer', validate_to_none),
        # http_referer_ip
        # http_referer_asn
        # http_referer_geo
    ],
    'constant_fields': {
        'classification.type': 'botnet drone',
        'protocol.transport': 'tcp',
        'protocol.application': 'http',
        'classification.taxonomy': 'Malicious Code',
        'classification.identifier': 'botnet',
        'feed.code': 'shadowserver-microsoft-sinkhole',
        'feed.name': 'shadowserver',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Redis
open_redis = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # version
        # git_sha1
        # git_dirty_flag
        # build_id
        # mode
        # os
        # architecture
        # multiplexing_api
        # gcc_version
        # process_id
        # run_id
        # uptime
        # connected_clients
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openredis',
        'feed.code': 'shadowserver-openredis',
        'feed.name': 'shadowserver',
        'protocol.application': 'redis',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Portmapper
open_portmapper = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # programs
        # mountd_port
        # exports
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openportmapper',
        'feed.code': 'shadowserver-openportmapper',
        'feed.name': 'shadowserver',
        'protocol.application': 'portmapper',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-IPMI
open_ipmi = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        # ipmi_version
        ('extra.', 'none_auth', convert_bool),
        ('extra.', 'md2_auth', convert_bool),
        ('extra.', 'md5_auth', convert_bool),
        ('extra.', 'passkey_auth', convert_bool),
        ('extra.', 'oem_auth', convert_bool),
        # defaultkg
        ('extra.', 'permessage_auth', convert_bool),
        ('extra.', 'userlevel_auth', convert_bool),
        ('extra.', 'usernames', convert_bool),
        ('extra.', 'nulluser', convert_bool),
        ('extra.', 'anon_login', convert_bool),
        # error
        # deviceid
        # devicerev
        # firmwarerev
        # version
        # manufacturerid
        # manufacturername
        # productid
        # productname
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openipmi',
        'feed.code': 'shadowserver-openipmi',
        'feed.name': 'shadowserver',
        'protocol.application': 'ipmi',
        'protocol.transport': 'udp',
    },
}


# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-QOTD
open_qotd = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # quote
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openqotd',
        'feed.code': 'shadowserver-openqotd',
        'feed.name': 'shadowserver',
        'protocol.application': 'qotd',
    },
}


# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-SSDP
open_ssdp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # header
        # systime
        # cache_control
        # location
        # server
        # search_target
        # unique_service_name
        # host
        # nts
        # nt
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openssdp',
        'feed.code': 'shadowserver-openssdp',
        'feed.name': 'shadowserver',
        'protocol.application': 'ssdp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-SNMP
open_snmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'version', convert_int),
        # sysdesc
        # sysname
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'protocol.application': 'snmp',
        'classification.identifier': 'opensnmp',
        'feed.code': 'shadowserver-opensnmp',
        'feed.name': 'shadowserver',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-MSSQL
open_mssql = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')  # TODO:  check if this is really the source.port!
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.local_hostname', 'server_name'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # version
        # instance_name
        # tcp_port  # TODO:  is this the source.port?
        # named_pipe
        # response_lenght
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openmssql',
        'feed.code': 'shadowserver-openmssql',
        'feed.name': 'shadowserver',
        'protocol.application': 'mssql',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-MongoDB
open_mongodb = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # version
        # gitversion
        # sysinfo
        # opensslversion
        # allocator
        # javascriptengine
        # bits
        # maxbsonobjectsize
        # ok
        # visible_databases
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openmongodb',
        'feed.code': 'shadowserver-openmongodb',
        'feed.name': 'shadowserver',
        'protocol.application': 'mongodb',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-NetBIOS
open_netbios = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.account', 'username'),
        ('source.local_hostname', 'machine_name'),
        # Other known fields which will go into "extra"
        # tag
        # mac_address
        # workgroup
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'opennetbios',
        'feed.code': 'shadowserver-opennetbios',
        'feed.name': 'shadowserver',
        'protocol.application': 'netbios',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Elasticsearch
open_elasticsearch = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'status', convert_int),
        ('extra.', 'build_snapshot', convert_bool),
        # version
        # ok
        # name
        # cluster_name
        # build_hash
        # build_timestamp
        # build_snapshot
        # lucene_version
        # tagline

    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openelasticsearch',
        'feed.code': 'shadowserver-openelasticsearch',
        'feed.name': 'shadowserver',
        'protocol.application': 'elasticsearch',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/DNS-open-resolvers
dns_open_resolvers = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        # Other known fields which will go into "extra"
        # min_amplification
        # dns_version
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'opendns',
        'feed.code': 'shadowserver-opendns',
        'feed.name': 'shadowserver',
        'protocol.application': 'dns',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/NTP-Monitor
ntp_monitor = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),  # TODO
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openntp',
        'feed.code': 'shadowserver-openntp',
        'feed.name': 'shadowserver',
        'protocol.application': 'ntp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Freak-Scan
ssl_freak_scan = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'SSL-FREAK',
        'feed.code': 'shadowserver-ssl-freak-scan',
        'feed.name': 'shadowserver',
        'protocol.application': 'https',
    },
}


# https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Scan
ssl_scan = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'SSL-Poodle',
        'feed.code': 'shadowserver-ssl-scan',
        'feed.name': 'shadowserver',
        'protocol.application': 'https',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Memcached
open_memcached = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),  # TODO
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'openmemcached',
        'feed.code': 'shadowserver-openmemcached',
        'feed.name': 'shadowserver',
        'protocol.application': 'memcached',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Botnet-Drone-Hadoop
botnet_drone_hadoop = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('destination.asn', 'cc_asn'),
        ('destination.geolocation.cc', 'cc_geo'),
        ('destination.ip', 'cc_ip', validate_ip),
        ('destination.port', 'cc_port'),
        ('destination.fqdn', 'cc_dns'),
        ('destination.url', 'url'),
        ('malware.name', 'infection'),
        ('protocol.application', 'application'),
        ('protocol.transport', 'type'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'hostname'),
        # Other known fields which will go into "extra"
        ('connection_count', 'count', convert_int),
        ('user_agent', 'agent'),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
    ],
    'constant_fields': {
        'classification.type': 'botnet drone',
        'classification.taxonomy': 'Malicious Code',
        'classification.identifier': 'botnet',
        'feed.code': 'shadowserver-botnet-drone-hadoop',
        'feed.name': 'shadowserver',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-XDMCP
open_xdmcp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'opcode'),
        ('extra.', 'reported_hostname'),
        ('extra.', 'status'),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'protocol.application': 'xdmcp',
        'feed.code': 'shadowserver-openxdmcp',
        'feed.name': 'shadowserver',
        'feed.url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-XDMCP',
        'classification.identifier': 'openxdmcp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-NATPMP
open_natpmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'version'),
        ('extra.', 'opcode'),
        ('extra.', 'uptime'),
        ('extra.', 'external_ip'),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'protocol.application': 'nat-pmp',
        'feed.code': 'shadowserver-opennatpmp',
        'feed.name': 'shadowserver',
        'feed.url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-NATPMP',
        'classification.identifier': 'opennatpmp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Compromised-Website
compromised_website = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('malware.name', 'tag'),
        ('protocol.application', 'application'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('event_description.url', 'url'),
        ('event_description.target', 'http_host'),
        ('event_description.text', 'category'),
        ('extra.', 'system', validate_to_none),
        ('extra.', 'detected_since', validate_to_none),
        ('extra.', 'server', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'compromised',
        'classification.identifier': 'compromised-website',
        'feed.code': 'shadowserver-compromised-website',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Netis-Router
open_netis = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('event_description.text', 'tag'),
        ('extra.', 'response', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'constant_fields': {
        'protocol.transport': 'udp',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'opennetis',
        'feed.code': 'shadowserver-opennetis',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/NTP-Version
ntp_version = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'clk_wander', validate_to_none),
        ('extra.', 'clock', validate_to_none),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'frequency', validate_to_none),
        ('extra.', 'jitter', validate_to_none),
        ('extra.', 'leap', validate_to_none),
        ('extra.', 'mintc', validate_to_none),
        ('extra.', 'noise', validate_to_none),
        ('extra.', 'offset', validate_to_none),
        ('extra.', 'peer', validate_to_none),
        ('extra.', 'phase', validate_to_none),
        ('extra.', 'poll', validate_to_none),
        ('extra.', 'precision', validate_to_none),
        ('extra.', 'processor', validate_to_none),
        ('extra.', 'refid', validate_to_none),
        ('extra.', 'reftime', validate_to_none),
        ('extra.', 'rootdelay', validate_to_none),
        ('extra.', 'rootdispersion', validate_to_none),
        ('extra.', 'stability', validate_to_none),
        ('extra.', 'state', validate_to_none),
        ('extra.', 'stratum', validate_to_none),
        ('extra.', 'system', validate_to_none),
        ('extra.', 'tai', validate_to_none),
        ('extra.', 'tc', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.identifier': 'openntpversion',
        'feed.code': 'shadowserver-openntpversion',
        'protocol.application': 'ntp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Sandbox-URL
sandbox_url = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
    ],
    'optional_fields': [
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('malware.hash.md5', 'md5hash'),
        ('event_description.url', 'url'),
        ('extra.', 'user_agent', validate_to_none),
        ('extra.', 'host', validate_to_none),
        ('extra.', 'method', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'malware',
        'feed.code': 'shadowserver-sandboxurl',
        'classification.identifier': 'sandboxurl',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Spam-URL
spam_url = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
    ],
    'optional_fields': [
        ('event_description.url', 'url'),
        ('source.reverse_dns', 'host'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'subject', validate_to_none),
        ('extra.', 'src', validate_to_none),
        ('extra.', 'src_asn', validate_to_none),
        ('extra.', 'src_geo', validate_to_none),
        ('extra.', 'src_region', validate_to_none),
        ('extra.', 'src_city', validate_to_none),
        ('extra.', 'sender', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'spam',
        'feed.code': 'shadowserver-spamurl',
        'classification.identifier': 'spamurl',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Proxy
open_proxy = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'dns'),
        #('source.reverse_dns', 'hostname'),  # ..this is an old column name
        ('protocol.application', 'type'),
        ('extra.', 'password', validate_to_none),
        ('extra.', 'os_name', validate_to_none),
        ('extra.', 'os_version', validate_to_none),
        ('event_description.text', 'via'),
    ],
    'constant_fields': {
        'classification.type': 'other',
        'feed.code': 'shadowserver-openproxy',
        'classification.identifier': 'openproxy',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Sinkhole-HTTP-Referer
sinkhole_http_referer = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        #('source.ip', 'ip'),  # ..this is an old column name
        ('source.ip', 'inet'),
    ],
    'optional_fields': [
        ('malware.name', 'type'),
        ('extra.', 'http_host', validate_to_none),
        ('extra.', 'http_referer', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
    ],
    'constant_fields': {
        'protocol.transport': 'tcp',
        'classification.type': 'compromised',
        'feed.code': 'shadowserver-sinkhole-http-referer',
        #'classification.identifier': 'compromised-website',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Vulnerable-ISAKMP
vulnerable_isakmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # This will be 'openike' in constant fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'initiator_spi', validate_to_none),
        ('extra.', 'responder_spi', validate_to_none),
        ('extra.', 'next_payload', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'exchange_type', validate_to_none),
        ('extra.', 'flags', validate_to_none),
        ('extra.', 'message_id', validate_to_none),
        ('extra.', 'next_payload2', validate_to_none),
        ('extra.', 'domain_of_interpretation', validate_to_none),
        ('extra.', 'protocol_id', validate_to_none),
        ('extra.', 'spi_size', validate_to_none),
        ('extra.', 'notify_message_type', validate_to_none),
    ],
    'constant_fields': {
        'protocol.transport': 'udp',
        'classification.type': 'vulnerable service',
        'feed.code': 'shadowserver-vulnerable-isakmp',
        'classification.identifier': 'openike',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Botnet-CCIP
# TODO: Recheck the format and field's names - in the latest/new reports they can be different
botnet_ccip = {
    'required_fields': [
        ('time.source', 'first_seen', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('extra.', 'channel', validate_to_none),
        ('source.asn', 'asn'),
        ('source.as_name', 'as_name'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.fqdn', 'domain'),
    ],
    'constant_fields': {
        'classification.type': 'c&c',
        'feed.code': 'shadowserver-botnet-ccip',
    }
}

accessible_rdp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # This will be 'openrdp' in constant fields
        ('extra.', 'handshake', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'rdp_protocol', validate_to_none),
        ('extra.', 'cert_length', validate_to_none),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', validate_to_none),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'protocol.transport': 'tcp',
        'protocol.application': 'rdp',
        'classification.type': 'vulnerable service',
        'feed.code': 'shadowserver-accessible-rdp',
        'classification.identifier': 'openrdp',
    },
}
