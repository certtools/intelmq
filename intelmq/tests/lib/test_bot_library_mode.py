# SPDX-FileCopyrightText: 2023 by Bundesamt für Sicherheit in der Informationstechnik (BSI)
#
# SPDX-License-Identifier: AGPL-3.0-or-later
# -*- coding: utf-8 -*-
"""
Copyright (c) 2023 by Bundesamt für Sicherheit in der Informationstechnik (BSI)

Software engineering by BSI & Intevation GmbH

This file tests IntelMQ bots in library mode (IEP007)
"""
import json
import unittest
from os.path import dirname, join
from pytest import raises

import intelmq.tests.bots.experts.domain_suffix.test_expert as domain_suffix_expert_test
from intelmq.bots.experts.domain_suffix.expert import DomainSuffixExpertBot
from intelmq.bots.experts.taxonomy.expert import TaxonomyExpertBot
from intelmq.bots.experts.url.expert import URLExpertBot
from intelmq.lib.bot import BotLibSettings, Dict39, ExpertBot
from intelmq.lib.message import Message, MessageFactory
from intelmq.tests.lib import test_parser_bot

EXAMPLE_DATA_URL = Dict39({'source.url': 'http://example.com/'})
EXAMPLE_DATA_URL_OUT = EXAMPLE_DATA_URL | {'source.fqdn': 'example.com',
                                           'source.port': 80,
                                           'source.urlpath': '/',
                                           'protocol.application': 'http',
                                           'protocol.transport': 'tcp'}
EXAMPLE_IP_INPUT = {"source.ip": "192.0.43.7",  # icann.org.
                    "destination.ip": "192.0.43.8",  # iana.org.
                    "time.observation": "2015-01-01T00:00:00+00:00",
                    }


class BrokenInitExpertBot(ExpertBot):
    def init(self):
        raise ValueError('This initialization intionally raises an error!')


class RaisesOnFirstRunExpertBot(ExpertBot):
    counter = 0

    def init(self):
        self.counter = 0

    def process(self):
        event = self.receive_message()
        self.counter += 1
        if self.counter == 1:
            raise ValueError('This initialization intionally raises an error!')
        self.send_message(event)
        self.acknowledge_message()


def assertMessageEqual(actual, expected):
    """
    Compare two messages as dicts.
    """
    if isinstance(actual, Message):
        actual = actual.to_dict(with_type=True)
    else:
        actual = actual.copy()

    if isinstance(expected, Message):
        expected = expected.to_dict(with_type=True)
    else:
        expected = expected.copy()

    if 'time.observation' in actual:
        del actual['time.observation']
    if 'time.observation' in expected:
        del expected['time.observation']
    if 'output' in actual:
        actual['output'] = json.loads(actual['output'])
    if 'output' in expected:
        expected['output'] = json.loads(expected['output'])

    assert actual == expected


def test_dummy_parser_bot():
    bot = test_parser_bot.DummyParserBot('dummy-bot', settings=BotLibSettings)
    sent_messages = bot.process_message(test_parser_bot.EXAMPLE_REPORT.copy())
    assertMessageEqual(sent_messages['output'][0], test_parser_bot.EXAMPLE_EVENT)
    assertMessageEqual(sent_messages['error'][0], MessageFactory.from_dict(test_parser_bot.EXPECTED_DUMP[0].copy(), default_type='Report'))
    assertMessageEqual(sent_messages['error'][1], MessageFactory.from_dict(test_parser_bot.EXPECTED_DUMP[1].copy(), default_type='Report'))


def test_domain_suffix():
    domain_suffix = DomainSuffixExpertBot('domain-suffix',
                                          settings=BotLibSettings | {'field': 'fqdn',
                                                                     'suffix_file': join(dirname(domain_suffix_expert_test.__file__), 'public_suffix_list.dat')})
    queues = domain_suffix.process_message({'source.fqdn': 'www.example.com'})
    assert queues['output'][0]['source.domain_suffix'] == 'example.com'


def test_url_expert():
    url_expert = URLExpertBot('url', settings=BotLibSettings)
    queues = url_expert.process_message(EXAMPLE_DATA_URL.copy())
    del url_expert
    assert queues['output'] == [EXAMPLE_DATA_URL_OUT]


def test_url_and_taxonomy():
    url_expert = URLExpertBot('url', settings=BotLibSettings)
    queues_url = url_expert.process_message(EXAMPLE_DATA_URL.copy())
    del url_expert
    message = queues_url['output'][0]
    taxonomy_expert = TaxonomyExpertBot('taxonomy', settings=BotLibSettings)
    queues = taxonomy_expert.process_message(message)
    assert queues['output'] == [Dict39(EXAMPLE_DATA_URL_OUT) | {'classification.taxonomy': 'other', 'classification.type': 'undetermined'}]


def test_bot_exception_init():
    """
    When a bot raises an exception during Bot initialization
    """
    with raises(ValueError):
        BrokenInitExpertBot('broken', settings=BotLibSettings)


def test_bot_multi_message():
    url_expert = URLExpertBot('url', settings=BotLibSettings)
    queues = url_expert.process_message(EXAMPLE_DATA_URL.copy(), EXAMPLE_DATA_URL.copy())
    del url_expert
    assert queues['output'] == [EXAMPLE_DATA_URL_OUT] * 2


def test_bot_raises_and_second_message():
    """
    The first message raises an error and the second message
    This test is based on an issue where the exception-raising message was not cleared from the internal message store of the Bot/Pipeline instance and thus re-used on the second run
    """
    raises_on_first_run = RaisesOnFirstRunExpertBot('raises', settings=BotLibSettings)
    with raises(ValueError):
        raises_on_first_run.process_message(EXAMPLE_DATA_URL)
    queues = raises_on_first_run.process_message(EXAMPLE_IP_INPUT)
    assert len(queues['output']) == 1
    assertMessageEqual(queues['output'][0], EXAMPLE_IP_INPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
