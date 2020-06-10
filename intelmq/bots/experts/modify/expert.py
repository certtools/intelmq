# -*- coding: utf-8 -*-
"""
Modify Expert bot let's you manipulate all fields with a config file.
"""
import re
import sys

from intelmq.lib.bot import Bot
from intelmq.lib.utils import load_configuration
from intelmq.lib.upgrades import modify_expert_convert_config


def is_re_pattern(value):
    """
    Checks if the given value is a re compiled pattern
    """
    if sys.version_info > (3, 7):
        return isinstance(value, re.Pattern)
    else:
        return hasattr(value, "pattern")


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
        config = load_configuration(self.parameters.configuration_path)
        if type(config) is dict:
            self.logger.warning('Support for dict-based configuration will be '
                                'removed in version 3.0. Have a look at the '
                                'NEWS file section 1.0.0.dev7.')
            config = modify_expert_convert_config(config)

        if getattr(self.parameters, 'case_sensitive', True):
            self.re_kwargs = {}
        else:
            self.re_kwargs = {'flags': re.IGNORECASE}

        if not hasattr(self.parameters, 'overwrite'):
            self.logger.warning("Parameter 'overwrite' is not given, assuming 'True'. "
                                "Please set it explicitly, default will change to "
                                "'False' in version 3.0.0'.")
        self.overwrite = getattr(self.parameters, 'overwrite', True)

        # regex compilation
        self.config = []
        for rule in config:
            self.config.append(rule)
            for field, expression in rule["if"].items():
                if isinstance(expression, str) and expression != '':
                    self.config[-1]["if"][field] = re.compile(expression, **self.re_kwargs)

        self.maximum_matches = getattr(self.parameters, 'maximum_matches', None)

    def matches(self, identifier, event, condition):
        matches = {}

        for name, rule in condition.items():
            # empty string means non-existent field
            if rule == '':
                if name in event:
                    return None
                else:
                    continue
            if name not in event:
                return None
            if is_re_pattern(rule):
                if isinstance(event[name], (int, float)):
                    match = rule.search(str(event[name]))
                    if match is None:
                        return None
                    else:
                        matches[name] = match
                else:
                    match = rule.search(event[name])
                    if match is None:
                        return None
                    else:
                        matches[name] = match
            else:  # rule is boolean, int, float, etc
                if event[name] != rule:
                    return None

        return matches

    def apply_action(self, event, action, matches):
        for name, value in action.items():
            try:
                newvalue = value.format(msg=event,
                                        matches={k: MatchGroupMapping(v)
                                                 for (k, v) in matches.items()})
            except AttributeError:  # value has ne format: int, bool etc
                newvalue = value
            event.add(name, newvalue,
                      overwrite=self.overwrite)

    def process(self):
        event = self.receive_message()
        num_matches = 0

        for rule in self.config:
            rule_id, rule_selection, rule_action = rule['rulename'], rule['if'], rule['then']
            matches = self.matches(rule_id, event, rule_selection)
            if matches is not None:
                num_matches += 1
                self.logger.debug('Apply rule %s.', rule_id)
                self.apply_action(event, rule_action, matches)
                if self.maximum_matches and num_matches >= self.maximum_matches:
                    self.logger.debug('Reached maximum number of matches, breaking.')
                    break

        self.send_message(event)
        self.acknowledge_message()


BOT = ModifyExpertBot
