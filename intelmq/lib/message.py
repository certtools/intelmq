import json
import hashlib

class Message(object):
    message_type = 'Message'
    
    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = dict()
            self.add('_type', self.message_type)
    
    
    def add(self, key, value):
        if not value or key in self.message:
            return False
        
        self.message[key] = value
        return True
    
    
    def update(self, key, value):
        if not value:
            return False
        
        self.message[key] = value
        return True
    
    
    def discard(self, key, value):
        self.clear(key)
        
    
    def clear(self, key):
        if key in self.message:
            return self.message.pop(key)
        else:
            return None
        
        
    def value(self, key):
        if key in self.message:
            return self.message[key]
        else:
            return None
        
        
    def keys(self):
        return self.message.keys()
    
    
    def items(self):
        return self.message.items()
    
    
    def contains(self, key):
        if key in self.message:
            return self.message[key]
        else:
            return None
    
    
    def to_dict(self):
        return dict(self.message)
    
    
    @staticmethod
    def from_dict(message_dict):
        import intelmq.lib.message
        message_class = getattr(intelmq.lib.message, message_dict['_type'])
        
        return message_class(message_dict)
    
    
    def to_unicode(self):
        return unicode(json.dumps(self.message))
    
    
    @staticmethod
    def from_unicode(message_string):
        message_dict = json.loads(message_string)
        
        return Message.from_dict(message_dict)
    
    
    def __hash__(self):
        evhash = hashlib.sha1()
    
        for key, value in sorted(self.items()):
            evhash.update(key.encode("utf-8"))
            evhash.update("\xc0")
            evhash.update(value.encode("utf-8"))
            evhash.update("\xc0")
    
        return int(evhash.hexdigest(), 16) # FIXME: the int stuff should be done by cache
        #return hash(self.message)
    
    
    def __eq__(self, message2):
        return self.message == message2.message
    
    
    def __unicode__(self):
        return self.to_unicode()
    
    
    def __repr__(self):
        return repr(self.message)
    
    
    def __str__(self):
        return str(self.message)
    
    
class Event(Message):
    message_type = 'Event'
    
    
class Report(Message):
    message_type = 'Report'
    
    #TODO: Modificar todos os parsers e collectors


