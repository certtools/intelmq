# SPDX-FileCopyrightText: 2026 BharatDeva
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from types import SimpleNamespace

from importlib.metadata import PackageNotFoundError
from packaging.version import Version

import intelmq.lib.mixins.stomp as stomp


def test_stomp_version_uses_distribution_metadata(monkeypatch):
    monkeypatch.setattr(stomp, "version", lambda _: "8.2.0")
    monkeypatch.setattr(stomp, "stomp", SimpleNamespace(__version__=(4, 1, 12)))

    assert stomp.stomp_version() == Version("8.2.0")


def test_stomp_version_falls_back_to_tuple_module_version(monkeypatch):
    def missing_distribution(_):
        raise PackageNotFoundError

    monkeypatch.setattr(stomp, "version", missing_distribution)
    monkeypatch.setattr(stomp, "stomp", SimpleNamespace(__version__=(4, 1, 12)))

    assert stomp.stomp_version() == Version("4.1.12")
