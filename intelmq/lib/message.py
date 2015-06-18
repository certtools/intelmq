import json 
import hashlib
import base64
from intelmq import HARMONIZATION_CONF_FILE
from intelmq.lib import utils
import intelmq.lib.harmonization
import intelmq.lib.exceptions as exceptions


class MessageFactory(object):

    @staticmethod
    def unserialize(raw_message):
        message = Message.unserialize(raw_message)
        class_reference = getattr(intelmq.lib.message, message["__type"])
        del message["__type"]
        return class_reference(message)

    @staticmethod
    def serialize(message):
        super(Message, message).__setitem__("__type", message.__class__.__name__)
        raw_message = Message.serialize(message)
        return raw_message


class Message(dict):

    harmonization_config = utils.load_configuration(HARMONIZATION_CONF_FILE)

    def __init__(self, message=None):
        if message:
            super(Message, self).__init__(message)
        else:
            super(Message, self).__init__()

        self.harmonization_config = self.harmonization_config[self.__class__.__name__.lower()]

    def __setitem__(self, key, value):
        self.add(key, value)

    def add(self, key, value, sanitize=False, force=False, ignore=[]):
        if not force and key in self:
            raise exceptions.KeyExists(key)

        if value == None or value == "":
            return

        for invalid_value in ["-", "N/A"]:
            if value == invalid_value:
                return
    
        if not self.__is_valid_key(key):
            raise exceptions.InvalidKey(key)

        if type(ignore) == list:
            if value in ignore:
                return
        else:
            raise exceptions.InvalidArgument(ignore)

        if sanitize:
            old_value = value
            value = self.__sanitize_value(key, value)            
            if not value:
                raise exceptions.InvalidValue(key, old_value)

        if not self.__is_valid_value(key, value):
            raise exceptions.InvalidValue(key, value)

        super(Message, self).__setitem__(key, value)

    def __getitem__(self, key):
        return self.value(key)
        
    def value(self, key):
        return super(Message, self).__getitem__(key)
        
    def update(self, key, value, sanitize=False):
        if key not in self:
            raise exceptions.KeyNotExists(key)
        self.add(key, value, sanitize)
        
    def clear(self, key):
        self.__delitem__(key)
        
    def __delitem__(self, key):
        if key in self:
            super(Message, self).__delitem__(key)

    def contains(self, key):
        return key in self
        
    def items(self):
        return super(Message, self).items()

    def finditems(self, keyword):
        for key, value in super(Message, self).iteritems():
            if key.startswith(keyword):
                yield key, value

    def copy(self):
        return Message(super(Message, self).copy())
        
    def deep_copy(self):
        return Message(self.serialize())
        
    def __unicode__(self):
        return self.serialize()

    def serialize(self):
        return json.dumps(self) # FIXME: dont know if json take care of encoding issues
        # FIXME: raw need to be decoded from base64 (may be not here)
            
    @staticmethod
    def unserialize(message_string):
        return json.loads(message_string) # FIXME: dont know if json take care of encoding issues
        # FIXME: raw need to be decoded from base64 (may be not here)

    def __is_valid_key(self, key):
        if key in self.harmonization_config:
            return True
        return False

    def __is_valid_value(self, key, value):   
        class_name = self.__get_class_name_from_key_type(key)
        class_reference = getattr(intelmq.lib.harmonization, class_name)
        return class_reference().is_valid(key, value)

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

                if not subkey in json_dict_fp:
                    json_dict_fp[subkey] = dict()

                json_dict_fp = json_dict_fp[subkey]
        return json_dict

    def to_json(self):
        json_dict = self.to_dict()
        return json.dumps(json_dict, ensure_ascii=False).encode("utf-8")


class Report(Message):
    pass
