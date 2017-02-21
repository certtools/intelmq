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
import base64
import json
import logging
import logging.handlers
import os
import re
import sys
import traceback

from typing import Sequence, Union

import intelmq

__all__ = ['base64_decode', 'base64_encode', 'decode', 'encode',
           'load_configuration', 'load_parameters', 'log', 'parse_logline',
           'reverse_readline', 'error_message_from_exc',
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


def decode(text: Union[bytes, str], encodings: Sequence[str]=("utf-8", ),
           force: bool=False) -> str:
    """
    Decode given string to UTF-8 (default).

    Parameters:
        text: if unicode string is given, same object is returned
        encodings: list/tuple of encodings to use
        force: Ignore invalid characters

    Returns:
        text: converted unicode string

    Raises:
        ValueError: if decoding failed
    """
    if isinstance(text, str):
        return text

    for encoding in encodings:
        try:
            return str(text.decode(encoding))
        except ValueError:
            pass

    if force:
        for encoding in encodings:
            try:
                return str(text.decode(encoding, 'ignore'))
            except ValueError:
                pass

    raise ValueError("Could not decode string with given encodings{!r}"
                     ".".format(encodings))


def encode(text: Union[bytes, str], encodings: Sequence[str]=("utf-8", ),
           force: bool=False) -> str:
    """
    Encode given string from UTF-8 (default).

    Parameters:
        text: if bytes string is given, same object is returned
        encodings: list/tuple of encodings to use
        force: Ignore invalid characters

    Returns
        text: converted bytes string

    Raises:
        ValueError: if encoding failed
    """
    if isinstance(text, bytes):
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


def base64_decode(value: Union[bytes, str]) -> str:
    """
    Parameters:
        value: base64 encoded string

    Returns:
        retval: decoded string

    Notes:
        Possible bytes - unicode conversions problems are ignored.
    """
    return decode(base64.b64decode(encode(value, force=True)), force=True)


def base64_encode(value: Union[bytes, str]) -> str:
    """
    Parameters:
        value: string to be encoded

    Returns:
        retval: base64 representation of value

    Notes:
        Possible bytes - unicode conversions problems are ignored.
    """
    return decode(base64.b64encode(encode(value, force=True)), force=True)


def load_configuration(configuration_filepath: str) -> dict:
    """
    Load JSON configuration file.

    Parameters:
        configuration_filepath: Path to JSON file to load.

    Returns:
        config: Parsed configuration

    Raises:
        ValueError: if file not found
    """
    if os.path.exists(configuration_filepath):
        with open(configuration_filepath, 'r') as fpconfig:
            config = json.loads(fpconfig.read())
    else:
        raise ValueError('File not found: %r.' % configuration_filepath)
    return config


def load_parameters(*configs: dict) -> Parameters:
    """
    Load dictionaries into new Parameters() instance.

    Parameters:
        *configs: Arbitrary number of dictionaries to load.

    Returns:
        parameters: class instance with items of configs as attributes
    """
    parameters = Parameters()
    for config in configs:
        for option, value in config.items():
            setattr(parameters, option, value)
    return parameters


class FileHandler(logging.FileHandler):
    def emit_print(self, record):
        print(record.msg, record.args)

    def handleError(self, record):
        type, value, traceback = sys.exc_info()
        if type is OSError and value.errno == 28:
            self.emit = self.emit_print
            raise


class StreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            if record.levelno < 30:  # Lower than warning (debug, info)
                stream = sys.stdout
            else:  # (warning, error, critical)
                stream = sys.stderr
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


def log(name: str, log_path: str=intelmq.DEFAULT_LOGGING_PATH, log_level: str="DEBUG",
        stream: Union[None, object]=None, syslog: Union[bool, str, list, tuple]=None):
    """
    Returns a logger instance logging to file and sys.stderr or other stream.

    Parameters:
        name: filename for logfile or string preceding lines in stream
        log_path: Path to log directory, defaults to DEFAULT_LOGGING_PATH
            If False, nothing is logged to files.
        log_level: default is "DEBUG"
        stream: By default (None), stderr will be used, stream objects can be
            given. If False, stream output is not used.
        syslog:
            If False (default), FileHandler will be used. Otherwise either a list/
            tuple with address and UDP port are expected, e.g. `["localhost", 514]`
            or a string with device name, e.g. `"/dev/log"`.

    Returns:
        logger: An instance of logging.Logger

    See also:
        LOG_FORMAT: Default log format for file handler
        LOG_FORMAT_STREAM: Default log format for stream handler
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if log_path and not syslog:
        handler = FileHandler("%s/%s.log" % (log_path, name))
        handler.setLevel(log_level)
    elif syslog:
        if type(syslog) is tuple or type(syslog) is list:
            handler = logging.handlers.SysLogHandler(address=tuple(syslog))
        else:
            handler = logging.handlers.SysLogHandler(address=syslog)
        handler.setLevel(log_level)

    if log_path or syslog:
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if stream or stream is None:
        console_formatter = logging.Formatter(LOG_FORMAT_STREAM)
        if stream is None:
            console_handler = StreamHandler()
        else:
            console_handler = logging.StreamHandler(stream)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        console_handler.setLevel(log_level)

    return logger


def reverse_readline(filename: str, buf_size=100000) -> str:
    """
    See also:
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


def parse_logline(logline: str) -> dict:
    """
    Parses the given logline string into its components.

    Parameters:
        logline: logline to be parsed

    Returns:
        result: dictionary with keys: ['date', 'bot_id', 'log_level', 'message']
    """

    match = re.match(LOG_REGEX, logline)
    fields = ("date", "bot_id", "log_level", "message")

    try:
        return dict(list(zip(fields, match.group(*fields))))
    except AttributeError:
        return logline


def error_message_from_exc(exc: Exception) -> str:
    """
    >>> exc = IndexError('This is a test')
    >>> error_message_from_exc(exc)
    'This is a test'

    Parameters:
        exc

    Returns:
        result: The error message of exc
    """
    return traceback.format_exception_only(type(exc), exc)[-1].strip().replace(type(exc).__name__ + ': ', '')
