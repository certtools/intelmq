# SPDX-FileCopyrightText: 2017 Antoine Neuenschwander
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
SieveExpertBot filters and modifies events based on a specification language similar to mail sieve.

Parameters:
    file: string
"""
import ipaddress
import os
import re
import traceback
import datetime
import operator

from typing import Optional
from enum import Enum, auto
from functools import partial

import intelmq.lib.exceptions as exceptions
from intelmq import HARMONIZATION_CONF_FILE
from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.utils import parse_relative
from intelmq.lib.harmonization import DateTime

try:
    import textx.model
    from textx.metamodel import metamodel_from_file
    from textx.exceptions import TextXError, TextXSemanticError
except ImportError:
    metamodel_from_file = None


class Procedure(Enum):
    CONTINUE = auto()  # continue processing subsequent statements (default)
    KEEP = auto()      # stop processing and keep event
    DROP = auto()      # stop processing and drop event


class SieveExpertBot(Bot):
    """Filter and modify events based on a sieve-based language"""
    _message_processed_verb = 'Forwarded'

    _harmonization = None
    file: str = "/opt/intelmq/var/lib/bots/sieve/filter.sieve"  # TODO: should be pathlib.Path

    _string_op_map = {
        '==': operator.eq,
        '!=': operator.ne,
        ':contains': lambda lhs, rhs: lhs.find(rhs) >= 0,
        '=~': lambda lhs, rhs: re.search(rhs, lhs) is not None,
        '!~': lambda lhs, rhs: re.search(rhs, lhs) is None,
    }

    _string_multi_op_map = {
        ':in': lambda lhs, rhs: lhs in rhs,
        ':containsany': lambda lhs, rhs: any(lhs.find(s) >= 0 for s in rhs),
        ':regexin': lambda lhs, rhs: any(re.search(s, lhs) is not None for s in rhs),
    }

    _list_op_map = {
        ':setequals': operator.eq,
        ':overlaps': lambda l, r: not l.isdisjoint(r),
        ':subsetof': set.issubset,
        ':supersetof': set.issuperset,
    }

    _numeric_op_map = {
        '==': operator.eq,
        '!=': operator.ne,
        '<=': operator.le,
        '>=': operator.ge,
        '<': operator.lt,
        '>': operator.gt,
    }

    _numeric_multi_op_map = {
        ':in': lambda lhs, rhs: lhs in rhs,
    }

    _basic_math_op_map = {
        '+=': operator.add,
        '-=': operator.sub,
    }

    _bool_op_map = {
        '==': operator.eq,
        '!=': operator.ne,
    }

    _cond_map = {
        'ExistMatch': lambda self, match, event: self.process_exist_match(match.key, match.op, event),
        'SingleStringMatch': lambda self, match, event: self.process_single_string_match(match.key, match.op, match.value, event),
        'MultiStringMatch': lambda self, match, event: self.process_multi_string_match(match.key, match.op, match.value, event),
        'SingleNumericMatch': lambda self, match, event: self.process_single_numeric_match(match.key, match.op, match.value, event),
        'MultiNumericMatch': lambda self, match, event: self.process_multi_numeric_match(match.key, match.op, match.value, event),
        'IpRangeMatch': lambda self, match, event: self.process_ip_range_match(match.key, match.range, event),
        'ListMatch': lambda self, match, event: self.process_list_match(match.key, match.op, match.value, event),
        'BoolMatch': lambda self, match, event: self.process_bool_match(match.key, match.op, match.value, event),
        'Expression': lambda self, match, event: self.match_expression(match, event),
    }

    def init(self) -> None:
        if not SieveExpertBot._harmonization:
            harmonization_config = utils.load_configuration(HARMONIZATION_CONF_FILE)
            SieveExpertBot._harmonization = harmonization_config['event']

        self.metamodel = SieveExpertBot.init_metamodel()
        self.sieve = SieveExpertBot.read_sieve_file(self.file, self.metamodel)

    @staticmethod
    def init_metamodel():
        if metamodel_from_file is None:
            raise MissingDependencyError("textx")

        try:
            grammarfile = os.path.join(os.path.dirname(__file__), 'sieve.tx')
            metamodel = metamodel_from_file(grammarfile)

            # apply custom validation rules
            metamodel.register_obj_processors({
                'SingleStringMatch': SieveExpertBot.validate_string_match,
                'MultiStringMatch': SieveExpertBot.validate_string_match,
                'SingleNumericMatch': SieveExpertBot.validate_numeric_match,
                'MultiNumericMatch': SieveExpertBot.validate_numeric_match,
                'SingleIpRange': SieveExpertBot.validate_ip_range,
            })

            return metamodel
        except TextXError as e:
            raise ValueError(f'Could not process sieve grammar file. Error in ({e.line}, {e.col}): {e}')

    @staticmethod
    def read_sieve_file(filename, metamodel):
        if not os.path.exists(filename):
            raise exceptions.InvalidArgument('file', got=filename, expected='existing file')

        try:
            sieve = metamodel.model_from_file(filename)
            return sieve
        except TextXError as e:
            raise ValueError(f'Could not parse sieve file {filename!r}, error in ({e.line}, {e.col}): {e}')

    @staticmethod
    def check(parameters):
        try:
            harmonization_config = utils.load_configuration(HARMONIZATION_CONF_FILE)
            SieveExpertBot._harmonization = harmonization_config['event']

            grammarfile = os.path.join(os.path.dirname(__file__), 'sieve.tx')
            if not os.path.exists(grammarfile):
                raise FileExistsError(f'Sieve grammar file not found: {grammarfile!r}.')

            metamodel = None

            try:
                metamodel = metamodel_from_file(grammarfile)
            except TextXError as e:
                raise ValueError(f'Could not process sieve grammar file. Error in ({e.line}, {e.col}).')

            if not os.path.exists(parameters['file']):
                raise ValueError(f'File does not exist: {parameters["file"]!r}')

            try:
                metamodel.model_from_file(parameters['file'])
            except TextXError as e:
                raise ValueError(f'Could not process sieve file {parameters["file"]!r}. Error in ({e.line}, {e.col}).')
        except Exception:
            return [['error', f'Validation of Sieve file failed with the following traceback: {traceback.format_exc()!r}']]

    def process(self) -> None:
        event = self.receive_message()
        procedure = Procedure.CONTINUE
        if self.sieve:  # empty rules file results in empty string
            for statement in self.sieve.statements:
                procedure = self.process_statement(statement, event)
                if procedure == Procedure.KEEP:
                    self.logger.debug(f'Stop processing based on statement at {self.get_linecol(statement)}: event.')
                    break
                elif procedure == Procedure.DROP:
                    self.logger.debug(f'Dropped event based on statement at {self.get_linecol(statement)}: {event}.')
                    break

        # forwarding decision
        if procedure != Procedure.DROP:
            paths = getattr(event, "path", ("_default", ))
            if hasattr(paths, 'values'):  # PathValueList
                paths = tuple(path.value for path in paths.values)
            elif hasattr(paths, 'value'):  # SinglePathValue
                paths = (paths.value, )
            # else: default value -> pass
            for path in paths:
                self.send_message(event, path=path)

        self.acknowledge_message()

    def process_statement(self, statement, event):
        name = statement.__class__.__name__
        if name == 'Branching':
            return self.process_branching(statement, event)
        elif name == 'Action':
            return self.process_action(statement.action, event)

    def process_branching(self, rule, event) -> Procedure:
        # process optional 'if' clause
        if rule.if_:
            result = self.process_clause(rule.if_, event)
            if isinstance(result, Procedure):
                return result

        # process optional 'elif' clauses
        for clause in rule.elif_:
            result = self.process_clause(clause, event)
            if isinstance(result, Procedure):
                return result

        # process optional 'else' clause
        if rule.else_:
            result = self.process_clause(rule.else_, event, True)
            if isinstance(result, Procedure):
                return result

        return Procedure.CONTINUE

    def process_clause(self, clause, event, else_clause=False) -> Optional[Procedure]:
        if else_clause or self.match_expression(clause.expr, event):
            self.logger.debug(f'Matched event based on rule at {self.get_linecol(clause)}: {event}.')

            for procedure in (self.process_statement(statement, event) for statement in clause.statements):
                if procedure != Procedure.CONTINUE:
                    return procedure
            if not else_clause:
                return Procedure.CONTINUE
        return None

    def match_expression(self, expr, event) -> bool:
        return any(self.process_conjunction(conj, event) for conj in expr.conj)

    def process_conjunction(self, conj, event) -> bool:
        return all(self.process_condition(cond, event) for cond in conj.cond)

    def process_condition(self, cond, event) -> bool:
        name = cond.match.__class__.__name__
        return cond.neg ^ self._cond_map[name](self, cond.match, event)

    @staticmethod
    def process_exist_match(key, op, event) -> bool:
        return (key in event) ^ (op == ':notexists')

    def process_single_string_match(self, key, op, value, event) -> bool:
        if key not in event:
            return op in {'!=', '!~'}

        return self._string_op_map[op](event[key], value.value)

    def process_multi_string_match(self, key, op, value, event) -> bool:
        if key not in event:
            return False

        return self._string_multi_op_map[op](event[key], (v.value for v in value.values))

    def process_single_numeric_match(self, key, op, value, event) -> bool:
        if key not in event:
            return False

        return self._numeric_op_map[op](event[key], value.value)

    def process_multi_numeric_match(self, key, op, value, event) -> bool:
        if key not in event:
            return False

        return self._numeric_multi_op_map[op](event[key], (v.value for v in value.values))

        if name == 'SingleNumericValue':
            return self.process_numeric_operator(event[key], op, value.value)
        elif name == 'NumericValueList':
            return any(self.process_numeric_operator(event[key], op, val.value) for val in value.values)
        raise TextXSemanticError(f'Unhandled type: {name}')

    def process_ip_range_match(self, key, ip_range, event) -> bool:
        if key not in event:
            return False

        try:
            addr = ipaddress.ip_address(event[key])
        except ValueError:
            self.logger.warning(f'Could not parse IP address {key}={event[key]} in {event}.')
            return False

        name = ip_range.__class__.__name__

        if name == 'SingleIpRange':
            return addr in ipaddress.ip_network(ip_range.value, strict=False)
        elif name == 'IpRangeList':
            return any(addr in ipaddress.ip_network(val.value, strict=False) for val in ip_range.values)
        raise TextXSemanticError(f'Unhandled type: {name}')

    def process_list_match(self, key, op, value, event) -> bool:
        if not (key in event and isinstance(event[key], list)):
            return False

        lhs = event[key]
        rhs = value.values
        return lhs == rhs if op == ':equals' else self._list_op_map[op](set(lhs), set(rhs))

    def process_bool_match(self, key, op, value, event):
        if not (key in event and isinstance(event[key], bool)):
            return False

        return self._bool_op_map[op](event[key], value)

    def compute_basic_math(self, action, event) -> str:
        date = DateTime.parse_utc_isoformat(event[action.key], True)
        delta = datetime.timedelta(minutes=parse_relative(action.value))

        return self._basic_math_op_map[action.operator](date, delta).isoformat()

    def process_action(self, action, event) -> Procedure:
        name = action.__class__.__name__
        if action == 'drop':
            return Procedure.DROP
        elif action == 'keep':
            return Procedure.KEEP
        elif name == 'PathAction':
            event.path = action.path
        elif name == 'AddAction':
            if action.key not in event:
                value = action.value
                if action.operator != '=':
                    value = self.compute_basic_math(action, event)
                event.add(action.key, value)
        elif name == 'AddForceAction':
            value = action.value
            if action.operator != '=':
                value = self.compute_basic_math(action, event)
            event.add(action.key, value, overwrite=True)
        elif name == 'UpdateAction':
            if action.key in event:
                value = action.value
                if action.operator != '=':
                    value = self.compute_basic_math(action, event)
                event.change(action.key, value)
        elif name == 'RemoveAction':
            if action.key in event:
                del event[action.key]
        elif name == 'AppendAction':
            if action.key in event:
                if isinstance(event[action.key], list):  # silently ignore existing non-list values
                    event[action.key].append(action.value)
            else:
                event[action.key] = [action.value]
        elif name == 'AppendForceAction':
            if action.key in event:
                old_value = event[action.key]
                list_ = old_value if isinstance(old_value, list) else [old_value]
            else:
                list_ = []

            list_.append(action.value)
            event.add(action.key, list_, overwrite=True)

        return Procedure.CONTINUE

    @staticmethod
    def validate_ip_range(ip_range) -> None:
        try:
            ipaddress.ip_network(ip_range.value, strict=False)
        except ValueError:
            position = SieveExpertBot.get_linecol(ip_range, as_dict=True)
            raise TextXSemanticError(f'Invalid ip range: {ip_range.value}.', **position)

    @staticmethod
    def validate_numeric_match(num_match) -> None:
        """ Validates a numeric match expression.

        Checks if the event key (given on the left hand side of the expression) is of a valid type for a numeric
        match, according the the IntelMQ harmonization.

        Raises:
            TextXSemanticError: when the key is of an incompatible type for numeric match expressions.
        """
        valid_types = {'Integer', 'Float', 'Accuracy', 'ASN'}
        position = SieveExpertBot.get_linecol(num_match.value, as_dict=True)

        # validate harmonization type (event key)
        try:
            type = SieveExpertBot._harmonization[num_match.key]['type']
            if type not in valid_types:
                raise TextXSemanticError(f'Incompatible type: {type}.', **position)
        except KeyError:
            raise TextXSemanticError(f'Invalid key: {num_match.key}.', **position)

    @staticmethod
    def validate_string_match(str_match) -> None:
        """ Validates a string match expression.

        Checks if the type of the value given on the right hand side of the expression matches the event key in the left
        hand side, according to the IntelMQ harmonization.

        Raises:
            TextXSemanticError: when the value is of incompatible type with the event key.
        """

        # validate IPAddress
        ipaddr_types = (k for k, v in SieveExpertBot._harmonization.items() if v['type'] == 'IPAddress')
        if str_match.key in ipaddr_types:
            name = str_match.value.__class__.__name__
            if name == 'SingleStringValue':
                SieveExpertBot.validate_ip_address(str_match.value)
            elif name == 'StringValueList':
                for val in str_match.value.values:
                    SieveExpertBot.validate_ip_address(val)

    @staticmethod
    def validate_ip_address(ipaddr) -> None:
        try:
            ipaddress.ip_address(ipaddr.value)
        except ValueError:
            position = SieveExpertBot.get_linecol(ipaddr, as_dict=True)
            raise TextXSemanticError(f'Invalid IP address: {ipaddr.value}.', **position)

    @staticmethod
    def get_linecol(model_obj, as_dict=False):
        """ Gets the position of a model object in the sieve file.

        Args:
            model_obj: the model object
            as_dict: return the position as a dict instead of a tuple.

        Returns:
            Returns the line and column number for the model object's position in the sieve file.
            Default return type is a tuple of (line,col). Optionally, returns a dict when as_dict == True.

        """
        # The __version__ attribute is first available with version 1.7.0
        if hasattr(textx, '__version__'):
            parser = textx.model.get_model(model_obj)._tx_parser
        else:
            parser = textx.model.metamodel(model_obj).parser
        tup = parser.pos_to_linecol(model_obj._tx_position)
        if as_dict:
            return dict(zip(['line', 'col'], tup))
        return tup


BOT = SieveExpertBot
