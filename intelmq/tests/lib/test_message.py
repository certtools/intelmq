# -*- coding: utf-8 -*-
"""
Testing the Message classes of intelmq.

Unicode is used for all tests.
Most tests are performed on Report, as it is formally the same as Message,
but has a valid Harmonization configuration.
"""
from __future__ import unicode_literals

import json
import unittest

import intelmq.lib.exceptions as exceptions
import intelmq.lib.utils as utils
import pkg_resources
import six

conf_filename = pkg_resources.resource_filename('intelmq',
                                                'conf/harmonization.conf')
harm_config = utils.load_configuration(conf_filename)
import intelmq.lib.message as message

LOREM_BASE64 = 'bG9yZW0gaXBzdW0='
DOLOR_BASE64 = 'ZG9sb3Igc2l0IGFtZXQ='
FEED = {'feed.url': u'https://example.com/', 'feed.name': u'Lorem ipsum'}
URL_UNSANE = 'https://example.com/ \r\n'
URL_SANE = 'https://example.com/'
URL_INVALID = '/exampl\n'
ACCURACY_UNSANE = '100'
ACCURACY_SANE = 100
ACCURACY_INVALID = -1


class TestMessageFactory(unittest.TestCase):
    """
    Testing basic functionality of MessageFactory.
    """

    def add_report_examples(self, report):
        report.add('feed.name', 'Example')
        report.add('feed.url', URL_SANE)
        report.add('raw', LOREM_BASE64)
        return report

    def add_event_examples(self, event):
        event.add('feed.name', 'Example')
        event.add('feed.url', URL_SANE)
        event.add('raw', LOREM_BASE64)
        event.add('time.observation', u'2015-01-01T13:37:00+00:00')
        return event

    def test_report_type(self):
        """ Test if MessageFactory returns a Report. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        self.assertEqual(type(report),
                         message.Report)

    def test_event_type(self):
        """ Test if MessageFactory returns a Event. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertEqual(type(event),
                         message.Event)

    def test_report_subclass(self):
        """ Test if MessageFactory returns a Report subclassed from dict. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        self.assertTrue(isinstance(report, (message.Message, dict)))

    def test_event_subclass(self):
        """ Test if MessageFactory returns a Event subclassed from dict. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertTrue(isinstance(event, (message.Message, dict)))

    def test_invalid_type(self):
        """ Test if Message raises InvalidArgument for invalid type. """
        with self.assertRaises(exceptions.InvalidArgument):
            message.MessageFactory.unserialize('{"__type": "Message"}')

    def test_invalid_type2(self):
        """ Test if MessageFactory raises InvalidArgument for invalid type. """
        with self.assertRaises(exceptions.InvalidArgument):
            message.MessageFactory.unserialize('{"__type": "Invalid"}')

    def test_report_invalid_key(self):
        """ Test if report raises InvalidKey for invalid key in add(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidKey):
            report.add('invalid', 0)

    def test_report_add_raw(self):
        """ Test if report can add raw value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        self.assertDictContainsSubset({'raw': LOREM_BASE64},
                                      report)

    def test_report_value(self):
        """ Test if report return value in value(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        self.assertEqual(LOREM_BASE64, report.value('raw'))

    def test_report_get(self):
        """ Test if report return value in get(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        self.assertEqual(LOREM_BASE64, report.get('raw'))

    def test_report_add_invalid(self):
        """ Test report add raises on invalid value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.url', '\r\n')

    def test_report_getitem(self):
        """ Test if report return value in __getitem__(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        self.assertEqual(LOREM_BASE64, report['raw'])

    def test_report_setitem(self):
        """ Test if report sets value in __setitem__(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report['raw'] = LOREM_BASE64
        self.assertEqual(LOREM_BASE64, report['raw'])

    def test_report_ignore_none(self):
        """ Test if report ignores None. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', None)
        self.assertNotIn('feed.name', report)

    def test_report_ignore_empty(self):
        """ Test if report ignores empty string. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', "")
        self.assertNotIn('feed.name', report)

    def test_report_ignore_hyphen(self):
        """ Test if report ignores '-'. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', '-')
        self.assertNotIn('feed.name', report)

    def test_report_ignore_na(self):
        """ Test if report ignores 'N/A'. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'N/A')
        self.assertNotIn('feed.name', report)

    def test_report_ignore_given(self):
        """ Test if report ignores given ignore value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'IGNORE_THIS', ignore=('IGNORE_THIS'))
        self.assertNotIn('feed.name', report)

    def test_report_ignore_given_invalid(self):
        """ Test if report ignores given ignore value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidArgument):
            report.add('feed.name', 'IGNORE_THIS', ignore=1337)

    def test_report_add_duplicate(self):
        """ Test if report can add raw value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        with self.assertRaises(exceptions.KeyExists):
            report.add('raw', LOREM_BASE64)

    def test_report_add_duplicate_force(self):
        """ Test if report can add raw value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        report.add('raw', DOLOR_BASE64, force=True)
        self.assertDictContainsSubset({'raw': DOLOR_BASE64},
                                      report)

    def test_report_del_(self):
        """ Test if report can del a value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        del report['raw']
        self.assertNotIn('raw', report)

    def test_report_clear(self):
        """ Test if report can clear a value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        report.clear('raw')
        self.assertNotIn('raw', report)

    def test_report_asdict(self):
        """ Test if report compares as dictionary. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        for key, value in FEED.items():
            report.add(key, value)
        self.assertDictEqual(FEED, report)

    def test_report_finditems(self):
        """ Test report finditems() generator. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        for key, value in FEED.items():
            report.add(key, value)
        self.assertDictEqual(FEED, dict(report.finditems('feed.')))

    def test_report_items(self):
        """ Test if report returns all keys in list with items(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        for key, value in FEED.items():
            report.add(key, value)
        self.assertListEqual(list(FEED.items()), list(report.items()))

    def test_report_add_byte(self):
        """ Test if report rejects a byte string. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises((exceptions.InvalidValue,
                                TypeError)):
            report.add('raw', bytes(LOREM_BASE64))

    def test_report_sanitize_url(self):
        """ Test if report sanitizes an URL. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.url', URL_UNSANE, sanitize=True)
        self.assertEqual(URL_SANE, report['feed.url'])

    def test_report_invalid_url(self):
        """ Test if report sanitizes an invalid URL. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.url', URL_INVALID)

    def test_report_add_sane_accuracy(self):
        """ Test if report accepts a sane accuracy. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.accuracy', ACCURACY_SANE, sanitize=False)
        self.assertEqual(ACCURACY_SANE, report['feed.accuracy'])

    def test_report_sanitize_accuracy(self):
        """ Test if report sanitizes the accuracy parameter. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.accuracy', ACCURACY_UNSANE, sanitize=True)
        self.assertEqual(ACCURACY_SANE, report['feed.accuracy'])

    def test_report_invalid_accuracy(self):
        """ Test if report sanitizes an invalid accuracy. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.accuracy', ACCURACY_INVALID)

    def test_report_invalid_string(self):
        """ Test if report raises error when invalid after sanitize. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.name', u'\r\n', sanitize=True)

    def test_report_update(self):
        """ Test report value update function. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'Example 1')
        report.update('feed.name', 'Example 2')
        self.assertEqual('Example 2', report['feed.name'])

    def test_report_contains(self):
        """ Test report value contains function. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'Example 1')
        self.assertTrue(report.contains('feed.name'))

    def test_report_update_duplicate(self):
        """ Test report value update function, rejects duplicate. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.KeyNotExists):
            report.update('feed.name', 'Example')

    def test_factory_serialize(self):
        """ Test MessageFactory serialize method. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'Example')
        report.add('feed.url', URL_SANE)
        report.add('raw', LOREM_BASE64)
        actual = message.MessageFactory.serialize(report)
        expected = ('{"raw": "bG9yZW0gaXBzdW0=", "__type": "Report", "feed.url'
                    '": "https://example.com/", "feed.name": "Example"}')
        self.assertDictEqual(json.loads(expected),
                             json.loads(actual))

    def test_report_unicode(self):
        """ Test Message __unicode__ function, pointing to serialize. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertEqual(report.serialize(),
                         six.text_type(report))

    def test_deep_copy_content(self):
        """ Test if deep_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertSetEqual(set(report.deep_copy().items()),
                            set(report.items()))

    def test_deep_copy_items(self):  # TODO: Sort by key
        """ Test if deep_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertNotEqual(set(map(id, report.deep_copy())),
                            set(map(id, report)))

    def test_deep_copy_object(self):
        """ Test if depp_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertIsNot(report.deep_copy(), report)

    def test_copy_content(self):
        """ Test if deep_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertSetEqual(set(report.copy().items()),
                            set(report.items()))

    def test_copy_items(self):
        """ Test if deep_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertEqual(set(map(id, report.copy())),
                         set(map(id, report)))

    def test_copy_object(self):
        """ Test if deep_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertIsNot(report.copy(), report)

    def test_event_hash(self):
        """ Test Event __hash__ 'time.observation should be ignored. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        event1 = self.add_event_examples(event)
        event2 = event1.deep_copy()
        event2.add('time.observation', u'2015-12-12T13:37:50+01:00',
                   force=True, sanitize=True)
        self.assertEqual(hash(event1), hash(event2))

    def test_event_dict(self):
        """ Test Event to_dict. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        event = self.add_event_examples(event)
        self.assertDictEqual({'feed': {'name': 'Example',
                                       'url': 'https://example.com/'},
                              'raw': 'bG9yZW0gaXBzdW0=',
                              'time': {'observation': '2015-01-01T13:37:00+'
                                                      '00:00'}},
                             event.to_dict())

    def test_event_json(self):
        """ Test Event to_json. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        event = self.add_event_examples(event)
        actual = event.to_json()
        self.assertIsInstance(actual, six.text_type)
        expected = ('{"feed": {"url": "https://example.com/", "name": '
                    '"Example"}, "raw": "bG9yZW0gaXBzdW0=", "time": '
                    '{"observation": "2015-01-01T13:37:00+00:00"}}')
        self.assertDictEqual(json.loads(expected), json.loads(actual))

    def test_event_serialize(self):
        """ Test Event serialize. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertEqual('{"__type": "Event"}',
                         event.serialize())

    def test_event_string(self):
        """ Test Event serialize. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertEqual('{"__type": "Event"}',
                         event.serialize())

    def test_event_unicode(self):
        """ Test Event serialize. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertEqual('{"__type": "Event"}',
                         event.serialize())

    def test_event_hash_regex(self):
        """ Test if the regex for event_hash is tested correctly. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        with self.assertRaises(exceptions.InvalidValue):
            event.add('event_hash', u'dasf78')

    def test_port_regex(self):
        """ Test if the regex for port (integer) is tested correctly. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        with self.assertRaises(exceptions.InvalidValue):
            event.add('source.port', 123456)

    def test_malwarename_regex(self):
        """ Test if the regex for malware.name is tested correctly. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        event.add('malware.name', 'multiple-malware citadel:report')
        del event['malware.name']
        with self.assertRaises(exceptions.InvalidValue):
            event.add('malware.name', 'tu234t2t$#%$')

    def test_protocol_ascii(self):
        """ Test if ascii for protocol is tested correctly. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        with self.assertRaises(exceptions.InvalidValue):
            event.add('protocol.application', 'a€80"')

    def test_protocol_length(self):
        """ Test if the length for protocol is tested correctly. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        with self.assertRaises(exceptions.InvalidValue):
            event.add('protocol.transport', 'unknown')

    def test_message_from_dict_return_type(self):
        """ Test if from_dict() returns the correct class. """
        event = {'__type': 'Event'}
        event_type = type(message.MessageFactory.from_dict(event))
        self.assertTrue(event_type is message.Event,
                        msg='Type is {} instead of Event.'.format(event_type))

if __name__ == '__main__':
    unittest.main()
