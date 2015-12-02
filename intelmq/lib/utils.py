# -*- coding: utf-8 -*-
"""
Common utility functions for intelmq.

decode
encode
base64_decode
base64_encode
load_configuration
log
reverse_readline
parse_logline
"""
from __future__ import unicode_literals

import base64
import json
import logging
import os
import re
import six
import sys

from intelmq import DEFAULT_LOGGING_PATH


__all__ = ['decode', 'encode', 'base64_encode', 'base64_decode',
           'load_configuration', 'load_parameters', 'log', 'reverse_readline',
           'parse_logline']

# Used loglines format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FORMAT_STREAM = '%(name)s: %(message)s'

# Regex for parsing the above LOG_FORMAT
LOG_REGEX = (r'^(?P<asctime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) -'
             r' (?P<name>[-\w]+) - '
             r'(?P<levelname>[A-Z]+) - '
             r'(?P<message>.+)$')


class Parameters(object):
    pass


def decode(text, encodings=("utf-8", ), force=False):
    """
    Decode given string to UTF-8 (default).

    Parameters:
    -----------
    text : bytes string
        if unicode string is given, same object is returned
    encodings : iterable of strings
        list/tuple of encodings to use, default ('utf-8')
    force : boolean
        Ignore invalid characters, default: False

    Returns
    -------
    text : unicode string
        unicode string is always returned, even when encoding is ascii
        (Python 3 compat)
    """
    if isinstance(text, six.text_type):
        return text

    for encoding in encodings:
        try:
            return six.text_type(text.decode(encoding))
        except ValueError:
            pass

    if force:
        for encoding in encodings:
            try:
                return six.text_type(text.decode(encoding, 'ignore'))
            except ValueError:
                pass

    raise ValueError("Could not decode string with given encodings{!r}"
                     ".".format(encodings))


def encode(text, encodings=("utf-8", ), force=False):
    """
    Encode given string from UTF-8 (default).

    Parameters:
    -----------
    text : unicode string
        if bytes string is given, same object is returned
    encodings : iterable of strings
        list/tuple of encodings to use, default ('utf-8')
    force : boolean
        Ignore invalid characters, default: False
    """
    if isinstance(text, six.binary_type):
        return text

    for encoding in encodings:
        try:
            return text.encode(encoding)
        except ValueError:
            pass

    if force:
        for encoding in encodings:
            try:
                return text.encode(encoding, 'ignore')
            except ValueError:
                pass

    raise ValueError("Could not encode string with given encodings{!r}"
                     ".".format(encodings))


def base64_decode(value):
    """
    Parameters
    ----------
    value : string
        base 64, will be encoded to bytes if not already.

    Returns
    -------
    retval : unicode string
    """
    return decode(base64.b64decode(encode(value)))


def base64_encode(value):
    """
    Parameters
    ----------
    value : string
        Will be encoded to bytes if not already of type bytes.

    Returns
    -------
    retval : unicode string
    """
    return decode(base64.b64encode(encode(value)))


def load_configuration(configuration_filepath):
    """
    Load JSON configuration file.

    Parameters:
    -----------
    configuration_filepath : string
        Path to JSON file to load

    Returns:
    --------
    config : dict
        Parsed configuration
    """
    with open(configuration_filepath, 'r') as fpconfig:
        config = json.loads(fpconfig.read())
    return config


def load_parameters(*configs):
    """
    Load dictionaries into new Parameters() instance.

    Parameters:
    -----------
    *configs : dict
        Arbitrary number of dictionaries to load.

    Returns:
    --------
    parameters : Parameters
        class instance with items of configs as attributes
    """
    parameters = Parameters()
    for config in configs:
        for option, value in config.items():
            setattr(parameters, option, value)
    return parameters


def log(name, log_path=DEFAULT_LOGGING_PATH, log_level="DEBUG", stream=None):
    """
    Returns a logger instance logging to file and sys.stderr or other stream.

    Parameters:
    -----------
        name : string
            filename for logfile or string preceding lines in stream
        log_path : string
            Path to log directory, defaults to DEFAULT_LOGGING_PATH
        log_level : string
            default is "DEBUG"
        stream : object
            By default (None), stderr will be used, stream objects can be
            given. If False, stream output is not used.

    Returns
    -------
        logger : object
            A `logging` instance.

    See also
    --------
        LOG_FORMAT : string
            Default log format for file handler
        LOG_FORMAT_STREAM : string
            Default log format for stream handler
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    handler = logging.FileHandler("%s/%s.log" % (log_path, name))
    handler.setLevel(log_level)

    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if stream or stream is None:
        console_formatter = logging.Formatter(LOG_FORMAT_STREAM)
        if stream is None:
            console_handler = logging.StreamHandler(sys.stderr)
        else:
            console_handler = logging.StreamHandler(stream)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        console_handler.setLevel(log_level)

    return logger


def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order
    http://stackoverflow.com/a/23646049/2851664"""
    with open(filename) as handle:
        segment = None
        offset = 0
        handle.seek(0, os.SEEK_END)
        total_size = remaining_size = handle.tell()
        while remaining_size > 0:
            offset = min(total_size, offset + buf_size)
            handle.seek(-offset, os.SEEK_END)
            buf = handle.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buf.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first
                if buf[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if len(lines[index]):
                    yield lines[index]
        yield segment


def parse_logline(logline):
    """
    Parses the given logline string into its components.

    Parameters:
    -----------
    logline : string

    Returns:
    --------
    result : dict
        dictionary with keys: ['message', 'name', 'levelname', 'asctime']
    """

    match = re.match(LOG_REGEX, logline)
    result = {}
    fields = ("asctime", "name", "levelname", "message")

    if match:
        result = dict(list(zip(fields, match.group(*fields))))

    return result
