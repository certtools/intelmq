# SPDX-FileCopyrightText: 2023 by Bundesamt für Sicherheit in der Informationstechnik (BSI)
#
# SPDX-License-Identifier: AGPL-3.0-or-later
# -*- coding: utf-8 -*-
"""
Copyright (c) 2023 by Bundesamt für Sicherheit in der Informationstechnik (BSI)

Software engineering by BSI & Intevation GmbH

This tests IntelMQ bots in library mode (IEP007)
"""
import unittest

from intelmq.lib.bot import Dict39, BotLibSettings

from intelmq.bots.experts.url.expert import URLExpertBot
from intelmq.bots.experts.taxonomy.expert import TaxonomyExpertBot
from intelmq.bots.experts.jinja.expert import JinjaExpertBot

EXAMPLE_DATA_URL = Dict39({'source.url': 'http://example.com/'})
BOT_CONFIG_JINJA_FAILING = Dict39({
    'fields': {
        'feed.url': "{{ error! msg['source.fqdn'] | upper }}"
    }
})


def test_url_expert():
    url_expert = URLExpertBot('url', settings=BotLibSettings)
    queues = url_expert.process_message(EXAMPLE_DATA_URL.copy())
    del url_expert
    print(0, queues)
    assert queues['output'] == [EXAMPLE_DATA_URL | {'source.fqdn': 'example.com',
                                                    'source.port': 80,
                                                    'source.urlpath': '/',
                                                    'protocol.application': 'http',
                                                    'protocol.transport': 'tcp'}]


def test_url_and_taxonomy():
    url_expert = URLExpertBot('url', settings=BotLibSettings)
    queues_url = url_expert.process_message(EXAMPLE_DATA_URL.copy())
    del url_expert
    message = queues_url['output'][0]
    taxonomy_expert = TaxonomyExpertBot('taxonomy', settings=BotLibSettings)
    queues = taxonomy_expert.process_message(message)
    assert queues['output'] == [EXAMPLE_DATA_URL | {'source.fqdn': 'example.com',
                                                    'source.port': 80,
                                                    'source.urlpath': '/',
                                                    'protocol.application': 'http', 'protocol.transport': 'tcp',
                                                    'classification.taxonomy': 'other', 'classification.type': 'undetermined'}]


def test_bot_exception_import():
    """
    When a bot raises an exception during Bot initialization
    """
    try:
        JinjaExpertBot('jinja', settings=BotLibSettings | BOT_CONFIG_JINJA_FAILING)
    except:
        pass


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
