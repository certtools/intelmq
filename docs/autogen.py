# -*- coding: utf-8 -*-

# This script generates the files
# `guides/Harmonization-fields.md`
# and `guides/Feeds.md`

import codecs
import json
import os.path
import textwrap

import yaml

import intelmq.lib.harmonization


HEADER = """#########################
Harmonization field names
#########################

=========================== =================================== ========================= ===========
Section                     Name                                Type                      Description
=========================== =================================== ========================= ===========
"""
HEADER_1 = """
=========================== =================================== ========================= ===========

Harmonization types
-------------------

"""
BASEDIR = os.path.join(os.path.dirname(__file__), '../')


def harm_docs():
    output = HEADER

    with codecs.open(os.path.join(BASEDIR, 'intelmq/etc/harmonization.conf'), encoding='utf-8') as fhandle:
        HARM = json.load(fhandle)['event']

    for key, value in sorted(HARM.items()):
        section = ' '.join([sec.title() for sec in key.split('.')[:-1]])
        output += '{:27} {:35} {:25} {}\n'.format('|' if not section else section,  # needed for GitHub
                                                  key,
                                                  ':ref:`'+value['type'].lower()+'`',
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
                output += ".. _{}:\n\n{}\n{}\n{}\n\n".format(value.lower(),value,'-'*len(value),doc)
        except TypeError:
            pass

    return output


def info(key, value=""):
    return ("* **%s:** %s\n" % (key.title(), value)).strip() + '\n'


def feeds_docs():
    with codecs.open(os.path.join(BASEDIR, 'intelmq/etc/feeds.yaml'), encoding='utf-8') as fhandle:
        config = yaml.safe_load(fhandle.read())

    output = """Feeds
======

The available feeds are grouped by the provider of the feeds.
For each feed the collector and parser that can be used is documented as well as any feed-specific parameters.
To add feeds to this file add them to `intelmq/etc/feeds.yaml` and then rebuild the documentation.

.. contents ::

"""

    for provider, feeds in sorted(config['providers'].items(), key=lambda x: x[0]):

        output += f"{provider}\n"
        output += "-"*len(provider) + "\n"

        for feed, feed_info in sorted(feeds.items(), key=lambda x: x[0]):

            output += f"{feed}\n"
            output += "^"*len(feed) + "\n"

            output += info("public", "yes") if feed_info.get('public') else info("public", "no")

            output += info("revision", feed_info['revision'])

            if feed_info.get('documentation') is not None:
                output += info("documentation", feed_info['documentation'])

            output += info("description", feed_info['description'])

            if feed_info.get('additional_information') is not None:
                output += info("additional information", feed_info['additional_information'])

            output += '\n'

            for bot, bot_info in sorted(feed_info['bots'].items(), key=lambda x: x[0]):

                output += "**%s**\n\n" % bot.title()

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

                        output += "   * `%s`: `%s`\n" % (key, value)

                output += '\n'

            output += '\n'

    return output


if __name__ == '__main__':  # pragma: no cover
    with codecs.open('dev/harmonization-fields.rst', 'w', encoding='utf-8') as handle:
        handle.write(harm_docs())
    with codecs.open('user/feeds.rst', 'w', encoding='utf-8') as handle:
        handle.write(feeds_docs())
