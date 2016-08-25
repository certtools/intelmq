# -*- coding: utf-8 -*-
"""
Utilities for intelmqcli.

Static data (queries)
"""
import json
import os
import subprocess

import psycopg2

__all__ = ['APPNAME', 'BASE_WHERE', 'CSV_FIELDS', 'DESCRIPTION', 'EPILOG',
           'QUERY_DISTINCT_CONTACTS_BY_INCIDENT', 'QUERY_EVENTS_BY_ASCONTACT_INCIDENT',
           'QUERY_FEED_NAMES', 'QUERY_GET_TEXT', 'QUERY_IDENTIFIER_NAMES',
           'QUERY_INSERT_CONTACT', 'QUERY_OPEN_EVENTS_BY_FEEDNAME',
           'QUERY_OPEN_EVENT_IDS_BY_TAXONOMY', 'QUERY_OPEN_EVENT_REPORTS_BY_TAXONOMY',
           'QUERY_OPEN_FEEDNAMES', 'QUERY_OPEN_TAXONOMIES', 'QUERY_TAXONOMY_NAMES',
           'QUERY_TEXT_NAMES', 'QUERY_TYPE_NAMES', 'QUERY_UPDATE_CONTACT', 'USAGE',
           'connect_database', 'getTerminalHeight', 'read_config',
           ]

APPNAME = "intelmqcli"
DESCRIPTION = """
"""
EPILOG = """
Searches for all unprocessed incidents. Incidents will be filtered by country
code and the TLD of a domain according to configuration.
The search can be restricted to one source feed.

After the start, intelmqcli will immediately connect to RT with the given
credentials. The incidents will be shown grouped by the contact address if
known or the ASN otherwise.

You have 3 options here:
* Select one group by giving the id (number in first column) and show the email
and all events in detail
* Automatic sending of all incidents with 'a'
* Quit with 'q'

For the detailed view, the recipient, the subject and the mail text will be
shown, and below the technical data as csv. If the terminal is not big enough,
the data will not be shown in full. In this case, you can press 't' for the
table mode. less will be opened with the full text and data, whereas the data
will be formated as table, which is much easier to read and interpret.
The requestor (recipient of the mail) can be changed manually by pressing 'r'
and in the following prompt the address is asked. After sending, you can
optionally save the (new) address to the database linked to the ASNs.
If you are ready to submit the incidents to RT and send the mails out, press
's'.
'b' for back jumps to the incident overview and 'q' quits.
"""
USAGE = '''
    intelmqcli
    intelmqcli --dry-run
    intelmqcli --verbose
    intelmqcli --batch
    intelmqcli --quiet
    intelmqcli --compress-csv
    intelmqcli --list-feeds
    intelmqcli --list-identifiers
    intelmqcli --list-taxonomies
    intelmqcli --taxonomy='taxonomy'
    intelmqcli --list-types
    intelmqcli --list-texts
    intelmqcli --text='boilerplate name'
    intelmqcli --feed='feedname' '''

QUERY_FEED_NAMES = "SELECT DISTINCT \"feed.name\" from events"

QUERY_IDENTIFIER_NAMES = "SELECT DISTINCT \"classification.identifier\" from events"

QUERY_TAXONOMY_NAMES = "SELECT DISTINCT \"classification.taxonomy\" from events"

QUERY_TYPE_NAMES = "SELECT DISTINCT \"classification.type\" from events"

QUERY_TEXT_NAMES = "SELECT DISTINCT \"key\" from boilerplates"

""" This is the list of fields (and their respective order) which we intend to
send out.  This is based on the order and fields of shadowserver.

Shadowserver format:
    timestamp,"ip","protocol","port","hostname","packets","size","asn","geo","region","city","naics","sic","sector"
"""
CSV_FIELDS=["time.source", "source.ip", "protocol.transport", "source.port", "protocol.application",
            "source.fqdn", "source.local_hostname", "source.local_ip", "source.url",
            "source.asn", "source.geolocation.cc",
            "source.geolocation.city",
            "classification.taxonomy", "classification.type", "classification.identifier",
            "destination.ip", "destination.port", "destination.fqdn", "destination.url",
            "feed", "event_description.text", "event_description.url", "malware.name", "extra", "comment", "additional_field_freetext", "version: 1.1"
            ]

QUERY_UPDATE_CONTACT = """
UPDATE as_contacts SET
    contacts = %s
WHERE
    asnum = %s
"""

QUERY_INSERT_CONTACT = """
INSERT INTO as_contacts (
    asnum, contacts, comment, unreliable
) VALUES (
    %s, %s, %s, FALSE
)
"""

QUERY_GET_TEXT = """
SELECT
    body
FROM {texttab}
WHERE
    key = %s
"""

BASE_WHERE = """
"notify" = TRUE AND
"time.source" IS NOT NULL AND
"sent_at" IS NULL AND
"feed.name" IS NOT NULL AND
"classification.taxonomy" IS NOT NULL AND
as_contacts.contacts IS NOT NULL AND
UPPER("source.geolocation.cc") = 'AT'
"""
# PART 1: CREATE REPORTS
QUERY_OPEN_FEEDNAMES = """
SELECT
    DISTINCT "feed.name"
FROM "events"
LEFT OUTER JOIN as_contacts ON events."source.asn" = as_contacts.asnum
WHERE
    "rtir_report_id" IS NULL AND
""" + BASE_WHERE
QUERY_OPEN_EVENTS_BY_FEEDNAME = """
SELECT *
FROM "events"
LEFT OUTER JOIN as_contacts ON events."source.asn" = as_contacts.asnum
WHERE
    "feed.name" = %s AND
    "rtir_report_id" IS NULL AND
""" + BASE_WHERE
# PART 2: INCIDENTS
QUERY_OPEN_TAXONOMIES = """
SELECT
    DISTINCT "classification.taxonomy"
FROM "events"
LEFT OUTER JOIN as_contacts ON events."source.asn" = as_contacts.asnum
WHERE
    "rtir_report_id" IS NOT NULL AND
    "rtir_incident_id" IS NULL AND
""" + BASE_WHERE
QUERY_OPEN_EVENT_REPORTS_BY_TAXONOMY = """
SELECT
    DISTINCT "rtir_report_id"
FROM "events"
LEFT OUTER JOIN as_contacts ON events."source.asn" = as_contacts.asnum
WHERE
    "rtir_report_id" IS NOT NULL AND
    "rtir_incident_id" IS NULL AND
    "classification.taxonomy" = %s AND
""" + BASE_WHERE
QUERY_OPEN_EVENT_IDS_BY_TAXONOMY = """
SELECT
    "id"
FROM "events"
LEFT OUTER JOIN as_contacts ON events."source.asn" = as_contacts.asnum
WHERE
    "rtir_report_id" IS NOT NULL AND
    "rtir_incident_id" IS NULL AND
    "classification.taxonomy" = %s AND
""" + BASE_WHERE
# PART 3: INVESTIGATIONS
QUERY_DISTINCT_CONTACTS_BY_INCIDENT = """
SELECT
DISTINCT "contacts"
FROM events
LEFT OUTER JOIN as_contacts ON events."source.asn" = as_contacts.asnum
WHERE
    rtir_report_id IS NOT NULL AND
    rtir_incident_id = %s AND
    rtir_investigation_id IS NULL AND
""" + BASE_WHERE
QUERY_EVENTS_BY_ASCONTACT_INCIDENT = """
SELECT
    to_char(events."time.source",
            'YYYY-MM-DD"T"HH24:MI:SSOF') as "time.source",
    events.id,
    events."feed.code" as feed,
    events."source.ip",
    events."source.port",
    events."source.asn",
    events."source.network",
    events."source.geolocation.cc",
    events."source.geolocation.region",
    events."source.geolocation.city",
    events."source.account",
    events."source.fqdn",
    events."source.local_hostname",
    events."source.local_ip",
    events."source.reverse_dns",
    events."source.tor_node",
    events."source.url",
    events."classification.identifier",
    events."classification.taxonomy",
    events."classification.type",
    events."comment",
    events."destination.ip",
    events."destination.port",
    events."destination.asn",
    events."destination.network",
    events."destination.geolocation.cc",
    events."destination.geolocation.region",
    events."destination.geolocation.city",
    events."destination.account",
    events."destination.fqdn",
    events."destination.local_hostname",
    events."destination.local_ip",
    events."destination.reverse_dns",
    events."destination.tor_node",
    events."destination.url",
    events."event_description.target",
    events."event_description.text",
    events."event_description.url",
    events."event_hash",
    events."extra",
    events."feed.accuracy",
    events."malware.hash",
    events."malware.hash.md5",
    events."malware.hash.sha1",
    events."malware.name",
    events."malware.version",
    events."misp_uuid",
    events."notify",
    events."protocol.application",
    events."protocol.transport",
    events."rtir_report_id",
    events."screenshot_url",
    events."status",
    events."time.observation"
FROM events
LEFT OUTER JOIN as_contacts ON events."source.asn" = as_contacts.asnum
WHERE
    events.rtir_report_id IS NOT NULL AND
    events.rtir_incident_id = %s AND
    events.rtir_investigation_id IS NULL AND
    as_contacts.contacts = %s AND
""" + BASE_WHERE


def read_config():
    with open('/etc/intelmq/intelmqcli.conf') as conf_handle:
        config = json.load(conf_handle)
    home = os.path.expanduser("~")
    with open(os.path.expanduser(home + '/.intelmq/intelmqcli.conf')) as conf_handle:
        user_config = json.load(conf_handle)

    for key, value in user_config.items():
        if key in config and isinstance(value, dict):
            config[key].update(value)
        else:
            config[key] = value
    return config


def connect_database(config):
    con = psycopg2.connect(database=config['database']['database'],
                           user=config['database']['user'],
                           password=config['database']['password'],
                           host=config['database']['host'],
                           port=config['database']['port'],
                           sslmode=config['database']['sslmode'],
                           )
    con.autocommit = True
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def getTerminalHeight():
    return int(subprocess.check_output(['stty', 'size']).strip().split()[0])
