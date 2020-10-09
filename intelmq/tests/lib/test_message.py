# -*- coding: utf-8 -*-
"""
Testing the Message classes of intelmq.

Unicode is used for all tests.
Most tests are performed on Report, as it is formally the same as Message,
but has a valid Harmonization configuration.
"""
import json
import unittest

import pkg_resources

import intelmq.lib.exceptions as exceptions
import intelmq.lib.message as message  # noqa
from intelmq.lib.utils import load_configuration

HARM = load_configuration(pkg_resources.resource_filename('intelmq',
                                                          'etc/harmonization.conf'))

LOREM_BASE64 = 'bG9yZW0gaXBzdW0='
DOLOR_BASE64 = 'ZG9sb3Igc2l0IGFtZXQ='
FEED = {'feed.url': 'https://example.com/', 'feed.name': 'Lorem ipsum'}
URL_UNSANE = 'https://example.com/ \r\n'
URL_SANE = 'https://example.com/'
URL_INVALID = '/exampl\n'
ACCURACY_UNSANE = '100'
ACCURACY_SANE = 100
ACCURACY_INVALID = -1
FEED_FIELDS = {'feed.accuracy': 80,
               'feed.code': 'code',
               'feed.documentation': 'https://www.example.com/docs',
               'feed.name': 'Feed',
               'feed.provider': 'Feed Provider',
               'feed.url': 'https://www.example.com',
               'rtir_id': 1337,
               'extra.mail_subject': 'This is a test',
               }


class TestMessageFactory(unittest.TestCase):
    """
    Testing basic functionality of MessageFactory.
    """

    def assertListUnorderdEqual(self, expected, actual):
        """
        Checks sequences for same content, regardless of order.
        """
        self.assertCountEqual(expected, actual)

    def assertDictContainsSubset(self, actual, expected):
        """
        Checks whether expected is a subset of actual.

        https://docs.python.org/3/whatsnew/3.2.html?highlight=assertdictcontainssubset

        https://stackoverflow.com/a/57386339/2851664
        cc by-sa 3.0 John1024
        """
        self.assertGreaterEqual(expected.items(), actual.items())

    def new_report(self, auto=False, examples=False):
        report = message.Report(harmonization=HARM, auto=auto)
        if examples:
            return self.add_report_examples(report)
        else:
            return report

    def new_event(self):
        return message.Event(harmonization=HARM)

    def add_report_examples(self, report):
        report.add('feed.name', 'Example')
        report.add('feed.url', URL_SANE)
        report.add('raw', LOREM_BASE64, sanitize=False)
        return report

    def add_event_examples(self, event):
        event.add('feed.name', 'Example')
        event.add('feed.url', URL_SANE)
        event.add('raw', LOREM_BASE64, sanitize=False)
        event.add('time.observation', '2015-01-01T13:37:00+00:00')
        return event

    def test_report_type(self):
        """ Test if MessageFactory returns a Report. """
        report = self.new_report()
        self.assertEqual(type(report),
                         message.Report)

    def test_event_type(self):
        """ Test if MessageFactory returns a Event. """
        event = self.new_event()
        self.assertEqual(type(event),
                         message.Event)

    def test_report_init_auto(self):
        """ Test if serialize does pass auto=True """
        report = self.new_report()
        self.assertIn('time.observation', report)

    def test_report_serialize_auto(self):
        """ Test if serialize does pass auto=True """
        report = self.new_report(auto=True)
        self.assertNotIn('time.observation', report)

    def test_report_subclass(self):
        """ Test if MessageFactory returns a Report subclassed from dict. """
        report = self.new_report()
        self.assertTrue(isinstance(report, (message.Message, dict)))

    def test_event_subclass(self):
        """ Test if MessageFactory returns a Event subclassed from dict. """
        event = self.new_event()
        self.assertTrue(isinstance(event, (message.Message, dict)))

    def test_message_eq(self):
        """ Test if Message.__eq__ works. """
        event1 = self.add_event_examples(self.new_event())
        event2 = self.add_event_examples(self.new_event())
        self.assertTrue(event1 == event2)

    def test_message_ne(self):
        """ Test if Message.__ne__ works. """
        event1 = self.add_event_examples(self.new_event())
        event2 = self.add_event_examples(self.new_event())
        self.assertFalse(event1 != event2)

    def test_event_report_eq(self):
        """ Test if empty Message is not equal empty Report. """
        event = self.new_event()
        report = self.new_report(auto=True)
        self.assertFalse(event == report)

    def test_event_report_ne(self):
        """ Test if empty Message is not equal empty Report. """
        event = self.new_event()
        report = self.new_report(auto=True)
        self.assertTrue(event != report)

    def test_event_eq_different_config(self):
        """ Test if empty Message is not equal empty Report. """
        event1 = message.Event(harmonization=HARM)
        event2 = message.Event(harmonization={"event": {"extra": {"type": "JSON"}}})
        self.assertFalse(event1 == event2)

    def test_event_ne_different_config(self):
        """ Test if empty Message is not equal empty Report. """
        event1 = message.Event(harmonization=HARM)
        event2 = message.Event(harmonization={"event": {"extra": {"type": "JSON"}}})
        self.assertTrue(event1 != event2)

    def test_invalid_type(self):
        """ Test if Message raises InvalidArgument for invalid type. """
        with self.assertRaises(exceptions.InvalidArgument):
            message.MessageFactory.unserialize('{"__type": "Message"}', harmonization=HARM)

    def test_invalid_type2(self):
        """ Test if MessageFactory raises InvalidArgument for invalid type. """
        with self.assertRaises(exceptions.InvalidArgument):
            message.MessageFactory.unserialize('{"__type": "Invalid"}', harmonization=HARM)

    def test_report_invalid_key(self):
        """ Test if report raises InvalidKey for invalid key in add(). """
        report = self.new_report()
        with self.assertRaises(exceptions.InvalidKey):
            report.add('invalid', 0)

    def test_report_add_raw(self):
        """ Test if report can add raw value. """
        report = self.new_report(auto=True)
        report.add('raw', 'lorem ipsum')
        self.assertDictContainsSubset({'raw': LOREM_BASE64},
                                      report)

    def test_report_get(self):
        """ Test if report return value in get(). """
        report = self.new_report()
        report.add('raw', LOREM_BASE64, sanitize=False)
        self.assertEqual(LOREM_BASE64, report.get('raw'))

    def test_report_add_invalid(self):
        """ Test report add raises on invalid value. """
        report = self.new_report()
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.url', '\r\n')

    def test_report_getitem(self):
        """ Test if report return value in __getitem__(). """
        report = self.new_report()
        report.add('raw', LOREM_BASE64, sanitize=False)
        self.assertEqual(LOREM_BASE64, report['raw'])

    def test_report_setitem(self):
        """ Test if report sets value in __setitem__(). """
        report = self.new_report()
        report['raw'] = 'lorem ipsum'
        self.assertEqual(LOREM_BASE64, report['raw'])

    def test_report_ignore_none(self):
        """ Test if report ignores None. """
        report = self.new_report()
        report.add('feed.name', None)
        self.assertNotIn('feed.name', report)

    def test_report_change_delete_none(self):
        """ Test if report ignores None. """
        report = self.new_report()
        report.add('feed.name', 'foo')
        report.change('feed.name', None)
        self.assertNotIn('feed.name', report)

    def test_report_ignore_empty(self):
        """ Test if report ignores empty string. """
        report = self.new_report()
        report.add('feed.name', "")
        self.assertNotIn('feed.name', report)

    def test_report_ignore_hyphen(self):
        """ Test if report ignores '-'. """
        report = self.new_report()
        report.add('feed.name', '-')
        self.assertNotIn('feed.name', report)

    def test_report_is_valid(self):
        """ Test if report ignores '-'. """
        event = self.new_event()
        self.assertFalse(event.is_valid('feed.name', '-'))
        self.assertFalse(event.is_valid('feed.name', None))
        self.assertFalse(event.is_valid('source.ip', '127.0.0.1/24'))
        self.assertFalse(event.is_valid('source.ip', '127.0.0.1/24', sanitize=False))
        self.assertTrue(event.is_valid('source.ip', '127.0.0.1'))
        with self.assertRaises(exceptions.InvalidKey):
            event.is_valid('invalid', 0)

    def test_report_ignore_na(self):
        """ Test if report ignores 'N/A'. """
        report = self.new_report()
        report.add('feed.name', 'N/A')
        self.assertNotIn('feed.name', report)

    def test_report_ignore_given(self):
        """ Test if report ignores given ignore value. """
        report = self.new_report()
        report.add('feed.name', 'IGNORE_THIS', ignore=('IGNORE_THIS'))
        self.assertNotIn('feed.name', report)

    def test_report_ignore_given_invalid(self):
        """ Test if report ignores given ignore value. """
        report = self.new_report()
        with self.assertRaises(exceptions.InvalidArgument):
            report.add('feed.name', 'IGNORE_THIS', ignore=1337)

    def test_report_add_duplicate(self):
        """ Test if report can add raw value. """
        report = self.new_report()
        report.add('raw', LOREM_BASE64)
        with self.assertRaises(exceptions.KeyExists):
            report.add('raw', LOREM_BASE64)

    def test_report_del_(self):
        """ Test if report can del a value. """
        report = self.new_report()
        report.add('raw', LOREM_BASE64)
        del report['raw']
        self.assertNotIn('raw', report)

    def test_report_asdict(self):
        """ Test if report compares as dictionary. """
        report = self.new_report(auto=True)
        for key, value in FEED.items():
            report.add(key, value)
        self.assertDictEqual(FEED, report)

    def test_report_finditems(self):
        """ Test report finditems() generator. """
        report = self.new_report()
        for key, value in FEED.items():
            report.add(key, value)
        self.assertDictEqual(FEED, dict(report.finditems('feed.')))

    def test_report_items(self):
        """ Test if report returns all keys in list with items(). """
        report = self.new_report(auto=True)
        for key, value in FEED.items():
            report.add(key, value)
        self.assertListUnorderdEqual(list(FEED.items()), list(report.items()))

    def test_report_add_raise_failure(self):
        """ Test if report returns all keys in list with items(). """
        report = self.new_report()
        self.assertFalse(report.add('feed.url', 'invalid', raise_failure=False))

    def test_report_add_byte(self):
        """ Test if report rejects a byte string. """
        report = self.new_report()
        with self.assertRaises((exceptions.InvalidValue,
                                TypeError)):
            report.add('raw', bytes(LOREM_BASE64), sanitize=False)

    def test_report_sanitize_url(self):
        """ Test if report sanitizes an URL. """
        report = self.new_report()
        report.add('feed.url', URL_UNSANE)
        self.assertEqual(URL_SANE, report['feed.url'])

    def test_report_invalid_url(self):
        """ Test if report sanitizes an invalid URL. """
        report = self.new_report()
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.url', URL_INVALID)

    def test_report_add_sane_accuracy(self):
        """ Test if report accepts a sane accuracy. """
        report = self.new_report()
        report.add('feed.accuracy', ACCURACY_SANE, sanitize=False)
        self.assertEqual(ACCURACY_SANE, report['feed.accuracy'])

    def test_report_sanitize_accuracy(self):
        """ Test if report sanitizes the accuracy parameter. """
        report = self.new_report()
        report.add('feed.accuracy', ACCURACY_UNSANE)
        self.assertEqual(ACCURACY_SANE, report['feed.accuracy'])

    def test_report_invalid_accuracy(self):
        """ Test if report sanitizes an invalid accuracy. """
        report = self.new_report()
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.accuracy', ACCURACY_INVALID)

    def test_report_invalid_string(self):
        """ Test if report raises error when invalid after sanitize. """
        report = self.new_report()
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.name', '\r\n')

    def test_report_change(self):
        """ Test report value change function. """
        report = self.new_report()
        report.add('feed.name', 'Example 1')
        report.change('feed.name', 'Example 2')
        self.assertEqual('Example 2', report['feed.name'])

    def test_report_in(self):
        """ Test report value in function. """
        report = self.new_report()
        report.add('feed.name', 'Example 1')
        self.assertTrue('feed.name' in report)

    def test_report_change_duplicate(self):
        """ Test report value change function, rejects duplicate. """
        report = self.new_report()
        with self.assertRaises(exceptions.KeyNotExists):
            report.change('feed.name', 'Example')

    def test_factory_serialize(self):
        """ Test MessageFactory serialize method. """
        report = self.new_report(auto=True)
        report.add('feed.name', 'Example')
        report.add('feed.url', URL_SANE)
        report.add('raw', LOREM_BASE64, sanitize=False)
        actual = message.MessageFactory.serialize(report)
        expected = ('{"raw": "bG9yZW0gaXBzdW0=", "__type": "Report", "feed.url'
                    '": "https://example.com/", "feed.name": "Example"}')
        self.assertDictEqual(json.loads(expected),
                             json.loads(actual))

    def test_deep_copy_content(self):
        """ Test if deep_copy does return the same items. """
        report = self.new_report(examples=True)
        self.assertSetEqual(set(report.deep_copy().items()),
                            set(report.items()))

    def test_deep_copy_items(self):
        """ Test if deep_copy does not return the same objects. """
        report = self.new_report(examples=True)
        self.assertNotEqual(set(map(id, report.deep_copy())),
                            set(map(id, report)))

    def test_deep_copy_object(self):
        """ Test if depp_copy does not return the same object. """
        report = self.new_report(examples=True)
        self.assertIsNot(report.deep_copy(), report)

    def test_copy_content(self):
        """ Test if copy does return the same items. """
        report = self.new_report(examples=True)
        self.assertSetEqual(set(report.copy().items()),
                            set(report.items()))

    def test_copy_items(self):
        """ Test if copy does return the same objects. """
        report = self.new_report(examples=True)
        self.assertEqual(set(map(id, report.copy())),
                         set(map(id, report)))

    def test_copy_object(self):
        """ Test if copy does not return the same object. """
        report = self.new_report(examples=True)
        self.assertIsNot(report.copy(), report)

    def test_event_hash(self):
        """ Test Event __hash__ 'time.observation should be ignored. """
        event = self.new_event()
        event1 = self.add_event_examples(event)
        event2 = event1.deep_copy()
        event2.add('time.observation', '2015-12-12T13:37:50+01:00',
                   overwrite=True)
        self.assertEqual(hash(event1), hash(event2))

    def test_event_hash_fixed(self):
        """ Test if Event hash hasn't changed unintentionally. """
        event = self.new_event()
        event1 = self.add_event_examples(event)
        event2 = event1.deep_copy()
        event2.add('time.observation', '2015-12-12T13:37:50+01:00',
                   overwrite=True)
        self.assertEqual(event1.hash(),
                         'd04aa050afdc58a39329c78c3b59ce6fb6f11effe180fe8084b4f1e89007de71')

    def test_event_hash_method(self):
        """ Test Event hash() 'time.observation' should be ignored. """
        event = self.new_event()
        event1 = self.add_event_examples(event)
        event2 = event1.deep_copy()
        event2.add('time.observation', '2015-12-12T13:37:50+01:00',
                   overwrite=True)
        self.assertEqual(event1.hash(), event2.hash())

    def test_event_hash_method_blacklist(self):
        """ Test Event hash(blacklist) """
        event = self.new_event()
        event1 = self.add_event_examples(event)
        event2 = event1.deep_copy()
        event2.add('time.observation', '2015-12-12T13:37:50+01:00',
                   overwrite=True)
        event2.add('feed.name', 'Some Other Feed', overwrite=True)
        # The feed.name is usually taken into account:
        self.assertNotEqual(event1.hash(), event2.hash())
        # But not if we blacklist it (time.observation does not have to
        # blacklisted explicitly):
        self.assertEqual(event1.hash(filter_type="blacklist",
                                     filter_keys={"feed.name"}),
                         event2.hash(filter_type="blacklist",
                                     filter_keys={"feed.name"}))

        self.assertNotEqual(event1.hash(filter_type="blacklist",
                                        filter_keys={"feed.url", "raw"}),
                            event2.hash(filter_type="blacklist",
                                        filter_keys={"feed.url", "raw"}))

    def test_event_hash_method_whitelist(self):
        """ Test Event hash(blacklist) """
        event = self.new_event()

        event1 = self.add_event_examples(event)
        event2 = event1.deep_copy()

        event2.add('feed.name', 'Some Other Feed', overwrite=True)

        self.assertNotEqual(event1.hash(), event2.hash())

        self.assertNotEqual(event1.hash(filter_type="whitelist",
                                        filter_keys={"feed.name"}),
                            event2.hash(filter_type="whitelist",
                                        filter_keys={"feed.name"}))

        self.assertEqual(event1.hash(filter_type="whitelist",
                                     filter_keys={"feed.url", "raw"}),
                         event2.hash(filter_type="whitelist",
                                     filter_keys={"feed.url", "raw"}))

    def test_event_dict(self):
        """ Test Event to_dict. """
        event = self.new_event()
        event = self.add_event_examples(event)
        self.assertDictEqual({'feed.name': 'Example',
                              'feed.url': 'https://example.com/',
                              'raw': 'bG9yZW0gaXBzdW0=',
                              'time.observation': '2015-01-01T13:37:00+00:00'},
                             event.to_dict())

    def test_event_dict_hierarchical(self):
        """ Test Event to_dict. """
        event = self.new_event()
        event = self.add_event_examples(event)
        self.assertDictEqual({'feed': {'name': 'Example',
                                       'url': 'https://example.com/'},
                              'raw': 'bG9yZW0gaXBzdW0=',
                              'time': {'observation': '2015-01-01T13:37:00+'
                                                      '00:00'}},
                             event.to_dict(hierarchical=True))

    def test_event_json(self):
        """ Test Event to_json. """
        event = self.new_event()
        event = self.add_event_examples(event)
        actual = event.to_json()
        self.assertIsInstance(actual, str)
        expected = ('{"feed.url": "https://example.com/", "feed.name": '
                    '"Example", "raw": "bG9yZW0gaXBzdW0=", "time.observation": '
                    '"2015-01-01T13:37:00+00:00"}')
        self.assertDictEqual(json.loads(expected), json.loads(actual))

    def test_event_json_hierarchical(self):
        """ Test Event to_json. """
        event = self.new_event()
        event = self.add_event_examples(event)
        actual = event.to_json(hierarchical=True)
        self.assertIsInstance(actual, str)
        expected = ('{"feed": {"url": "https://example.com/", "name": '
                    '"Example"}, "raw": "bG9yZW0gaXBzdW0=", "time": '
                    '{"observation": "2015-01-01T13:37:00+00:00"}}')
        self.assertDictEqual(json.loads(expected), json.loads(actual))

    def test_event_serialize(self):
        """ Test Event serialize. """
        event = self.new_event()
        self.assertEqual('{"__type": "Event"}',
                         event.serialize())

    def test_event_string(self):
        """ Test Event serialize. """
        event = self.new_event()
        self.assertEqual('{"__type": "Event"}',
                         event.serialize())

    def test_event_unicode(self):
        """ Test Event serialize. """
        event = self.new_event()
        self.assertEqual('{"__type": "Event"}',
                         event.serialize())

    def test_event_from_report(self):
        """ Data from report should be in event, except for extra. """
        report = self.new_report()
        report.update(FEED_FIELDS)
        event = message.Event(report, harmonization=HARM)
        del report['extra']
        self.assertDictContainsSubset(event, report)

    def test_event_hash_regex(self):
        """ Test if the regex for event_hash is tested correctly. """
        event = self.new_event()
        with self.assertRaises(exceptions.InvalidValue):
            event.add('event_hash', 'das f78')

    def test_port_regex(self):
        """ Test if the regex for port (integer) is tested correctly. """
        event = self.new_event()
        with self.assertRaises(exceptions.InvalidValue):
            event.add('source.port', 123456)

    def test_malwarename_regex(self):
        """ Test if the regex for malware.name is tested correctly. """
        event = self.new_event()
        event.add('malware.name', 'multiple-malware citadel:report')
        event.change('malware.name', 'yahoo!')
        del event['malware.name']
        with self.assertRaises(exceptions.InvalidValue):
            event.add('malware.name', 'tu234t2\nt$#%$')

    def test_protocol_ascii(self):
        """ Test if ascii for protocol is tested correctly. """
        event = self.new_event()
        with self.assertRaises(exceptions.InvalidValue):
            event.add('protocol.application', 'A\n€80"')

    def test_protocol_length(self):
        """ Test if the length for protocol is tested correctly. """
        event = self.new_event()
        with self.assertRaises(exceptions.InvalidValue):
            event.add('protocol.transport', 'unknown')

    def test_message_from_dict_return_type(self):
        """ Test if from_dict() returns the correct class. """
        event = {'__type': 'Event'}
        event_type = type(message.MessageFactory.from_dict(event,
                                                           harmonization=HARM))
        self.assertTrue(event_type is message.Event,
                        msg='Type is {} instead of Event.'.format(event_type))

    def test_event_init_check(self):
        """ Test if initialization method checks fields. """
        event = {'__type': 'Event', 'source.asn': 'foo'}
        with self.assertRaises(exceptions.InvalidValue):
            message.Event(event, harmonization=HARM)

    def test_event_init_check_tuple(self):
        """ Test if initialization method checks fields from tuple. """
        event = (('__type', 'Event'), ('source.asn', 'foo'))
        with self.assertRaises(exceptions.InvalidValue):
            message.Event(event, harmonization=HARM)

    def test_event_init(self):
        """ Test if initialization method checks fields. """
        event = '{"__type": "Event", "source.asn": "foo"}'
        with self.assertRaises(exceptions.InvalidValue):
            message.MessageFactory.unserialize(event, harmonization=HARM)

    def test_malware_hash_md5(self):
        """ Test if MD5 is checked correctly. """
        event = self.new_event()
        event.add('malware.hash.md5', 'mSwgIswdjlTY0YxV7HBVm0')
        self.assertEqual(event['malware.hash.md5'], 'mSwgIswdjlTY0YxV7HBVm0')
        event.change('malware.hash.md5', '$md5$mSwgIswdjlTY0YxV7HBVm0')
        event.change('malware.hash.md5', '$md5,rounds=500$mSwgIswdjlTY0YxV7HBVm0')
        # TODO: Fix when normalization of hashes is defined
#        with self.assertRaises(exceptions.InvalidValue):
#            event.change('malware.hash.md5', '$md5, $mSwgIswdjlTY0YxV7HBVm0')

    def test_malware_hash_sha1(self):
        """ Test if SHA1 is checked correctly. """
        event = self.new_event()
        event.add('malware.hash.sha1', 'hBNaIXkt4wBI2o5rsi8KejSjNqIq')
        self.assertEqual(event['malware.hash.sha1'], 'hBNaIXkt4wBI2o5rsi8KejSjNqIq')
        event.change('malware.hash.sha1', '$sha1$hBNaIXkt4wBI2o5rsi8KejSjNqIq')
        event.change('malware.hash.sha1', '$sha1$40000$hBNaIXkt4wBI2o5rsi8KejSjNqIq')
        event.change('malware.hash.sha1', '$sha1$40000$jtNX3nZ2$hBNaIXkt4wBI2o5rsi8KejSjNqIq')
        # TODO: Fix when normalization of hashes is defined
#        with self.assertRaises(exceptions.InvalidValue):
#            event.change('malware.hash.sha1', '$sha1$ $jtNX3nZ2$hBNaIXkt4wBI2o5rsi8KejSjNqIq')

    def test_registry(self):
        """ Test source.registry """
        event = self.new_event()
        event.add('source.registry', 'APNIC')
        event.change('source.registry', 'afrinic')
        with self.assertRaises(exceptions.InvalidValue):
            event.change('source.registry', 'afrinic', sanitize=False)
        with self.assertRaises(exceptions.InvalidValue):
            event.change('source.registry', 'afri nic', sanitize=False)

    def test_message_update(self):
        """ Test Message.update """
        event = self.new_event()
        with self.assertRaises(exceptions.InvalidValue):
            event.update({'source.asn': 'AS0'})

    def test_message_extra_construction(self):
        """
        Test if field with name starting with 'extra.' is accepted and saved.
        """
        event = self.new_event()
        event.add('extra.test', 'foobar')
        event.add('extra.test2', 'foobar2')
        self.assertEqual(event.to_dict(hierarchical=True),
                         {'extra': {"test": "foobar", "test2": "foobar2"}}
                         )
        self.assertEqual(event.to_dict(hierarchical=False),
                         {'extra.test': "foobar", "extra.test2": "foobar2"}
                         )

    def test_message_extra_getitem(self):
        """
        Test if extra field is saved and can be get.
        """
        event = self.new_event()
        event.add('extra.test', 'foobar')
        self.assertEqual(event['extra.test'], 'foobar')

    def test_message_extra_get(self):
        """
        Test if extra field can be get with .get().
        """
        event = self.new_event()
        event.add('extra.test', 'foobar')
        self.assertEqual(event.get('extra'), '{"test": "foobar"}')

    def test_message_extra_set_oldstyle_string(self):
        """
        Test if extra accepts a string (backwards-compat) and field can be get.
        """
        event = self.new_event()
        event.add('extra', '{"foo": "bar"}')
        self.assertEqual(event['extra'], '{"foo": "bar"}')
        self.assertEqual(event['extra.foo'], 'bar')

    def test_message_extra_set_oldstyle_dict(self):
        """
        Test if extra accepts a dict and field can be get.
        """
        event = self.new_event()
        event.add('extra', {"foo": "bar"})
        self.assertEqual(event['extra'], '{"foo": "bar"}')
        self.assertEqual(event['extra.foo'], 'bar')

    def test_message_extra_set_oldstyle_dict_overwrite_empty(self):
        """
        Test if extra behaves backwards compatible concerning overwrite and empty items
        """
        event = self.new_event()
        event["extra"] = {"a": {"x": 1}, "b": "foo"}
        self.assertEqual(json.loads(event['extra']),
                         {"a": {"x": 1}, "b": "foo"})
        event.add("extra", {"a": {}}, overwrite=True)
        self.assertEqual(json.loads(event['extra']),
                         {"a": {}})

    def test_message_extra_set_dict_empty(self):
        """
        Test if extra accepts a dict and field can be get.
        """
        event = self.new_event()
        event.add('extra', {"foo": ''})
        self.assertEqual(json.loads(event['extra']),
                         {"foo": ''})

    def test_message_extra_in_backwardcomp(self):
        """
        Test if 'extra' in event works for backwards compatibility.
        """
        event = self.new_event()
        self.assertFalse('extra' in event)
        event.add('extra.foo', 'bar')
        self.assertTrue('extra' in event)

    def test_overwrite_true(self):
        """
        Test if values can be overwritten.
        """
        event = self.new_event()
        event.add('comment', 'foo')
        event.add('comment', 'bar', overwrite=True)
        self.assertEqual(event['comment'], 'bar')

    def test_overwrite_none(self):
        """
        Test if exception is raised when values exist and can't be overwritten.
        """
        event = self.new_event()
        event.add('comment', 'foo')
        with self.assertRaises(exceptions.KeyExists):
            event['comment'] = 'bar'

    def test_overwrite_false(self):
        """
        Test if values are not overwritten.
        """
        event = self.new_event()
        event.add('comment', 'foo')
        event.add('comment', 'bar', overwrite=False)
        self.assertEqual(event['comment'], 'foo')

    def test_to_dict_jsondict_as_string(self):
        """
        Test if to_dict(jsondict_as_string) works correctly.
        """
        event = self.new_event()
        event.add('extra.foo', 'bar')
        self.assertDictEqual(event.to_dict(hierarchical=False, jsondict_as_string=True),
                             {'extra': '{"foo": "bar"}'})

    def test_invalid_harm_key(self):
        """ Test if error is raised when using an invalid key. """
        with self.assertRaises(exceptions.InvalidKey):
            message.Event(harmonization={'event': {'foo..bar': {}}})
        with self.assertRaises(exceptions.InvalidKey):
            message.Event(harmonization={'event': {'foo.bar.': {}}})


class TestReport(unittest.TestCase):
    """
    Test the Report class.
    """
    def test_report_from_event(self):
        event = message.Event(harmonization=HARM)
        event.add('feed.code', 'adasd')
        event.add('source.fqdn', 'example.com')
        report = message.Report(event, harmonization=HARM).to_dict()
        self.assertNotIn('source.fqdn', report)
        self.assertIn('feed.code', report)

    def test_report_from_event_with_raw(self):
        """ raw must not be sanitized (base64 encoded) """
        event = message.Event(harmonization=HARM)
        event.add('raw', 'foobar')
        report = message.Report(event, harmonization=HARM)
        self.assertEqual(report['raw'], 'Zm9vYmFy')


class TestEvent(unittest.TestCase):
    """
    Tests the Event class.
    """
    def test_event_no_default_value(self):
        event = message.Event(harmonization=HARM)
        with self.assertRaises(KeyError):
            event['source.ip']

    def test_event_default_value(self):
        event = message.Event(harmonization=HARM)
        event.set_default_value(None)
        event['source.ip']


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
