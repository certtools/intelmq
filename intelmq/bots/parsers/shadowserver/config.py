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
    Also to be found on the [ENISA page](https://www.enisa.europa.eu/topics/csirt-cert-services/community-projects/existing-taxonomies)

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
        "Ssl-Scan": ssl_scan,  # Aka Poodle
        "NTP-Monitor": ntp_monitor,
        "DNS-open-resolvers": dns_open_resolvers,  # TODO Check implementation.
        "Open-Elasticsearch": open_elasticsearch,
        "Open-Net BIOS": open_net_bios,  # TODO Check implementation.
        "Open-Mongo DB": open_mongo_db,  # TODO Check implementation.
        "Open-MSSQL": open_mssql,  # TODO Check implementation.
        "Open-SNMP": open_snmp,
        "Open-SSDP": open_ssdp,  # TODO Check implementation.
        "Open-IPMI": open_ipmi,  # TODO VERIFY THIS FEED, as dmth did not have example data
        "Open-Portmapper": open_portmapper,  # TODO Check implementation.
        "Open-Redis": open_redis,  # TODO Check implementation.
        "Microsoft-Sinkhole": microsoft_sinkhole,
        "Open-TFTP": open_tftp,  # TODO Check implementation.
        "Open-Chargen": open_chargen,
        "Open-QOTD": open_qotd,
        "Sinkhole-HTTP-Drone": sinkhole_http_drone,  # TODO Check implementation. Especially the TOR-Converter
        "Open-m DNS": open_m_dns,  # TODO Check implementation.
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
open_m_dns = {
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
        # mdns_name
        # mdns_ipv4
        # mdns_ipv6
        # workstation_name
        # workstation_ipv4
        # workstation_ipv6
        # workstation_info
        # http_name"
        # http_ipv4
        # http_ipv6
        # http_ptr
        # http_info
        # http_target
        # http_port
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'protocol.application': 'mdns',
        'classification.identifier': 'mdns',
    },
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
        ('response_size', 'size', int),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # sector
    ],
    'constant_fields': {
        'classification.identifier': 'chargen',
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
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
        ('extra.', 'size', int),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # tag
        # opcode
        # errocode
        # error
        # errormessage
    ],
    'constant_fields': {
        'classification.identifier': 'opentftp',
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
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
        ('destination.ip', 'dst_ip'),
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
        ('destination.ip', 'dst_ip'),
        ('destination.asn', 'dst_asn'),
        ('destination.geolocation.cc', 'dst_geo'),
        # Other known fields which will go into "extra"
        ('user_agent', 'http_agent'),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('destination.url', 'http_host', convert_host_and_url, True),
        ('', 'url', lambda x: None),  # remove URl here, is included in above conversion
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http_referer', validate_to_none),
        # http_referer_ip
        # http_referer_asn
        # http_referer_geo
    ],
    'constant_fields': {
        'classification.type': 'botnet drone',
        'protocol.application': 'http',
        'classification.taxonomy': 'Malicious Code',
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
        'classification.identifier': 'openredis',
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
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
        'classification.identifier': 'openportmapper',
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
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
        ('protocol.transport', 'protocol'),
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
        'classification.identifier': 'openipmi',
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'protocol.application': 'ipmi',
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
        'classification.identifier': 'qotd',
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
        ('extra.', 'version', int),
        # sysdesc
        # sysname
        # sector
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'protocol.application': 'snmp',
        'classification.identifier': 'snmp',
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
        'protocol.application': 'mssql',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-MongoDB
open_mongo_db = {
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
        'protocol.application': 'mongodb',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-NetBIOS
open_net_bios = {
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
        # Other known fields which will go into "extra"
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        # elasticsearch
        # version
        # ok
        # name
        # cluster_name
        # status
        # build_hash
        # build_timestamp
        # build_snaphost
        # lucene_version
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'Vulnerable',
        'classification.identifier': 'opendns',
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
        'protocol.application': 'ntp',
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
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),  # TODO
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        # XXX FIXME needs work!!
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
        ('connection_count', 'count', int),
        ('user_agent', 'agent'),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
    ],
    'constant_fields': {
        'classification.type': 'botnet drone',
        'classification.taxonomy': 'Malicious Code',
    },
}
