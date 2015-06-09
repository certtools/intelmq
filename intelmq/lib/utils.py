import logging
import hashlib


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


def log(logs_path, name, loglevel="DEBUG"):
    """Creates a new logger with given logs_path/name"""
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)

    handler = logging.FileHandler("%s/%s.log" % (logs_path, name))
    handler.setLevel(loglevel)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def hashgen(data, func=hashlib.sha1):
    """Generates a hash string based on the given data"""
    result = func()
    result.update(data)
    return result.hexdigest()
