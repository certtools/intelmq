"""Annotations for contacts and related information"""


class AnnotationError(Exception):
    pass


class Annotation:

    def __init__(self, tag, condition=True):
        self.tag = tag
        self.condition = condition

    def __eq__(self, other):
        return self.tag == other.tag and self.condition == other.condition

    def __hash__(self):
        return hash((self.tag, self.condition))

    @classmethod
    def from_json(cls, json_obj):
        if "tag" not in json_obj:
            raise AnnotationError("Annotation misses a tag attribute")
        tag = json_obj["tag"]
        if not isinstance(tag, str):
            raise AnnotationError("Annotation's tag is not a string")
        return cls(tag, expr_from_json(json_obj.get("condition", "true")))

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
        assert isinstance(json_obj, (str, bool))
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
    elif isinstance(json_obj, (str, bool)):
        return Const.from_json(json_obj)


def from_json(json_obj):
    return Annotation.from_json(json_obj)
