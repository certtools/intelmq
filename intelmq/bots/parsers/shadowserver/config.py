# -*- coding: utf-8 -*-
"""
Copyright (c)2016-2018 by Bundesamt für Sicherheit in der Informationstechnik (BSI)

Software engineering by BSI & Intevation GmbH

This is a configuration File for the shadowserver parser

In the following, *intelmqkey* are arbitrary keys from intelmq's harmonization
and *shadowkey* is a column name from shadowserver's data.

Every bot-type is defined by a dictionary with three values:
- `required_fields`: A list of tuples containing intelmq's field name, field
  name from data and an optional conversion function. Errors are raised, if the
  field does not exists in data.
- `optional_fields`: Same format as above, but does not raise errors if the
  field does not exist. If there's no mapping to an intelmq field, you can set
  the intelmqkey to `extra.` and the field will be added to the extra field
  using the original field name. See section below for possible tuple-values.
- `constant_fields`: A dictionary with a static mapping of field name to data,
  e.g. to set classifications or protocols.

The tuples can be of following format:

- `('intelmqkey', 'shadowkey')`, the data from the column *shadowkey* will be
  saved in the event's field *intelmqkey*. Logically equivalent to:
  `event[`*intelmqkey*`] = row[`*shadowkey*`]`.
- `('intelmqkey', 'shadowkey', conversion_function)`, the given function will be
  used to convert and/or validate the data. Logically equivalent to:
  `event[`*intelmqkey*`] = conversion_function(row[`*shadowkey*`)]`.
- `('intelmqkey', 'shadowkey', conversion_function, True)`, the function gets
  two parameters here, the second one is the full row (as dictionary). Logically
  equivalent to:
  `event[`*intelmqkey*`] = conversion_function(row[`*shadowkey*`, row)]`.
- `('extra.', 'shadowkey', conversion_function)`, the data will be added to
  extra in this case, the resulting name is `extra.[shadowkey]`. The
  `conversion_function` is optional. Logically equivalent to:
  `event[extra.`*intelmqkey*`] = conversion_function(row[`*shadowkey*`)]`.
- `(False, 'shadowkey')`, the column will be ignored.

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
    * when setting the classification.* fields,
      please use the taxonomy from the Data Harmonization
      :ref:`data harmonization classification`
      or upstream from https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/
    * please respect the Data harmonization ontology: :doc:`/dev/data-harmonization`


TODOs:
    There is a bunch of inline todos.
    Most of them show lines of code were the mapping has to be validated

    @ Check-Implementation Tags for parser configs.
    dmth thinks it's not sufficient. Some CERT-Expertise is needed to
    check if the mappings are correct.

    feed_idx is not complete.

"""
import re

import intelmq.lib.harmonization as harmonization


def get_feed_by_feedname(given_feedname):
    for feedname, filename, function in mapping:
        if given_feedname == feedname:
            return function
    else:
        return None


def get_feed_by_filename(given_filename):
    for feedname, filename, function in mapping:
        if given_filename == filename:
            return feedname, function
    else:
        return None


def add_UTC_to_timestamp(value):
    return value + ' UTC'


def convert_bool(value):
    if value.lower() in ('y', 'yes', 'true', 'enabled', '1'):
        return True
    elif value.lower() in ('n', 'no', 'false', 'disabled', '0'):
        return False


def validate_to_none(value):
    if not len(value) or value in ('0', 'unknown'):
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


def convert_http_host_and_url(value, row):
    """
    URLs are split into hostname and path. The column names differ in reports.
    Compromised-Website: http_host, url
    Drone: cc_dns, url
    IPv6-Sinkhole-HTTP-Drone: http_host, http_url
    Microsoft-Sinkhole: http_host, url
    Sinkhole-HTTP-Drone: http_host, url
    With some reports, url/http_url holds only the path, with others the full HTTP request.
    """
    if "cc_dns" in row:
        hostname = row.get('cc_dns', '')
    elif "http_host" in row:
        hostname = row.get('http_host', '')
    else:
        hostname = ''

    if "url" in row:
        path = row.get('url', '')
    elif "http_url" in row:
        path = row.get('http_url', '')
    else:
        path = ''

    if hostname and path:
        # remove potential leading/trailing HTTP request information
        path = re.sub(r'^[^/]*', '', path)
        path = re.sub(r'\s.*$', '', path)

        application = "http"
        if "application" in row:
            if row['application'] in ['http', 'https']:
                application = row['application']

        return application + "://" + hostname + path

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

    # FIX: https://github.com/certtools/intelmq/issues/1720 # TODO: Find better fix
    if '/' in value:
        return None

    if harmonization.IPAddress.is_valid(value, sanitize=True):
        return value


def validate_network(value):
    # FIX: https://github.com/certtools/intelmq/issues/1720 # TODO: Find better fix
    if '/' not in value:
        return None

    if harmonization.IPNetwork.is_valid(value, sanitize=True):
        return value


def validate_fqdn(value):
    if value and harmonization.FQDN.is_valid(value, sanitize=True):
        return value


def convert_date(value):
    return harmonization.DateTime.sanitize(value)


# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-DB2
open_db2_discovery_service = {
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
        ('extra.', 'db2_hostname', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'size', convert_int),
        ('extra.', 'servername', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-db2-discovery-service',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/vulnerable-http-report/
# https://www.shadowserver.org/what-we-do/network-reporting/accessible-http-report/
#
# This mapping is for two feeds as they are the same, so we can use this mapping for
# both :)
#
accessible_vulnerable_http = {
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
        ('extra.', 'tag'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'content_length', invalidate_zero),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'classification.identifier': 'accessible-http',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-mDNS
open_mdns = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-mdns' in constant_fields
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
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-mdns',
        'protocol.application': 'mdns',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Chargen
open_chargen = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-chargen' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.response_size', 'size', convert_int),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-chargen',
        'protocol.application': 'chargen',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-TFTP
open_tftp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-tftp' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'size', convert_int),
        ('extra.', 'opcode', validate_to_none),
        ('extra.', 'errorcode', validate_to_none),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'errormessage', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-tftp',
        'protocol.application': 'tftp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Sinkhole-HTTP-Drone
sinkhole_http_drone = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'src_port'),
    ],
    'optional_fields': [
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('destination.url', 'url', convert_http_host_and_url, True),
        ('malware.name', 'type'),
        ('user_agent', 'http_agent'),
        ('source.tor_node', 'tor', set_tor_node),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('source.reverse_dns', 'hostname'),
        ('destination.port', 'dst_port'),
        ('destination.fqdn', 'http_host', validate_fqdn),
        ('extra.', 'http_referer', validate_to_none),
        ('extra.', 'http_referer_ip', validate_ip),
        ('extra.', 'http_referer_asn', convert_int),
        ('extra.', 'http_referer_geo', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.asn', 'dst_asn'),
        ('destination.geolocation.cc', 'dst_geo'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http_referer_naics', validate_to_none),
        ('extra.', 'http_referer_sic', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'ssl_cipher', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious code',
        'classification.type': 'infected-system',
        # classification.identifier will be set to (harmonized) malware name by modify expert
        # The feed does not include explicit information on the protocol
        # but since it is about HTTP the protocol is always set to 'tcp'.
        'protocol.transport': 'tcp',
        'protocol.application': 'http',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Sinkhole6-HTTP-Drone
ipv6_sinkhole_http_drone = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip'),
        ('source.port', 'src_port')
    ],
    'optional_fields': [
        ('source.asn', 'src_asn'),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.asn', 'dst_asn'),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.port', 'dst_port'),
        ('protocol.transport', 'protocol'),
        ('malware.name', 'tag'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'sysdesc', validate_to_none),
        ('extra.', 'sysname', validate_to_none),
        ('destination.url', 'http_url', convert_http_host_and_url, True),
        ('extra.', 'http_agent', validate_to_none),
        ('destination.fqdn', 'http_host'),
        ('extra.', 'http_referer', validate_to_none),
        ('extra.', 'http_referer_ip', validate_to_none),
        ('extra.', 'http_referer_asn', validate_to_none),
        ('extra.', 'http_referer_geo', validate_to_none),
        ('extra.', 'http_referer_region', validate_to_none),
        ('extra.', 'forwarded_by', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious code',
        'classification.type': 'infected-system',
        # classification.identifier will be set to (harmonized) malware name by modify expert
        # The feed does not include explicit information on the protocol
        # but since it is about HTTP the protocol is always set to 'tcp'.
        'protocol.transport': 'tcp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Microsoft-Sinkhole
microsoft_sinkhole = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'src_port'),
    ],
    'optional_fields': [
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('destination.url', 'url', convert_http_host_and_url, True),
        ('malware.name', 'type'),
        ('source.tor_node', 'tor', set_tor_node),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('source.reverse_dns', 'hostname'),
        ('destination.port', 'dst_port'),
        ('destination.fqdn', 'http_host', validate_fqdn),
        ('extra.', 'http_agent', validate_to_none),
        ('extra.', 'http_referer', validate_to_none),
        ('extra.', 'http_referer_ip', validate_ip),
        ('extra.', 'http_referer_asn', convert_int),
        ('extra.', 'http_referer_geo', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.asn', 'dst_asn'),
        ('destination.geolocation.cc', 'dst_geo'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http_referer_naics', invalidate_zero),
        ('extra.', 'http_referer_sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'ssl_cipher', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious code',
        'classification.type': 'infected-system',
        # classification.identifier will be set to (harmonized) malware name by modify expert
        'protocol.transport': 'tcp',
        'protocol.application': 'http',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Redis
open_redis = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-redis' in constant_fields
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'git_sha1', validate_to_none),
        ('extra.', 'git_dirty_flag', validate_to_none),
        ('extra.', 'build_id', validate_to_none),
        ('extra.', 'mode', validate_to_none),
        ('extra.os.name', 'os', validate_to_none),
        ('extra.', 'architecture', validate_to_none),
        ('extra.', 'multiplexing_api', validate_to_none),
        ('extra.', 'gcc_version', validate_to_none),
        ('extra.', 'process_id', validate_to_none),
        ('extra.', 'run_id', validate_to_none),
        ('extra.', 'uptime', validate_to_none),
        ('extra.', 'connected_clients', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-redis',
        'protocol.application': 'redis',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Portmapper
open_portmapper = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-portmapper' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'programs', validate_to_none),
        ('extra.', 'mountd_port', validate_to_none),
        ('extra.', 'exports', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-portmapper',
        'protocol.application': 'portmapper',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-IPMI
open_ipmi = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-ipmi' in constant_fields
        ('extra.', 'ipmi_version', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'none_auth', convert_bool),
        ('extra.', 'md2_auth', convert_bool),
        ('extra.', 'md5_auth', convert_bool),
        ('extra.', 'passkey_auth', convert_bool),
        ('extra.', 'oem_auth', convert_bool),
        ('extra.', 'defaultkg', validate_to_none),
        ('extra.', 'permessage_auth', convert_bool),
        ('extra.', 'userlevel_auth', convert_bool),
        ('extra.', 'usernames', convert_bool),
        ('extra.', 'nulluser', convert_bool),
        ('extra.', 'anon_login', convert_bool),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'deviceid', validate_to_none),
        ('extra.', 'devicerev', validate_to_none),
        ('extra.', 'firmwarerev', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'manufacturerid', validate_to_none),
        ('extra.', 'manufacturername', validate_to_none),
        ('extra.', 'productid', validate_to_none),
        ('extra.', 'productname', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-ipmi',
        'protocol.application': 'ipmi',
        'protocol.transport': 'udp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-QOTD
open_qotd = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-qotd' in constant_fields
        ('extra.', 'quote', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-qotd',
        'protocol.application': 'qotd',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-SSDP
open_ssdp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-ssdp' in constant_fields
        ('extra.', 'header', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'systime', validate_to_none),
        ('extra.', 'cache_control', validate_to_none),
        ('extra.', 'location', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'search_target', validate_to_none),
        ('extra.', 'unique_service_name', validate_to_none),
        ('extra.', 'host', validate_to_none),
        ('extra.', 'nts', validate_to_none),
        ('extra.', 'nt', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-ssdp',
        'protocol.application': 'ssdp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-SNMP
open_snmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'sysdesc', validate_to_none),
        ('extra.', 'sysname', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'version', convert_int),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-snmp',
        'protocol.application': 'snmp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-MSSQL
open_mssql = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-mssql' in constant_fields
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('source.local_hostname', 'server_name'),
        ('extra.', 'instance_name', validate_to_none),
        ('extra.', 'tcp_port', convert_int),
        ('extra.', 'named_pipe', validate_to_none),
        ('extra.', 'response_length', convert_int),
        ('extra.', 'amplification', convert_float),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-mssql',
        'protocol.application': 'mssql',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-MongoDB
open_mongodb = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-mongodb' in constant_fields
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'gitversion', validate_to_none),
        ('extra.', 'sysinfo', validate_to_none),
        ('extra.', 'opensslversion', validate_to_none),
        ('extra.', 'allocator', validate_to_none),
        ('extra.', 'javascriptengine', validate_to_none),
        ('extra.', 'bits', validate_to_none),
        ('extra.', 'maxbsonobjectsize', validate_to_none),
        ('extra.', 'ok', validate_to_none),
        ('extra.', 'visible_databases', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-mongodb',
        'protocol.application': 'mongodb',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-NetBIOS
open_netbios_nameservice = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-netbios-nameservice' in constant_fields
        ('extra.', 'mac_address', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'workgroup', validate_to_none),
        ('extra.', 'machine_name', validate_to_none),
        ('source.account', 'username'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-netbios-nameservice',
        'protocol.application': 'netbios-nameservice',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Elasticsearch
open_elasticsearch = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-elasticsearch' in constant_fields
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'ok', convert_bool),
        ('extra.', 'name', validate_to_none),
        ('extra.', 'cluster_name', validate_to_none),
        ('extra.', 'status', convert_int),
        ('extra.', 'build_hash', validate_to_none),
        ('extra.', 'build_timestamp', validate_to_none),
        ('extra.', 'build_snapshot', convert_bool),
        ('extra.', 'lucene_version', validate_to_none),
        ('extra.', 'tagline', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-elasticsearch',
        'protocol.application': 'elasticsearch',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/DNS-open-resolvers
dns_open_resolvers = {
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
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'dns-open-resolver' in constant_fields
        ('extra.', 'min_amplification', convert_float),
        ('extra.', 'dns_version', validate_to_none),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.type': 'vulnerable service',
        'classification.taxonomy': 'vulnerable',
        'classification.identifier': 'dns-open-resolver',
        'protocol.application': 'dns',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/NTP-Monitor
ntp_monitor = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'packets', convert_int),
        ('extra.', 'size', convert_int),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'ntp-monitor',
        'protocol.application': 'ntp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Freak-Scan
ssl_freak_vulnerable_servers = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'ssl-freak' in constant_fields
        ('extra.', 'handshake', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', validate_to_none),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'freak_vulnerable', convert_bool),
        ('extra.', 'freak_cipher_suite', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'http_response_type', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'http_connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server_type', validate_to_none),
        ('extra.', 'content_length', validate_to_none),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'browser_trusted', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'browser_error', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'ssl-freak',
        'protocol.application': 'https',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Scan
ssl_poodle_vulnerable_servers = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'ssl-poodle' in constant_fields
        ('extra.', 'handshake', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'ssl_poodle', convert_bool),
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
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'http_response_type', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'http_connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server_type', validate_to_none),
        ('extra.', 'content_length', validate_to_none),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'browser_trusted', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'browser_error', validate_to_none),
        ('extra.', 'tlsv13_support', validate_to_none),
        ('extra.', 'tlsv13_cipher', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'ssl-poodle',
        'protocol.application': 'https',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Memcached
open_memcached = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-memcached' in constant_fields
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'pid', convert_int),
        ('extra.', 'pointer_size', convert_int),
        ('extra.', 'uptime', convert_int),
        ('extra.', 'time', validate_to_none),
        ('extra.', 'curr_connections', convert_int),
        ('extra.', 'total_connections', convert_int),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-memcached',
        'protocol.application': 'memcached',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/drone-botnet-drone-report/
drone = {
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
        ('source.reverse_dns', 'hostname'),
        ('protocol.transport', 'type'),
        ('malware.name', 'infection'),
        ('destination.url', 'url', convert_http_host_and_url, True),
        ('user_agent', 'agent'),
        ('destination.ip', 'cc_ip', validate_ip),
        ('destination.port', 'cc_port'),
        ('destination.asn', 'cc_asn'),
        ('destination.geolocation.cc', 'cc_geo'),
        ('destination.fqdn', 'cc_dns', validate_fqdn),
        ('connection_count', 'count', convert_int),
        ('extra.', 'proxy', convert_bool),
        ('protocol.application', 'application'),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('extra.', 'machine_name', validate_to_none),
        ('extra.', 'id', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.destination.naics', 'cc_naics', invalidate_zero),
        ('extra.destination.sic', 'cc_sic', invalidate_zero),
        ('extra.destination.sector', 'cc_sector', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'ssl_cipher', validate_to_none),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious code',
        'classification.type': 'infected-system',
        # classification.identifier will be set to (harmonized) malware name by modify expert
    },
}
drone_spam = {
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
        ('source.fqdn', 'hostname'),
        ('protocol.transport', 'type'),
        (False, 'infection'),  # is just 'spam'
        ('source.url', 'url', convert_http_host_and_url, True),
        ('user_agent', 'agent'),
        ('destination.ip', 'cc_ip', validate_ip),
        ('destination.port', 'cc_port'),
        ('destination.asn', 'cc_asn'),
        ('destination.geolocation.cc', 'cc_geo'),
        ('destination.fqdn', 'cc_dns', validate_fqdn),
        ('connection_count', 'count', convert_int),
        ('extra.', 'proxy', convert_bool),
        ('protocol.application', 'application'),
        ('os.name', 'p0f_genre'),
        ('os.version', 'p0f_detail'),
        ('extra.', 'machine_name', validate_to_none),
        ('extra.', 'id', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.destination.naics', 'cc_naics', invalidate_zero),
        ('extra.destination.sic', 'cc_sic', invalidate_zero),
        ('extra.destination.sector', 'cc_sector', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'ssl_cipher', validate_to_none),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'abusive content',
        'classification.type': 'spam',
        'classification.identifier': 'spam',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-XDMCP
open_xdmcp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-xdmcp' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'opcode', validate_to_none),
        ('extra.', 'reported_hostname', validate_to_none),
        ('extra.', 'status', validate_to_none),
        ('extra.', 'size', convert_int),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-xdmcp',
        'protocol.application': 'xdmcp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Compromised-Website
compromised_website = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('malware.name', 'tag'),
        ('protocol.application', 'application'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.url', 'url', convert_http_host_and_url, True),
        ('source.fqdn', 'http_host', validate_fqdn),
        ('event_description.text', 'category'),
        ('extra.', 'system', validate_to_none),
        ('extra.', 'detected_since', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'redirect_target', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'intrusions',
        'classification.type': 'compromised',
        'classification.identifier': 'compromised-website',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-NATPMP
open_natpmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-natpmp' in constant_fields
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'opcode', validate_to_none),
        ('extra.', 'uptime', validate_to_none),
        ('extra.', 'external_ip', validate_ip),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-natpmp',
        'protocol.application': 'natpmp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Netis-Router
open_netis = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-netis' in constant_fields
        ('extra.', 'response', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-netis',
        'protocol.transport': 'udp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/NTP-Version
ntp_version = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
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
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'ntp-version',
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
        ('user_agent', 'user_agent', validate_to_none),
        ('source.fqdn', 'host', validate_fqdn),
        ('extra.', 'method', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious code',
        'classification.type': 'malware',
        'classification.identifier': 'sandbox-url',
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
        ('extra.', 'ip', validate_ip),
        ('extra.', 'src_asn', convert_int),
        ('extra.', 'src_geo', validate_to_none),
        ('extra.', 'src_region', validate_to_none),
        ('extra.', 'src_city', validate_to_none),
        ('extra.', 'sender', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
    ],
    'constant_fields': {
        'classification.taxonomy': 'abusive content',
        'classification.type': 'spam',
        'classification.identifier': 'spam-url',
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
        # ('classification.identifier', 'tag'),  # always set to 'open-ike' in constant_fields
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
        ('extra.', 'message_id', validate_to_none),
        ('extra.', 'next_payload2', convert_int),
        ('extra.', 'domain_of_interpretation', convert_int),
        ('extra.', 'protocol_id', convert_int),
        ('extra.', 'spi_size', convert_int),
        ('extra.', 'notify_message_type', convert_int),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-ike',
        'protocol.application': 'ipsec',
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
        # ('classification.identifier', 'tag'),  # always set to 'open-rdp' in constant_fields
        ('extra.', 'handshake', validate_to_none),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'rdp_protocol', validate_to_none),
        ('extra.', 'cert_length', convert_int),
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
        ('extra.', 'tlsv13_support', validate_to_none),  # always empty so far
        ('extra.', 'tlsv13_cipher', validate_to_none),  # always empty so far
        ('extra.', 'cve20190708_vulnerable', convert_bool),
        ('extra.', 'bluekeep_vulnerable', convert_bool),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-rdp',
        'protocol.transport': 'tcp',
        'protocol.application': 'rdp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-SMB
accessible_smb = {
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
        ('extra.', 'smb_implant', convert_bool),
        ('extra.', 'arch', validate_to_none),
        ('extra.', 'key', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-smb',
        'protocol.transport': 'tcp',
        'protocol.application': 'smb',
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
        # ('classification.identifier', 'tag'),  # always set to 'open-ldap' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'size', convert_int),
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
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-ldap',
        'protocol.application': 'ldap',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/blocklist-report/
blocklist = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
    ],
    'optional_fields': [
        ('source.ip', 'ip', validate_ip),
        ('source.network', 'ip', validate_network),
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
        'classification.taxonomy': 'other',
        'classification.type': 'blacklist',
        'classification.identifier': 'blacklisted-ip',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-Telnet
accessible_telnet = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-telnet' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'banner', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-telnet',
        'protocol.application': 'telnet',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-CWMP
accessible_cwmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-cwmp' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
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
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-cwmp',
        'protocol.application': 'cwmp',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-VNC
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
        ('extra.', 'product', validate_to_none),
        ('extra.', 'banner', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-vnc',
        'protocol.transport': 'tcp',
        'protocol.application': 'vnc',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-CiscoSmartInstall
accessible_cisco_smart_install = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'accessible-cisco-smart-install' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-cisco-smart-install',
        'protocol.application': 'cisco-smart-install',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Drone-BruteForce
drone_brute_force = {
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
        ('source.reverse_dns', 'hostname'),
        ('destination.ip', 'dest_ip', validate_ip),
        ('destination.port', 'dest_port'),
        ('destination.asn', 'dest_asn'),
        ('destination.geolocation.cc', 'dest_geo'),
        ('destination.fqdn', 'dest_dns'),
        ('protocol.application', 'service'),
        ('classification.identifier', 'service'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.destination.naics', 'dest_naics', invalidate_zero),
        ('extra.destination.sic', 'dest_sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.destination.sector', 'dest_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('extra.', 'start_time', validate_to_none),
        ('extra.', 'end_time', validate_to_none),
        ('extra.', 'client_version', validate_to_none),
        ('destination.account', 'username', validate_to_none),
        ('extra.', 'password', validate_to_none),
        ('extra.', 'payload_url', validate_to_none),
        ('extra.', 'payload_md5', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'intrusion attempts',
        'classification.type': 'brute-force',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-Hadoop
accessible_hadoop = {
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
        ('extra.', 'version', validate_to_none),
        ('extra.', 'server_type', validate_to_none),
        ('extra.', 'clusterid', validate_to_none),
        ('extra.', 'total_disk', invalidate_zero),
        ('extra.', 'used_disk', invalidate_zero),
        ('extra.', 'free_disk', invalidate_zero),
        ('extra.', 'livenodes', validate_to_none),
        ('extra.', 'namenodeaddress', validate_to_none),
        ('extra.', 'volumeinfo', validate_to_none),
    ],
    'constant_fields': {
        'protocol.application': 'hadoop',
        'protocol.transport': 'tcp',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-hadoop',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-ADB
accessible_adb = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'accessible-adb' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'name', validate_to_none),
        ('extra.', 'model', validate_to_none),
        ('extra.', 'device', validate_to_none),
        ('extra.', 'features', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-adb',
        'protocol.application': 'adb',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Outdated-DNSSEC-Key
# https://www.shadowserver.org/wiki/pmwiki.php/Services/Outdated-DNSSEC-Key-IPv6
outdated_dnssec_key = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
    ],
    'optional_fields': [
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'hostname'),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', convert_int),
        ('destination.geolocation.cc', 'dst_geo'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sic', 'dst_sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        # ('classification.identifier', 'tag'),  # always set to 'outdated-dnssec-key' in constant_fields
        ('extra.', 'public_source', validate_to_none),
        ('protocol.transport', 'protocol'),
    ],
    'constant_fields': {
        'protocol.application': 'dns',
        'classification.taxonomy': 'availability',
        'classification.type': 'other',  # change to "misconfiguration" when available
        'classification.identifier': 'outdated-dnssec-key',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-rsync
accessible_rsync = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'accessible-rsync' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'module', validate_to_none),
        ('extra.', 'motd', validate_to_none),
        ('extra.', 'password', convert_bool),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-rsync',
        'protocol.application': 'rsync',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-AFP
accessible_afp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'accessible-afp' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'machine_type', validate_to_none),
        ('extra.', 'afp_versions', validate_to_none),
        ('extra.', 'uams', validate_to_none),
        ('extra.', 'flags', validate_to_none),
        ('extra.', 'server_name', validate_to_none),
        ('extra.', 'signature', validate_to_none),
        ('extra.', 'directory_service', validate_to_none),
        ('extra.', 'utf8_servername', validate_to_none),
        ('extra.', 'network_address', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-afp',
        'protocol.application': 'afp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Darknet
darknet = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
    ],
    'optional_fields': [
        ('source.port', 'port'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'type', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', convert_int),
        ('destination.geolocation.cc', 'dst_geo'),
        ('extra.', 'count', convert_int),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sic', 'dst_sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'family', validate_to_none),
        ('classification.identifier', 'tag'),  # different values possible in this report
        ('extra.', 'public_source', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Amplification-DDoS-Victim
amplification_ddos_victim = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
    ],
    'optional_fields': [
        ('source.port', 'src_port'),
        ('protocol.transport', 'protocol'),
        ('destination.port', 'dst_port'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'request', validate_to_none),
        ('extra.', 'count', convert_int),
        ('extra.', 'bytes', convert_int),
        ('extra.', 'sensor_geo', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'end_time', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'availability',
        'classification.type': 'ddos',
        'classification.identifier': 'amplification-ddos-victim',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/HTTP-Scanners
http_scanners = {
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
        ('source.reverse_dns', 'hostname'),
        ('destination.ip', 'dst_ip'),
        ('destination.port', 'dst_port'),
        ('destination.asn', 'dst_asn'),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.fqdn', 'dst_dns', validate_fqdn),
        ('extra.', 'type', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('extra.', 'sensorid', validate_to_none),
        ('extra.', 'pattern', validate_to_none),
        ('extra.', 'url', validate_to_none),
        ('extra.file.md5', 'file_md5', validate_to_none),
        ('extra.file.sha256', 'file_sha256', validate_to_none),
        ('extra.', 'request_raw', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'information gathering',
        'classification.type': 'scanner',
        'classification.identifier': 'http',
        'protocol.application': 'http',
        'protocol.transport': 'tcp',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/ICS-Scanners
ics_scanners = {
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
        ('source.reverse_dns', 'hostname'),
        ('protocol.application', 'protocol'),
        ('destination.ip', 'dst_ip'),
        ('destination.port', 'dst_port'),
        ('destination.asn', 'dst_asn'),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.fqdn', 'dst_dns', validate_fqdn),
        ('extra.', 'type', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('extra.', 'sensorid', validate_to_none),
        ('extra.', 'state', validate_to_none),
        ('extra.', 'slave_id', validate_to_none),
        ('extra.', 'function_code', convert_int),
        ('extra.', 'request', validate_to_none),
        ('extra.', 'response', convert_int),
    ],
    'constant_fields': {
        'classification.taxonomy': 'information gathering',
        'classification.type': 'scanner',
        'classification.identifier': 'ics',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Ubiquiti
accessible_ubiquiti_discovery_service = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'accessible-ubiquiti-discovery-service' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.mac_address', 'mac', validate_to_none),
        ('extra.radio_name', 'radioname', validate_to_none),
        ('extra.', 'essid', validate_to_none),
        ('extra.model', 'modelshort', validate_to_none),
        ('extra.model_full', 'modelfull', validate_to_none),
        ('extra.firmwarerev', 'firmware', validate_to_none),
        ('extra.response_size', 'size', convert_int),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-ubiquiti-discovery-service',
    }
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Accessible-FTP
accessible_ftp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'accessible-ftp' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'banner', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', validate_to_none),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'auth_tls_response', validate_to_none),
        ('extra.', 'auth_ssl_response', validate_to_none)
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-ftp',
        'protocol.application': 'ftp',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-mqtt-report/
open_mqtt = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-mqtt' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'anonymous_access', convert_bool),
        ('extra.', 'raw_response', validate_to_none),
        ('extra.', 'hex_code', validate_to_none),
        ('extra.', 'code', validate_to_none)
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-mqtt',
        'protocol.application': 'mqtt',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-ipp-report/
open_ipp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'open-ipp' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'ipp_version', validate_to_none),
        ('extra.', 'cups_version', validate_to_none),
        ('extra.', 'printer_uris', validate_to_none),
        ('extra.', 'printer_name', validate_to_none),
        ('extra.', 'printer_info', validate_to_none),
        ('extra.', 'printer_more_info', validate_to_none),
        ('extra.', 'printer_make_and_model', validate_to_none),
        ('extra.', 'printer_firmware_name', validate_to_none),
        ('extra.', 'printer_firmware_string_version', validate_to_none),
        ('extra.', 'printer_firmware_version', validate_to_none),
        ('extra.', 'printer_organization', validate_to_none),
        ('extra.', 'printer_organization_unit', validate_to_none),
        ('extra.', 'printer_uuid', validate_to_none),
        ('extra.', 'printer_wifi_ssid', validate_to_none)
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'open-ipp',
        'protocol.application': 'ipp',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-coap-report/
accessible_coap = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        # ('classification.identifier', 'tag'),  # always set to 'accessible-coap' in constant_fields
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'response', validate_to_none)
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-coap',
        'protocol.application': 'coap',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-apple-remote-desktop-ard-report/
accessible_ard = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port'),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn'),
        # ('classification.identifier', 'tag'),  # always 'ard' - set in constant fields
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('protocol.transport', 'protocol'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'machine_name', validate_to_none),
        ('extra.', 'response_size', convert_int),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
        'classification.identifier': 'accessible-ard',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-radmin-report/
accessible_radmin = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.asn', 'asn', convert_int),
        # ('classification.identifier', 'tag'),  # always 'accessible-radmin' - set in constant_fields
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'hostname', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('extra.', 'naics', convert_int),
        ('extra.', 'version', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-radmin',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/caida-ip-spoofer-report/
# NOTE: The "type" field is included twice with the same values
caida = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
    ],
    'optional_fields': [
        ('source.asn', 'asn', convert_int),
        # ('classification.identifier', 'tag'),  # always 'ip-spoofer' - set in constant_fields
        ('classification.identifier', 'infection'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'hostname', validate_to_none),
        ('extra.', 'type', validate_to_none),
        ('extra.', 'naics', convert_int),
        ('extra.', 'sic', convert_int),
        ('extra.', 'sector', validate_to_none),
        # FIXME Is is mappable to some classification.* field? Not included in example data.
        ('extra.', 'family', validate_to_none),
        ('source.network', 'network', validate_to_none),
        (False, 'version', validate_to_none),  # we can ignore the IP version, it's obvious from the address
        ('extra.', 'routedspoof', validate_to_none),
        ('extra.', 'session', convert_int),
        ('extra.', 'nat', convert_bool),
        ('extra.', 'public_source', validate_to_none),
    ],
    'constant_fields': {
        # FIXME Check if the classification is correct
        'classification.identifier': 'ip-spoofer',
        'classification.taxonomy': 'fraud',
        'classification.type': 'masquerade',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-ms-rdpeudp/
accessible_msrdpeudp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int)
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.asn', 'asn', convert_int),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag'),
        ('extra.', 'naics', convert_int),
        ('extra.', 'sic', convert_int),
        ('extra.', 'sessionid'),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-msrdpeudp',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable service',
    }
}

# https://www.shadowserver.org/what-we-do/network-reporting/sinkhole-dns-report/
sinkhole_dns = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int)
    ],
    'optional_fields': [
        ('source.reverse_dns', 'host'),
        ('source.asn', 'asn', convert_int),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('extra.dns_query_type', 'type'),
        ('extra.dns_query', 'query'),
        ('extra.', 'count', convert_int),
        ('extra.', 'response'),
        ('extra.', 'tag'),
        ('extra.', 'sector'),
        ('extra.', 'naics', convert_int),
    ],
    'constant_fields': {
        'classification.identifier': 'sinkholedns',
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'dns',
    }
}

mapping = (
    # feed name, file name, function
    ('Accessible-ADB', 'scan_adb', accessible_adb),
    ('Accessible-AFP', 'scan_afp', accessible_afp),
    ('Accessible-ARD', 'scan_ard', accessible_ard),
    ('Accessible-CoAP', 'scan_coap', accessible_coap),
    ('Accessible-CWMP', 'scan_cwmp', accessible_cwmp),
    ('Accessible-Cisco-Smart-Install', 'cisco_smart_install', accessible_cisco_smart_install),
    ('Accessible-FTP', 'scan_ftp', accessible_ftp),
    ('Accessible-HTTP', 'scan_http', accessible_vulnerable_http),
    ('Accessible-Hadoop', 'scan_hadoop', accessible_hadoop),
    ('Accessible-MS-RDPEUDP', 'scan_msrdpeudp', accessible_msrdpeudp),
    ('Accessible-Radmin', 'scan_radmin', accessible_radmin),
    ('Accessible-RDP', 'scan_rdp', accessible_rdp),
    ('Accessible-Rsync', 'scan_rsync', accessible_rsync),
    ('Accessible-SMB', 'scan_smb', accessible_smb),
    ('Accessible-Telnet', 'scan_telnet', accessible_telnet),
    ('Accessible-Ubiquiti-Discovery-Service', 'scan_ubiquiti', accessible_ubiquiti_discovery_service),
    ('Accessible-VNC', 'scan_vnc', accessible_vnc),
    ('Amplification-DDoS-Victim', 'ddos_amplification', amplification_ddos_victim),
    ('Blacklisted-IP', 'blacklist', blocklist),
    ('Blocklist', 'blocklist', blocklist),
    ('CAIDA-IP-Spoofer', 'caida_ip_spoofer', caida),
    ('Compromised-Website', 'compromised_website', compromised_website),
    ('DNS-Open-Resolvers', 'scan_dns', dns_open_resolvers),
    ('Darknet', 'darknet', darknet),
    ('Drone', 'botnet_drone', drone),
    ('Drone-Brute-Force', 'drone_brute_force', drone_brute_force),
    ('HTTP-Scanners', 'hp_http_scan', http_scanners),
    ('ICS-Scanners', 'hp_ics_scan', ics_scanners),
    ('IPv6-Sinkhole-HTTP-Drone', 'sinkhole6_http', ipv6_sinkhole_http_drone),
    ('Microsoft-Sinkhole', 'microsoft_sinkhole', microsoft_sinkhole),
    ('NTP-Monitor', 'scan_ntpmonitor', ntp_monitor),
    ('NTP-Version', 'scan_ntp', ntp_version),
    ('Open-Chargen', 'scan_chargen', open_chargen),
    ('Open-DB2-Discovery-Service', 'scan_db2', open_db2_discovery_service),
    ('Open-Elasticsearch', 'scan_elasticsearch', open_elasticsearch),
    ('Open-IPMI', 'scan_ipmi', open_ipmi),
    ('Open-IPP', 'scan_ipp', open_ipp),
    ('Open-LDAP', 'scan_ldap', open_ldap),
    ('Open-LDAP-TCP', 'scan_ldap_tcp', open_ldap),
    ('Open-MQTT', 'scan_mqtt', open_mqtt),
    ('Open-MSSQL', 'scan_mssql', open_mssql),
    ('Open-Memcached', 'scan_memcached', open_memcached),
    ('Open-MongoDB', 'scan_mongodb', open_mongodb),
    ('Open-NATPMP', 'scan_nat_pmp', open_natpmp),
    ('Open-NetBIOS-Nameservice', 'scan_netbios', open_netbios_nameservice),
    ('Open-Netis', 'netis_router', open_netis),
    ('Open-Portmapper', 'scan_portmapper', open_portmapper),
    ('Open-QOTD', 'scan_qotd', open_qotd),
    ('Open-Redis', 'scan_redis', open_redis),
    ('Open-SNMP', 'scan_snmp', open_snmp),
    ('Open-SSDP', 'scan_ssdp', open_ssdp),
    ('Open-TFTP', 'scan_tftp', open_tftp),
    ('Open-XDMCP', 'scan_xdmcp', open_xdmcp),
    ('Open-mDNS', 'scan_mdns', open_mdns),
    ('Outdated-DNSSEC-Key', 'outdated_dnssec_key', outdated_dnssec_key),
    ('Outdated-DNSSEC-Key-IPv6', 'outdated_dnssec_key_v6', outdated_dnssec_key),
    ('SSL-FREAK-Vulnerable-Servers', 'scan_ssl_freak', ssl_freak_vulnerable_servers),
    ('SSL-POODLE-Vulnerable-Servers', 'scan_ssl_poodle', ssl_poodle_vulnerable_servers),
    ('Sandbox-URL', 'cwsandbox_url', sandbox_url),
    ('Sinkhole-DNS', 'sinkhole_dns', sinkhole_dns),
    ('Sinkhole-HTTP-Drone', 'sinkhole_http_drone', sinkhole_http_drone),
    ('Spam-URL', 'spam_url', spam_url),
    ('Vulnerable-ISAKMP', 'scan_isakmp', vulnerable_isakmp),
    ('Vulnerable-HTTP', 'scan_http', accessible_vulnerable_http),
)
