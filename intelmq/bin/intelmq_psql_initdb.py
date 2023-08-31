# SPDX-FileCopyrightText: 2015 Sebastian Wagner, 2023 CERT.at GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Generates a SQL command file with commands to create the events table.

Reads the harmonization configuration and generates an SQL command from it.
The SQL file is saved in `/tmp/initdb.sql` or a temporary name if the other one
exists.
"""
import argparse
import json
import os
import sys
import tempfile

from intelmq import HARMONIZATION_CONF_FILE

INDICES = ['classification.identifier', 'classification.taxonomy',
           'classification.type', 'feed.code', 'feed.name',
           'source.abuse_contact', 'source.asn', 'source.ip', 'source.fqdn',
           'time.observation', 'time.source']

DESCRIPTION = """
Generates a SQL command file with commands to create the events table.

Reads the harmonization configuration and generates an SQL command from it.
The SQL file is saved by default in `/tmp/initdb.sql` or a temporary name
if the other one exists.
"""


def _generate_events_schema(fields: dict, partition_key: str = None) -> list:
    sql_lines = []
    sql_lines.append("CREATE TABLE{if_not_exist} events (")
    sql_lines.append(f'    "id" BIGSERIAL{" UNIQUE PRIMARY KEY" if not partition_key else ""},')

    for field, field_type in sorted(fields.items()):
        sql_lines.append(f'    "{field}" {field_type},')

    if not partition_key:
        sql_lines[-1] = sql_lines[-1][:-1]  # remove last ','
    else:
        sql_lines.append(f'    PRIMARY KEY ("id", "{partition_key}")')
    sql_lines.append(");")

    for index in INDICES:
        sql_lines.append(f'CREATE INDEX{{if_not_exist}} "idx_events_{index}" ON events USING btree ("{index}");')
    return sql_lines


RAW_TABLE_PART = """
CREATE TABLE{if_not_exist} public.raws (
    event_id bigint,
    raw text,
    PRIMARY KEY(event_id)"""

RAW_TRIGGER = """
CREATE{or_replace} TRIGGER tr_events
    INSTEAD OF INSERT
    ON public.v_events
    FOR EACH ROW
    EXECUTE FUNCTION public.process_v_events_insert();
"""


def _generate_separated_raws_schema(fields: dict, partition_key: str) -> list:
    sorted_fields = sorted(key for key in fields.keys() if key != "raw")
    sql_lines = ['', '-- Create the table holding only the "raw" values', RAW_TABLE_PART]
    if not partition_key:
        sql_lines[-1] += ","
        sql_lines.append("    CONSTRAINT raws_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE CASCADE")
    sql_lines.append(");")

    sql_lines.extend([
        '',
        '-- Create the v_events view which joins the tables "events" and "raws"\n',
        'CREATE{or_replace} VIEW public.v_events AS',
        '    SELECT',
        '        events.id,',
    ])
    for field in sorted_fields:
        sql_lines.append(f'        events."{field}",')
    sql_lines.extend([
        '        raws."event_id",',
        '        raws."raw"',
        '    FROM (',
        '        public.events',
        '        JOIN public.raws ON ((events.id = raws.event_id)));'
    ])

    sql_lines.extend([
        '',
        '-- Establish the INSERT trigger for the events table, splitting the data into events and raws',
        '',
        'CREATE{or_replace} FUNCTION public.process_v_events_insert()',
        '    RETURNS trigger',
        '    LANGUAGE plpgsql',
        '    AS $$',
        '    DECLARE event_id integer;',
        '',
        '    BEGIN',
        '        INSERT INTO',
        '            events (',
    ])
    for field in sorted_fields:
        sql_lines.append(f'                "{field}"{"," if field != sorted_fields[-1] else ""}')
    sql_lines.extend([
        '            )',
        '        VALUES',
        '            (',
    ])
    for field in sorted_fields:
        sql_lines.append(f'                NEW."{field}"{"," if field != sorted_fields[-1] else ""}')
    sql_lines.extend([
        '            )',
        '            RETURNING id INTO event_id;',
        '        INSERT INTO',
        '            raws ("event_id", "raw")',
        '        VALUES',
        '            (event_id, NEW.raw);',
        '        RETURN NEW;',
        '    END;',
        '$$;'
    ])

    sql_lines.append(RAW_TRIGGER)

    return sql_lines


def generate(harmonization_file=HARMONIZATION_CONF_FILE, skip_events=False,
             separate_raws=False, partition_key=None, skip_or_replace=False):
    FIELDS = {}
    sql_lines = []

    try:
        print("INFO - Reading %s file" % harmonization_file)
        with open(harmonization_file) as fp:
            DATA = json.load(fp)['event']
    except OSError:
        print("ERROR - Could not find %s" % harmonization_file)
        print("ERROR - Make sure that you have intelmq installed.")
        sys.exit(2)

    for field in DATA.keys():
        value = DATA[field]

        if value['type'] in ('String', 'Base64', 'URL', 'FQDN',
                             'MalwareName', 'ClassificationType',
                             'LowercaseString', 'UppercaseString', 'Registry',
                             'TLP', 'ClassificationTaxonomy',
                             ):
            if 'length' in value:
                dbtype = 'varchar({})'.format(value['length'])
            else:
                dbtype = 'text'
        elif value['type'] in ('IPAddress', 'IPNetwork'):
            dbtype = 'inet'
        elif value['type'] == 'DateTime':
            dbtype = 'timestamp with time zone'
        elif value['type'] == 'Boolean':
            dbtype = 'boolean'
        elif value['type'] in ('Integer', 'ASN'):
            dbtype = 'integer'
        elif value['type'] in ('Float', 'Accuracy'):
            dbtype = 'real'
        elif value['type'] == 'UUID':
            dbtype = 'UUID'
        elif value['type'] in ('JSON', 'JSONDict'):
            dbtype = 'json'
        else:
            raise ValueError('Unknown type %r.' % value['type'])

        FIELDS[field] = dbtype

    if not skip_events:
        sql_lines.extend(_generate_events_schema(FIELDS, partition_key))

    if separate_raws:
        sql_lines.extend(_generate_separated_raws_schema(FIELDS, partition_key))

    existing_clause = " IF NOT EXISTS" if skip_or_replace else ""
    replace_clause = " OR REPLACE" if skip_or_replace else ""

    return "\n".join(
        line.format(if_not_exist=existing_clause, or_replace=replace_clause) for line in sql_lines
    )


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-o', '--outputfile',
                        help='Defines the Ouputfile',
                        default='/tmp/initdb.sql'
                        )
    parser.add_argument("--no-events", action="store_true", default=False,
                        help="Skip generating the events table schema")
    parser.add_argument("--separate-raws", action="store_true", default=False,
                        help="Generate v_events view to separate raw field from the rest of the data on insert")
    parser.add_argument("--partition-key", default=None,
                        help=("Add given field to the primary key of the events table. "
                              "Useful when utilizing partitioning for TimescaleDB. "
                              "If combined with --separate-raws, the v_events does not get foreign key"))
    parser.add_argument("--harmonization", default=HARMONIZATION_CONF_FILE,
                        help="Path to the harmonization file")
    parser.add_argument("--skip-or-replace", default=False, action="store_true",
                        help="Add IF NOT EXISTS or REPLACE directive to created schemas")
    args = parser.parse_args()

    OUTPUTFILE = args.outputfile
    fp = None
    try:
        if os.path.exists(OUTPUTFILE):
            print(f'INFO - File {OUTPUTFILE} exists, generating temporary file.')
            os_fp, OUTPUTFILE = tempfile.mkstemp(suffix='.initdb.sql',
                                                 text=True)
            fp = os.fdopen(os_fp, 'wt')
        else:
            fp = open(OUTPUTFILE, 'w')
        psql = generate(args.harmonization,
                        skip_events=args.no_events,
                        separate_raws=args.separate_raws,
                        partition_key=args.partition_key,
                        skip_or_replace=args.skip_or_replace,
                        )
        print("INFO - Writing %s file" % OUTPUTFILE)
        fp.write(psql)
    finally:
        if fp:
            fp.close()


if __name__ == '__main__':  # pragma: no cover
    main()
