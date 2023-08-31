# SPDX-FileCopyrightText: 2016 Sebastian Wagner, 2023 CERT.at GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:04:13 2016

@author: sebastian
"""
import json
import os
import re
import tempfile
import unittest

import pkg_resources

import intelmq.bin.intelmq_psql_initdb as psql_initdb


class TestPsqlInit(unittest.TestCase):
    """
    A TestCase for intelmq_psql_initdb.
    """

    def setUp(self) -> None:
        super().setUp()

        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)

        self.harmonization_path = f"{self.tempdir.name}/harmonization.conf"
        self._create_simple_harmonization()

    def _create_simple_harmonization(self):
        simple_harmonization = {
            "event": {
                "classification.identifier": {
                    "type": "String"
                },
                "time.source": {
                    "type": "DateTime"
                },
                "raw": {
                    "type": "Base64"
                }
            }
        }
        with open(self.harmonization_path, "w+") as f:
            json.dump(simple_harmonization, f)

    def test_output(self):
        """ Compare output to cached one. """
        with open(os.path.join(os.path.dirname(__file__),
                               'initdb.sql')) as handle:
            expected = handle.read()
        fname = pkg_resources.resource_filename('intelmq', 'etc/harmonization.conf')
        self.assertEqual(psql_initdb.generate(fname).strip(), expected.strip())

    def test_generating_events_schema(self):
        expected_table = """
        CREATE TABLE events (
            "id" BIGSERIAL UNIQUE PRIMARY KEY,
            "classification.identifier" text,
            "raw" text,
            "time.source" timestamp with time zone
        );
        """
        expected_table = self._normalize_leading_whitespaces(expected_table)
        expected_indexes = [
            """CREATE INDEX "idx_events_classification.identifier" ON events USING btree ("classification.identifier");""",
            """CREATE INDEX "idx_events_time.source" ON events USING btree ("time.source");"""
        ]
        generated = psql_initdb.generate(self.harmonization_path)

        self.assertTrue(self._normalize_leading_whitespaces(generated).startswith(expected_table))

        for index in expected_indexes:
            self.assertIn(index, generated)

    def test_skip_generating_events_table_schema(self):
        generated = psql_initdb.generate(self.harmonization_path, skip_events=True)

        self.assertNotIn("CREATE TABLE events", generated)
        self.assertNotIn("CREATE INDEX", generated)

    def test_separated_raws_view_schema(self):
        expected_view = """
        CREATE VIEW public.v_events AS
            SELECT
                events.id,
                events."classification.identifier",
                events."time.source",
                raws."event_id",
                raws."raw"
            FROM (
                public.events
                JOIN public.raws ON ((events.id = raws.event_id)));
        """
        generated = psql_initdb.generate(self.harmonization_path, separate_raws=True)
        generated = self._normalize_leading_whitespaces(generated)
        self.assertIn("CREATE TABLE public.raws", generated)  # static schema, check if added
        self.assertIn(self._normalize_leading_whitespaces(expected_view), generated)

    def test_separated_raws_trigger(self):
        expected_function = """
        CREATE FUNCTION public.process_v_events_insert()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            DECLARE event_id integer;

            BEGIN
                INSERT INTO
                    events (
                        "classification.identifier",
                        "time.source"
                    )
                VALUES
                    (
                        NEW."classification.identifier",
                        NEW."time.source"
                    )
                RETURNING id INTO event_id;
                INSERT INTO
                    raws ("event_id", "raw")
                VALUES
                    (event_id, NEW.raw);
                RETURN NEW;
            END;
        $$;
        """

        generated = psql_initdb.generate(self.harmonization_path, separate_raws=True)
        generated = self._normalize_leading_whitespaces(generated)
        self.assertIn(self._normalize_leading_whitespaces(expected_function), generated)
        self.assertIn("CREATE TRIGGER tr_events", generated)  # Static, check if added

    @staticmethod
    def _normalize_leading_whitespaces(data: str) -> str:
        return re.sub(r"^(\s)*", " ", data.strip(), flags=re.MULTILINE)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
