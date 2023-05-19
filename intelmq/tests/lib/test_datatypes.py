# SPDX-FileCopyrightText: 2023 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import unittest

from intelmq.lib.datatypes import TimeFormat
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.harmonization import DateTime


class TestTimeFormat(unittest.TestCase):

    def test_no_argument(self):
        time_format = TimeFormat()
        self.assertIs(time_format.convert, DateTime.from_fuzzy)
        self.assertIsNone(time_format.format_string)

    def test_none(self):
        time_format = TimeFormat(None)
        self.assertIs(time_format.convert, DateTime.from_fuzzy)
        self.assertIsNone(time_format.format_string)

    def test_empty_string(self):
        time_format = TimeFormat("")
        self.assertIs(time_format.convert, DateTime.from_fuzzy)
        self.assertIsNone(time_format.format_string)

    def test_from_timestamp(self):
        time_format = TimeFormat("timestamp")
        self.assertIs(time_format.convert, DateTime.from_timestamp)
        self.assertIsNone(time_format.format_string)

    def test_from_windows_nt(self):
        time_format = TimeFormat("windows_nt")
        self.assertIs(time_format.convert, DateTime.from_windows_nt)
        self.assertIsNone(time_format.format_string)

    def test_from_epoch_millis(self):
        time_format = TimeFormat("epoch_millis")
        self.assertIs(time_format.convert, DateTime.from_epoch_millis)
        self.assertIsNone(time_format.format_string)

    def test_from_format(self):
        time_format = TimeFormat("from_format|%Y-%m-%d %H:%M:%S")
        self.assertIs(time_format.convert, DateTime.from_format)
        self.assertEqual(time_format.format_string, "%Y-%m-%d %H:%M:%S")

    def test_from_format_midnight(self):
        time_format = TimeFormat("from_format_midnight|%Y-%m-%d")
        self.assertIs(time_format.convert, DateTime.from_format_midnight)
        self.assertEqual(time_format.format_string, "%Y-%m-%d")

    def test_from_utc_isoformat(self):
        time_format = TimeFormat("utc_isoformat")
        self.assertIs(time_format.convert, DateTime.from_isoformat)
        self.assertIsNone(time_format.format_string)

    def test_from_fuzzy(self):
        time_format = TimeFormat("fuzzy")
        self.assertIs(time_format.convert, DateTime.from_fuzzy)
        self.assertIsNone(time_format.format_string)

    def test_raise_on_invalid_conversion_name(self):
        self.assertRaises(InvalidArgument, TimeFormat, "from_meatloaf")

    def test_raise_on_missing_format_string(self):
        self.assertRaises(InvalidArgument, TimeFormat, "from_format")
        self.assertRaises(InvalidArgument, TimeFormat, "from_format_midnight")

    def test_raise_on_extra_format_string(self):
        self.assertRaises(InvalidArgument, TimeFormat, "timestamp|%Y-%m-%d")
        self.assertRaises(InvalidArgument, TimeFormat, "windows_nt|%Y-%m-%d")
        self.assertRaises(InvalidArgument, TimeFormat, "epoch_millis|%Y-%m-%d")
        self.assertRaises(InvalidArgument, TimeFormat, "utc_isoformat|%Y-%m-%d")
        self.assertRaises(InvalidArgument, TimeFormat, "fuzzy|%Y-%m-%d")
