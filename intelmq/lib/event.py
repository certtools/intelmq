import json
import hashlib

class Event(object):

    def __init__(self, event=None):
        if event:
            self.event = event
        else:
            self.event = dict()


    def add(self, key, value):
        if not value or key in self.event:
            return False
        
        self.event[key] = value
        return True
    
    
    def update(self, key, value):
        if not value:
            return False
        
        self.event[key] = value
        return True


    def discard(self, key, value):
        self.clear(key)
        

    def clear(self, key):
        if key in self.event:
            return self.event.pop(key)
        else:
            return None
        
        
    def value(self, key):
        if key in self.event:
            return self.event[key]
        else:
            return None
        
        
    def keys(self):
        return self.event.keys()


    def items(self):
        return self.event.items()


    def contains(self, key):
        if key in self.event:
            return self.event[key]
        else:
            return None


    def to_dict(self):
        return dict(self.event)


    def to_unicode(self):
        return unicode(json.dumps(self.event))
    

    @staticmethod
    def from_unicode(event_string):
        return Event(json.loads(event_string))
    

    def __hash__(self):
        evhash = hashlib.sha1()

        for key, value in sorted(self.items()):
            evhash.update(key.encode("utf-8"))
            evhash.update("\xc0")
            evhash.update(value.encode("utf-8"))
            evhash.update("\xc0")

        return int(evhash.hexdigest(), 16) # FIXME: the int stuff should be done by cache
        #return hash(self.event)


    def __eq__(self, event2):
        return self.event == event2


    def __unicode__(self):
        return self.to_unicode()


    def __repr__(self):
        return repr(self.event)


    def __str__(self):
        return str(self.event)
