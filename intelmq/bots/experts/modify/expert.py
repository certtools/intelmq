# -*- coding: utf-8 -*-
"""
Modify Expert bot let's you manipulate all fields with a config file.


"""
from __future__ import unicode_literals
import re

from intelmq import MODIFY_CONF_FILE
from intelmq.lib.bot import Bot
import intelmq.lib.utils


def matches(event, *rules):
    condition = {}
    for rule in rules:
        condition.update(rule)

    for name, rule in condition.items():
        if name not in event:
            return False
        if not re.search(rule, event[name]):
            return False

    return True


def apply_action(event, action):
    for name, value in action.items():
        event.add(name, value.format(msg=event), sanitize=True, force=True)


class ModifyExpertBot(Bot):

    def init(self):
        self.config = intelmq.lib.utils.load_configuration(MODIFY_CONF_FILE)

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for section_id, section in self.config.items():
            default_cond = section['__default'][0]
            default_action = section['__default'][1]
            if not matches(event, default_cond):
                continue

            applied = False
            for rule_id, (rule_cond, rule_action) in section.items():
                if rule_id == '__default':
                    continue
                if matches(event, default_cond, rule_cond):
                    self.logger.debug('Apply rule {}/{}.'.format(section_id,
                                                                 rule_id))
                    apply_action(event, rule_action)
                    applied = True
                    continue

            if not applied:
                self.logger.debug('Apply default rule {}/__default.'
                                  ''.format(section_id))
                apply_action(event, default_action)

        self.send_message(event)
        self.acknowledge_message()
