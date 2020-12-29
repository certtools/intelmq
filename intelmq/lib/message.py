# -*- coding: utf-8 -*-
"""
Messages are the information packages in pipelines.

Use MessageFactory to get a Message object (types Report and Event).
"""
import hashlib
import json
import re
import warnings
from collections import defaultdict
from typing import Any, Dict, Iterable, Optional, Sequence, Union

import intelmq.lib.exceptions as exceptions
import intelmq.lib.harmonization
from intelmq import HARMONIZATION_CONF_FILE
from intelmq.lib import utils

__all__ = ['Event', 'Message', 'MessageFactory', 'Report']
VALID_MESSSAGE_TYPES = ('Event', 'Message', 'Report')


class MessageFactory(object):
    """
    unserialize: JSON encoded message to object
    serialize: object to JSON encoded object
    """

    @staticmethod
    def from_dict(message: dict, harmonization=None,
                  default_type: Optional[str] = None) -> dict:
        """
        Takes dictionary Message object, returns instance of correct class.

        Parameters:
            message: the message which should be converted to a Message object
            harmonization: a dictionary holding the used harmonization
            default_type: If '__type' is not present in message, the given type will be used

        See also:
            MessageFactory.unserialize
            MessageFactory.serialize
        """
        if default_type and "__type" not in message:
            message["__type"] = default_type
        try:
            class_reference = getattr(intelmq.lib.message, message["__type"])
        except AttributeError:
            raise exceptions.InvalidArgument('__type',
                                             got=message["__type"],
                                             expected=VALID_MESSSAGE_TYPES,
                                             docs=HARMONIZATION_CONF_FILE)
        del message["__type"]
        return class_reference(message, auto=True, harmonization=harmonization)

    @staticmethod
    def unserialize(raw_message: str, harmonization: dict = None,
                    default_type: Optional[str] = None) -> dict:
        """
        Takes JSON-encoded Message object, returns instance of correct class.

        Parameters:
            message: the message which should be converted to a Message object
            harmonization: a dictionary holding the used harmonization
            default_type: If '__type' is not present in message, the given type will be used

        See also:
            MessageFactory.from_dict
            MessageFactory.serialize
        """
        message = Message.unserialize(raw_message)
        return MessageFactory.from_dict(message, harmonization=harmonization,
                                        default_type=default_type)

    @staticmethod
    def serialize(message):
        """
        Takes instance of message-derived class and makes JSON-encoded Message.

        The class is saved in __type attribute.
        """
        raw_message = Message.serialize(message)
        return raw_message


class Message(dict):

    _IGNORED_VALUES = ["", "-", "N/A"]
    _default_value_set = False

    def __init__(self, message: Union[dict, tuple] = (), auto: bool = False,
                 harmonization: dict = None) -> None:
        try:
            classname = message['__type'].lower()
            del message['__type']
        except (KeyError, TypeError):
            classname = self.__class__.__name__.lower()

        if harmonization is None:
            harmonization = utils.load_configuration(HARMONIZATION_CONF_FILE)
        try:
            self.harmonization_config = harmonization[classname]
        except KeyError:
            raise exceptions.InvalidArgument('__type',
                                             got=classname,
                                             expected=VALID_MESSSAGE_TYPES,
                                             docs=HARMONIZATION_CONF_FILE)

        if (classname == 'event' and 'extra' in self.harmonization_config and
           self.harmonization_config['extra']['type'] == 'JSON'):
            warnings.warn("Assuming harmonization type 'JSONDict' for harmonization field 'extra'. "
                          "This assumption will be removed in version 3.0.", DeprecationWarning)
            self.harmonization_config['extra']['type'] = 'JSONDict'
        for harm_key in self.harmonization_config.keys():
            if not re.match('^[a-z_](.[a-z_0-9]+)*$', harm_key) and harm_key != '__type':
                raise exceptions.InvalidKey("Harmonization key %r is invalid." % harm_key)

        super().__init__()
        if isinstance(message, dict):
            iterable = message.items()
        elif isinstance(message, tuple):
            iterable = message
        else:
            raise ValueError("Type %r of message can't be handled, must be dict or tuple.", type(message))
        for key, value in iterable:
            if not self.add(key, value, sanitize=False, raise_failure=False):
                self.add(key, value, sanitize=True)

    def __setitem__(self, key: str, value: Any) -> None:
        self.add(key, value)

    def __getitem__(self, key) -> Any:
        class_name, subitem = self.__get_type_config(key)
        if class_name['type'] == 'JSONDict' and not subitem:
            # return extra as string for backwards compatibility
            return json.dumps(self.to_dict(hierarchical=True)[key.split('.')[0]])
        else:
            try:
                return super().__getitem__(key)
            except KeyError:
                if self._default_value_set:
                    return self.default_value
                else:
                    raise

    def __delitem__(self, item):
        if item == 'extra':
            for key in [key for key in self.keys() if key.startswith('extra.')]:
                del self[key]
            return
        return super().__delitem__(item)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def is_valid(self, key: str, value: str, sanitize: bool = True) -> bool:
        """
        Checks if a value is valid for the key (after sanitation).

        Parameters:
            key: Key of the field
            value: Value of the field
            sanitize: Sanitation of harmonization type will be called before validation
                (default: True)

        Returns:
            True if the value is valid, otherwise False

        Raises:
            intelmq.lib.exceptions.InvalidKey: if given key is invalid.

        """
        if not self.__is_valid_key(key):
            raise exceptions.InvalidKey(key)

        if value is None or value in ["", "-", "N/A"]:
            return False
        if sanitize:
            value = self.__sanitize_value(key, value)
        valid = self.__is_valid_value(key, value)
        if valid[0]:
            return True
        return False

    def add(self, key: str, value: str, sanitize: bool = True,
            overwrite: Optional[bool] = None, ignore: Sequence = (),
            raise_failure: bool = True) -> Optional[bool]:
        """
        Add a value for the key (after sanitation).

        Parameters:
            key: Key as defined in the harmonization
            value: A valid value as defined in the harmonization
                If the value is None or in _IGNORED_VALUES the value will be ignored.
                If the value is ignored, the key exists and overwrite is True, the key
                is deleted.
            sanitize: Sanitation of harmonization type will be called before validation
                (default: True)
            overwrite: Overwrite an existing value if it already exists (default: None)
                If True, overwrite an existing value
                If False, do not overwrite an existing value
                If None, raise intelmq.exceptions.KeyExists for an existing value
            raise_failure: If a intelmq.lib.exceptions.InvalidValue should be raised for
                invalid values (default: True). If false, the return parameter will be
                False in case of invalid values.

        Returns:
            * True if the value has been added.
            * False if the value is invalid and raise_failure is False or the value existed
                and has not been overwritten.
            * None if the value has been ignored.

        Raises:
            intelmq.lib.exceptions.KeyExists: If key exists and won't be overwritten explicitly.
            intelmq.lib.exceptions.InvalidKey: if key is invalid.
            intelmq.lib.exceptions.InvalidArgument: if ignore is not list or tuple.
            intelmq.lib.exceptions.InvalidValue: If value is not valid for the given key and
                raise_failure is True.
        """
        if overwrite is None and key in self:
            raise exceptions.KeyExists(key)
        if overwrite is False and key in self:
            return False

        if value is None or value in self._IGNORED_VALUES:
            if overwrite and key in self:
                del self[key]
            return

        if not self.__is_valid_key(key):
            raise exceptions.InvalidKey(key)

        try:
            if value in ignore:
                return
        except TypeError:
            raise exceptions.InvalidArgument('ignore',
                                             got=type(ignore),
                                             expected='list or tuple')

        if sanitize and not key == '__type':
            old_value = value
            value = self.__sanitize_value(key, value)
            if value is None:
                if raise_failure:
                    raise exceptions.InvalidValue(key, old_value)
                else:
                    return False

        valid_value = self.__is_valid_value(key, value)
        if not valid_value[0]:
            if raise_failure:
                raise exceptions.InvalidValue(key, value, reason=valid_value[1])
            else:
                return False

        class_name, subitem = self.__get_type_config(key)
        if class_name and class_name['type'] == 'JSONDict' and not subitem:
            # for backwards compatibility allow setting the extra field as string
            if overwrite and key in self:
                del self[key]
            for extrakey, extravalue in json.loads(value).items():
                # For extra we must not ignore empty or invalid values because of backwards compatibility issues #1335
                if key != 'extra' and hasattr(extravalue, '__len__'):
                    if not len(extravalue):  # ignore empty values
                        continue
                if key != 'extra' and extravalue in self._IGNORED_VALUES:
                    continue
                super().__setitem__('{}.{}'.format(key, extrakey),
                                    extravalue)
        else:
            super().__setitem__(key, value)
        return True

    def update(self, other: dict):
        for key, value in other.items():
            if not self.add(key, value, sanitize=False, raise_failure=False, overwrite=True):
                self.add(key, value, sanitize=True, overwrite=True)

    def change(self, key: str, value: str, sanitize: bool = True):
        if key not in self:
            raise exceptions.KeyNotExists(key)
        return self.add(key, value, overwrite=True, sanitize=sanitize)

    def finditems(self, keyword: str):
        for key, value in super().items():
            if key.startswith(keyword):
                yield key, value

    def copy(self):
        class_ref = self.__class__.__name__
        self['__type'] = class_ref
        retval = getattr(intelmq.lib.message,
                         class_ref)(super().copy(),
                                    harmonization={self.__class__.__name__.lower(): self.harmonization_config})
        del self['__type']
        return retval

    def deep_copy(self):
        return MessageFactory.unserialize(MessageFactory.serialize(self),
                                          harmonization={self.__class__.__name__.lower(): self.harmonization_config})

    def __str__(self):
        return self.serialize()

    def serialize(self):
        self['__type'] = self.__class__.__name__
        json_dump = utils.decode(json.dumps(self))
        del self['__type']
        return json_dump

    @staticmethod
    def unserialize(message_string: str):
        message = json.loads(message_string)
        return message

    def __is_valid_key(self, key: str):
        try:
            class_name, subitem = self.__get_type_config(key)
        except KeyError:
            return False
        if key in self.harmonization_config or key == '__type' or subitem:
            return True
        return False

    def __is_valid_value(self, key: str, value: str):
        if key == '__type':
            return (True, )
        config, subitem = self.__get_type_config(key)
        class_reference = getattr(intelmq.lib.harmonization, config['type'])
        if not subitem:
            validation = class_reference().is_valid(value)
        else:
            validation = class_reference().is_valid_subitem(value)
        if not validation:
            return (False, 'is_valid returned False.')
        if 'length' in config:
            length = len(str(value))
            if not length <= config['length']:
                return (False, 'too long: {} > {}.'.format(length,
                                                           config['length']))
        if 'regex' in config:
            if not re.search(config['regex'], str(value)):
                return (False, 'regex did not match.')
        if 'iregex' in config:
            if not re.search(config['iregex'], str(value), re.IGNORECASE):
                return (False, 'regex (case insensitive) did not match.')
        return (True, )

    def __sanitize_value(self, key: str, value: str):
        class_name, subitem = self.__get_type_config(key)
        class_reference = getattr(intelmq.lib.harmonization, class_name['type'])
        if not subitem:
            return class_reference().sanitize(value)
        else:
            return class_reference().sanitize_subitem(value)

    def __get_type_config(self, key: str):
        if key == '__type':
            return None, None
        try:
            class_name = self.harmonization_config[key]
        except KeyError:
            # Could be done recursively in the future if needed
            class_name = self.harmonization_config[key.split('.')[0]]
            subitem = True
        else:
            subitem = False
        return class_name, subitem

    def __hash__(self):
        return int(self.hash(), 16)

    def hash(self, *, filter_keys: Iterable = frozenset(), filter_type: str = "blacklist"):
        """Return a SHA256 hash of the message as a hexadecimal string.
        The hash is computed over almost all key/value pairs. Depending on
        filter_type parameter (blacklist or whitelist), the keys defined in
        filter_keys_list parameter will be considered as the keys to ignore
        or the only ones to consider. If given, the filter_keys_list
        parameter should be a set.

        'time.observation' will always be ignored.
        """

        if filter_type not in ["whitelist", "blacklist"]:

            raise exceptions.InvalidArgument('filter_type',
                                             got=filter_type,
                                             expected=['whitelist', 'blacklist'])

        event_hash = hashlib.sha256()

        for key, value in sorted(self.items()):
            if "time.observation" == key:
                continue

            if filter_type == "whitelist" and key not in filter_keys:
                continue

            if filter_type == "blacklist" and key in filter_keys:
                continue

            event_hash.update(utils.encode(key))
            event_hash.update(b"\xc0")
            event_hash.update(utils.encode(repr(value)))
            event_hash.update(b"\xc0")

        return event_hash.hexdigest()

    def to_dict(self, hierarchical: bool = False, with_type: bool = False,
                jsondict_as_string: bool = False) -> dict:
        """
        Returns a copy of self, only based on a dict class.

        Parameters:
            hierarchical: Split all keys at a dot and save these subitems
                in dictionaries.
            with_type: Add a value named `__type` containing the message type
            jsondict_as_string:
                If False (default) treat values in JSONDict fields just as normal ones
                If True, save such fields as JSON-encoded string. This is the old behavior
                    before version 1.1.

        Returns:
            new_dict: A dictionary as copy of itself modified according
                to the given parameters
        """
        new_dict = {}  # type: Dict[str, Any]

        if with_type:
            new_dict['__type'] = self.__class__.__name__

        jsondicts = defaultdict(dict)  # type: Dict[str, Any]

        for key, value in self.items():
            splitted_key = key.split('.')
            if hierarchical:
                subkeys = splitted_key
            else:
                subkeys = [key]
            json_dict_fp = new_dict  # type: Dict[str, Any]

            try:
                key_type = self.__get_type_config(splitted_key[0])[0]['type']
            except KeyError:
                key_type = None
            if key_type == 'JSONDict' and jsondict_as_string:
                jsondicts[splitted_key[0]]['.'.join(splitted_key[1:])] = value
                continue

            for subkey in subkeys:
                if subkey == subkeys[-1]:
                    json_dict_fp[subkey] = value
                    break

                if subkey not in json_dict_fp:
                    json_dict_fp[subkey] = {}

                json_dict_fp = json_dict_fp[subkey]

        for key, value in jsondicts.items():
            new_dict[key] = json.dumps(value, ensure_ascii=False)

        return new_dict

    def to_json(self, hierarchical=False, with_type=False, jsondict_as_string=False):
        json_dict = self.to_dict(hierarchical=hierarchical, with_type=with_type)
        return json.dumps(json_dict, ensure_ascii=False, sort_keys=True)

    def __eq__(self, other: dict) -> bool:
        """
        Wrapper is necessary as we have additional members
        harmonization_config and types.
        The additional checks are only performed for subclasses of Message.

        Comparison with other types e.g. dicts does not check the harmonization_config.
        """
        dict_eq = super().__eq__(other)
        if dict_eq and issubclass(type(other), Message):
            type_eq = type(self) == type(other)
            harm_eq = self.harmonization_config == other.harmonization_config if hasattr(other, 'harmonization_config') else False
            if type_eq and harm_eq:
                return True
        elif dict_eq:
            return True
        return False

    def __ne__(self, other: dict) -> bool:
        return not self.__eq__(other)

    def set_default_value(self, value: Any = None):
        """
        Sets a default value for items.
        """
        self._default_value_set = True
        self.default_value = value

    def __contains__(self, item: str) -> bool:
        if item == 'extra':
            return 'extra' in self.to_dict(hierarchical=True)
        return super().__contains__(item)


class Event(Message):

    def __init__(self, message: Union[dict, tuple] = (), auto: bool = False,
                 harmonization: Optional[dict] = None) -> None:
        """
        Parameters:
            message: Give a report and feed.name, feed.url and
                time.observation will be used to construct the Event if given.
                If it's another type, the value is given to dict's init
            auto: unused here
            harmonization: Harmonization definition to use
        """
        if isinstance(message, Report):
            template = {}
            if 'feed.accuracy' in message:
                template['feed.accuracy'] = message['feed.accuracy']
            if 'feed.code' in message:
                template['feed.code'] = message['feed.code']
            if 'feed.documentation' in message:
                template['feed.documentation'] = message['feed.documentation']
            if 'feed.name' in message:
                template['feed.name'] = message['feed.name']
            if 'feed.provider' in message:
                template['feed.provider'] = message['feed.provider']
            if 'feed.url' in message:
                template['feed.url'] = message['feed.url']
            if 'rtir_id' in message:
                template['rtir_id'] = message['rtir_id']
            if 'time.observation' in message:
                template['time.observation'] = message['time.observation']
        else:
            template = message
        super().__init__(template, auto, harmonization)


class Report(Message):

    def __init__(self, message: Union[dict, tuple] = (), auto: bool = False,
                 harmonization: Optional[dict] = None) -> None:
        """
        Parameters:
            message: Passed along to Message's and dict's init.
                If this is an instance of the Event class, the resulting Report instance
                has only the fields which are possible in Report, all others are stripped.
            auto: if False (default), time.observation is automatically added.
            harmonization: Harmonization definition to use
        """
        if isinstance(message, Event):
            super().__init__({}, auto, harmonization)
            for key, value in message.items():
                if self._Message__is_valid_key(key):
                    self.add(key, value, sanitize=False)
        else:
            super().__init__(message, auto, harmonization)
        if not auto and 'time.observation' not in self:
            time_observation = intelmq.lib.harmonization.DateTime().generate_datetime_now()
            self.add('time.observation', time_observation, sanitize=False)

    def copy(self):
        retval = super().copy()
        if 'time.observation' in retval and 'time.observation' not in self:
            del retval['time.observation']
        return retval
