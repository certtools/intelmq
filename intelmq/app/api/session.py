"""Session support for IntelMQ-Manager

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>
"""

import os
from typing import Tuple, Optional, Union
from contextlib import contextmanager
import json
import threading
import hashlib

import sqlite3


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

LOOKUP_SESSION_SQL = """
SELECT data FROM session WHERE session_id = ?;
"""

STORE_SESSION_SQL = """
INSERT OR REPLACE INTO session (session_id, modified, data)
VALUES (?, CURRENT_TIMESTAMP, ?);
"""

EXPIRATION_SQL = """
DELETE FROM session
 WHERE strftime('%s', 'now') - strftime('%s', modified) > ?;
"""

TOUCH_SESSION_SQL = """
UPDATE session SET modified = CURRENT_TIMESTAMP WHERE session_id = ?;
"""

ADD_USER_SQL = """
INSERT OR REPLACE INTO user (username, password, salt) VALUES (?, ?, ?);
"""

LOOKUP_USER_SQL = """
SELECT username, password, salt FROM user WHERE username = ?;
"""


class SessionStore:
    """Session store based on SQLite

    The SQLite database is used in autocommit mode avoid blocking
    connections to the same database from other processes. This ensures
    that no transactions are open for very long. The transactions this
    class needs to do are all single statements anyway, so autocommit is
    no problem.

    Instances of this class can be used by multiple threads
    simultaneously. Use of the underlying sqlite connection object is
    serialized between threads with a lock.
    """

    def __init__(self, dbname: str, max_duration: int):
        self.dbname = dbname
        self.max_duration = max_duration
        if not os.path.isfile(self.dbname):
            self.init_sqlite_db()
        self.lock = threading.Lock()
        self.connection = self.connect()

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.dbname, check_same_thread=False,
                               isolation_level=None)

    @contextmanager
    def get_con(self):
        with self.lock:
            yield self.connection

    def init_sqlite_db(self):
        with self.connect() as con:
            con.executescript(INIT_DB_SQL)

    def execute(self, stmt: str, params: tuple) -> Optional[tuple]:
        try:
            with self.get_con() as con:
                return con.execute(stmt, params).fetchone()
        except sqlite3.OperationalError as exc:
            print(f"SQLite3-Error ({exc}): Possibly missing write permissions to"
                  " session file (or the folder it is located in).")
            return None

    #
    # Methods for session data
    #

    def expire_sessions(self):
        self.execute(EXPIRATION_SQL, (self.max_duration,))

    def get(self, session_id: str) -> Optional[dict]:
        self.expire_sessions()
        row = self.execute(LOOKUP_SESSION_SQL, (session_id,))
        if row is not None:
            return json.loads(row[0])
        return None

    def set(self, session_id: str, session_data: dict):
        self.execute(STORE_SESSION_SQL,
                     (session_id, json.dumps(session_data)))

    def new_session(self, session_data: dict) -> str:
        token = os.urandom(16).hex()
        self.set(token, session_data)
        return token

    def verify_token(self, token: str) -> Union[bool, dict]:
        session_data = self.get(token)
        if session_data is not None:
            self.execute(TOUCH_SESSION_SQL, (token,))
            return session_data
        return False

    #
    # User account methods
    #

    def add_user(self, username: str, password: str):
        hashed, salt = self.hash_password(password)
        self.execute(ADD_USER_SQL, (username, hashed, salt))

    def verify_user(self, username: str, password: str) -> Optional[dict]:
        row = self.execute(LOOKUP_USER_SQL, (username,))
        if row is not None:
            username, stored_hash, salt = row
            hashed = self.hash_password(password, bytes.fromhex(salt))[0]
            if hashed == stored_hash:
                return {"username": username}
        return None

    def hash_password(self, password: str,
                      salt: Optional[bytes] = None) -> Tuple[str, str]:
        if salt is None:
            salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf8"), salt,
                                     100000)
        return (hashed.hex(), salt.hex())
