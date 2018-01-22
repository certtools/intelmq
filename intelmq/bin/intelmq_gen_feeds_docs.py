#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys

try:
    import yaml
except:
    print("[-] Please install yaml using the following command: 'pip install pyyaml'.", file=sys.stderr)
    sys.exit(-1)


def print_header():
    text = """# Available Feeds\n"""
    text += """\nThe available feeds are grouped by the provider of the feeds. """
    text += """For each feed the collector and parser that can be used is documented as well as any feed-specific parameters.\n"""
    print(text)


def print_index(providers):
    text = """<!-- TOC depthFrom:2 depthTo:2 withLinks:1 updateOnSave:1 orderedList:0 -->\n"""
    text += "\n%s\n" % get_providers_index(providers)
    text += "<!-- /TOC -->\n"
    print(text)


def get_providers_index(providers):
    text = ""
    for provider in sorted(providers):
        provider_link = provider.replace('.', '')
        provider_link = provider_link.replace(' ', '-')
        text += "- [%s](#%s)\n" % (provider, provider_link.lower())
    return text


def print_h1(value):
    print("# %s" % value)
    print()


def print_h2(value, title=True):
    if title:
        print("## %s" % value.title())
    else:
        print("## %s" % value)
    print()


def print_h3(value):
    print("### %s" % value.title())
    print()


def print_info(key, value=""):
    print(("* **%s:** %s" % (key.title(), value)).strip())


def print_config_param(key, value):
    print("*  * `%s`: `%s`" % (key, value))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='IntelMQ Feeds Documentation Generator tool',
    )

    parser.add_argument('--feeds-file',
                        action="store",
                        dest="feeds_file",
                        metavar="<filepath>",
                        required=True,
                        help='config file (JSON or YAML)')

    arguments = parser.parse_args()

    with open(arguments.feeds_file) as fp:
        config = yaml.load(fp.read())

    print_header()
    print_index(config['providers'].keys())

    for provider, feeds in sorted(config['providers'].items(), key=lambda x: x[0]):

        print_h1(provider)

        for feed, feed_info in sorted(feeds.items(), key=lambda x: x[0]):

            print_h2(feed, title=False)

            if feed_info['status']:
                print_info("status", "on")
            else:
                print_info("status", "off")

            print_info("revision", feed_info['revision'])

            if feed_info['documentation'] is not None:
                print_info("documentation", feed_info['documentation'])

            print_info("description", feed_info['description'])

            if feed_info['additional_information'] is not None:
                print_info("additional information", feed_info['additional_information'])

            print()

            for bot, bot_info in sorted(feed_info['bots'].items(), key=lambda x: x[0]):

                print_h3(bot)

                print_info("Module", bot_info['module'])
                print_info("Configuration Parameters")

                if bot_info['parameters']:
                    for key, value in sorted(bot_info['parameters'].items(), key=lambda x: x[0]):
                        print_config_param(key, value)

                print()

            print()
