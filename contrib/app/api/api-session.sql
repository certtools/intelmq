-- Session database structure for intelmq-api
-- 
-- SPDX-FileCopyrightText: 2021 Birger Schacht <schacht@cert.at>
-- SPDX-License-Identifier: AGPL-3.0-or-later

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
