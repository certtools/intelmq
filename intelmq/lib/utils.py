import logging
import hashlib
import re


def decode(text, encodings=["utf-8", "ISO-8859-15"], force=False):
    """Returns the given text with the given encodings,
       else it raises an exception"""
    for encoding in encodings:
        try:
            return text.decode(encoding)
        except ValueError as e:
            pass

    if force:
        for encoding in encodings:
            try:
                return text.decode(encoding, 'ignore')
            except ValueError as e:
                pass

    raise Exception("Found a problem when decoding.")


def encode(text, encodings=["utf-8"], force=False):
    """Returns the given text encoded using the given encodings,
        else it raises an exception"""
    for encoding in encodings:
        try:
            return text.encode(encoding)
        except ValueError as e:
            pass

    if force:
        for encoding in encodings:
            try:
                return text.decode(encoding, 'ignore')
            except ValueError as e:
                pass

    raise Exception("Found a problem when encoding.")


# Used loglines format
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Regex for parsing the above log_format
log_regex  = ('^(?P<asctime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) -'
              ' (?P<name>[-\w]+) - '
              '(?P<levelname>[A-Z]+) - '
              '(?P<message>.+)$')

def create_file_logger(logs_path, name, loglevel="DEBUG"):
    """Creates a logger specific for files with IntelMQ logging format"""

    # create_file_logger is the same as create_stream_logger,
    # the only difference is that one creates a logger for a
    # stream and the other creates a logger for a file
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)

    handler = logging.FileHandler("%s/%s.log" % (logs_path, name))
    handler.setLevel(loglevel)

    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

log = create_file_logger  # alias for create_file_logger, remove if desired


def create_stream_logger(stream, name, loglevel="DEBUG"):
    """Creates a logger object for stream logging.
        Everything else behaves like create_file_logger"""

    # create_file_logger is the same as create_stream_logger,
    # the only difference is that one creates a logger for a
    # stream and the other creates a logger for a file
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)

    handler = logging.StreamHandler(stream)
    handler.setLevel(loglevel)

    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def parse_logline(logline):
    """Parses the given logline string into its components"""

    match = re.match(log_regex, logline)
    result = {}
    fields = ("asctime", "name", "levelname", "message")

    if match:
        result = dict(zip(fields, match.group(*fields)))

    return result


def hashgen(data, func=hashlib.sha1):
    """Generates a hash string based on the given data"""
    result = func()
    result.update(data)
    return result.hexdigest()
