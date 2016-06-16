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
 3) The classification type of this field and additional properties.

The first value is the IntelMQ key,
the second value is the row in the shadowserver csv.

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
        "Open-Elasticsearch": open_elasticsearch,  # TODO Check implementation.
        "Open-Net BIOS": open_net_bios,  # TODO Check implementation.
        "Open-Mongo DB": open_mongo_db,  # TODO Check implementation.
        "Open-MSSQL": open_mssql,  # TODO Check implementation.
        "Open-SNMP": open_snmp,  # TODO Check implementation.
        "Open-SSDP": open_ssdp,  # TODO Check implementation.
        "Open-IPMI": open_ipmi,  # TODO VERIFY THIS FEED, as dmth did not have example data
        "Open-Portmapper": open_portmapper,  # TODO Check implementation.
        "Open-Redis": open_redis,  # TODO Check implementation.
        "Microsoft-Sinkhole": microsoft_sinkhole,
        "Open-TFTP": open_tftp,  # TODO Check implementation.
        "Open-Chargen": open_chargen,  # TODO Check implementation.
        "Sinkhole-HTTP-Drone": sinkhole_http_drone,  # TODO Check implementation. Especially the TOR-Converter
        "Open-m DNS": open_m_dns,  # TODO Check implementation.
    }

    return feed_idx.get(feedname)


def add_UTC_to_timestamp(value):
    return value + ' UTC'


# TODO this function is a wild guess...
def set_tor_node(value):
    if value:
        return True
    else:
        return None

# Remove "invalid" IP.
def validate_ip(value):
    if value == '0.0.0.0':
        return None

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
        # Other known fields  which will go into "extra"
        # tag
        # naics
        # sic
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
    'classification_type': 'exploit',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-mDNS'
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
        # Other known fields  which will go into "extra"
        # tag
        # size
        # naics
        # sic
        # sector
    ],
    'classification_type': 'exploit',  # TODO the original parser lists vulnerable service here.
    # Not sure if this is correct
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Chargen'
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
        # Other known fields  which will go into "extra"
        # tag
        # naics
        # sic
        # opcode
        # errocode
        # error
        # errormessage
        # size
    ],
    'classification_type': 'vulnerable service',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-TFTP'
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
        ('destination.geolocation.cc', 'dst_geo')
        # Other known fields  which will go into "extra"
        # http_agent
        # p0f_genre
        # p0f_detail
        # http_host
        # http_referer
        # http_referer_ip
        # http_referer_asn
        # http_referer_geo
        # naics
        # sic
    ],
    'classification_type': 'botnet drone',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Sinkhole-HTTP-Drone'
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
        ('destination.geolocation.cc', 'dst_geo')
        # Other known fields  which will go into "extra"
        # http_agent
        # p0f_genre
        # p0f_detail
        # http_host
        # http_referer
        # http_referer_ip
        # http_referer_asn
        # http_referer_geo
        # naics
        # sic
    ],
    'classification_type': 'botnet drone',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Microsoft-Sinkhole'
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
        # Other known fields  which will go into "extra"
        # tag
        # version
        # naics
        # sic
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
    'classification_type': 'vulnerable service',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Microsoft-Sinkhole'
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
        # Other known fields  which will go into "extra"
        # tag
        # naics
        # sic
        # programs
        # mountd_port
        # exports
        # sector
    ],
    'classification_type': 'exploit',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Portmapper'
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
        # Other known fields  which will go into "extra"
        # ipmi_version
        # none_auth
        # md2_auth
        # md5_auth
        # passkey_auth
        # oem_auth
        # defaultkg
        # permessage_auth
        # userlevel_auth
        # usernames
        # nulluser
        # anon_login
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
    'classification_type': 'vulnerable service',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-IPMI'
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
        # Other known fields  which will go into "extra"
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
        # naics
        # sic
        # sector
    ],
    'classification_type': 'exploit',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-SSDP'
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
        # Other known fields  which will go into "extra"
        # sysdesc
        # sysname
        # naics
        # sic
        # sector
    ],
    'classification_type': 'exploit',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-SNMP'
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
        ('source.local_hostname', 'server_name')
        # Other known fields  which will go into "extra"
        # tag
        # version
        # naics
        # sic
        # instance_name
        # tcp_port  # TODO:  is this the source.port?
        # named_pipe
        # response_lenght
        # sector
    ],
    'classification_type': 'vulnerable service',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-MSSQL'
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
        # Other known fields  which will go into "extra"
        # tag
        # version
        # naics
        # sic
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
    'classification_type': 'vulnerable service',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-MongoDB'
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
        ('source.local_hostname', 'machine_name')
        # Other known fields  which will go into "extra"
        # tag
        # mac_address
        # workgroup
    ],
    'classification_type': 'vulnerable service',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-NetBIOS'
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
        # Other known fields  which will go into "extra"
        # min_amplification
        # dns_version
        # p0f_genre
        # p0f_detail
    ],
    'classification_type': 'exploit',  # TODO
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Elasticsearch'
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
        # elasticsearch
        # version
        # naics
        # sic
        # ok
        # name
        # cluster_name
        # status
        # build_hash
        # build_timestamp
        # build_snaphost
        # lucene_version
    ],
    'classification_type': 'exploit',  # TODO
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/DNS-open-resolvers'
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
    'classification_type': 'exploit',  # TODO
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/NTP-Monitor'
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
    'classification_type': 'vulnerable service',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Scan'
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
    'classification_type': 'vulnerable service',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Memcached'
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
        ('source.reverse_dns', 'hostname'),  # TODO
        ('source.local_hostname', 'machine_name')
    ],
    'classification_type': 'botnet drone',
    'feed_url': 'https://www.shadowserver.org/wiki/pmwiki.php/Services/Botnet-Drone-Hadoop'
}
