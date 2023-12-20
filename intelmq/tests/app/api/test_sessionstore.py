"""Tests for IntelMQ-Manager

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import unittest
import tempfile
import os
from pathlib import Path

from intelmq_api.session import SessionStore


class TestSessionStore(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def test_basic_usage(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"),
                             3600)
        session_data = {"csrf_token": "very-secret"}
        store.set("some-uniqe-id", session_data)
        self.assertEqual(store.get("some-uniqe-id"), session_data)

    def test_unknown_session_is_None(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"),
                             3600)
        self.assertIsNone(store.get("some-unknown-id"))

    def test_set_overwriting(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"),
                             3600)
        store.set("just-a-session-id", {"some": "thing"})
        new_data = {"some": "other-thing"}
        store.set("just-a-session-id", new_data)
        self.assertEqual(store.get("just-a-session-id"), new_data)

    def test_new_session(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"),
                             3600)
        token = store.new_session({"username": "some-user"})
        self.assertEqual(store.verify_token(token),
                         {"username": "some-user"})

    def test_verify_unknown_token(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"),
                             3600)
        token = store.new_session({"username": "some-user"})
        # Check that verify_token returns exactly False. This is what
        # hug checks for as well in hug.authentication.authenticator
        self.assertIs(store.verify_token("wrong-token"), False)

    def test_user_account(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"),
                             3600)
        store.add_user("someone", "some-password")
        self.assertEqual(store.verify_user("someone", "some-password"),
                         {"username": "someone"})

    def test_user_account_verify_failed(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"),
                             3600)
        store.add_user("someone", "some-password")
        self.assertEqual(store.verify_user("someone", "wrong-password"), None)
