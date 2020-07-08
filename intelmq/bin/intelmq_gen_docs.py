#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os.path
import textwrap

import yaml

import intelmq.lib.harmonization


HEADER = """
Harmonization field names
=========================

|Section|Name|Type|Description|
|:------|:---|:---|:----------|
"""
HEADER_1 = """

Harmonization types
-------------------

"""
TYPE_SECTION = """### {}
{}

"""
BASEDIR = os.path.join(os.path.dirname(__file__), '../../')


def harm_docs():
    output = HEADER

    with open(os.path.join(BASEDIR, 'intelmq/etc/harmonization.conf')) as fhandle:
        HARM = json.load(fhandle)['event']

    for key, value in sorted(HARM.items()):
        section = ' '.join([sec.title() for sec in key.split('.')[:-1]])
        output += '|{}|{}|[{}](#{})|{}|\n'.format(' ' if not section else section,  # needed for GitHub
                                                  key, value['type'],
                                                  value['type'].lower(),
                                                  value['description'])

    output += HEADER_1

    for value in sorted(dir(intelmq.lib.harmonization)):
        if value == 'GenericType' or value.startswith('__'):
            continue
        obj = getattr(intelmq.lib.harmonization, value)
        try:
            if issubclass(obj, intelmq.lib.harmonization.GenericType):
                doc = getattr(obj, '__doc__', '')
                if doc is None:
                    doc = ''
                else:
                    doc = textwrap.dedent(doc)
                output += TYPE_SECTION.format(value, doc)
        except TypeError:
            pass

    return output


def info(key, value=""):
    return ("* **%s:** %s\n" % (key.title(), value)).strip() + '\n'


def feeds_docs():
    with open(os.path.join(BASEDIR, 'intelmq/etc/feeds.yaml')) as fhandle:
        config = yaml.safe_load(fhandle.read())

    toc = ""
    for provider in sorted(config['providers'].keys()):
        provider_link = provider.replace('.', '')
        provider_link = provider_link.replace(' ', '-')
        toc += "- [%s](#%s)\n" % (provider, provider_link.lower())

    output = """# Available Feeds

The available feeds are grouped by the provider of the feeds.
For each feed the collector and parser that can be used is documented as well as any feed-specific parameters.
To add feeds to this file add them to `intelmq/etc/feeds.yaml` and then run
`intelmq/bin/intelmq_gen_feeds_docs.py` to generate the new content of this file.

<!-- TOC depthFrom:2 depthTo:2 withLinks:1 updateOnSave:1 orderedList:0 -->

%s

<!-- /TOC -->\n

""" % toc

    for provider, feeds in sorted(config['providers'].items(), key=lambda x: x[0]):

        output += "# %s\n\n" % provider

        for feed, feed_info in sorted(feeds.items(), key=lambda x: x[0]):

            output += "## %s\n\n" % feed

            if feed_info['public']:
                output += info("public", "yes" if feed_info['public'] else "no")
            else:
                output += info("public", "unknown")

            output += info("revision", feed_info['revision'])

            if feed_info['documentation'] is not None:
                output += info("documentation", feed_info['documentation'])

            output += info("description", feed_info['description'])

            if feed_info['additional_information'] is not None:
                output += info("additional information", feed_info['additional_information'])

            output += '\n'

            for bot, bot_info in sorted(feed_info['bots'].items(), key=lambda x: x[0]):

                output += "### %s\n\n" % bot.title()

                output += info("Module", bot_info['module'])
                output += info("Configuration Parameters")

                if bot_info.get('parameters'):
                    for key, value in sorted(bot_info['parameters'].items(), key=lambda x: x[0]):

                        if value == "__FEED__":
                            value = feed

                        if value == "__PROVIDER__":
                            value = provider

                        # format non-empty lists with double-quotes
                        # single quotes are not conform JSON and not correctly detected/transformed by the manager
                        if isinstance(value, (list, tuple)) and value:
                            value = '["%s"]' % '", "'.join(value)

                        output += "*  * `%s`: `%s`\n" % (key, value)

                output += '\n'

            output += '\n'

    return output


if __name__ == '__main__':  # pragma: no cover
    with open(os.path.join(BASEDIR, 'docs/Harmonization-fields.md'), 'w') as handle:
        handle.write(harm_docs())
    with open(os.path.join(BASEDIR, 'docs/Feeds.md'), 'w') as handle:
        handle.write(feeds_docs())
