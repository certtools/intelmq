# -*- coding: utf-8 -*-
"""
Modify Expert bot let's you manipulate all fields with a config file.
"""
import re

from intelmq.lib.bot import Bot
from intelmq.lib.utils import load_configuration


class MatchGroupMapping:

    """Wrapper for a regexp match object with a dict-like interface.
    With this, we can access the match groups from within a format
    replacement field.
    """

    def __init__(self, match):
        self.match = match

    def __getitem__(self, key):
        return self.match.group(key)


class ModifyExpertBot(Bot):

    def init(self):
        self.config = load_configuration(self.parameters.configuration_path)

    def matches(self, identifiers, event, *rules):
        condition = {}
        for rule in rules:
            condition.update(rule)

        matches = {}

        for name, rule in condition.items():
            # empty string means non-existant field
            if rule == '':
                if name in event:
                    return None
                else:
                    continue
            if name not in event:
                return None
            if not isinstance(rule, type(event[name])):
                if isinstance(rule, str) and isinstance(event[name], (int, float)):
                    match = re.search(rule, str(event[name]))
                    if match is None:
                        return None
                    else:
                        matches[name] = match
                else:
                    self.logger.warn("Type of rule ({!r}) and data ({!r}) do not "
                                     "match in {!s}, {}!".format(type(rule), type(event[name]), identifiers, name))
            elif not isinstance(event[name], str):  # int, float, etc
                if event[name] != rule:
                    return None
            else:
                match = re.search(rule, event[name])
                if match is None:
                    return None
                else:
                    matches[name] = match

        return matches

    def apply_action(self, event, action, matches):
        for name, value in action.items():
            event.add(name, value.format(msg=event,
                                         matches={k: MatchGroupMapping(v)
                                                  for (k, v) in matches.items()}),
                      overwrite=True)

    def process(self):
        event = self.receive_message()

        for section_id, section in self.config.items():
            default_cond = section.get('__default', [{}, {}])[0]
            default_action = section.get('__default', [{}, {}])[1]
            default_matches = self.matches((section_id, '__default'),
                                           event, default_cond)
            if default_matches is None:
                continue

            applied = False
            for rule_id, (rule_cond, rule_action) in section.items():
                if rule_id == '__default':
                    continue
                matches = self.matches((section_id, rule_id),
                                       event, default_cond, rule_cond)
                if matches is not None:
                    self.logger.debug('Apply rule {}/{}.'.format(section_id,
                                                                 rule_id))
                    self.apply_action(event, rule_action, matches)
                    applied = True
                    continue

            if not applied and default_action != {}:
                self.logger.debug('Apply {}/__default.'.format(section_id))
                self.apply_action(event, default_action, default_matches)

        self.send_message(event)
        self.acknowledge_message()


BOT = ModifyExpertBot
