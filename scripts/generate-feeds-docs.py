#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2020 Sebastian Wagner, 2023 Filip Pokorný
# SPDX-License-Identifier: AGPL-3.0-or-later

# This script generates the "feeds.md" documentation page.

import codecs
import json
import os.path

from ruamel.yaml import YAML

BASEDIR = os.path.join(os.path.dirname(__file__), '../')
yaml = YAML(typ="safe", pure=True)

HEADER = """\
<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
   
   This document is automatically generated. To add feeds here you need to edit `intelmq/etc/feeds.yaml`
   file and rebuild the documentation.
-->

# Feeds

The available feeds are grouped by the provider of the feeds.
For each feed the collector and parser that can be used is documented as well as any feed-specific parameters.
To add feeds to this file add them to `intelmq/etc/feeds.yaml` and then rebuild the documentation.

"""


def info(key, value=""):
    return f"**{key.title()}:** {str(value).strip()}\n\n"


def main():
    with codecs.open(os.path.join(BASEDIR, 'intelmq/etc/feeds.yaml'), encoding='utf-8') as fhandle:
        config = yaml.load(fhandle.read())

    output = HEADER

    for provider, feeds in sorted(config['providers'].items(), key=lambda x: x[0]):

        output += f"## {provider}\n\n"

        for feed_name, feed_info in sorted(feeds.items(), key=lambda x: x[0]):

            output += f"### {feed_name}\n\n"

            output += feed_info['description']
            output += '\n\n'

            output += info("public", "yes") if feed_info.get('public') else info("public", "no")
            output += info("revision", feed_info['revision'])

            if feed_info.get('documentation') is not None:
                output += info("documentation", f"<{feed_info['documentation']}>")

            if feed_info.get('additional_information') is not None:
                output += info("additional information", feed_info['additional_information'])

            output += '\n'

            for bot, bot_info in sorted(feed_info['bots'].items(), key=lambda x: x[0]):

                output += f"**{bot.title()} configuration**\n\n"

                output += "```yaml\n"
                output += f"module: {bot_info['module']}\n"

                if bot_info.get('parameters'):
                    output += "parameters:\n"
                    for key, value in sorted(bot_info['parameters'].items(), key=lambda x: x[0]):

                        if value == "__FEED__":
                            value = feed_name

                        if value == "__PROVIDER__":
                            value = provider

                        # format non-empty lists with double-quotes
                        # single quotes are not conform JSON and not correctly detected/transformed by the manager
                        if isinstance(value, (list, tuple)) and value:
                            value = json.dumps(value)

                        output += f"  {key}: {value}\n"

                output += "```\n\n"

            output += "---\n\n\n"

    return output


if __name__ == '__main__':
    with codecs.open(os.path.join(BASEDIR, 'docs/user/feeds.md'), 'w', encoding='utf-8') as f:
        f.write(main())
