import json

class Event(object):

    def __init__(self, event=None):
        if event:
            self.event = event
        else.
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


    @staticmethod
    def to_unicode():
        return json.dumps(self.event)
    

    @staticmethod
    def from_unicode(event_string):
        return json.loads(event_string)
    

    def __hash__(self):
        return hash(self.event)
    

    def __eq__(self, event2):
        return self.event == event2


    def __unicode__(self):
        return unicode(self.event)


    def __repr__(self):
        return repr(self.event)


    def __str__(self):
        return str(self.event)