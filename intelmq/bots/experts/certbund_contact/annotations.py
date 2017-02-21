"""Annotations for contacts and related information"""


class AnnotationError(Exception):
    pass


class Tag:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def from_json(cls, json_obj):
        assert json_obj["type"] == "tag"
        if "value" not in json_obj:
            raise AnnotationError("Tag annotations must have a value attribute")
        value = json_obj["value"]
        if not isinstance(value, str):
            raise AnnotationError("The value of a tag annotations must be a"
                                  " string, not %r" % (type(value),))
        return cls(value)


class Inhibition:

    """An Inhibition annotation defines when a notification should not be sent.

    The annotation has a boolean expression (see Expr) which can be
    evaluated in a rule context with the matches method. If that returns
    true, the contact to which the annotation belongs should be ignored
    when determining which notifications to send.
    """

    def __init__(self, condition):
        self.condition = condition

    def __eq__(self, other):
        return self.condition == other.condition

    def __hash__(self):
        return hash(self.condition)

    @classmethod
    def from_json(cls, json_obj):
        assert json_obj["type"] == "inhibition"
        if "condition" not in json_obj:
            raise AnnotationError("Inhibition annotations must have a"
                                  " condition attribute")
        return cls(expr_from_json(json_obj["condition"]))

    def matches(self, context):
        return self.condition.evaluate(context)


class Expr:

    def evaluate(self, context):
        raise NotImplementedError



class Eq(Expr):

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def __eq__(self, other):
        return self.exp1 == other.exp1 and self.exp2 == other.exp2

    def __hash__(self):
        return hash((self.exp1, self.exp2))

    @classmethod
    def from_json(cls, json_obj):
        assert json_obj[0] == "eq"
        if len(json_obj) != 3:
            raise AnnotationError("'eq' must have exactly two parameters")
        json1, json2 = json_obj[1:]
        return cls(expr_from_json(json1), expr_from_json(json2))

    def evaluate(self, context):
        val1 = self.exp1.evaluate(context)
        val2 = self.exp2.evaluate(context)
        return val1 == val2


class EventFieldReference(Expr):

    def __init__(self, fieldname):
        self.fieldname = fieldname

    def __eq__(self, other):
        return self.fieldname == other.fieldname

    def __hash__(self):
        return hash(self.fieldname)

    @classmethod
    def from_json(cls, json_obj):
        assert json_obj[0] == "event_field"
        if len(json_obj) != 2:
            raise AnnotationError("'event_field' must have exactly 1 parameter")
        fieldname = json_obj[1]
        if not isinstance(fieldname, str):
            raise AnnotationError("'event_field' must have a string as"
                                  " parameter, not %r" % (type(fieldname),))

        return cls(fieldname)


    def evaluate(self, context):
        return context.get(self.fieldname)


class Const(Expr):

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def from_json(cls, json_obj):
        assert isinstance(json_obj, str)
        return cls(json_obj)

    def evaluate(self, context):
        return self.value


def expr_from_json(json_obj):
    if isinstance(json_obj, list):
        if len(json_obj) < 1:
            raise AnnotationError("The list for an expression must have at"
                                  " least one element")
        name = json_obj[0]
        if name == "eq":
            return Eq.from_json(json_obj)
        if name == "event_field":
            return EventFieldReference.from_json(json_obj)
        else:
            raise AnnotationError("Unknown expression function: %r" % (name,))
    elif isinstance(json_obj, str):
        return Const.from_json(json_obj)


def from_json(json_obj):
    annotation_type = json_obj.get("type")
    if annotation_type == "tag":
        return Tag.from_json(json_obj)
    elif annotation_type == "inhibition":
        return Inhibition.from_json(json_obj)
    else:
        raise AnnotationError("Unknown annotation type: %r"
                              % (annotation_type,))
