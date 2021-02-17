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
import grp
import gzip
import io
import json
import logging
import logging.handlers
import os
import pwd
import re
import requests
import shutil
import sys
import tarfile
import traceback
import warnings
import zipfile
from typing import Any, Dict, Generator, Iterator, Optional, Sequence, Union

import dateutil.parser
from dateutil.relativedelta import relativedelta
from termstyle import red

import intelmq
from intelmq.lib.exceptions import DecodingError
from intelmq import DEFAULTS_CONF_FILE

__all__ = ['base64_decode', 'base64_encode', 'decode', 'encode',
           'load_configuration', 'load_parameters', 'log', 'parse_logline',
           'reverse_readline', 'error_message_from_exc', 'parse_relative',
           'RewindableFileHandle',
           'file_name_from_response',
           ]

# Used loglines format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FORMAT_STREAM = '%(name)s: %(message)s'
LOG_FORMAT_SYSLOG = '%(name)s: %(levelname)s %(message)s'
LOG_FORMAT_SIMPLE = '%(message)s'

# Regex for parsing the above LOG_FORMAT
LOG_REGEX = (r'^(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) -'
             r' (?P<bot_id>([-\w]+|py\.warnings))'
             r'(?P<thread_id>\.[0-9]+)? - '
             r'(?P<log_level>[A-Z]+) - '
             r'(?P<message>.+)$')
SYSLOG_REGEX = (r'^(?P<date>\w{3} \d{2} \d{2}:\d{2}:\d{2}) (?P<hostname>[-\.\w]+) '
                r'(?P<bot_id>([-\w]+|py\.warnings))'
                r'(?P<thread_id>\.[0-9]+)?'
                r': (?P<log_level>[A-Z]+) (?P<message>.+)$')
RESPONSE_FILENAME = re.compile("filename=(.+)")


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
    exception = None

    for encoding in encodings:
        try:
            return str(text.decode(encoding))
        except ValueError as exc:
            exception = exc

    if force:
        for encoding in encodings:
            try:
                return str(text.decode(encoding, 'ignore'))
            except ValueError as exc:
                exception = exc

    raise DecodingError(encodings=encodings, exception=exception, object=text)


def encode(text: Union[bytes, str], encodings: Sequence[str] = ("utf-8",),
           force: bool = False) -> bytes:
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


def flatten_queues(queues: Union[list, Dict]) -> Iterator[str]:
    """
    Assure that output value will be a flattened.

    Parameters:
        queues: either list [...] or object that contain values of strings and lists {"": str, "": list}.
            As used in the pipeline configuration.

    Returns:
        flattened_queues: queues without dictionaries as values, just lists with the values
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
            config = json.load(fpconfig)
    else:
        raise ValueError('File not found: %r.' % configuration_filepath)
    return config


def write_configuration(configuration_filepath: str,
                        content: dict, backup: bool = True,
                        new=False) -> Optional[bool]:
    """
    Writes a configuration to the file, optionally with making a backup.
    Checks if the file needs to be written at all.
    Accepts dicts as input and formats them like all configurations.

    Parameters:
        configuration_filepath: the path to the configuration file
        content: the configuration itself as dictionary
        backup: make a backup of the file and delete the old backup (default)
        new: If the file is expected to be new, do not attempt to read or backup it.

    Returns:
        True if file has been written successfully
        None if the file content was the same

    Raises:
        In case of errors, e.g. PermissionError
    """
    if not new:
        old_content = load_configuration(configuration_filepath=configuration_filepath)
        if content == old_content:
            return None
    if not new and backup:
        shutil.copy2(configuration_filepath, configuration_filepath + '.bak')
    with open(configuration_filepath, 'w') as handle:
        json.dump(content, fp=handle, indent=4,
                  sort_keys=True,
                  separators=(',', ': '))
        handle.write('\n')


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


class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    shell_color_pattern = re.compile(r'\x1b\[\d+m')

    def emit_print(self, record):
        print(record.msg, record.args)

    def handleError(self, record):
        type, value, traceback = sys.exc_info()
        if type is OSError and value.errno == 28:
            self.emit = self.emit_print
            raise

    def emit(self, record):
        """
        Strips shell colorization from messages
        """
        record.msg = self.shell_color_pattern.sub('', record.msg)
        super().emit(record)


class StreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            if record.levelno < logging.WARNING:  # debug, info
                stream = sys.stdout
                stream.write(msg)
            else:  # warning, error, critical
                stream = sys.stderr
                stream.write(red(msg))
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


class ListHandler(logging.StreamHandler):
    """
    Logging handler which saves the messages in a list which can be accessed with the
    `buffer` attribute.
    """
    buffer = []  # type: list

    def emit(self, record):
        self.buffer.append((record.levelname.lower(), record.getMessage()))


def log(name: str, log_path: Union[str, bool] = intelmq.DEFAULT_LOGGING_PATH,
        log_level: str = intelmq.DEFAULT_LOGGING_LEVEL,
        stream: Optional[object] = None, syslog: Union[bool, str, list, tuple] = None,
        log_format_stream: str = LOG_FORMAT_STREAM,
        logging_level_stream: Optional[str] = None,
        log_max_size: Optional[int] = 0, log_max_copies: Optional[int] = None):
    """
    Returns a logger instance logging to file and sys.stderr or other stream.
    The warnings module will log to the same handlers.

    Parameters:
        name: filename for logfile or string preceding lines in stream
        log_path: Path to log directory, defaults to DEFAULT_LOGGING_PATH
            If False, nothing is logged to files.
        log_level: default is %r
        stream: By default (None), stdout and stderr will be used depending on the level.
            If False, stream output is not used.
            For everything else, the argument is used as stream output.
        syslog:
            If False (default), FileHandler will be used. Otherwise either a list/
            tuple with address and UDP port are expected, e.g. `["localhost", 514]`
            or a string with device name, e.g. `"/dev/log"`.
        log_format_stream:
            The log format used for streaming output. Default: LOG_FORMAT_STREAM
        logging_level_stream:
            The logging level for stream (console) output.
            By default the same as log_level.

    Returns:
        logger: An instance of logging.Logger

    See also:
        LOG_FORMAT: Default log format for file handler
        LOG_FORMAT_STREAM: Default log format for stream handler
        LOG_FORMAT_SYSLOG: Default log format for syslog
    """ % intelmq.DEFAULT_LOGGING_LEVEL
    logging.captureWarnings(True)
    warnings_logger = logging.getLogger("py.warnings")
    # set the name of the warnings logger to the bot neme, see #1184
    warnings_logger.name = name

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logging_level_stream:
        logging_level_stream = log_level

    if log_path and not syslog:
        handler = RotatingFileHandler("%s/%s.log" % (log_path, name),
                                      maxBytes=log_max_size,
                                      backupCount=log_max_copies)
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
    elif syslog:
        if type(syslog) is tuple or type(syslog) is list:
            handler = logging.handlers.SysLogHandler(address=tuple(syslog))
        else:
            handler = logging.handlers.SysLogHandler(address=syslog)
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter(LOG_FORMAT_SYSLOG))

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
        console_handler.setLevel(logging_level_stream)

    return logger


def reverse_readline(filename: str, buf_size=100000) -> Generator[str, None, None]:
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


def parse_logline(logline: str, regex: str = LOG_REGEX) -> Union[dict, str]:
    """
    Parses the given logline string into its components.

    Parameters:
        logline: logline to be parsed
        regex: The regular expression used to parse the line

    Returns:
        result: dictionary with keys: ['date', 'bot_id', 'log_level', 'message']
            or string if the line can't be parsed

    See also:
        LOG_REGEX: Regular expression for default log format of file handler
        SYSLOG_REGEX: Regular expression for log format of syslog
    """

    match = re.match(regex, logline)
    fields = ("date", "bot_id", "thread_id", "log_level", "message")

    try:
        value = dict(list(zip(fields, match.group(*fields))))
        date = dateutil.parser.parse(value['date'])
        value['date'] = date.isoformat()
        if value['date'].endswith('+00:00'):
            value['date'] = value['date'][:-6]
        if value["thread_id"]:
            value["thread_id"] = int(value["thread_id"][1:])
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
        result = re.findall(r'^(\d+)\s+(\w+[^s])s?$', relative_time.strip(), re.UNICODE)
    except ValueError as e:
        raise ValueError("Could not apply regex to attribute \"%s\" with exception %s.",
                         repr(relative_time), repr(e.args))
    if len(result) == 1 and len(result[0]) == 2 and result[0][1] in TIMESPANS:
        return int(result[0][0]) * TIMESPANS[result[0][1]]
    else:
        raise ValueError("Could not process result of regex for attribute " + repr(relative_time))


def extract_tar(file):
    tar = tarfile.open(fileobj=io.BytesIO(file))

    def extract(filename):
        return tar.extractfile(filename).read()

    return tuple(file.name for file in tar.getmembers()), tar, extract


def extract_gzip(file):
    return None, gzip.decompress(file), None


def extract_zip(file):
    zfp = zipfile.ZipFile(io.BytesIO(file), "r")
    return zfp.namelist(), zfp, zfp.read


def unzip(file: bytes, extract_files: Union[bool, list], logger=None,
          try_gzip: bool = True,
          try_zip: bool = True, try_tar: bool = True,
          return_names: bool = False,
          ) -> list:
    """
    Extracts given compressed (tar.)gz file and returns content of specified or all files from it.
    Handles tarfiles, compressed tarfiles and gzipped files.

    First the function tries to handle the file with the tarfile library which handles
    compressed archives too.
    Second, it tries to uncompress the file with gzip.

    Parameters:
        file: a binary representation of compressed file
        extract_files: a value which specifies files to be extracted:
                True: all
                list: some
        logger: optional Logger object
        try_gzip: Try to uncompress the file using gzip, default: True
        try_zip: Try to uncompress and extract files using zip, default: True
        try_tar: Try to uncompress and extract files using tar, default: True
        return_names: If true, return tuples of (file name, file content) instead of
            only the file content.
            False by default

    Returns:
        result: tuple containing the string representation of specified files
            if extract_names is True, each element is a tuple of file name and the file content

    Raises:
        TypeError: If file isn't tar.gz
    """
    for tryit, name, function in zip((try_zip, try_tar, try_gzip),
                                     ('zip', 'tar', 'gzip'),
                                     (extract_zip, extract_tar, extract_gzip)):
        if not tryit:
            continue
        try:
            files, archive, extract_function = function(file)
        except Exception as exc:
            if logger:
                logger.debug("Uncompression using %s failed with: %s.",
                             name, exc)
        else:
            if logger:
                logger.debug('Detected %s archive.', name)
            break
    else:
        raise ValueError("Failed to uncompress the given file.")

    if files is None:
        if return_names:
            return ((None, archive),)
        else:
            return (archive,)

    if logger:
        logger.debug("Found files %r in archive.", files)

    if isinstance(extract_files, bool):
        extract_files = files
    if logger:
        logger.debug("Extracting %r from archive.", extract_files)

    if return_names:
        return ((filename, extract_function(filename))
                for filename in files
                if filename in extract_files)
    else:
        return (extract_function(filename)
                for filename in files
                if filename in extract_files)


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


def object_pair_hook_bots(*args, **kwargs) -> Dict:
    """
    A object_pair_hook function for the BOTS file to be used in the json's dump functions.

    Usage: BOTS = json.loads(raw, object_pairs_hook=object_pair_hook_bots)

    """
    # Do not sort collector bots
    if len(args[0]) and len(args[0][0]) == 2 and isinstance(args[0][0][1], dict) and \
            'module' in args[0][0][1] and '.collectors' in args[0][0][1]['module']:
        return collections.OrderedDict(*args, **kwargs)
    # Do not sort bot groups
    if len(args[0]) and len(args[0][0]) and len(args[0][0][0]) and args[0][0][0] == 'Collector':
        return collections.OrderedDict(*args, **kwargs)
    return dict(sorted(*args), **kwargs)


def seconds_to_human(seconds: int, precision: int = 0) -> str:
    """
    Converts second count to a human readable description.
    >>> seconds_to_human(60)
    "1m"
    >>> seconds_to_human(3600)
    "1h"
    >>> seconds_to_human(3601)
    "1h 0m 1s"
    """
    relative = relativedelta(seconds=seconds)
    result = []
    for frame in ('days', 'hours', 'minutes', 'seconds'):
        if getattr(relative, frame):
            result.append('%.{}f%s'.format(precision) % (getattr(relative, frame), frame[0]))
    return ' '.join(result)


def drop_privileges() -> bool:
    """
    Checks if the current user is root. If yes, it tries to change to intelmq user and group.

    returns:
        success: If the drop of privileges did work
    """
    if os.geteuid() == 0:
        try:
            os.setgid(grp.getgrnam('intelmq').gr_gid)
            os.setuid(pwd.getpwnam('intelmq').pw_uid)
        except (OSError, KeyError):
            # KeyError: User or group 'intelmq' does not exist
            return False
    if os.geteuid() != 0:  # For the unprobably possibility that intelmq is root
        return True
    return False


def setup_list_logging(name: str = 'intelmq', logging_level: str = 'INFO'):
    check_logger = logging.getLogger('check')  # name does not matter
    list_handler = ListHandler()
    list_handler.setLevel('INFO')
    check_logger.addHandler(list_handler)
    check_logger.setLevel('INFO')
    return check_logger, list_handler


def version_smaller(version1: tuple, version2: tuple) -> Optional[bool]:
    """
    Parameters:
        version1: A tuple of integer and string values
        version2: Same as version1
        Integer values are expected as integers (__version_info__).

    Returns:
        True if version1 is smaller
        False if version1 is greater
        None if both are equal
    """
    if len(version1) == 3:
        version1 = version1 + ('stable', 0)
    if len(version1) == 4:
        version1 = version1 + (0,)
    if len(version2) == 3:
        version2 = version2 + ('stable', 0)
    if len(version2) == 4:
        version2 = version2 + (0,)
    for level1, level2 in zip(version1, version2):
        if level1 > level2:
            return False
        if level1 < level2:
            return True
    return None


def lazy_int(value: Any) -> Optional[Any]:
    """
    Tries to convert the value to int if possible. Original value otherwise
    """
    try:
        return int(value)
    except ValueError:
        return value


class TimeoutHTTPAdapter(requests.adapters.HTTPAdapter):
    """
    A requests-HTTP Adapter which can set the timeout generally.
    """

    def __init__(self, *args, timeout=None, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        return super().send(*args, **kwargs)


def create_request_session_from_bot(bot: type) -> requests.Session:
    warnings.warn("This function is deprecated in favor of create_request_session"
                  " and will be removed in version 3.0.0.",
                  DeprecationWarning)
    return create_request_session(bot)


def create_request_session(bot: type = None) -> requests.Session:
    """
    Creates a requests.Session object preconfigured with the parameters
    set by the Bot.set_request_parameters and given by the bot instance.
    If no bot is specified then the Session is preconfigured only with
    parameters from defaults.conf.

    Parameters:
        bot_instance: An instance of a Bot

    Returns:
        session: A preconfigured instance of requests.Session
    """
    defaults = load_configuration(DEFAULTS_CONF_FILE)
    session = requests.Session()

    # tls settings
    if bot and hasattr(bot, 'http_verify_cert'):
        session.verify = bot.http_verify_cert
    else:
        defaults.get('http_verify_cert', True)

    # tls certificate settings
    if bot and hasattr(bot, 'ssl_client_cert'):
        session.cert = bot.ssl_client_cert

    # auth settings
    if bot and hasattr(bot, 'auth'):
        session.auth = bot.auth

    # headers settings
    if bot and hasattr(bot, 'http_header'):
        session.headers.update(bot.http_header)
    elif defaults.get('http_user_agent'):
        session.headers.update({"User-Agent": defaults.get('http_user_agent')})

    # proxy settings
    if bot and hasattr(bot, 'proxy'):
        session.proxies = bot.proxy
    elif defaults.get('http_proxy') and defaults.get('https_proxy'):
        session.proxies = {
            'http': defaults.get('http_proxy'),
            'https': defaults.get('https_proxy')
        }

    # timeout settings
    if bot and hasattr(bot, 'http_timeout_max_tries'):
        max_retries = bot.http_timeout_max_tries - 1
    else:
        max_retries = defaults.get('http_timeout_max_tries', 3)

    if bot and hasattr(bot, 'http_timeout_sec'):
        timeout = bot.http_timeout_sec
    else:
        timeout = defaults.get('http_timeout_sec', 30)

    adapter = TimeoutHTTPAdapter(max_retries=max_retries, timeout=timeout)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session


def file_name_from_response(response: requests.Response) -> str:
    """
    Extract the file name from the Content-Disposition header of the Response object
    or the URL as fallback

    Parameters:
        response: a Response object retrieved from a call with the requests library

    Returns:
        file_name: The file name
    """
    try:
        file_name = RESPONSE_FILENAME.findall(response.headers["Content-Disposition"])[0]
    except KeyError:
        file_name = response.url.split("/")[-1]
    return file_name
