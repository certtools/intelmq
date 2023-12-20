"""Basic tests for the API endpoints

SPDX-FileCopyrightText: 2022 CERT.at Gmbh <https://cert.at/>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import json
import os
import subprocess
import tempfile
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional
from unittest import TestCase, mock

from fastapi.testclient import TestClient
from intelmq.lib import utils  # type: ignore

from intelmq_api import dependencies
from intelmq_api.api import runner
from intelmq_api.config import Config
from intelmq_api.dependencies import session_store
from intelmq_api.main import app
from intelmq_api.runctl import RunIntelMQCtl
from intelmq_api.session import SessionStore
from intelmq_api.version import __version__


class DummyConfig(Config):
    def __init__(self):
        # Prevent loading from file
        pass


class DummyRunner(RunIntelMQCtl):

    def __init__(self, base_cmd, paths: Optional[dict] = None):
        super().__init__(base_cmd)
        self._paths = paths

    def _run_intelmq_ctl(self, args: List[str]) -> subprocess.CompletedProcess:
        # simulate dummy response from the CLI command
        return subprocess.CompletedProcess(args, 0, b'{"some": "json"}')

    def get_paths(self) -> Dict[str, str]:
        if self._paths is None:
            return super().get_paths()
        else:
            return self._paths


def get_dummy_reader(**kwargs):
    def dummy_runner():
        return DummyRunner([], **kwargs)
    return dummy_runner


class TestApiWithCLI(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app=app)
        dependencies.startup(DummyConfig())
        app.dependency_overrides[runner] = get_dummy_reader()

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    def test_version(self):
        response = self.client.get("/v1/api/version")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()["intelmq-api"], __version__)

    def test_ensure_response_get_values_and_is_json(self):
        json_paths = ["botnet?action=status", "bot?action=status&id=1",
                      "getlog?lines=1&id=1", "queues", "queues-and-status",
                      "bots", "check", "debug"]

        for path in json_paths:
            with self.subTest(path):
                response = self.client.get(f"/v1/api/{path}")
                self.assertEqual(response.status_code, 200)
                self.assertIsInstance(response.json(), dict)
                self.assertEqual(response.json(), {"some": "json"})

    def test_run_input(self):
        response = self.client.post(
            "/v1/api/run?bot=feodo-tracker-browse-parser&cmd=get&dry=false&show=false",
            data={"msg": "some message"})
        self.assertEqual(response.status_code, 200)


class TestApiWithDir(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app=app)
        dependencies.startup(DummyConfig())
        self.conf_dir = TemporaryDirectory()
        app.dependency_overrides[runner] = get_dummy_reader(
            paths={"CONFIG_DIR": self.conf_dir.name})

        self.save_runtime()
        self.save_positions()

        self.path_patcher = mock.patch(
            "intelmq.lib.utils.RUNTIME_CONF_FILE", f"{self.conf_dir.name}/runtime.yaml")
        self.path_patcher.start()

    def save_runtime(self):
        with open(f"{self.conf_dir.name}/runtime.yaml", "w+") as f:
            json.dump({}, f)

    def save_positions(self):
        os.makedirs(f"{self.conf_dir.name}/manager", exist_ok=True)
        with open(f"{self.conf_dir.name}/manager/positions.conf", "w+") as f:
            json.dump({}, f)

    def tearDown(self) -> None:
        app.dependency_overrides = {}
        self.path_patcher.stop()
        self.conf_dir.cleanup()

    def test_handle_path_with_doubled_slashes(self):
        """The IntelMQ Manager doubles slashes in some paths, but FastAPI doesn't handle it.

        In addition, IntelMQ Manager doesn't respect redirection. As so, keeping the invalid
        paths for backward compatibility."""
        PATHS = ["/v1/api//runtime", "/v1/api//positions"]
        for path in PATHS:
            with self.subTest(path):
                response = self.client.post(path, json={})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.text, "success")

    def test_post_runtime(self):
        data = {
            "some-bot": {
                "bot_id": "bot-1",
                "description": "Test",
                "enabled": True,
                "parameters": {
                    "destination_queues": {
                        "_default": [
                            "file-output-queue"
                        ]
                    },
                    "overwrite": True,
                },
                "run_mode": "continuous"
            }
        }
        response = self.client.post("/v1/api/runtime", json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "success")

        self.assertEqual(utils.get_runtime(), data)

    def test_post_positions(self):
        data = {
            "some-bot": {
                "x": 21,
                "y": 314
            }
        }
        response = self.client.post("/v1/api/positions", json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "success")

        with open(f"{self.conf_dir.name}/manager/positions.conf", "r") as f:
            saved = json.load(f)
        self.assertEqual(saved, data)


class TestAPILogin(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app=app)
        dependencies.startup(DummyConfig())
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.session = SessionStore(os.path.join(self.temp_dir.name, 'sessionsb'), 1000000)
        self.session.add_user('test', 'pass')

        app.dependency_overrides[session_store] = lambda: self.session
        app.dependency_overrides[runner] = get_dummy_reader()

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    def test_login(self):
        response = self.client.post("/v1/api/login", data={"username": "test", "password": "pass"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json().get("login_token"))

    def test_login_and_call(self):
        response = self.client.post("/v1/api/login", data={"username": "test", "password": "pass"})
        self.assertEqual(response.status_code, 200)

        token = response.json().get("login_token")
        authorized_response = self.client.get("/v1/api/version", headers={"authorization": token})
        self.assertEqual(authorized_response.status_code, 200)
        self.assertEqual(authorized_response.json()["intelmq-api"], __version__)

    def test_unauthorized_call(self):
        response = self.client.get("/v1/api/version")
        self.assertEqual(response.status_code, 401)

    def test_bad_token(self):
        response = self.client.get(
            "/v1/api/version", headers={"authorization": "not-a-valid-token"})
        self.assertEqual(response.status_code, 401)
