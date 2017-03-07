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


def convert_config(old):
    config = []
    for groupname, group in old.items():
        for rule_name, rule in group.items():
            config.append({"rulename": groupname + ' ' + rule_name,
                           "if": rule[0],
                           "then": rule[1]})

    return config


class ModifyExpertBot(Bot):

    def init(self):
        self.config = load_configuration(self.parameters.configuration_path)
        if type(self.config) is dict:
            self.config = convert_config(self.config)

    def matches(self, identifier, event, condition):
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
                                     "match in {!s}, {}!".format(type(rule), type(event[name]),
                                                                 identifier, name))
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

        for rule in self.config:
            rule_id, rule_selection, rule_action = rule['rulename'], rule['if'], rule['then']
            matches = self.matches(rule_id, event, rule_selection)
            if matches is not None:
                self.logger.debug('Apply rule {}.'.format(rule_id))
                self.apply_action(event, rule_action, matches)

        self.send_message(event)
        self.acknowledge_message()


BOT = ModifyExpertBot
