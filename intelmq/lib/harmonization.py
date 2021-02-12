# -*- coding: utf-8 -*-
"""
The following types are implemented with sanitize() and is_valid() functions:

 - Base64
 - Boolean
 - ClassificationType
 - DateTime
 - FQDN
 - Float
 - Accuracy
 - GenericType
 - IPAddress
 - IPNetwork
 - Integer
 - JSON
 - JSONDict
 - LowercaseString
 - Registry
 - String
 - URL
 - ASN
 - UppercaseString
 - TLP
"""
import binascii
import datetime
import ipaddress
import json
import re
import socket
import sys
import urllib.parse as parse

import dateutil.parser
import dns.resolver
import pytz

import intelmq.lib.utils as utils

from typing import Optional, Union

__all__ = ['Base64', 'Boolean', 'ClassificationType', 'DateTime', 'FQDN',
           'Float', 'Accuracy', 'GenericType', 'IPAddress', 'IPNetwork',
           'Integer', 'JSON', 'JSONDict', 'LowercaseString', 'Registry',
           'String', 'URL', 'ASN', 'UppercaseString', 'TLP',
           ]


class GenericType(object):

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = GenericType().sanitize(value)

        if not value:
            return False

        if not isinstance(value, str):
            return False

        if len(value) == 0:
            return False

        return True

    @staticmethod
    def sanitize(value) -> Optional[str]:
        if not value:
            return None

        if isinstance(value, str):
            return value.strip()

        if isinstance(value, bytes):
            try:
                value = value.decode('utf-8')
            except UnicodeDecodeError:
                value = value.decode('utf-8', 'ignore')
            return value.strip()

        return str(value)


class String(GenericType):
    """
    Any non-empty string without leading or trailing whitespace.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = GenericType().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if type(value) is not str:
            return False

        if len(value) == 0:
            return False

        return True


class Base64(String):
    """
    Base64 type. Always gives unicode strings.

    Sanitation encodes to base64 and accepts binary and unicode strings.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = Base64().sanitize(value)

        try:
            utils.base64_decode(value)
        except (TypeError, AttributeError):
            return False

        if not GenericType().is_valid(value):
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        try:
            value = utils.base64_encode(value)
        except AttributeError:  # None
            return None
        return value


class Boolean(GenericType):
    """
    Boolean type. Without sanitation only python bool is accepted.

    Sanitation accepts string 'true' and 'false' and integers 0 and 1.
    """

    @staticmethod
    def is_valid(value: bool, sanitize: bool = False) -> bool:
        if isinstance(value, bool):
            return True
        else:
            if sanitize:
                value = Boolean().sanitize(value)
                if value is not None:
                    return True
            return False

    @staticmethod
    def sanitize(value: bool) -> Optional[bool]:
        if isinstance(value, (str, bytes)):
            value = value.strip().lower()
            if value == 'true':
                return True
            elif value == 'false':
                return False
        elif isinstance(value, int):
            if value == 0:
                return False
            elif value == 1:
                return True
        return None


class ClassificationType(String):
    """
    `classification.type` type.

    The mapping follows
    Reference Security Incident Taxonomy Working Group – RSIT WG
    https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/
    with extensions.

    These old values are automatically mapped to the new ones:
        'botnet drone' -> 'infected-system'
        'ids alert' -> 'ids-alert'
        'c&c' -> 'c2server'
        'infected system' -> 'infected-system'
        'malware configuration' -> 'malware-configuration'

    Allowed values are:
     * """

    allowed_values = ["application-compromise",
                      'backdoor',
                      'blacklist',
                      'brute-force',
                      "burglary",
                      'c2server',
                      'compromised',
                      "copyright",
                      "data-loss",
                      'ddos',
                      "ddos-amplifier",
                      'defacement',
                      'dga domain',
                      "dos",
                      'dropzone',
                      'exploit',
                      'harmful-speech',
                      'ids-alert',
                      'infected-system',
                      "information-disclosure",
                      'leak',
                      'malware',
                      'malware-configuration',
                      'malware-distribution',
                      "masquerade",
                      'other',
                      'outage',
                      'phishing',
                      "potentially-unwanted-accessible",
                      "privileged-account-compromise",
                      'proxy',
                      'ransomware',
                      'sabotage',
                      'scanner',
                      'sniffing',
                      'social-engineering',
                      'spam',
                      'test',
                      'tor',
                      "Unauthorised-information-access",
                      "Unauthorised-information-modification",
                      'unauthorized-command',
                      'unauthorized-login',
                      "unauthorized-use-of-resources",
                      'unknown',
                      "unprivileged-account-compromise",
                      'violence',
                      'vulnerable client',
                      'vulnerable service',
                      "vulnerable-system",
                      "weak-crypto",
                      ]

    __doc__ += '\n     * '.join(allowed_values)

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = ClassificationType().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if not isinstance(value, str):
            return False

        if value not in ClassificationType().allowed_values:
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        value = LowercaseString.sanitize(value)
        if not value:
            return None
        if value == 'botnet drone':
            value = 'infected-system'
        elif value == 'ids alert':
            value = 'ids-alert'
        elif value == 'c&c':
            value = 'c2server'
        elif value == 'infected system':
            value = 'infected-system'
        elif value == 'malware configuration':
            value = 'malware-configuration'
        return GenericType().sanitize(value)


class DateTime(String):
    """
    Date and time type for timestamps.

    Valid values are timestamps with time zone and in the format '%Y-%m-%dT%H:%M:%S+00:00'.
    Invalid are missing times and missing timezone information (UTC).
    Microseconds are also allowed.

    Sanitation normalizes the timezone to UTC, which is the only allowed timezone.

    The following additional conversions are available with the convert function:
    """
    midnight = datetime.time(0, 0, 0, 0)

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = DateTime().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if value != DateTime.__parse(value):
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        try:
            value = DateTime.__parse(value)
        except TypeError:  # None
            return None
        return GenericType().sanitize(value)

    @staticmethod
    def __parse(value: str) -> Optional[str]:
        try:
            DateTime.parse_utc_isoformat(value)
        except ValueError:
            pass
        else:
            return utils.decode(value)

        try:
            value = dateutil.parser.parse(value, fuzzy=True)
            value = value.astimezone(pytz.utc)
            value = value.isoformat()
        except (ValueError, OverflowError):
            return None
        return utils.decode(value)

    @staticmethod
    def parse_utc_isoformat(value: str, return_datetime: bool = False) -> Union[datetime.datetime, str]:
        """
        Parse format generated by datetime.isoformat() method with UTC timezone.
        It is much faster than universal dateutil parser.
        Can be used for parsing DateTime fields which are already parsed.

        Returns a string with ISO format.
        If return_datetime is True, the return value is a datetime.datetime object.
        """
        try:
            dtvalue = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+00:00')
        except ValueError:
            # With microseconds
            dtvalue = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f+00:00')

        if return_datetime:
            return pytz.utc.localize(dtvalue)
        else:
            return value

    @staticmethod
    def from_epoch_millis(tstamp: str, tzone='UTC') -> datetime.datetime:
        """
        Returns ISO formatted datetime from given epoch timestamp with milliseconds.
        It ignores the milliseconds, converts it into normal timestamp and processes it.
        """
        bytecount = len(str(tstamp))
        int_tstamp = int(tstamp)
        if bytecount == 10:
            return DateTime.from_timestamp(int_tstamp, tzone)
        if bytecount == 12:
            return DateTime.from_timestamp(int_tstamp // 100, tzone)
        if bytecount == 13:
            return DateTime.from_timestamp(int_tstamp // 1000, tzone)

    @staticmethod
    def from_timestamp(tstamp: int, tzone='UTC') -> str:
        """
        Returns ISO formatted datetime from given timestamp.
        You can give timezone for given timestamp, UTC by default.
        """
        dtime = (datetime.datetime(1970, 1, 1, tzinfo=pytz.utc) +
                 datetime.timedelta(seconds=tstamp))
        localized = pytz.timezone(tzone).normalize(dtime)
        return str(localized.isoformat())

    @staticmethod
    def from_windows_nt(tstamp: int) -> str:
        """
        Converts the Windows NT / LDAP / Active Directory format to ISO format.

        The format is: 100 nanoseconds (10^-7s) since 1601-01-01.
        UTC is assumed.

        Parameters:
            tstamp: Time in LDAP format as integer or string. Will be converted if necessary.

        Returns:
            Converted ISO format string

        See also:
            https://www.epochconverter.com/ldap
        """
        epoch = datetime.datetime(1601, 1, 1, tzinfo=pytz.utc)
        dtime = epoch + datetime.timedelta(seconds=int(tstamp) * 10**-7)
        return dtime.isoformat()

    @staticmethod
    def generate_datetime_now() -> str:
        value = datetime.datetime.now(pytz.timezone('UTC'))
        value = value.replace(microsecond=0)
        return value.isoformat()

    @staticmethod
    def convert_from_format(value: str, format: str) -> str:
        """
        Converts a datetime with the given format.
        """
        value = datetime.datetime.strptime(value, format)
        if not value.tzinfo and sys.version_info <= (3, 6):
            value = pytz.utc.localize(value)
        elif not value.tzinfo:
            value = value.astimezone(pytz.utc)
        return value.isoformat()

    @staticmethod
    def convert_from_format_midnight(value: str, format: str) -> str:
        """
        Converts a date with the given format and adds time 00:00:00 to it.
        """
        date = datetime.datetime.strptime(value, format)
        if sys.version_info <= (3, 6):
            value = datetime.datetime.combine(date, DateTime.midnight)
            value = pytz.utc.localize(value)
        else:
            value = datetime.datetime.combine(date, DateTime.midnight,
                                              tzinfo=pytz.utc)
        return value.isoformat()

    @staticmethod
    def convert_fuzzy(value) -> str:
        value = dateutil.parser.parse(value, fuzzy=True)
        if not value.tzinfo and sys.version_info <= (3, 6):
            value = pytz.utc.localize(value)  # pragma: no cover
        elif not value.tzinfo:
            value.astimezone(pytz.utc)
        iso = value.isoformat()
        if '+' not in iso:
            return iso + '+00:00'
        else:
            return iso

    @staticmethod
    def convert(value, format='fuzzy') -> str:
        """
        Converts date time strings according to the given format.
        If the timezone is not given or clear, the local time zone is assumed!

        * timestamp
        * windows_nt: From Windows NT / AD / LDAP
        * epoch_millis: From Milliseconds since Epoch
        * from_format: From a given format, eg. 'from_format|%H %M %S %m %d %Y %Z'
        * from_format_midnight: Date from a given format and assume midnight, e.g. 'from_format_midnight|%d-%m-%Y'
        * utc_isoformat: Parse date generated by datetime.isoformat()
        * fuzzy (or None): Use dateutils' fuzzy parser, default if no specific parser is given
        """
        if format is None:
            format = 'fuzzy'
        if format.startswith('from_format|'):
            return DateTime.convert_from_format(value, format=format[12:])
        elif format.startswith('from_format_midnight|'):
            return DateTime.convert_from_format_midnight(value, format=format[21:])
        else:
            return DateTime.TIME_CONVERSIONS[format](value)


DateTime.TIME_CONVERSIONS = {'timestamp': DateTime.from_timestamp,
                             'windows_nt': DateTime.from_windows_nt,
                             'epoch_millis': DateTime.from_epoch_millis,
                             'from_format': DateTime.convert_from_format,
                             'from_format_midnight': DateTime.convert_from_format_midnight,
                             'utc_isoformat': DateTime.parse_utc_isoformat,
                             'fuzzy': DateTime.convert_fuzzy,
                             None: DateTime.convert_fuzzy,
                             }
__convert_doc_position = DateTime.convert.__doc__.find('\n\n') + 1
DateTime.__doc__ += DateTime.convert.__doc__[__convert_doc_position:]


class Float(GenericType):
    """
    Float type. Without sanitation only python float/integer/long is
    accepted. Boolean is explicitly denied.

    Sanitation accepts strings and everything float() accepts.
    """

    @staticmethod
    def is_valid(value: float, sanitize: bool = False) -> bool:
        if sanitize:
            value = Float().sanitize(value)
            if value is not None:
                return True

        # Bool is subclass of int
        if isinstance(value, bool):
            return False
        if isinstance(value, (int, float)):
            return True

        return False

    @staticmethod
    def sanitize(value: float) -> Optional[float]:
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


class Accuracy(Float):
    """
    Accuracy type. A Float between 0 and 100.
    """

    @staticmethod
    def is_valid(value: float, sanitize: bool = False) -> bool:
        if sanitize:
            value = Accuracy.sanitize(value)
            if value is not None and value >= 0 and value <= 100:
                return True

        # Bool is subclass of int
        if isinstance(value, bool):
            return True
        if isinstance(value, (int, float)) and value >= 0 and value <= 100:
            return True

        return False

    @staticmethod
    def sanitize(value: float) -> Optional[float]:
        try:
            if isinstance(value, bool):
                return float(value) * 100

            value = float(value)
            if value >= 0 and value <= 100:
                return value
        except (ValueError, TypeError):
            return None


class FQDN(String):
    """
    Fully qualified domain name type.

    All valid lowercase domains are accepted, no IP addresses or URLs. Trailing
    dot is not allowed.

    To prevent values like '10.0.0.1:8080' (#1235), we check for the
    non-existence of ':'.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = FQDN().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if value.strip('.') != value or value != value.lower() or ':' in value:
            return False

        if IPAddress().is_valid(value):
            return False

        url = parse.urlsplit(value)
        if (url.scheme != '' or url.netloc != '' or url.query != '' or url.fragment != '' or
           url.path.find('/') >= 0):
            return False

        if value.encode('idna').decode() != value:
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        try:
            value = GenericType().sanitize(value)
        except ValueError:
            return
        if not isinstance(value, str):
            return
        value = value.strip('.')
        if value:
            try:
                return value.encode('idna').decode().lower()
            except UnicodeError:
                return

    @staticmethod
    def to_ip(value: str) -> Optional[str]:
        try:
            value = str(dns.resolver.query(value, 'A')[0])
        except dns.resolver.NXDOMAIN:  # domain not found
            value = None
        return value


class Integer(GenericType):
    """
    Integer type. Without sanitation only python integer/long is accepted.
    Bool is explicitly denied.

    Sanitation accepts strings and everything int() accepts.
    """

    @staticmethod
    def is_valid(value: int, sanitize: bool = False) -> bool:
        if sanitize:
            value = Integer().sanitize(value)
            if value is not None:
                return True

        # Bool is subclass of int
        if isinstance(value, bool):
            return False
        if isinstance(value, int):
            return True

        return False

    @staticmethod
    def sanitize(value: int) -> Optional[int]:
        try:
            return int(value)
        except (ValueError, TypeError):
            return None


class ASN(Integer):
    """
    ASN type. Derived from Integer with forbidden values.

    Only valid are: 0 < asn <= 4294967295
    See https://en.wikipedia.org/wiki/Autonomous_system_(Internet)
    > The first and last ASNs of the original 16-bit integers, namely 0 and
    > 65,535, and the last ASN of the 32-bit numbers, namely 4,294,967,295 are
    > reserved and should not be used by operators.
    """
    @staticmethod
    def check_asn(value: int) -> bool:
        if 0 < value <= 4294967295:
            return True
        else:
            return False

    @staticmethod
    def is_valid(value: int, sanitize: bool = False) -> bool:
        if sanitize:
            value = ASN().sanitize(value)
        if not Integer.is_valid(value):
            return False
        if not ASN.check_asn(value):
            return False
        return True

    @staticmethod
    def sanitize(value: int) -> Optional[int]:
        if isinstance(value, str) and value.lower().startswith('as'):
            value = value[2:]
        value = Integer.sanitize(value)
        if value and ASN.check_asn(value):
            return value


class IPAddress(String):
    """
    Type for IP addresses, all families. Uses the ipaddress module.

    Sanitation accepts integers, strings and objects of ipaddress.IPv4Address and ipaddress.IPv6Address.

    Valid values are only strings. 0.0.0.0 is explicitly not allowed.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = IPAddress().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            return False

        if address == ipaddress.ip_address('0.0.0.0'):
            return False

        if '%' in value:
            # IPv6 address with scope ID
            # https://github.com/certtools/intelmq/issues/1550
            return False

        return True

    @staticmethod
    def sanitize(value: Union[int, str]) -> Optional[str]:
        if not isinstance(value, int):  # can be str/bytes or ipaddress.ip_address object
            try:
                value = GenericType().sanitize(value)
            except ValueError:
                return None

        # support for integer IP-address which are given as string
        try:
            if (str(value) == str(int(value))):
                value = int(value)
        except (ValueError, TypeError):
            pass
        # Convert integers to strings
        # either from the conversion above, or the value is already given as int
        if isinstance(value, int):
            try:
                value = ipaddress.ip_address(value)
            except ValueError:
                return None
            # we don't need the specialized checks below, return early
            return GenericType().sanitize(value)

        try:
            # Remove the scope ID if it's detected.
            text_scope_id = value.split('%')
            if len(text_scope_id) > 1:
                value = text_scope_id[0]
        except AttributeError:  # None
            return None

        # Check if it is syntacticlly a valid IP Address/Network
        try:
            network = ipaddress.ip_network(str(value))
        except ValueError:
            return None
        # And then make sure it is an address or remove the CIDR (converts addresses with CIDR to addresses without CIDR)
        if network.num_addresses == 1:
            value = str(network.network_address)
        else:
            return None

        return GenericType().sanitize(value)

    @staticmethod
    def to_int(value: str) -> Optional[int]:
        try:
            ip_integer = socket.inet_pton(socket.AF_INET, value)
        except socket.error:
            try:
                ip_integer = socket.inet_pton(socket.AF_INET6, value)
            except socket.error:
                return None

        ip_integer = int(binascii.hexlify(ip_integer), 16)
        return ip_integer

    @staticmethod
    def version(value: str) -> int:
        return ipaddress.ip_address(value).version

    @staticmethod
    def to_reverse(ip_addr: str) -> str:
        return str(dns.reversename.from_address(ip_addr))


class IPNetwork(String):
    """
    Type for IP networks, all families. Uses the ipaddress module.

    Sanitation accepts strings and objects of ipaddress.IPv4Network and ipaddress.IPv6Network.
    If host bits in strings are set, they will be ignored (e.g 127.0.0.1/32).

    Valid values are only strings.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = IPNetwork().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        try:
            ipaddress.ip_network(value)
        except ValueError:
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:

        try:
            value = GenericType().sanitize(value)
            value = str(ipaddress.ip_network(str(value), strict=False))
        except ValueError:
            return None

        return GenericType().sanitize(value)

    @staticmethod
    def version(value: str) -> int:
        return ipaddress.ip_network(str(value)).version


class JSON(String):
    """
    JSON type.

    Sanitation accepts any valid JSON objects.

    Valid values are only unicode strings with JSON objects.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = JSON().sanitize(value)

        if not isinstance(value, str):
            return False

        try:
            json.loads(value)
        except ValueError:
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, (str, bytes)):
            sanitized = GenericType.sanitize(value)
            if JSON.is_valid(sanitized):
                return sanitized
        try:
            return GenericType().sanitize(json.dumps(value, sort_keys=True))
        except TypeError:
            return None


class JSONDict(JSON):
    """
    JSONDict type.

    Sanitation accepts pythons dictionaries and JSON strings.

    Valid values are only unicode strings with JSON dictionaries.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = JSONDict().sanitize(value)

        if not isinstance(value, str):
            return False

        try:
            unpacked = json.loads(value)
        except ValueError:
            return False
        else:
            if isinstance(unpacked, dict) and unpacked != {}:
                return True

        return False

    @staticmethod
    def is_valid_subitem(value: str) -> bool:
        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        if not value:
            return None
        if isinstance(value, (str, bytes)):
            sanitized = GenericType.sanitize(value)
            if JSONDict.is_valid(sanitized):
                return sanitized
        try:
            return GenericType().sanitize(json.dumps(value, sort_keys=True))
        except TypeError:
            return None

    @staticmethod
    def sanitize_subitem(value: str) -> str:
        return value


class LowercaseString(String):
    """
    Like string, but only allows lower case characters.

    Sanitation lowers all characters.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = String().sanitize(value)
            value = LowercaseString().sanitize(value)

        if not String().is_valid(value):
            return False

        if value != value.lower():
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[bool]:
        try:
            value = value.lower()
        except AttributeError:  # None
            return None
        return String().sanitize(value)


class URL(String):
    """
    URI type. Local and remote.

    Sanitation converts hxxp and hxxps to http and https.
    For local URIs (file) a missing host is replaced by localhost.

    Valid values must have the host (network location part).
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = URL().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        result = parse.urlsplit(value)
        if result.netloc == "":
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        value = GenericType().sanitize(value)
        if not value:
            return

        value = value.replace('hxxp://', 'http://')
        value = value.replace('hxxps://', 'https://')

        result = parse.urlsplit(value)
        if result.scheme == "file" and result.netloc == '':
            # add localhost as netloc
            result_split = list(result)
            result_split[1] = 'localhost'
            value = parse.urlunsplit(result_split)
            result = parse.urlsplit(value)

        if result.netloc != "":
            return value

    @staticmethod
    def to_ip(url: str) -> Optional[str]:
        value = parse.urlsplit(url)
        if value.netloc != "":
            return FQDN().to_ip(value.netloc)
        return None

    @staticmethod
    def to_domain_name(url: str) -> Optional[str]:
        value = parse.urlsplit(url)
        if value.netloc != "" and not IPAddress.is_valid(value.netloc):
            return value.netloc
        return None


class UppercaseString(String):
    """
    Like string, but only allows upper case characters.

    Sanitation uppers all characters.
    """

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = UppercaseString().sanitize(value)

        if not String().is_valid(value):
            return False

        if value != value.upper():
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        try:
            value = value.upper()
        except AttributeError:  # None
            return None
        return String().sanitize(value)


class Registry(UppercaseString):
    """
    Registry type. Derived from UppercaseString.

    Only valid values: AFRINIC, APNIC, ARIN, LACNIC, RIPE.
    RIPE-NCC and RIPENCC are normalized to RIPE.
    """
    ENUM = ['AFRINIC', 'APNIC', 'ARIN', 'LACNIC', 'RIPE']

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = Registry.sanitize(value)

        if not UppercaseString.is_valid(value):
            return False

        if value not in Registry.ENUM:
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> str:
        value = UppercaseString.sanitize(value)
        if value in ['RIPENCC', 'RIPE-NCC']:
            value = 'RIPE'
        return value


class TLP(UppercaseString):
    """
    TLP level type. Derived from UppercaseString.

    Only valid values: WHITE, GREEN, AMBER, RED.

    Accepted for sanitation are different cases and the prefix 'tlp:'.
    """
    enum = ['WHITE', 'GREEN', 'AMBER', 'RED']
    prefix_pattern = re.compile(r'^(TLP:?)?\s*', flags=re.IGNORECASE)

    @staticmethod
    def is_valid(value: str, sanitize: bool = False) -> bool:
        if sanitize:
            value = TLP.sanitize(value)

        if not UppercaseString.is_valid(value):
            return False

        if value not in TLP.enum:
            return False

        return True

    @staticmethod
    def sanitize(value: str) -> Optional[str]:
        value = UppercaseString.sanitize(value)
        if value:
            value = TLP.prefix_pattern.sub('', value)
            return value
