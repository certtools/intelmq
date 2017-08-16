# -*- coding: utf-8 -*-
"""
SieveExpertBot filters and modifies events based on a specification language similar to mail sieve.

TODO: Document possible necessary configurations.
Parameters:
    file: string
"""
from __future__ import unicode_literals

# imports for additional libraries and intelmq
import os
import intelmq.lib.exceptions as exceptions
import re
from intelmq.lib.bot import Bot
from textx.metamodel import metamodel_from_file
from textx.exceptions import TextXError


class SieveExpertBot(Bot):

    def init(self):
        # read the sieve grammar
        try:
            filename = os.path.join(os.path.dirname(__file__), 'sieve.tx')
            self.metamodel = metamodel_from_file(filename)
        except TextXError as e:
            self.logger.error('Could not process sieve grammar file. Error in (%d, %d).', e.line, e.col)
            self.logger.error(str(e))
            self.stop()

        # validate parameters
        if not os.path.exists(self.parameters.file):
            raise exceptions.InvalidArgument('file', got=self.parameters.file, expected='existing file')

        # parse sieve file
        try:
            self.sieve = self.metamodel.model_from_file(self.parameters.file)
        except TextXError as e:
            self.logger.error('Could not parse sieve file %r, error in (%d, %d).', self.parameters.file, e.line, e.col)
            self.logger.error(str(e))
            self.stop()

    def process(self):
        event = self.receive_message()

        keep = False
        for rule in self.sieve.rules:
            keep = self.process_rule(rule, event)
            if not keep:
                self.logger.debug('Dropped event based on rule at %s: %s.', self.get_position(rule), event)
                break

        if keep:
            self.send_message(event)

        self.acknowledge_message()

    def process_rule(self, rule, event):
        match = SieveExpertBot.match_expression(rule.expr, event)
        keep = True
        if match:
            self.logger.debug('Matched event based on rule at %s: %s.', self.get_position(rule), event)
            for action in rule.actions:
                keep = SieveExpertBot.process_action(action.action, event)
                if not keep:
                    break
        return keep

    @staticmethod
    def match_expression(expr, event):
        for conj in expr.conj:
            if SieveExpertBot.process_conjunction(conj, event):
                return True
        return False

    @staticmethod
    def process_conjunction(conj, event):
        for cond in conj.cond:
            if not SieveExpertBot.process_condition(cond, event):
                return False
        return True

    @staticmethod
    def process_condition(cond, event):
        match = cond.match
        if match.__class__.__name__ == 'ExistMatch':
            return SieveExpertBot.process_exist_match(match.key, event)
        elif match.__class__.__name__ == 'StringMatch':
            return SieveExpertBot.process_string_match(match.key, match.op, match.value, event)
        elif match.__class__.__name__ == 'NumericMatch':
            return SieveExpertBot.process_numeric_match(match.key, match.op, match.value, event)
        elif match.__class__.__name__ == 'Expression':
            return SieveExpertBot.match_expression(match, event)
        pass

    @staticmethod
    def process_exist_match(key, event):
        return key in event

    @staticmethod
    def process_string_match(key, op, value, event):
        if key not in event:
            return False

        if value.__class__.__name__ == 'SingleStringValue':
            return SieveExpertBot.process_string_operator(event[key], op, value.value)
        elif value.__class__.__name__ == 'StringValueList':
            for val in value.values:
                if SieveExpertBot.process_string_operator(event[key], op, val):
                    return True
            return False

    @staticmethod
    def process_string_operator(lhs, op, rhs):
        if op == '==':
            return lhs == rhs
        elif op == '!=':
            return lhs != rhs
        elif op == ':contains':
            return lhs.find(rhs) >= 0
        elif op == '=~':
            return re.fullmatch(rhs, lhs) is not None
        elif op == '!~':
            return re.fullmatch(rhs, lhs) is None

    @staticmethod
    def process_numeric_match(key, op, value, event):
        if key not in event:
            return False

        if value.__class__.__name__ == 'SingleNumericValue':
            return SieveExpertBot.process_numeric_operator(event[key], op, value.value)
        elif value.__class__.__name__ == 'NumericValueList':
            for val in value.values:
                if SieveExpertBot.process_numeric_operator(event[key], op, val):
                    return True
            return False

    @staticmethod
    def process_numeric_operator(lhs, op, rhs):
        return eval(str(lhs) + op + str(rhs))

    @staticmethod
    def process_action(action, event):
        print(type(event))
        if action == 'drop':
            return False
        elif action.__class__.__name__  == 'AddAction':
            if action.key not in event:
                event.add(action.key, action.value)
        elif action.__class__.__name__ == 'AddForceAction':
            event.add(action.key, action.value, overwrite=True)
        elif action.__class__.__name__ == 'ModifyAction':
            if action.key in event:
                event.change(action.key, action.value)
        elif action.__class__.__name__ == 'RemoveAction':
            if action.key in event:
                del event[action.key]
        return True

    def get_position(self, entity):
        """ returns the position (line,col) of an entity in the sieve file. """
        parser = self.metamodel.parser
        return parser.pos_to_linecol(entity._tx_position)

BOT = SieveExpertBot
