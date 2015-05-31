
message = MessageFactory.unserialize(self.current_message)


class MessageFactory(object):

    @staticmethod
    def unserialize(raw_message):
        message = Message.unserialize(raw_message)
        class_reference = get_class_refence(message["__type"], intelmq.lib.message)
        return class_reference(message)

    @staticmethod
    def serialize(message):
        message.add("__type", message.__class__.__name__)
        raw_message = Message.serialize(message)
        return raw_message


class Message(dict):

    harmonization_config = utils.load_configuration(HARMONIZATION_CONF_FILE)

    def __init__(self, message=None):
        if message:
            super(Message, self).__init__(message)
        else:
            super(Message, self).__init__()

        self.harmonization_config = self.harmonization_config[self.__class__.__name__]


class Report(Message):
    pass
