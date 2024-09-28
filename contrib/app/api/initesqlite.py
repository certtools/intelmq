""" Initialize session database for intelmq-api

SPDX-FileCopyrightText: 2021 Birger Schacht <schacht@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later

"""

import sqlite3
import pathlib
import sys

folder = pathlib.Path(__file__).parent

if len(sys.argv) > 1:
    folder = pathlib.Path(sys.argv[1])

conn = sqlite3.connect(folder / 'api-session.sqlite')

INIT_DB_SQL = """
BEGIN;
CREATE TABLE version (version INTEGER);
INSERT INTO version (version) VALUES (1);

CREATE TABLE session (
    session_id TEXT PRIMARY KEY,
    modified TIMESTAMP,
    data BLOB
);

CREATE TABLE user(
    username TEXT PRIMARY KEY,
    password TEXT,
    salt TEXT
);

COMMIT;
"""

c = conn.cursor()
c.executescript(INIT_DB_SQL)
