# SPDX-FileCopyrightText: 2016 aaronkaplan
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os
from types import SimpleNamespace
from unittest.mock import Mock

from packaging.version import Version

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.outputs.stomp.output

from intelmq.bots.outputs.stomp.output import StompOutputBot


def test_connect_with_string_stomp_version(monkeypatch):
    bot = StompOutputBot.__new__(StompOutputBot)
    bot.logger = Mock()
    bot._connect_kwargs = {"wait": True}
    bot._conn = SimpleNamespace(start=Mock(), connect=Mock())

    monkeypatch.setattr("intelmq.bots.outputs.stomp.output.stomp_version",
                        lambda: Version("8.2.0"))

    bot.connect()

    bot._conn.start.assert_not_called()
    bot._conn.connect.assert_called_once_with(wait=True)
