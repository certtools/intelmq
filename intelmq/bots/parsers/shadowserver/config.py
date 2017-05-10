# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik

Software engineering by Intevation GmbH

This is a configuration File for the shadowserver parser

Mappings are "straight forward" each mapping is a dict
of at least three keys:

1. required fields:
   the parser will work this keys first.
2. optional fields:
   the parser will try to interpret these values.
   if it fails, the value is written to the extra field
3. constant fields:
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
    * please respect the Data harmonization ontology: https://github.com/certtools/intelmq/blob/master/docs/Data-Harmonization.md


TODOs:
    There is a bunch of inline todos.
    Most of them show lines of code were the mapping  has to be validated

    @ Check-Implementation Tags for parser configs.
    dmth thinks it's not sufficient. Some CERT-Expertise is needed to
    check if the mappings are correct.

"""
import intelmq.lib.harmonization as harmonization


def get_feed(feedname):
    # TODO should this be case insensitive?
    feed_idx = {
        "Accessible-CWMP": accessible_cwmp,
        "Accessible-RDP": accessible_rdp,
        "Accessible-Telnet": accessible_telnet,
        "Accessible-VNC": accessible_vnc,
        "Blacklisted-IP": blacklisted_ip,
        "Botnet-Drone-Hadoop": botnet_drone_hadoop,
        "Compromised-Website": compromised_website,
        "DNS-open-resolvers": dns_open_resolvers,
        "Microsoft-Sinkhole": microsoft_sinkhole,
        "NTP-Monitor": ntp_monitor,
        "NTP-Version": ntp_version,
        "Open-Chargen": open_chargen,
        "Open-Elasticsearch": open_elasticsearch,
        "Open-IPMI": open_ipmi,
        "Open-LDAP": open_ldap,
        "Open-mDNS": open_mdns,
        "Open-Memcached": open_memcached,
        "Open-MongoDB": open_mongodb,
        "Open-MSSQL": open_mssql,
        "Open-NATPMP": open_natpmp,
        "Open-NetBIOS": open_netbios,
        "Open-Netis": open_netis,
        "Open-Portmapper": open_portmapper,
        "Open-QOTD": open_qotd,
        "Open-Redis": open_redis,
        "Open-SNMP": open_snmp,
        "Open-SSDP": open_ssdp,
        "Open-TFTP": open_tftp,
        "Open-XDMCP": open_xdmcp,
        "Sandbox-URL": sandbox_url,
        "Sinkhole-HTTP-Drone": sinkhole_http_drone,
        "Spam-URL": spam_url,
        "Ssl-Freak-Scan": ssl_freak_scan,  # Only differs in a few extra fields
        "Ssl-Scan": ssl_scan,  # a.k.a POODLE
        "Vulnerable-ISAKMP": vulnerable_isakmp,
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
    if not len(value) or value in ['0', 'unknown']:
        return None
    return value


def convert_int(value):
    """ Returns an int or None for empty strings. """
    if not value:
        return None
    else:
        return int(value)


def convert_float(value):
    """ Returns an float or None for empty strings. """
    if not value:
        return None
    else:
        return float(value)


def convert_hostname_and_url(value, row):
    """
    URLs are split into hostname and path, we can also guess the protocol here.
    but only guess if the protocol is in a set of known good values.
    """
    if row['application'] in ['http', 'https', 'irc']:
        if row['hostname'] and row['url']:
            url = row['url'] if row['url'].startswith('/') else '/' + row['url']
            return row['application'] + '://' + row['hostname'] + url

        elif row['hostname'] and not row['url']:
            return row['application'] + '://' + row['hostname']

    return value


def convert_httphost_and_url(value, row):
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
    if harmonization.IPAddress.is_valid(value, sanitize=True):
        return value


def validate_fqdn(value):
    if harmonization.FQDN.is_valid(value, sanitize=True):
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
        'classification.taxonomy': 'Vulnerable',
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
        ('destination.url', 'url', convert_httphost_and_url, True),
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
        # --- moving this to extra: ('source.local_hostname', 'machine_name'),
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
        ('destination.url', 'url', convert_hostname_and_url, True),
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
        # 'feed.url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-XDMCP',
        'classification.identifier': 'openxdmcp',
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
        ('source.url', 'url', convert_hostname_and_url, True),
        ('source.fqdn', 'http_host', validate_fqdn),
        ('event_description.text', 'category'),
        ('extra.', 'system', validate_to_none),
        ('extra.', 'detected_since', validate_to_none),
        ('extra.', 'server', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'compromised',
        'classification.identifier': 'compromised-website',
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
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'opcode', validate_to_none),
        ('extra.', 'uptime', validate_to_none),
        ('extra.', 'external_ip', validate_ip),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.identifier': 'opennatpmp',
        'protocol.application': 'nat-pmp',
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
        ('extra.', 'clk_wander', convert_float),
        ('extra.', 'clock', validate_to_none),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'frequency', convert_float),
        ('extra.', 'jitter', convert_float),
        ('extra.', 'leap', convert_int),
        ('extra.', 'mintc', validate_to_none),
        ('extra.', 'noise', convert_float),
        ('extra.', 'offset', convert_float),
        ('extra.', 'peer', convert_int),
        ('extra.', 'phase', convert_float),
        ('extra.', 'poll', convert_int),
        ('extra.', 'precision', convert_int),
        ('extra.', 'processor', validate_to_none),
        ('extra.', 'refid', validate_to_none),
        ('extra.', 'reftime', validate_to_none),
        ('extra.', 'rootdelay', convert_float),
        ('extra.', 'rootdispersion', convert_float),
        ('extra.', 'stability', convert_float),
        ('extra.', 'state', convert_int),
        ('extra.', 'stratum', convert_int),
        ('extra.', 'system', validate_to_none),
        ('extra.', 'tai', convert_int),
        ('extra.', 'tc', convert_int),
        ('extra.', 'naics', convert_int),
        ('extra.', 'sic', convert_int),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.identifier': 'openntpversion',
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
        ('source.url', 'url'),
        ('extra.', 'user_agent', validate_to_none),
        ('source.fqdn', 'host', validate_fqdn),
        ('extra.', 'method', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'malware',
        'classification.identifier': 'sandboxurl',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Spam-URL
spam_url = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src'),
    ],
    'optional_fields': [
        ('source.url', 'url'),
        ('source.reverse_dns', 'host'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'subject', validate_to_none),
        ('extra.', 'ip', validate_to_none),
        ('extra.', 'src_asn', validate_to_none),
        ('extra.', 'src_geo', validate_to_none),
        ('extra.', 'src_region', validate_to_none),
        ('extra.', 'src_city', validate_to_none),
        ('extra.', 'sender', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'spam',
        'classification.identifier': 'spamurl',
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
        ('protocol.transport', 'protocol'),
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
        ('extra.', 'next_payload', convert_int),
        ('extra.', 'exchange_type', convert_int),
        ('extra.', 'flags', convert_int),
        ('extra.', 'message_id'),
        ('extra.', 'next_payload2', convert_int),
        ('extra.', 'domain_of_interpretation', convert_int),
        ('extra.', 'protocol_id', convert_int),  # no data seen here yet
        ('extra.', 'spi_size', convert_int),
        ('extra.', 'notify_message_type', convert_int),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.identifier': 'openike',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-RDP
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
        ('extra.', 'cert_length', invalidate_zero),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', invalidate_zero),
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
        'classification.identifier': 'openrdp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-LDAP
open_ldap = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # This will be 'openldap' in constant fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'size', validate_to_none),
        ('extra.', 'configuration_naming_context', validate_to_none),
        ('extra.', 'current_time', validate_to_none),
        ('extra.', 'default_naming_context', validate_to_none),
        ('source.local_hostname', 'dns_host_name'),
        ('extra.', 'domain_controller_functionality', convert_int),
        ('extra.', 'domain_functionality', convert_int),
        ('extra.', 'ds_service_name', validate_to_none),
        ('extra.', 'forest_functionality', convert_int),
        ('extra.', 'highest_committed_usn', convert_int),
        ('extra.', 'is_global_catalog_ready', convert_bool),
        ('extra.', 'is_synchronized', convert_bool),
        ('extra.', 'ldap_service_name', validate_to_none),
        ('extra.', 'naming_contexts', validate_to_none),
        ('extra.', 'root_domain_naming_context', validate_to_none),
        ('extra.', 'schema_naming_context', validate_to_none),
        ('extra.', 'server_name', validate_to_none),
        ('extra.', 'subschema_subentry', validate_to_none),
        ('extra.', 'supported_capabilities', validate_to_none),
        ('extra.', 'supported_control', validate_to_none),
        ('extra.', 'supported_ldap_policies', validate_to_none),
        ('extra.', 'supported_ldap_version', validate_to_none),
        ('extra.', 'supported_sasl_mechanisms', validate_to_none),
    ],
    'constant_fields': {
        'protocol.application': 'ldap',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'openldap',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Blacklist
blacklisted_ip = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'source', validate_to_none),
        ('extra.', 'reason', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'blacklist',
        'classification.identifier': 'blacklisted',
    }
}


accessible_telnet = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        # 'tag' will always be 'telnet', so it's inside constant fields as 'protocol.application'
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'banner', validate_to_none),
    ],
    'constant_fields': {
        'protocol.transport': 'tcp',
        'protocol.application': 'telnet',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'opentelnet',
    }
}


accessible_cwmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # 'tag' will always be 'cwmp', so it's inside constant fields as 'protocol.application'
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', invalidate_zero),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'date', validate_to_none),
    ],
    'constant_fields': {
        'protocol.application': 'cwmp',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'opencwmp',
    }
}

accessible_vnc = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'banner', validate_to_none),
        ('extra.', 'product', validate_to_none),
    ],
    'constant_fields': {
        'protocol.transport': 'tcp',
        'protocol.application': 'vnc',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessiblevnc',
    }
}
