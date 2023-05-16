# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import base64
import unittest
import unittest.mock as mock
import warnings

import intelmq.lib.bot as bot
import intelmq.lib.test as test
import intelmq.lib.utils as utils

RAW = """# ignore this
2015/06/04 13:37 +00,example.org,192.0.2.3,reverse.example.net,example description,report@example.org,1

2015/06/04 13:38 +00,example.org,19a2.0.2.3,reverse.example.net,example description,report@example.org,1
2015/06/04 13:38 +00,example.org,19b2.0.2.3,reverse.example.net,example description,report@example.org,1
#ending line"""
RAW_SPLIT = RAW.splitlines()

EXAMPLE_REPORT = {"feed.url": "http://www.example.com/",
                  "time.observation": "2015-08-11T13:03:40+00:00",
                  "raw": utils.base64_encode(RAW),
                  "__type": "Report",
                  "feed.name": "Example"}
EXAMPLE_EVENT = {"feed.url": "http://www.example.com/",
                 "source.ip": "192.0.2.3",
                 "time.source": "2015-06-04T13:37:00+00:00",
                 "source.reverse_dns": "reverse.example.net",
                 "source.fqdn": "example.org",
                 "source.account": "report@example.org",
                 "time.observation": "2015-08-11T13:03:40+00:00",
                 "__type": "Event",
                 "classification.type": "malware-distribution",
                 "event_description.text": "example description",
                 "source.asn": 1,
                 "feed.name": "Example",
                 "raw": utils.base64_encode('\n'.join(RAW_SPLIT[:2]))}

EXPECTED_DUMP = [EXAMPLE_REPORT.copy(), EXAMPLE_REPORT.copy()]
del EXPECTED_DUMP[0]['__type'], EXPECTED_DUMP[1]['__type']
EXPECTED_DUMP[0]['raw'] = base64.b64encode('\n'.join((RAW_SPLIT[0], RAW_SPLIT[3], RAW_SPLIT[5])).encode()).decode()
EXPECTED_DUMP[1]['raw'] = base64.b64encode('\n'.join((RAW_SPLIT[0], RAW_SPLIT[4], RAW_SPLIT[5])).encode()).decode()
EXAMPLE_EMPTY_REPORT = {"feed.url": "http://www.example.com/",
                        "__type": "Report",
                        "feed.name": "Example"}

RAW = """
# ignore this
source.ip,foobar
192.0.2.3,bllaa
#ending line
"""

EXAMPLE_REPO_1 = {"feed.url": "http://www.example.com/",
                  "time.observation": "2015-08-11T13:03:40+00:00",
                  "raw": utils.base64_encode(RAW),
                  "__type": "Report",
                  "feed.name": "Example"}
EXAMPLE_EVE_1 = {"feed.url": "http://www.example.com/",
                 "source.ip": "192.0.2.3",
                 "__type": "Event",
                 "classification.type": "malware-distribution",
                 "feed.name": "Example",
                 'raw': 'c291cmNlLmlwLGZvb2JhcgoxOTIuMC4yLjMsYmxsYWE='
                 }

EXAMPLE_SHORT = EXAMPLE_REPORT.copy()
EXAMPLE_SHORT['raw'] = utils.base64_encode('\n'.join(RAW_SPLIT[:2] + [RAW_SPLIT[1]]))


class DummyParserBot(bot.ParserBot):
    """
    A dummy bot only for testing purpose.
    """

    def parse_line(self, line, report):
        if getattr(self, 'raise_warning', False):
            warnings.warn('This is a warning test.')
        if line.startswith('#'):
            self.logger.info('Lorem ipsum dolor sit amet.')
            self.tempdata.append(line)
        else:
            event = self.new_event(report)
            self.logger.debug('test!')
            line = line.split(',')
            event['time.source'] = line[0]
            event['source.fqdn'] = line[1]
            event['source.ip'] = line[2]
            event['source.reverse_dns'] = line[3]
            event['event_description.text'] = line[4]
            event['source.account'] = line[5]
            event['source.asn'] = line[6]
            event['classification.type'] = 'malware-distribution'
            event['raw'] = '\n'.join(self.tempdata + [','.join(line)])
            yield event

    def recover_line(self, line):
        return '\n'.join([self.tempdata[0], line, self.tempdata[1]])


class DummyCSVDictParserBot(bot.ParserBot):
    """
    A csv parser bot only for testing purpose.
    """
    csv_fieldnames = ['source.ip', 'foobar']
    _ignore_lines_starting = ['#']

    def parse_line(self, line, report):
        event = self.new_event(report)
        event['source.ip'] = line['source.ip']
        event['classification.type'] = 'malware-distribution'
        event['raw'] = self.recover_line(line)
        yield event

    parse = bot.ParserBot.parse_csv_dict
    recover_line = bot.ParserBot.recover_line_csv_dict


class TestDummyParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a DummyParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DummyParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'error_dump_message': True}
        cls.call_counter = 0

    def dump_message(self, error_traceback, message=None):
        self.assertDictEqual(EXPECTED_DUMP[self.call_counter], message)
        self.call_counter += 1

    def run_bot(self, *args, **kwargs):
        with mock.patch.object(bot.Bot, "_dump_message",
                               self.dump_message):
            super().run_bot(*args, **kwargs)

    def test_event(self):
        """ Test DummyParserBot """
        self.run_bot(allowed_error_count=2)
        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def test_default_fields_parameter(self):
        self.input_message = EXAMPLE_REPORT
        output_message = EXAMPLE_EVENT.copy()
        output_message["protocol.application"] = "http"
        self.run_bot(allowed_error_count=2, parameters={"default_fields": {"protocol.application": "http"}})
        self.assertMessageEqual(0, output_message)

    def test_bad_default_fields_parameter(self):
        self.input_message = EXAMPLE_SHORT
        self.run_bot(allowed_error_count=4, allowed_warning_count=1,
                     parameters={"error_dump_message": False, "default_fields": {"invalid_key": 100000}})
        self.assertAnyLoglineEqual(message="Invalid key 'invalid_key' in default_fields parameter.", levelname="ERROR")

    def test_bad_default_fields_parameter_2(self):
        self.input_message = EXAMPLE_SHORT
        self.run_bot(allowed_error_count=4, allowed_warning_count=1,
                     parameters={"error_dump_message": False, "default_fields": {"source.port": 100000}})
        self.assertAnyLoglineEqual(message="Invalid value of key 'source.port' in default_fields parameter.",
                                   levelname="ERROR")

    def test_missing_raw(self):
        """ Test DummyParserBot with missing raw. """
        self.input_message = EXAMPLE_EMPTY_REPORT
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertAnyLoglineEqual(message='Report without raw field received. Possible '
                                           'bug or misconfiguration in previous bots.',
                                   levelname='WARNING')

    def test_processed_messages_count(self):
        self.input_message = EXAMPLE_SHORT
        self.run_bot(parameters={'log_processed_messages_count': 1})
        self.assertAnyLoglineEqual(message='Processed 1 messages since last logging.',
                                   levelname='INFO')

    def test_processed_messages_seconds(self):
        self.input_message = EXAMPLE_SHORT
        self.run_bot(parameters={'log_processed_messages_count': 10,
                                 'log_processed_messages_seconds': 0})
        self.assertAnyLoglineEqual(message='Processed 2 messages since last logging.',
                                   levelname='INFO')

    def test_processed_messages_shutdown(self):
        self.input_message = EXAMPLE_SHORT
        self.run_bot()
        self.assertAnyLoglineEqual(message='Processed 2 messages since last logging.',
                                   levelname='INFO')


class TestDummyCSVDictParserBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = DummyCSVDictParserBot
        cls.default_input_message = EXAMPLE_REPO_1

    def test_event(self):
        """ Test DummyCSVDictParserBot. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVE_1)


class DummyCSVParserBot(DummyCSVDictParserBot):
    def parse_line(self, line, report):
        event = self.new_event(report)
        event['source.ip'] = line[0]
        event['classification.type'] = 'malware-distribution'
        event['raw'] = self.recover_line(line)
        yield event

    parse = bot.ParserBot.parse_csv
    recover_line = bot.ParserBot.recover_line_csv


class TestDummyCSVParserBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = DummyCSVParserBot
        # Dummy bot doesn't handle the header line
        raw_split = RAW.splitlines()
        report = {**EXAMPLE_REPO_1,
                  "raw": utils.base64_encode('\n'.join(raw_split[:2] + raw_split[3:]))}
        cls.default_input_message = report

    def test_event(self):
        """ Test DummyCSVParserBot. """
        self.run_bot()
        self.assertMessageEqual(0, {**EXAMPLE_EVE_1, "raw": "MTkyLjAuMi4zLGJsbGFhCg=="})


EXAMPLE_JSON_STREAM_REPORT = {'__type': 'Report',
                              'raw': utils.base64_encode('''{"a": 1}
{"a": 2}''')}
EXAMPLE_JSON_STREAM_EVENTS = [{'__type': 'Event',
                               'raw': utils.base64_encode('{"a": 1}'),
                               'event_description.text': '1',
                               'classification.type': 'other',
                               },
                              {'__type': 'Event',
                               'raw': utils.base64_encode('{"a": 2}'),
                               'event_description.text': '2',
                               'classification.type': 'other',
                               },
                              ]
JSON_STREAM_BOGUS_REPORT = {'__type': 'Report',
                            'raw': utils.base64_encode('''{"a": 1, "ip": "10.0.0.a"}
{"a": 2, "ip": "10.0.0.b"}''')}
JSON_STREAM_BOGUS_DUMP = [
    {'raw': utils.base64_encode('{"a": 1, "ip": "10.0.0.a"}')},
    {'raw': utils.base64_encode('{"a": 2, "ip": "10.0.0.b"}')}
]


class DummyJSONStreamParserBot(bot.ParserBot):
    parse = bot.ParserBot.parse_json_stream
    recover_line = bot.ParserBot.recover_line_json_stream

    def parse_line(self, line, report):
        event = self.new_event(report)
        event['event_description.text'] = line['a']
        event['classification.type'] = 'other'
        event['raw'] = self.recover_line()
        if 'ip' in line:
            event['source.ip'] = line['ip']
        yield event


class TestJSONStreamParserBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = DummyJSONStreamParserBot
        cls.default_input_message = EXAMPLE_JSON_STREAM_REPORT
        cls.call_counter = 0

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_JSON_STREAM_EVENTS[0])
        self.assertMessageEqual(1, EXAMPLE_JSON_STREAM_EVENTS[1])

    def dump_message(self, error_traceback, message=None):
        self.assertDictEqual(JSON_STREAM_BOGUS_DUMP[self.call_counter], message)
        self.call_counter += 1

    def run_bot(self, *args, **kwargs):
        with mock.patch.object(bot.Bot, "_dump_message",
                               self.dump_message):
            super().run_bot(*args, **kwargs)

    def test_dump(self):
        self.input_message = JSON_STREAM_BOGUS_REPORT
        self.run_bot(allowed_error_count=2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
