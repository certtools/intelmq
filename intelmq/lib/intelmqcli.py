# -*- coding: utf-8 -*-
"""
Utilities for intelmqcli.

Static data (queries)
"""
import subprocess

__all__ = ['QUERY_INSERT_CONTACT', 'QUERY_GET_TEXT', 'CSV_FIELDS', 'QUERY_BY_ASCONTACT',
           'getTerminalHeight', 'EPILOG', 'QUERY_BY_ASNUM', 'APPNAME', 'QUERY_COUNT_ASN',
           'QUERY_SET_RTIRID', 'USAGE', 'QUERY_UPDATE_CONTACT', 'DESCRIPTION',
           'QUERY_FEED_NAMES', 'QUERY_IDENTIFIER_NAMES', 'QUERY_TAXONOMY_NAMES',
           'QUERY_TYPE_NAMES', 'QUERY_TEXT_NAMES', 'target_from_row']
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
QUERY_COUNT_ASN = """
    SELECT
        COUNT(*) as count,
        COALESCE({conttab}.contacts, '') as contacts,
        string_agg(DISTINCT cast({evtab}."source.asn" as varchar), ', ') as asn,
        string_agg(DISTINCT {evtab}."classification.type", ', ') as classification,
        string_agg(DISTINCT {evtab}."classification.taxonomy", ', ') as taxonomy,
        string_agg(DISTINCT {evtab}."feed.code", ', ') as feeds,
        COALESCE({conttab}.contacts, cast({evtab}."source.asn" as varchar))
            as grouping
    FROM {evtab}
    LEFT OUTER JOIN as_contacts ON {evtab}."source.asn" = {conttab}.asnum
    WHERE
        notify = TRUE AND (
            {evtab}.rtir_report_id IS NULL OR
            {evtab}.rtir_incident_id IS NULL OR
            {evtab}.rtir_investigation_id IS NULL
        )
        AND
        (
            {evtab}."source.geolocation.cc" LIKE '{cc}' OR
            {evtab}."source.fqdn" LIKE %s
        )
        AND {evtab}."feed.name" ILIKE %s AND
        {evtab}."time.source" IS NOT NULL AND
        {evtab}."classification.taxonomy" ILIKE %s
    GROUP BY {conttab}.contacts, grouping;
    """

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
            "feed", "event_description.text", "event_description.url", "malware.name", "comment", "additional_field_freetext", "version: 1.0"
            ]

QUERY_BY_ASCONTACT = """
SELECT
    to_char({evtab}."time.source",
            'YYYY-MM-DD"T"HH24:MI:SSOF') as "time.source",
    {evtab}.id,
    {evtab}."feed.code" as feed,
    {evtab}."source.ip",
    {evtab}."source.port",
    {evtab}."source.asn",
    {evtab}."source.network",
    {evtab}."source.geolocation.cc",
    {evtab}."source.geolocation.region",
    {evtab}."source.geolocation.city",
    {evtab}."source.account",
    {evtab}."source.fqdn",
    {evtab}."source.local_hostname",
    {evtab}."source.local_ip",
    {evtab}."source.reverse_dns",
    {evtab}."source.tor_node",
    {evtab}."source.url",
    {evtab}."classification.identifier",
    {evtab}."classification.taxonomy",
    {evtab}."classification.type",
    {evtab}."comment",
    {evtab}."destination.ip",
    {evtab}."destination.port",
    {evtab}."destination.asn",
    {evtab}."destination.network",
    {evtab}."destination.geolocation.cc",
    {evtab}."destination.geolocation.region",
    {evtab}."destination.geolocation.city",
    {evtab}."destination.account",
    {evtab}."destination.fqdn",
    {evtab}."destination.local_hostname",
    {evtab}."destination.local_ip",
    {evtab}."destination.reverse_dns",
    {evtab}."destination.tor_node",
    {evtab}."destination.url",
    {evtab}."event_description.target",
    {evtab}."event_description.text",
    {evtab}."event_description.url",
    {evtab}."event_hash",
    {evtab}."extra",
    {evtab}."feed.accuracy",
    {evtab}."malware.hash",
    {evtab}."malware.hash.md5",
    {evtab}."malware.hash.sha1",
    {evtab}."malware.name",
    {evtab}."malware.version",
    {evtab}."misp_uuid",
    {evtab}."notify",
    {evtab}."protocol.application",
    {evtab}."protocol.transport",
    {evtab}."screenshot_url",
    {evtab}."status",
    {evtab}."time.observation"
FROM {evtab}
LEFT OUTER JOIN {conttab} ON {evtab}."source.asn" = {conttab}.asnum
WHERE
    notify = TRUE AND (
        {evtab}.rtir_report_id IS NULL OR
        {evtab}.rtir_incident_id IS NULL OR
        {evtab}.rtir_investigation_id IS NULL
    ) AND
    (
        {evtab}."source.geolocation.cc" LIKE '{cc}' OR
        {evtab}."source.fqdn" LIKE %s
    ) AND
    {conttab}.contacts = %s AND
    {evtab}."feed.name" ILIKE %s AND
    {evtab}."time.source" IS NOT NULL AND
    {evtab}."classification.taxonomy" ILIKE %s;
"""

QUERY_BY_ASNUM = """
SELECT
    to_char({evtab}."time.source" at time zone 'UTC',
            'YYYY-MM-DD"T"HH24:MI:SSOF') as "time.source",
    {evtab}.id,
    {evtab}."feed.code" as feed,
    {evtab}."source.ip",
    {evtab}."source.port",
    {evtab}."source.asn",
    {evtab}."source.network",
    {evtab}."source.geolocation.cc",
    {evtab}."source.geolocation.region",
    {evtab}."source.geolocation.city",
    {evtab}."source.account",
    {evtab}."source.fqdn",
    {evtab}."source.local_hostname",
    {evtab}."source.local_ip",
    {evtab}."source.reverse_dns",
    {evtab}."source.tor_node",
    {evtab}."source.url",
    {evtab}."classification.identifier",
    {evtab}."classification.taxonomy",
    {evtab}."classification.type",
    {evtab}."comment",
    {evtab}."destination.ip",
    {evtab}."destination.port",
    {evtab}."destination.asn",
    {evtab}."destination.network",
    {evtab}."destination.geolocation.cc",
    {evtab}."destination.geolocation.region",
    {evtab}."destination.geolocation.city",
    {evtab}."destination.account",
    {evtab}."destination.fqdn",
    {evtab}."destination.local_hostname",
    {evtab}."destination.local_ip",
    {evtab}."destination.reverse_dns",
    {evtab}."destination.tor_node",
    {evtab}."destination.url",
    {evtab}."event_description.target",
    {evtab}."event_description.text",
    {evtab}."event_description.url",
    {evtab}."event_hash",
    {evtab}."extra",
    {evtab}."feed.accuracy",
    {evtab}."malware.hash",
    {evtab}."malware.hash.md5",
    {evtab}."malware.hash.sha1",
    {evtab}."malware.name",
    {evtab}."malware.version",
    {evtab}."misp_uuid",
    {evtab}."notify",
    {evtab}."protocol.application",
    {evtab}."protocol.transport",
    {evtab}."screenshot_url",
    {evtab}."status",
    {evtab}."time.observation"
FROM {evtab}
LEFT OUTER JOIN {conttab} ON {evtab}."source.asn" = {conttab}.asnum
WHERE
    notify = TRUE AND (
        {evtab}.rtir_report_id IS NULL OR
        {evtab}.rtir_incident_id IS NULL OR
        {evtab}.rtir_investigation_id IS NULL
    ) AND
    (
        {evtab}."source.geolocation.cc" LIKE '{cc}' OR
        {evtab}."source.fqdn" LIKE %s
    ) AND
    {evtab}."source.asn" = %s AND
    {evtab}."feed.name" ILIKE %s AND
    {evtab}."time.source" IS NOT NULL AND
    {evtab}."classification.taxonomy" ILIKE %s;
"""


QUERY_SET_RTIRID = """
UPDATE {evtab} SET
    rtir_{type}_id = {rtirid},
    sent_at = LOCALTIMESTAMP
WHERE
    id = ANY('{{{ids}}}'::int[]);
"""

QUERY_UPDATE_CONTACT = """
UPDATE {conttab} SET
    contacts = %s
WHERE
    asnum = ANY('{{{ids}}}'::int[]);
"""

QUERY_INSERT_CONTACT = """
INSERT INTO {conttab} (
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


def getTerminalHeight():
    return int(subprocess.check_output(['stty', 'size']).strip().split()[0])


def target_from_row(row):
    """
    Returns the first value in give row that exists from this list of keys:
    'source.ip', 'source.fqdn', 'source.url', 'source.account'
    """
    keys = ['source.ip', 'source.fqdn', 'source.url', 'source.account']
    for key in keys:
        if key in row:
            return row[key]
