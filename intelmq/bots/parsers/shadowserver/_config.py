# SPDX-FileCopyrightText: 2016-2018 by Bundesamt für Sicherheit in der Informationstechnik (BSI)
#
# SPDX-License-Identifier: AGPL-3.0-or-later
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
      :ref:`data format classification`
      or upstream from https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/
    * please respect the Data format ontology: :doc:`/dev/data-format`


TODOs:
    There is a bunch of inline todos.
    Most of them show lines of code were the mapping has to be validated

    @ Check-Implementation Tags for parser configs.
    dmth thinks it's not sufficient. Some CERT-Expertise is needed to
    check if the mappings are correct.

    feed_idx is not complete.

"""
import os
import re
import base64
import binascii
import json
import urllib.request
import tempfile
from typing import Optional, Dict, Tuple, Any

import intelmq.lib.harmonization as harmonization


class __Container:
    pass


__config = __Container()
__config.schema_file = os.path.join(os.path.dirname(__file__), 'schema.json')
__config.schema_mtime = 0.0
__config.feedname_mapping = {}
__config.filename_mapping = {}


def set_logger(logger):
    """ Sets the logger instance. """
    __config.logger = logger


def get_feed_by_feedname(given_feedname: str) -> Optional[Dict[str, Any]]:
    reload()
    return __config.feedname_mapping.get(given_feedname, None)


def get_feed_by_filename(given_filename: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    reload()
    return __config.filename_mapping.get(given_filename, None)


def add_UTC_to_timestamp(value: str) -> str:
    return value + ' UTC'


def convert_bool(value: str) -> Optional[bool]:
    value = value.lower()
    if value in {'y', 'yes', 'true', 'enabled', '1'}:
        return True
    elif value in {'n', 'no', 'false', 'disabled', '0'}:
        return False

    return None


def validate_to_none(value: str) -> Optional[str]:
    return None if (not value or value in {'0', 'unknown'}) else value


def convert_int(value: str) -> Optional[int]:
    """ Returns an int or None for empty strings. """
    return int(value) if value else None


def convert_float(value: str) -> Optional[float]:
    """ Returns an float or None for empty strings. """
    return float(value) if value else None


def convert_http_host_and_url(value: str, row: Dict[str, str]) -> str:
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

        if "application" in row and row['application'] in {'http', 'https'}:
            application = row['application']
        else:
            application = 'http'

        return application + "://" + hostname + path

    return value


def invalidate_zero(value: str) -> Optional[int]:
    """ Returns an int or None for empty strings or '0'. """
    return int(value) if value and int(value) != 0 else None


def validate_ip(value: str) -> Optional[str]:
    """Remove "invalid" IP."""
    # FIX: https://github.com/certtools/intelmq/issues/1720 # TODO: Find better fix
    if not (value == '0.0.0.0' or '/' in value) and harmonization.IPAddress.is_valid(value, sanitize=True):
        return value

    return None


def validate_network(value: str) -> Optional[str]:
    # FIX: https://github.com/certtools/intelmq/issues/1720 # TODO: Find better fix
    if '/' in value and harmonization.IPNetwork.is_valid(value, sanitize=True):
        return value

    return None


def validate_fqdn(value: str) -> Optional[str]:
    if value and harmonization.FQDN.is_valid(value, sanitize=True):
        return value

    return None


def convert_date(value: str) -> Optional[str]:
    return harmonization.DateTime.sanitize(value)


def convert_date_utc(value: str) -> Optional[str]:
    """
    Parses a datetime from the value and assumes UTC by appending the TZ to the value.
    Not the same as add_UTC_to_timestamp, as convert_date_utc also does the sanitiation
    """
    return harmonization.DateTime.sanitize(value + '+00:00')


def force_base64(value: Optional[str]) -> Optional[str]:
    """
    Takes input strings that may be either base64-encoded bytestrings or plaintext string,
    and leaves the base64-encoded values untouched while encoding the non-encoded values,
    uniformly converting the data in the field to be base64-encoded
    """
    if not value:
        return None

    try:
        base64.b64decode(value, validate=True)  # return value intentionally ignored
    except binascii.Error:
        return base64.b64encode(value.encode()).decode()
    else:
        return value


def scan_exchange_taxonomy(field):
    if field == 'exchange;webshell':
        return 'intrusions'
    return 'vulnerable'


def scan_exchange_type(field):
    if field == 'exchange;webshell':
        return 'system-compromise'
    return 'infected-system'


def scan_exchange_identifier(field):
    if field == 'exchange;webshell':
        return 'exchange-server-webshell'
    return 'vulnerable-exchange-server'


functions = {
    'add_UTC_to_timestamp': add_UTC_to_timestamp,
    'convert_bool': convert_bool,
    'validate_to_none': validate_to_none,
    'convert_int': convert_int,
    'convert_float': convert_float,
    'convert_http_host_and_url': convert_http_host_and_url,
    'invalidate_zero': invalidate_zero,
    'validate_ip': validate_ip,
    'validate_network': validate_network,
    'validate_fqdn': validate_fqdn,
    'convert_date': convert_date,
    'convert_date_utc': convert_date_utc,
    'force_base64': force_base64,
    'scan_exchange_taxonomy': scan_exchange_taxonomy,
    'scan_exchange_type': scan_exchange_type,
    'scan_exchange_identifier': scan_exchange_identifier,
}


def reload():
    """ reload the configuration if it has changed """
    mtime = 0.0

    if os.path.isfile(__config.schema_file):
        mtime = os.path.getmtime(__config.schema_file)
        if __config.schema_mtime == mtime:
            return
    else:
        __config.logger.info("The schema file does not exist.")

    if __config.schema_mtime == 0.0 and mtime == 0.0 and not os.environ.get('INTELMQ_SKIP_INTERNET'):
        __config.logger.info("Attempting to download schema.")
        update_schema()

    __config.feedname_mapping.clear()
    __config.filename_mapping.clear()
    for schema_file in [__config.schema_file, ".".join([__config.schema_file, 'test'])]:
        if os.path.isfile(schema_file):
            with open(schema_file) as fh:
                schema = json.load(fh)
            for report in schema:
                if report == "_meta":
                    __config.logger.info("Loading schema %s." % schema[report]['date_created'])
                    for msg in schema[report]['change_log']:
                        __config.logger.info(msg)
                else:
                    __config.feedname_mapping[schema[report]['feed_name']] = (schema[report]['feed_name'], schema[report])
                    __config.filename_mapping[schema[report]['file_name']] = (schema[report]['feed_name'], schema[report])
    __config.schema_mtime = mtime


def update_schema():
    """ download the latest configuration """
    if os.environ.get('INTELMQ_SKIP_INTERNET'):
        return None

    (th, tmp) = tempfile.mkstemp(dir=os.path.dirname(__file__))
    url = 'https://interchange.shadowserver.org/intelmq/v1/schema'
    try:
        urllib.request.urlretrieve(url, tmp)
    except:
        raise ValueError("Failed to download %r" % url)

    new_version = ''
    old_version = ''

    try:
        with open(tmp) as fh:
            schema = json.load(fh)
            new_version = schema['_meta']['date_created']
    except:
        # leave tempfile behind for diagnosis
        raise ValueError("Failed to validate %r" % tmp)

    if os.path.exists(__config.schema_file):
        try:
            with open(__config.schema_file) as fh:
                schema = json.load(fh)
                old_version = schema['_meta']['date_created']
            if new_version != old_version:
                os.replace(__config.schema_file, ".".join([__config.schema_file, 'bak']))
        except:
            pass

    if new_version != old_version:
        os.replace(tmp, __config.schema_file)
    else:
        os.unlink(tmp)
