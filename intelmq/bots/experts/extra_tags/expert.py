# SPDX-FileCopyrightText: 2024 Manuel Subredu
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
from intelmq.lib.bot import ExpertBot


class ExtraTagsExpertBot(ExpertBot):
    """Add custom extra tags as needed"""
    overwrite: bool = False
    tags: dict = None

    def init(self):
        self.logger.debug("Found {} tags in config section.".format(len(self.tags.keys())))

    def process(self):
        event = self.receive_message()

        existing_tags = event.get('extra.tags')
        if existing_tags is None:
            event.add('extra.tags', self.tags)
        else:
            if self.overwrite is False:
                for tag in self.tags.keys():
                    print(tag in existing_tags)
                    if tag in existing_tags:
                        self.logger.info("Tag {} already exists. Skipping.".format(tag))
                    else:
                        existing_tags.update({tag: self.tags[tag]})
            else:
                existing_tags.update(self.tags)

            event.update({'extra.tags': existing_tags})
            self.logger.debug('extra.tags is now: {}.'.format(existing_tags))

        self.send_message(event)
        self.acknowledge_message()

BOT = ExtraTagsExpertBot
