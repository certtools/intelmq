"""Annotations for contacts and related information"""


class AnnotationError(Exception):
    pass


class Tag:

    def __init__(self, value):
        self.value = value

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


def from_json(json_obj):
    annotation_type = json_obj.get("type")
    if annotation_type == "tag":
        return Tag.from_json(json_obj)
    else:
        raise AnnotationError("Unknown annotation type: %r"
                              % (annotation_type,))
