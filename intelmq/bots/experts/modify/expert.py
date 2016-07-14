# -*- coding: utf-8 -*-
"""
Modify Expert bot let's you manipulate all fields with a config file.
"""
import re
import sys

from intelmq.lib.bot import Bot
from intelmq.lib.utils import load_configuration


class ModifyExpertBot(Bot):

    def init(self):
        self.config = load_configuration(self.parameters.configuration_path)

    def matches(self, identifiers, event, *rules):
        condition = {}
        for rule in rules:
            condition.update(rule)

        for name, rule in condition.items():
            # empty string means non-existant field
            if rule == '':
                if name in event:
                    return False
                else:
                    continue
            if name not in event:
                return False
            if not isinstance(rule, type(event[name])):
                if isinstance(rule, str) and isinstance(event[name], (int, float)):
                    if not re.search(rule, str(event[name])):
                        return False
                else:
                    self.logger.warn("Type of rule ({!r}) and data ({!r}) do not "
                                     "match in {!s}, {}!".format(type(rule), type(event[name]), identifiers, name))
            elif not isinstance(event[name], str):  # int, float, etc
                if event[name] != rule:
                    return False
            else:
                if not re.search(rule, event[name]):
                    return False

        return True

    def apply_action(self, event, action):
        for name, value in action.items():
            event.add(name, value.format(msg=event), force=True)

    def process(self):
        event = self.receive_message()

        for section_id, section in self.config.items():
            default_cond = section.get('__default', [{}, {}])[0]
            default_action = section.get('__default', [{}, {}])[1]
            if not self.matches((section_id, '__default'),
                                event, default_cond):
                continue

            applied = False
            for rule_id, (rule_cond, rule_action) in section.items():
                if rule_id == '__default':
                    continue
                if self.matches((section_id, rule_id),
                                event, default_cond, rule_cond):
                    self.logger.debug('Apply rule {}/{}.'.format(section_id,
                                                                 rule_id))
                    self.apply_action(event, rule_action)
                    applied = True
                    continue

            if not applied and default_action != {}:
                self.logger.debug('Apply {}/__default.'.format(section_id))
                self.apply_action(event, default_action)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ModifyExpertBot(sys.argv[1])
    bot.start()
