# -*- coding: utf-8 -*-
"""
Messages are as information packages in pipelines.

Use MessageFactory to get a Message object (types Report and Event).
"""
import json
import hashlib
from intelmq import HARMONIZATION_CONF_FILE
from intelmq.lib import utils
import intelmq.lib.harmonization
import intelmq.lib.exceptions as exceptions


harm_config = utils.load_configuration(HARMONIZATION_CONF_FILE)


class MessageFactory(object):

    @staticmethod
    def unserialize(raw_message):
        message = Message.unserialize(raw_message)
        try:
            class_reference = getattr(intelmq.lib.message, message["__type"])
        except AttributeError:
            raise exceptions.InvalidArgument('__type',
                                             got=message["__type"],
                                             expected=harm_config.keys(),
                                             docs=HARMONIZATION_CONF_FILE)
        del message["__type"]
        return class_reference(message)

    @staticmethod
    def serialize(message):
        super(Message, message).__setitem__("__type",
                                            message.__class__.__name__)
        raw_message = Message.serialize(message)
        del message["__type"]
        return raw_message


class Message(dict):

    def __init__(self, message=()):
        super(Message, self).__init__(message)
        try:
            classname = message['__type'].lower()
            del message['__type']
        except (KeyError, TypeError):
            classname = self.__class__.__name__.lower()

        try:
            self.harmonization_config = harm_config[classname]
        except KeyError:
            raise exceptions.InvalidArgument('__type',
                                             got=classname,
                                             expected=harm_config.keys(),
                                             docs=HARMONIZATION_CONF_FILE)

    def __setitem__(self, key, value):
        self.add(key, value)

    def add(self, key, value, sanitize=False, force=False, ignore=()):
        if not force and key in self:
            raise exceptions.KeyExists(key)

        if value is None or value == "":
            return

        for invalid_value in ["-", "N/A"]:
            if value == invalid_value:
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

        if sanitize:
            old_value = value
            value = self.__sanitize_value(key, value)
            if not value:
                raise exceptions.InvalidValue(key, old_value)

        if not self.__is_valid_value(key, value):
            raise exceptions.InvalidValue(key, value)

        super(Message, self).__setitem__(key, value)

#    def __getitem__(self, key):  # TODO: Remove, no implications
#        return self.value(key)

    def value(self, key):  # TODO: Remove? Use get instead
        return super(Message, self).__getitem__(key)

    def update(self, key, value, sanitize=False):
        if key not in self:
            raise exceptions.KeyNotExists(key)
        self.add(key, value, force=True, sanitize=sanitize)

    def clear(self, key):  # TODO: Remove?
        self.__delitem__(key)

#    def __delitem__(self, key):  # TODO: Remove, no implications
#        if key in self:
#            super(Message, self).__delitem__(key)

    def contains(self, key):
        return key in self

#    def items(self):  # TODO: Remove, no implications
#        return super(Message, self).items()

    def finditems(self, keyword):
        for key, value in super(Message, self).iteritems():
            if key.startswith(keyword):
                yield key, value

    def copy(self):
        class_ref = self.__class__.__name__
        self['__type'] = class_ref
        retval = getattr(intelmq.lib.message,
                         class_ref)(super(Message, self).copy())
        del self['__type']
        del retval['__type']
        return retval

    def deep_copy(self):
        return MessageFactory.unserialize(MessageFactory.serialize(self))

    def __unicode__(self):
        return self.serialize()

    def serialize(self):
        # FIXME: dont know if json take care of encoding issues
        # FIXME: raw need to be decoded from base64 (may be not here)
        self.__type = self.__class__.__name__
        json_dump = json.dumps(self)
        try:
            return unicode(json_dump)
        except NameError:  # pragma: no cover
            return json_dump

    @staticmethod
    def unserialize(message_string):
        return json.loads(message_string)
        # FIXME: dont know if json take care of encoding issues
        # FIXME: raw need to be decoded from base64 (may be not here)

    def __is_valid_key(self, key):
        if key in self.harmonization_config or key == '__type':
            return True
        return False

    def __is_valid_value(self, key, value):
        if key == '__type':
            return True
        class_name = self.__get_class_name_from_key_type(key)
        class_reference = getattr(intelmq.lib.harmonization, class_name)
        return class_reference().is_valid(value)

    def __sanitize_value(self, key, value):
        class_name = self.__get_class_name_from_key_type(key)
        class_reference = getattr(intelmq.lib.harmonization, class_name)
        return class_reference().sanitize(value)

    def __get_class_name_from_key_type(self, key):
        class_name = self.harmonization_config[key]["type"]
        return class_name


class Event(Message):

    def __hash__(self):
        event_hash = hashlib.sha256()

        for key, value in sorted(self.items()):
            if "time.observation" == key:
                continue

            event_hash.update(key.encode("utf-8"))
            event_hash.update("\xc0")
            event_hash.update(value.encode("utf-8"))
            event_hash.update("\xc0")

        return int(event_hash.hexdigest(), 16)

    def to_dict(self):
        json_dict = dict()

        for key, value in self.items():
            subkeys = key.split('.')
            json_dict_fp = json_dict

            for subkey in subkeys:
                if subkey == subkeys[-1]:
                    json_dict_fp[subkey] = value
                    break

                if subkey not in json_dict_fp:
                    json_dict_fp[subkey] = dict()

                json_dict_fp = json_dict_fp[subkey]
        return json_dict

    def to_json(self):
        json_dict = self.to_dict()
        return json.dumps(json_dict, ensure_ascii=False).encode("utf-8")


class Report(Message):
    pass
