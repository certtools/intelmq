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

import intelmq.lib.exceptions as exceptions
from intelmq import HARMONIZATION_CONF_FILE
from intelmq.lib import utils
from intelmq.lib.bot import Bot

try:
    import textx.model
    from textx.metamodel import metamodel_from_file
    from textx.exceptions import TextXError, TextXSemanticError
except ImportError:
    metamodel_from_file = None


class Procedure:
    CONTINUE = 1  # continue processing subsequent rules (default)
    KEEP = 2      # stop processing and keep event
    DROP = 3      # stop processing and drop event


class SieveExpertBot(Bot):
    _message_processed_verb = 'Forwarded'

    harmonization = None

    def init(self):
        if not SieveExpertBot.harmonization:
            harmonization_config = utils.load_configuration(HARMONIZATION_CONF_FILE)
            SieveExpertBot.harmonization = harmonization_config['event']

        self.metamodel = SieveExpertBot.init_metamodel()
        self.sieve = SieveExpertBot.read_sieve_file(self.parameters.file, self.metamodel)

    @staticmethod
    def init_metamodel():
        if metamodel_from_file is None:
            raise ValueError('Could not import textx. Please install it')

        try:
            grammarfile = os.path.join(os.path.dirname(__file__), 'sieve.tx')
            metamodel = metamodel_from_file(grammarfile)

            # apply custom validation rules
            metamodel.register_obj_processors({
                'StringMatch': SieveExpertBot.validate_string_match,
                'NumericMatch': SieveExpertBot.validate_numeric_match,
                'SingleIpRange': SieveExpertBot.validate_ip_range
            })

            return metamodel
        except TextXError as e:
            raise ValueError('Could not process sieve grammar file. Error in (%d, %d): %s' % (e.line, e.col, str(e)))

    @staticmethod
    def read_sieve_file(filename, metamodel):
        if not os.path.exists(filename):
            raise exceptions.InvalidArgument('file', got=filename, expected='existing file')

        try:
            sieve = metamodel.model_from_file(filename)
            return sieve
        except TextXError as e:
            raise ValueError('Could not parse sieve file %r, error in (%d, %d): %s' % (filename, e.line, e.col, str(e)))

    @staticmethod
    def check(parameters):
        try:
            harmonization_config = utils.load_configuration(HARMONIZATION_CONF_FILE)
            SieveExpertBot.harmonization = harmonization_config['event']

            metamodel = SieveExpertBot.init_metamodel()
            SieveExpertBot.read_sieve_file(parameters['file'], metamodel)
        except Exception as e:
            return [['error', 'Validation of Sieve file failed with the following traceback: %r' % traceback.format_exc()]]

    def process(self):
        event = self.receive_message()
        procedure = Procedure.CONTINUE
        if self.sieve:  # empty rules file results in empty string
            for rule in self.sieve.rules:
                procedure = self.process_rule(rule, event)
                if procedure == Procedure.KEEP:
                    self.logger.debug('Stop processing based on rule at %s: %s.', self.get_linecol(rule), event)
                    break
                elif procedure == Procedure.DROP:
                    self.logger.debug('Dropped event based on rule at %s: %s.', self.get_linecol(rule), event)
                    break

        # forwarding decision
        if procedure != Procedure.DROP:
            path = getattr(event, "path", "_default")
            self.send_message(event, path=path)

        self.acknowledge_message()

    def process_rule(self, rule, event):
        # process mandatory 'if' clause
        if self.match_expression(rule.if_.expr, event):
            self.logger.debug('Matched event based on rule at %s: %s.', self.get_linecol(rule.if_), event)
            for action in rule.if_.actions:
                procedure = self.process_action(action.action, event)
                if procedure != Procedure.CONTINUE:
                    return procedure
            return Procedure.CONTINUE

        # process optional 'elif' clauses
        for clause in rule.elif_:
            if self.match_expression(clause.expr, event):
                self.logger.debug('Matched event based on rule at %s: %s.', self.get_linecol(clause), event)
                for action in clause.actions:
                    procedure = self.process_action(action.action, event)
                    if procedure != Procedure.CONTINUE:
                        return procedure
                return Procedure.CONTINUE

        # process optional 'else' clause
        if rule.else_:
            self.logger.debug('Matched event based on rule at %s: %s.', self.get_linecol(rule.else_), event)
            for action in rule.else_.actions:
                procedure = self.process_action(action.action, event)
                if procedure != Procedure.CONTINUE:
                    return procedure

        return Procedure.CONTINUE

    def match_expression(self, expr, event):
        for conj in expr.conj:
            if self.process_conjunction(conj, event):
                return True
        return False

    def process_conjunction(self, conj, event):
        for cond in conj.cond:
            if not self.process_condition(cond, event):
                return False
        return True

    def process_condition(self, cond, event):
        match = cond.match
        if match.__class__.__name__ == 'ExistMatch':
            return self.process_exist_match(match.key, match.op, event)
        elif match.__class__.__name__ == 'StringMatch':
            return self.process_string_match(match.key, match.op, match.value, event)
        elif match.__class__.__name__ == 'NumericMatch':
            return self.process_numeric_match(match.key, match.op, match.value, event)
        elif match.__class__.__name__ == 'IpRangeMatch':
            return self.process_ip_range_match(match.key, match.range, event)
        elif match.__class__.__name__ == 'Expression':
            return self.match_expression(match, event)

    @staticmethod
    def process_exist_match(key, op, event):
        if op == ':exists':
            return key in event
        elif op == ':notexists':
            return key not in event

    def process_string_match(self, key, op, value, event):
        if key not in event:
            return op == '!=' or op == '!~' or op == ':notcontains'

        if value.__class__.__name__ == 'SingleStringValue':
            return self.process_string_operator(event[key], op, value.value)
        elif value.__class__.__name__ == 'StringValueList':
            for val in value.values:
                if self.process_string_operator(event[key], op, val.value):
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
        elif op == ':notcontains':
            return lhs.find(rhs) == -1
        elif op == '=~':
            return re.search(rhs, lhs) is not None
        elif op == '!~':
            return re.search(rhs, lhs) is None

    def process_numeric_match(self, key, op, value, event):
        if key not in event:
            return False

        if value.__class__.__name__ == 'SingleNumericValue':
            return self.process_numeric_operator(event[key], op, value.value)
        elif value.__class__.__name__ == 'NumericValueList':
            for val in value.values:
                if self.process_numeric_operator(event[key], op, val.value):
                    return True
            return False

    def process_numeric_operator(self, lhs, op, rhs):
        if not self.is_numeric(lhs) or not self.is_numeric(rhs):
            return False
        return eval(str(lhs) + op + str(rhs))

    def process_ip_range_match(self, key, ip_range, event):
        if key not in event:
            return False

        try:
            addr = ipaddress.ip_address(event[key])
        except ValueError:
            self.logger.warning("Could not parse IP address %s=%s in %s.", key, event[key], event)
            return False

        if ip_range.__class__.__name__ == 'SingleIpRange':
            network = ipaddress.ip_network(ip_range.value, strict=False)
            return addr in network
        elif ip_range.__class__.__name__ == 'IpRangeList':
            for val in ip_range.values:
                network = ipaddress.ip_network(val.value, strict=False)
                if addr in network:
                    return True
        return False

    @staticmethod
    def process_action(action, event):
        if action == 'drop':
            return Procedure.DROP
        elif action == 'keep':
            return Procedure.KEEP
        elif action.__class__.__name__ == 'PathAction':
            event.path = action.path
        elif action.__class__.__name__ == 'AddAction':
            if action.key not in event:
                event.add(action.key, action.value)
        elif action.__class__.__name__ == 'AddForceAction':
            event.add(action.key, action.value, overwrite=True)
        elif action.__class__.__name__ == 'UpdateAction':
            if action.key in event:
                event.change(action.key, action.value)
        elif action.__class__.__name__ == 'RemoveAction':
            if action.key in event:
                del event[action.key]
        return Procedure.CONTINUE

    @staticmethod
    def validate_ip_range(ip_range):
        try:
            ipaddress.ip_network(ip_range.value, strict=False)
        except ValueError:
            position = SieveExpertBot.get_linecol(ip_range, as_dict=True)
            raise TextXSemanticError('Invalid ip range: %s.' % ip_range.value, **position)

    @staticmethod
    def validate_numeric_match(num_match):
        """ Validates a numeric match expression.

        Checks if the event key (given on the left hand side of the expression) is of a valid type for a numeric
        match, according the the IntelMQ harmonization.

        Raises:
            TextXSemanticError: when the key is of an incompatible type for numeric match expressions.
        """
        valid_types = ['Integer', 'Float', 'Accuracy', 'ASN']
        position = SieveExpertBot.get_linecol(num_match.value, as_dict=True)

        # validate harmonization type (event key)
        try:
            type = SieveExpertBot.harmonization[num_match.key]['type']
            if type not in valid_types:
                raise TextXSemanticError('Incompatible type: %s.' % type, **position)
        except KeyError:
            raise TextXSemanticError('Invalid key: %s.' % num_match.key, **position)

    @staticmethod
    def validate_string_match(str_match):
        """ Validates a string match expression.

        Checks if the type of the value given on the right hand side of the expression matches the event key in the left
        hand side, according to the IntelMQ harmonization.

        Raises:
            TextXSemanticError: when the value is of incompatible type with the event key.
        """

        # validate IPAddress
        ipaddr_types = [k for k, v in SieveExpertBot.harmonization.items() if v['type'] == 'IPAddress']
        if str_match.key in ipaddr_types:
            if str_match.value.__class__.__name__ == 'SingleStringValue':
                SieveExpertBot.validate_ip_address(str_match.value)
            elif str_match.value.__class__.__name__ == 'StringValueList':
                for val in str_match.value.values:
                    SieveExpertBot.validate_ip_address(val)

    @staticmethod
    def validate_ip_address(ipaddr):
        try:
            ipaddress.ip_address(ipaddr.value)
        except ValueError:
            position = SieveExpertBot.get_linecol(ipaddr, as_dict=True)
            raise TextXSemanticError('Invalid ip address: %s.' % ipaddr.value, **position)

    @staticmethod
    def is_numeric(num):
        """ Returns True if argument is a number (integer or float). """
        return str(num).lstrip('-').replace('.', '', 1).isnumeric()

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
