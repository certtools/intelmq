# SPDX-FileCopyrightText: 2020 Bernhard Reiter
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
import unittest
from unittest.mock import Mock

from intelmq.bots.outputs.misp.output_api import MISPOBJECT_NAME, MISPAPIOutputBot


class TestMISPAPIOutputBot(unittest.TestCase):
    def setUp(self):
        # Exercise local event handling without a live MISP instance.
        self.bot = MISPAPIOutputBot.__new__(MISPAPIOutputBot)
        self.bot.logger = Mock()
        self.bot.misp = Mock()
        self.bot.significant_fields = ['source.fqdn']
        self.event_data = {'source.fqdn': 'example.org', 'feed.provider': 'Provider'}

    def misp_event(self, values=None):
        event = Mock()
        event.timestamp = datetime.datetime(2020, 1, 1)
        if values is None:
            event.get_objects_by_name.return_value = []
        else:
            obj = Mock()
            obj.get_attributes_by_relation.side_effect = (
                lambda field: [Mock(value=values[field])] if field in values else []
            )
            event.get_objects_by_name.return_value = [obj]
        return event

    def test_no_intelmq_object_is_not_updated(self):
        event = self.misp_event()
        original_timestamp = event.timestamp

        self.bot._update_misp_event(event, self.event_data)

        event.get_objects_by_name.assert_called_once_with(MISPOBJECT_NAME)
        self.bot.misp.update_event.assert_not_called()
        self.assertEqual(event.timestamp, original_timestamp)

    def test_matching_object_is_updated(self):
        event = self.misp_event(self.event_data)
        original_timestamp = event.timestamp

        self.bot._update_misp_event(event, self.event_data)

        self.bot.misp.update_event.assert_called_once_with(event)
        self.assertNotEqual(event.timestamp, original_timestamp)

    def test_mismatching_provider_is_not_updated(self):
        event = self.misp_event(dict(self.event_data, **{'feed.provider': 'Other'}))

        self.bot._update_misp_event(event, self.event_data)

        self.bot.misp.update_event.assert_not_called()

    def test_missing_significant_attribute_is_not_updated(self):
        event = self.misp_event({'feed.provider': 'Provider'})

        self.bot._update_misp_event(event, self.event_data)

        self.bot.misp.update_event.assert_not_called()

    def test_process_continues_after_unrelated_search_result(self):
        unrelated = self.misp_event()
        matching = self.misp_event(self.event_data)
        self.bot.misp.search.return_value = [unrelated, matching]
        self.bot.misp_tag_for_bot = 'IntelMQ'
        message = Mock()
        message.to_dict.return_value = self.event_data
        self.bot.receive_message = Mock(return_value=message)
        self.bot.acknowledge_message = Mock()

        self.bot.process()

        self.bot.misp.update_event.assert_called_once_with(matching)
        self.bot.acknowledge_message.assert_called_once_with()
        self.bot.misp.add_event.assert_not_called()


if __name__ == '__main__':
    unittest.main()
