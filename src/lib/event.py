import re
import hashlib
import inspect
import collections

from base64 import b64decode


def _replace_non_xml_chars(unicode_obj, replacement=u"\ufffd"):
    return _NON_XML.sub(replacement, unicode_obj)
_NON_XML = re.compile(u"[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff\ufffe\uffff]", re.U)


def _normalize(value):
    """Return the value converted to unicode. Raise a TypeError if the
    value is not a string.

    >>> _normalize("a")
    u'a'
    >>> _normalize(u"b")
    u'b'
    >>> _normalize(1)
    Traceback (most recent call last):
    ...
    TypeError: expected a string value, got the value 1 of type int

    When converting str objects the default encoding is tried, and an
    UnicodeDecodeError is raised if the value can not bot converted.

    >>> _normalize("\\xe4") #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnicodeDecodeError: <the error goes here>
    """

    if isinstance(value, basestring):
        return unicode(value)

    name = type(value).__name__
    module = inspect.getmodule(value)
    if module is not None and module.__name__ != "__builtin__":
        name = module.__name__ + "." + name
    msg = "expected a string value, got the value %r of type %s" % (value, name)
    raise TypeError(msg)


EVENT_NS = "abusehelper#event"


def _unicode_quote(string):
    r"""
    >>> _unicode_quote(u"a")
    u'a'
    >>> _unicode_quote(u"=")
    u'"="'
    >>> _unicode_quote(u"\n")
    u'"\n"'
    """

    if _UNICODE_QUOTE_CHECK.search(string):
        return u'"' + _UNICODE_QUOTE.sub(r'\\\g<0>', string) + u'"'
    return string
_UNICODE_QUOTE_CHECK = re.compile(r'[\s"\\,=]', re.U)
_UNICODE_QUOTE = re.compile(r'["\\]', re.U)


def _unicode_parse_part(string, start):
    match = _UNICODE_PART.match(string, start)
    quoted, unquoted = match.groups()
    end = match.end()

    if quoted is not None:
        return _UNICODE_UNQUOTE.sub("\\1", quoted), end
    if unquoted is not None:
        return unquoted, end
    return u"", end
_UNICODE_UNQUOTE = re.compile(r'\\(.)', re.U)
_UNICODE_PART = re.compile(r'\s*(?:(?:"((?:\\.|[^"])*)")|([^\s"=,]+)|)\s*', re.U)


class Event(object):
    __slots__ = ["_attrs"]

    _UNDEFINED = object()

    @classmethod
    def _itemize(cls, *args, **keys):
        result = dict()

        for obj in args + (keys,):
            if isinstance(obj, cls):
                for key, values in obj._attrs.iteritems():
                    if key not in result:
                        result[key] = set()
                    result[key].update(values)
                continue

            if hasattr(obj, "items"):
                obj = obj.items()

            for key, values in obj:
                if isinstance(values, basestring):
                    values = (values,)
                elif not values:
                    continue

                key = _normalize(key)
                if key not in result:
                    result[key] = set()
                result[key].update(_normalize(x) for x in values)

        return result

    @classmethod
    def from_unicode(cls, string):
        r"""
        >>> event = Event({"a": "b"})
        >>> Event.from_unicode(unicode(event)) == event
        True

        >>> event = event.union({u'=': u'"'})
        >>> Event.from_unicode(unicode(event)) == event
        True

        Regression test: Check that character escaping
        doesn't mess up parsing.

        >>> event = Event({
        ...     u"x": u"\\",
        ...     u"y": u"b"
        ... })
        >>> Event.from_unicode(ur'x="\\", "y"=b') == event
        True
        """

        string = string.strip()
        if not string:
            return cls()

        attrs = collections.defaultdict(list)

        index = 0
        length = len(string)
        while True:
            key, index = _unicode_parse_part(string, index)
            if index >= length:
                raise ValueError("unexpected string end")
            if string[index] != u"=":
                raise ValueError("unexpected character %r at index %d" %
                                 (string[index], index))
            index += 1

            value, index = _unicode_parse_part(string, index)
            attrs[key].append(value)

            if index >= length:
                return cls(attrs)

            if string[index] != u",":
                raise ValueError("unexpected character %r at index %d" %
                                 (string[index], index))
            index += 1

    @classmethod
    def from_elements(self, elements):
        """Yield events parsed from XML element(s).

        >>> element = Element("message")
        >>> list(Event.from_elements(element))
        []
        >>> element.add(Element("event", xmlns=EVENT_NS))
        >>> list(Event.from_elements(element)) == [Event()]
        True

        >>> event = Event({u"\\uffff": u"\\x05"}) # include some forbidden XML chars
        >>> element = Element("message")
        >>> element.add(event.to_elements())
        >>> list(Event.from_elements(element)) == [Event({u"\\ufffd": u"\\ufffd"})]
        True
        """

        # Future event format
        for event_element in elements.children("e", EVENT_NS):
            attrs = collections.defaultdict(list)
            for key_element in event_element.children("k").with_attrs("a"):
                key = b64decode(key_element.get_attr("a")).decode("utf-8")
                for value_element in key_element.children("v").with_attrs("a"):
                    value = b64decode(value_element.get_attr("a")).decode("utf-8")
                    attrs[key].append(value)
            yield Event(attrs)

        # Legacy event format
        for event_element in elements.children("event", EVENT_NS):
            attrs = collections.defaultdict(list)
            for attr in event_element.children("attr").with_attrs("key", "value"):
                key = attr.get_attr("key")
                value = attr.get_attr("value")
                attrs[key].append(value)
            yield Event(attrs)

    def __init__(self, *args, **keys):
        """
        Regression test: Keep the the correct internal encoding in the
        copy/merge constructor.

        >>> event = Event({u"\xe4": u"\xe4"})
        >>> Event(event).items()
        ((u'\\xe4', u'\\xe4'),)
        """

        self._attrs = self._itemize(*args, **keys)

    def union(self, *args, **keys):
        """Return a new event that contains all key-value pairs from
        appearing in the original event and/or Event(*args, **keys).

        >>> sorted(Event(a=["1", "2"]).union(a=["1", "3"]).items())
        [(u'a', u'1'), (u'a', u'2'), (u'a', u'3')]
        """

        return type(self)(self, *args, **keys)

    def difference(self, *args, **keys):
        """Return a new event that contains all key-value pairs
        from the original event except those also appearing in
        Event(*args, **keys).

        >>> sorted(Event(a=["1", "2"]).difference(a=["1", "3"]).items())
        [(u'a', u'2')]
        """

        other = self._itemize(*args, **keys)
        result = dict()
        for key, values in self._attrs.iteritems():
            diff = values.difference(other.get(key, ()))
            if diff:
                result[key] = diff
        return type(self)(result)

    def add(self, key, value, *values):
        """Add value(s) for a key.

        >>> event = Event()
        >>> event.add("key", "1")
        >>> event.values("key")
        (u'1',)

        More than one value can be added with one call.

        >>> event = Event()
        >>> event.add("key", "1", "2")
        >>> sorted(event.values("key"))
        [u'1', u'2']

        Key-value pairs is already contained by the event are ignored.

        >>> event = Event()
        >>> event.add("key", "1")
        >>> event.values("key")
        (u'1',)
        >>> event.add("key", "1")
        >>> event.values("key")
        (u'1',)
        """
        if value or values:
            self.update(key, (value,) + values)

    def update(self, key, values):
        """Update the values of a key.

        >>> event = Event()
        >>> event.update("key", ["1", "2"])
        >>> sorted(event.values("key"))
        [u'1', u'2']

        The event will not be modified if there are no values to add.

        >>> event = Event()
        >>> event.update("key", [])
        >>> event.contains("key")
        False
        """

        key = _normalize(key)
        if key not in self._attrs:
            self._attrs[key] = set()
        self._attrs[key].update(_normalize(value) for value in values)

    def discard(self, key, value, *values):
        """Discard some value(s) of a key.

        >>> event = Event()
        >>> event.add("key", "1", "2", "3")
        >>> event.discard("key", "1", "3")
        >>> event.values("key")
        (u'2',)

        Values that don't exist for the given key are silently ignored.

        >>> event = Event()
        >>> event.add("key", "2")
        >>> event.discard("key", "1", "2")
        >>> event.values("key")
        ()
        """

        key = _normalize(key)
        if key not in self._attrs:
            return
        valueset = self._attrs[key]
        valueset.difference_update(_normalize(value) for value in (value,) + values)
        if not valueset:
            del self._attrs[key]

    def clear(self, key):
        """Clear all values of a key.

        >>> event = Event()
        >>> event.add("key", "1")
        >>> event.clear("key")
        >>> event.contains("key")
        False

        Clearing keys that do not exist does nothing.

        >>> event = Event()
        >>> event.clear("key")
        """

        key = _normalize(key)
        self._attrs.pop(key, None)

    def _unkeyed(self):
        for values in self._attrs.itervalues():
            for value in values:
                yield value

    def _iter(self, key, parser, filter):
        if key is self._UNDEFINED:
            values = set(self._unkeyed())
        else:
            key = _normalize(key)
            values = self._attrs.get(key, ())

        if parser is not None:
            parsed = (parser(x) for x in values)

            if filter is not None:
                return (x for x in parsed if filter(x))
            else:
                return (x for x in parsed if x is not None)

        if filter is not None:
            return (x for x in values if filter(x))

        return values

    def values(self, key=_UNDEFINED, parser=None, filter=None):
        """Return a tuple of event values (for a specific key, if
        given).

        >>> event = Event(key=["1", "2"], other=["3", "4"])
        >>> sorted(event.values())
        [u'1', u'2', u'3', u'4']
        >>> sorted(event.values("key"))
        [u'1', u'2']

        Perform parsing, validation and filtering by passing in
        parsing and filtering functions (by default all None objects
        are filtered when a parsing function has been given).

        >>> import socket
        >>> def ipv4(string):
        ...     try:
        ...         return socket.inet_ntoa(socket.inet_aton(string))
        ...     except socket.error:
        ...         return None
        >>> event = Event(key=["1.2.3.4", "abba"], other="10.10.10.10")
        >>> event.values("key", parser=ipv4)
        ('1.2.3.4',)
        >>> sorted(event.values(parser=ipv4))
        ['1.2.3.4', '10.10.10.10']
        """

        if not self.contains(key):
            return None

        return tuple(self._iter(key, parser, filter))

    def value(self, key=_UNDEFINED, default=_UNDEFINED,
              parser=None, filter=None):
        """Return one event value (for a specific key, if given).

        The value can be picked either from the values of some
        specific key or amongst event values.

        >>> event = Event(key="1", other="2")
        >>> event.value("key")
        u'1'
        >>> event.value() in [u"1", u"2"]
        True

        A default return value can be defined in case no suitable
        value is available:

        >>> event = Event()
        >>> event.value("key", "default value")
        'default value'
        >>> event.value(default="default value")
        'default value'

        KeyError is raised if no suitable values are available and no
        default is given.

        >>> event = Event()
        >>> event.value()
        Traceback (most recent call last):
        ...
        KeyError: 'no value available'
        >>> event.value("somekey")
        Traceback (most recent call last):
        ...
        KeyError: 'somekey'

        As with .values(...), parsing and filtering functions can be
        given, and they will be used to modify the results.

        >>> def int_parse(string):
        ...     try:
        ...         return int(string)
        ...     except ValueError:
        ...         return None
        >>> event = Event(key=["1", "a"])
        >>> event.value(parser=int_parse)
        1
        >>> event.value("key", parser=int_parse)
        1
        >>> event.value("other", parser=int_parse)
        Traceback (most recent call last):
        ...
        KeyError: 'other'
        """
        
        if not self.contains(key):
            return None

        for value in self._iter(key, parser, filter):
            return value

        if default is self._UNDEFINED:
            if key is self._UNDEFINED:
                raise KeyError("no value available")
            raise KeyError(key)
        return default

    def contains(self, key=_UNDEFINED, value=_UNDEFINED,
                 parser=None, filter=None):
        """Return whether the event contains a key-value pair (for
        specific key and/or value, if given).

        >>> event = Event()
        >>> event.contains() # Does the event contain any values at all?
        False

        >>> event = event.union(key="1")
        >>> event.contains()
        True
        >>> event.contains("key") # Any value for key "key"?
        True
        >>> event.contains(value="1") # Value "1" for any key?
        True
        >>> event.contains("key", "1") # Value "1" for key "key"?
        True
        >>> event.contains("other", "2") # Value "2" for key "other"?
        False

        Parsing and filtering functions can be given to modify the results.

        >>> def int_parse(string):
        ...     try:
        ...         return int(string)
        ...     except ValueError:
        ...         return None
        >>> event.contains(parser=int_parse) # Any int value for any key?
        True
        >>> event.contains("key", parser=int_parse) # Any int value for "key"?
        True
        >>> event.contains(value=1, parser=int_parse) # Value 1 for any key?
        True
        >>> event = event.union(other="x")
        >>> event.contains("other", parser=int_parse)
        False
        """

        if key is self._UNDEFINED:
            values = set(self._unkeyed())
        else:
            key = _normalize(key)
            values = self._attrs.get(key, ())

        if parser is not None:
            parsed = (parser(x) for x in values)

            if filter is not None:
                filtered = (x for x in parsed if filter(x))
            else:
                filtered = (x for x in parsed if x is not None)
        elif filter is not None:
            filtered = (x for x in values if filter(x))
        else:
            filtered = values

        for filtered_value in filtered:
            if value is self._UNDEFINED or value == filtered_value:
                return True
        return False

    def items(self, parser=None, filter=None):
        """Return a tuple of key-value pairs contained by the event.

        >>> event = Event()
        >>> event.items()
        ()
        >>> event = event.union(key="1", other=["x", "y"])
        >>> sorted(event.items())
        [(u'key', u'1'), (u'other', u'x'), (u'other', u'y')]

        Parsing and filtering functions can be given to modify the results.

        >>> def int_parse(string):
        ...     try:
        ...         return int(string)
        ...     except ValueError:
        ...         return None
        >>> event.items(parser=int_parse)
        ((u'key', 1),)

        The order of the key-value pairs is undefined.
        """

        result = list()

        for key, values in self._attrs.iteritems():
            for value in values:
                if parser is not None:
                    value = parser(value)
                if filter is not None and not filter(value):
                    continue
                if filter is None and value is None:
                    continue
                result.append((key, value))

        return tuple(result)

    def keys(self, parser=None, filter=None):
        """Return a tuple of keys with at least one value.

        >>> event = Event()
        >>> event.keys()
        ()
        >>> event = event.union(key="1", other=["x", "y"])
        >>> sorted(event.keys())
        [u'key', u'other']

        Parsing and filtering functions can be given to modify the
        results.

        >>> def int_parse(string):
        ...     try:
        ...         return int(string)
        ...     except ValueError:
        ...         return None
        >>> sorted(event.keys(parser=int_parse))
        [u'key']
        """

        return tuple(key for key in self._attrs
                     if self.contains(key, parser=parser, filter=filter))

    def to_elements(self, include_body=True):
        element = Element("event", xmlns=EVENT_NS)

        for key, value in self.items():
            key = _replace_non_xml_chars(key)
            value = _replace_non_xml_chars(value)
            attr = Element("attr", key=key, value=value)
            element.add(attr)

        if not include_body:
            return element

        body = Element("body")
        body.text = _replace_non_xml_chars(unicode(self))
        return Elements(body, element)
    
    def __hash__(self):
        result = hashlib.sha1()

        for key, value in sorted(self.items()):
            result.update(key.encode("utf-8"))
            result.update("\xc0")
            result.update(value.encode("utf-8"))
            result.update("\xc0")

        return int(result.hexdigest(), 16)

    def __reduce__(self):
        return self.__class__, (self._attrs,)

    def __eq__(self, other):
        if not isinstance(other, Event):
            return NotImplemented
        return other._attrs == self._attrs

    def __ne__(self, other):
        value = self.__eq__(other)
        if value is NotImplemented:
            return NotImplemented
        return not value

    def __unicode__(self):
        """Return an unicode representation of the event.

        >>> unicode(Event())
        u''
        >>> unicode(Event({"a,": "b"}))
        u'"a,"=b'

        The specific order of the key-value pairs is undefined.
        """

        return u", ".join(_unicode_quote(key) + u"=" + _unicode_quote(value)
                          for (key, value) in self.items())

    def __repr__(self):
        attrs = dict()
        for key, value in self.items():
            attrs.setdefault(key, list()).append(value)
        return self.__class__.__name__ + "(" + repr(attrs) + ")"
