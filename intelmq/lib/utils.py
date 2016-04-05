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
import csv
import io
import json
import logging
import logging.handlers
import os
import pkg_resources
import re
import sys

import intelmq
import six

try:
    import unicodecsv
except ImportError:
    unicodecsv = None


__all__ = ['base64_decode', 'base64_encode', 'decode', 'encode',
           'load_configuration', 'load_parameters', 'log', 'parse_logline',
           'reverse_readline',
           ]

# Used loglines format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FORMAT_STREAM = '%(name)s: %(message)s'

# Regex for parsing the above LOG_FORMAT
LOG_REGEX = (r'^(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) -'
             r' (?P<bot_id>[-\w]+) - '
             r'(?P<log_level>[A-Z]+) - '
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

    Notes
    -----
    Possible bytes - unicode conversions problems are ignored.
    """
    return decode(base64.b64decode(encode(value, force=True)), force=True)


def base64_encode(value):
    """
    Parameters
    ----------
    value : string
        Will be encoded to bytes if not already of type bytes.

    Returns
    -------
    retval : unicode string

    Notes
    -----
    Possible bytes - unicode conversions problems are ignored.
    """
    return decode(base64.b64encode(encode(value, force=True)), force=True)


def load_configuration(configuration_filepath):
    """
    Load JSON configuration file.

    Parameters:
    -----------
    configuration_filepath : string
        Path to JSON file to load. If file does not exist, and the path begins
        with CONFIG_DIR (`/opt/intelmq/etc` by default), the file from it's
        package data is used.

    Returns:
    --------
    config : dict
        Parsed configuration
    """
    if os.path.exists(configuration_filepath):
        with open(configuration_filepath, 'r') as fpconfig:
            config = json.loads(fpconfig.read())
    elif configuration_filepath.find(intelmq.CONFIG_DIR) == 0:  # at beginning
        newpath = pkg_resources.resource_filename('intelmq', 'etc/')
        filepath = configuration_filepath.replace(intelmq.CONFIG_DIR,
                                                  newpath)
        if os.path.exists(filepath):
            with open(filepath, 'r') as fpconfig:
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


def log(name, log_path=intelmq.DEFAULT_LOGGING_PATH, log_level="DEBUG",
        stream=None, syslog=None):
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
    syslog: boolean, list/tuple, string
        If False (default), FileHandler will be used. Otherwise either a list/
        tuple with address and UDP port are expected, e.g. `["localhost", 514]`
        or a string with device name, e.g. `"/dev/log"`.

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

    if not syslog:
        handler = logging.FileHandler("%s/%s.log" % (log_path, name))
        handler.setLevel(log_level)
    else:
        if type(syslog) is tuple or type(syslog) is list:
            handler = logging.handlers.SysLogHandler(address=tuple(syslog))
        else:
            handler = logging.handlers.SysLogHandler(address=syslog)
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


def reverse_readline(filename, buf_size=100000):
    """
    https://github.com/certtools/intelmq/issues/393#issuecomment-154041996

    """
    with open(filename) as qfile:
        qfile.seek(0, os.SEEK_END)
        position = totalsize = qfile.tell()
        line = ''
        number = 0
        if buf_size < position:
            qfile.seek(totalsize - buf_size - 1)
            char = qfile.read(1)
            while char != '\n':
                char = qfile.read(1)
            number = totalsize - buf_size
        while position >= number:
            qfile.seek(position)
            next_char = qfile.read(1)
            if next_char == "\n":
                yield line[::-1]
                line = ''
            else:
                line += next_char
            position -= 1
        yield line[::-1]


def parse_logline(logline):
    """
    Parses the given logline string into its components.

    Parameters:
    -----------
    logline : string

    Returns:
    --------
    result : dict
        dictionary with keys: ['date', 'bot_id', 'log_level', 'message']
    """

    match = re.match(LOG_REGEX, logline)
    fields = ("date", "bot_id", "log_level", "message")

    try:
        return dict(list(zip(fields, match.group(*fields))))
    except AttributeError:
        return logline


def csv_reader(csv_data, dialect=csv.excel, dictreader=False, **kwargs):
    """
    Reads data from given string and parses as utf8.
    Only needed for Legcay Python, version 2.
    """
    if six.PY2:
        if unicodecsv is None:
            raise ValueError('Module unicodecsv is not available.')
        if dictreader:
            for row in unicodecsv.DictReader(io.BytesIO(csv_data), **kwargs):
                yield row
        else:
            for row in unicodecsv.reader(io.BytesIO(encode(csv_data)),
                                         **kwargs):
                yield row
    else:
        if dictreader:
            for row in csv.DictReader(io.StringIO(csv_data), **kwargs):
                yield row
        else:
            for row in csv.reader(io.StringIO(csv_data), **kwargs):
                yield row
