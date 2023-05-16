"""Tests for the intelmqsetup

SPDX-FileCopyrightText: 2023 CERT.at GmbH <https://cert.at/>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import unittest
from unittest import mock

from intelmq.bin import intelmqsetup


class TestOwnership(unittest.TestCase):
    @mock.patch("shutil.chown")
    def test_skip_changing_root_path_ownership(self, chown_mock):
        with mock.patch.object(intelmqsetup.Path, 'owner') as owner_mock:
            with mock.patch.object(intelmqsetup.Path, 'group') as group_mock:
                owner_mock.return_value = 'root'
                group_mock.return_value = 'root'
                intelmqsetup.change_owner('/', 'intelmq', 'intelmq')
                intelmqsetup.change_owner('//', 'intelmq', 'intelmq')
                intelmqsetup.change_owner('///', 'intelmq', 'intelmq')

        chown_mock.assert_not_called()

    @mock.patch("shutil.chown")
    def test_change_file_ownership(self, chown_mock):
        with mock.patch.object(intelmqsetup.Path, 'owner') as owner_mock:
            with mock.patch.object(intelmqsetup.Path, 'group') as group_mock:
                owner_mock.return_value = 'root'
                group_mock.return_value = 'root'
                intelmqsetup.change_owner('/the/path', 'intelmq', 'intelmq')

        chown_mock.assert_any_call('/the/path', user='intelmq')
        chown_mock.assert_any_call('/the/path', group='intelmq')
