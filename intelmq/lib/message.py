import json
import hashlib


class Event(object):

    def __init__(self, event=None):
        if event:
            self.event = event
        else:
            self.event = dict()

    def add(self, key, value):
        """Add key with specified value"""
        if not value or key in self.event:
            return False

        self.event[key] = value
        return True

    def update(self, key, new_value):
        """Updates key with new value"""
        if not new_value:
            return False

        self.event[key] = new_value
        return True

    def discard(self, key, value):
        """Discards the given key, value pair"""
        self.clear(key)

    def clear(self, key):
        """Clears the given key from event"""
        if key in self.event:
            return self.event.pop(key)
        else:
            return None

    def value(self, key):
        """Returns value of key or None if it doesn't exist"""
        if key in self.event:
            return self.event.get(key)
        else:
            return None

    def keys(self):
        """Return contained keys of event"""
        return self.event.keys()

    def items(self):
        """Return contained items of event"""
        return self.event.items()

    def contains(self, key):
        """Returns key in event"""
        if key in self.event:
            return self.event.get(key)
        else:
            return None

    def to_dict(self):
        """Converts event to a dict"""
        return dict(self.event)

    def to_unicode(self):

        return unicode(json.dumps(self.event))

    @staticmethod
    def from_unicode(event_string):
        return Event(json.loads(event_string))

    def __hash__(self):
        """Returns this event as a hash"""
        evhash = hashlib.sha1()

        for key, value in sorted(self.items()):
            evhash.update(key.encode("utf-8"))
            evhash.update("\xc0")
            evhash.update(value.encode("utf-8"))
            evhash.update("\xc0")

        # FIXME: the int stuff should be done by cache
        return int(evhash.hexdigest(), 16)

    def __eq__(self, other_event):
        """Return self == other_event"""
        return self.event == other_event

    def __unicode__(self):
        return self.to_unicode()

    def __repr__(self):
        return repr(self.event)

    def __str__(self):
        """Returns self (the event itself) as a string"""
        return str(self.event)
