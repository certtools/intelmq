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
import collections
import io
import json
import logging
import logging.handlers
import os
import re
import sys
import tarfile
import traceback
from typing import Sequence, Optional, Union, Generator

import dateutil.parser
import pytz

import intelmq

__all__ = ['base64_decode', 'base64_encode', 'decode', 'encode',
           'load_configuration', 'load_parameters', 'log', 'parse_logline',
           'reverse_readline', 'error_message_from_exc', 'parse_relative',
           'RewindableFileHandle',
           ]

# Used loglines format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FORMAT_STREAM = '%(name)s: %(message)s'
LOG_FORMAT_SYSLOG = '%(name)s: %(levelname)s %(message)s'

# Regex for parsing the above LOG_FORMAT
LOG_REGEX = (r'^(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) -'
             r' (?P<bot_id>([-\w]+|py\.warnings)) - '
             r'(?P<log_level>[A-Z]+) - '
             r'(?P<message>.+)$')
SYSLOG_REGEX = (r'^(?P<date>\w{3} \d{2} \d{2}:\d{2}:\d{2}) (?P<hostname>[-\.\w]+) '
                r'(?P<bot_id>([-\w]+|py\.warnings)): (?P<log_level>[A-Z]+) (?P<message>.+)$')


class Parameters(object):
    pass


def decode(text: Union[bytes, str], encodings: Sequence[str] = ("utf-8",),
           force: bool = False) -> str:
    """
    Decode given string to UTF-8 (default).

    Parameters:
        text: if unicode string is given, same object is returned
        encodings: list/tuple of encodings to use
        force: Ignore invalid characters

    Returns:
        converted unicode string

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


def encode(text: Union[bytes, str], encodings: Sequence[str] = ("utf-8",),
           force: bool = False) -> str:
    """
    Encode given string from UTF-8 (default).

    Parameters:
        text: if bytes string is given, same object is returned
        encodings: list/tuple of encodings to use
        force: Ignore invalid characters

    Returns:
        converted bytes string

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


def flatten_queues(queues) -> Generator[str, None, None]:
    """
    Assure that output value will be a flattened.

    Parameters:
        queues: either list [...] or object that that contain values of strings and lists {"": str, "": list}

    """
    return (item for sublist in (queues.values() if type(queues) is dict else queues) for item in
            (sublist if type(sublist) is list else [sublist]))


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
            if record.levelno < logging.WARNING:  # debug, info
                stream = sys.stdout
            else:  # warning, error, critical
                stream = sys.stderr
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


def log(name: str, log_path: str = intelmq.DEFAULT_LOGGING_PATH, log_level: str = "DEBUG",
        stream: Optional[object] = None, syslog: Union[bool, str, list, tuple] = None,
        log_format_stream: str = LOG_FORMAT_STREAM):
    """
    Returns a logger instance logging to file and sys.stderr or other stream.
    The warnings module will log to the same handlers.

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
        log_format_stream:
            The log format used for streaming output. Default: LOG_FORMAT_STREAM

    Returns:
        logger: An instance of logging.Logger

    See also:
        LOG_FORMAT: Default log format for file handler
        LOG_FORMAT_STREAM: Default log format for stream handler
        LOG_FORMAT_SYSLOG: Default log format for syslog
    """
    logging.captureWarnings(True)
    warnings_logger = logging.getLogger("py.warnings")
    # set the name of the warnings logger to the bot neme, see #1184
    warnings_logger.name = name

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if log_path and not syslog:
        handler = FileHandler("%s/%s.log" % (log_path, name))
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
    elif syslog:
        if type(syslog) is tuple or type(syslog) is list:
            handler = logging.handlers.SysLogHandler(address=tuple(syslog))
        else:
            handler = logging.handlers.SysLogHandler(address=syslog)
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter(LOG_FORMAT_SYSLOG))
    else:
        raise ValueError("Invalid configuration, neither log_path is given nor syslog is used.")

    if log_path or syslog:
        logger.addHandler(handler)
        warnings_logger.addHandler(handler)

    if stream or stream is None:
        console_formatter = logging.Formatter(log_format_stream)
        if stream is None:
            console_handler = StreamHandler()
        else:
            console_handler = logging.StreamHandler(stream)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        warnings_logger.addHandler(console_handler)
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


def parse_logline(logline: str, regex: str = LOG_REGEX) -> dict:
    """
    Parses the given logline string into its components.

    Parameters:
        logline: logline to be parsed
        regex: The regular expression used to parse the line

    Returns:
        result: dictionary with keys: ['date', 'bot_id', 'log_level', 'message']

    See also:
        LOG_REGEX: Regular expression for default log format of file handler
        SYSLOG_REGEX: Regular expression for log format of syslog
    """

    match = re.match(regex, logline)
    fields = ("date", "bot_id", "log_level", "message")

    try:
        value = dict(list(zip(fields, match.group(*fields))))
        date = dateutil.parser.parse(value['date'])
        try:
            date = date.astimezone(pytz.utc)
        except ValueError:  # astimezone() cannot be applied to a naive datetime
            pass
        value['date'] = date.isoformat()
        if value['date'].endswith('+00:00'):
            value['date'] = value['date'][:-6]
        return value
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


# number of minutes in time units
TIMESPANS = {'hour': 60, 'day': 24 * 60, 'week': 7 * 24 * 60,
             'month': 30 * 24 * 60, 'year': 365 * 24 * 60}


def parse_relative(relative_time: str) -> int:
    """
    Parse relative time attributes and returns the corresponding minutes.

    >>> parse_relative('4 hours')
    240

    Parameters:
        relative_time: a string holding a relative time specification

    Returns:
        result: Minutes

    Raises:
        ValueError: If relative_time is not parseable

    See also:
        TIMESPANS: Defines the conversion of verbal timespans to minutes
    """
    try:
        result = re.findall(r'^(\d+)\s+(\w+[^s])s?$', relative_time, re.UNICODE)
    except ValueError as e:
        raise ValueError("Could not apply regex to attribute \"%s\" with exception %s.",
                         repr(relative_time), repr(e.args))
    if len(result) == 1 and len(result[0]) == 2 and result[0][1] in TIMESPANS:
        return int(result[0][0]) * TIMESPANS[result[0][1]]
    else:
        raise ValueError("Could not process result of regex for attribute " + repr(relative_time))


def extract_tar(file: bytes, extract_files: Union[bool, list]) -> list:
    """
        Extracts given compressed tar.gz file and returns content of specified or all files from it.

        Parameters:
            file: a binary representation of compressed file
            extract_files: a value which specifies files to be extracted:
                    True: all
                    list: some

        Returns:
            result: list containing the string representation of specified files

        Raises:
            TypeError: If file isn't tar.gz
    """
    try:
        tar = tarfile.open(fileobj=io.BytesIO(file))
    except tarfile.TarError as te:
        raise TypeError("Could not process given file" + repr(te.args))

    if isinstance(extract_files, bool):
        extract_files = [file.name for file in tar.getmembers()]

    return [tar.extractfile(member).read() for member in tar.getmembers() if member.name in extract_files]


class RewindableFileHandle(object):
    """
    Can be used for easy retrieval of last input line to populate raw field
    during CSV parsing.
    """

    def __init__(self, f):
        self.f = f
        self.current_line = None
        self.first_line = None

    def __iter__(self):
        return self

    def __next__(self):
        self.current_line = next(self.f)
        if self.first_line is None:
            self.first_line = self.current_line
        return self.current_line


def object_pair_hook_bots(*args, **kwargs):
    """
    A object_pair_hook function for the BOTS file to be used in the json's dump functions.

    Usage: BOTS = json.loads(raw, object_pairs_hook=object_pair_hook_bots)

    """
    # Do not sort collector bots
    if len(args[0]) and len(args[0][0]) == 2 and isinstance(args[0][0][1], dict) and\
            'module' in args[0][0][1] and '.collectors' in args[0][0][1]['module']:
        return collections.OrderedDict(*args, **kwargs)
    # Do not sort bot groups
    if len(args[0]) and len(args[0][0]) and len(args[0][0][0]) and args[0][0][0] == 'Collector':
        return collections.OrderedDict(*args, **kwargs)
    return dict(sorted(*args), **kwargs)
