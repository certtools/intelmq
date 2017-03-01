# -*- coding: utf-8 -*-
"""
The following types are implemented with sanitize() and is_valid() functions:

 - Base64
 - ClassificationType
 - DNS
 - DateTime
 - FQDN
 - FeedName
 - GenericType
 - IPAddress
 - IPNetwork
 - LowercaseString
 - Registry
 - String
 - URL
"""
import binascii
import datetime
import ipaddress
import json
import socket
import urllib.parse as parse

import dateutil.parser
import dns.resolver
import pytz

import intelmq.lib.utils as utils

__all__ = ['Base64', 'Boolean', 'ClassificationType', 'DateTime', 'FQDN',
           'Float', 'Accuracy', 'GenericType', 'IPAddress', 'IPNetwork',
           'Integer', 'JSON', 'LowercaseString', 'Registry', 'String', 'URL',
           ]


class GenericType(object):

    @staticmethod
    def is_valid(value, sanitize=False):
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
    def sanitize(value):
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


class Base64(GenericType):
    """
    Base64 type. Always gives unicode strings.

    Sanitation encodes to base64 and accepts binary and unicode strings.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = Base64().sanitize(value)

        try:
            utils.base64_decode(value)
        except TypeError:
            return False

        if not GenericType().is_valid(value):
            return False

        return True

    @staticmethod
    def sanitize(value):
        value = utils.base64_encode(value)
        return value


class Boolean(GenericType):
    """
    Boolean type. Without sanitation only python bool is accepted.

    Sanitation accepts string 'true' and 'false' and integers 0 and 1.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
        if isinstance(value, bool):
            return True
        else:
            if sanitize:
                value = Boolean().sanitize(value)
                if value is not None:
                    return True
            return False

    @staticmethod
    def sanitize(value):
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


class ClassificationType(GenericType):

    allowed_values = ['spam',
                      'malware',
                      'botnet drone',
                      'ransomware',
                      'dga domain',
                      'malware configuration',
                      'c&c',
                      'scanner',
                      'exploit',
                      'brute-force',
                      'ids alert',
                      'defacement',
                      'compromised',
                      'backdoor',
                      'ddos',
                      'dropzone',
                      'phishing',
                      'proxy',
                      'vulnerable service',
                      'blacklist',
                      'other',
                      'unknown'
                      ]

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = ClassificationType().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if not isinstance(value, str):
            return False

        if value not in ClassificationType().allowed_values:
            return False

        return True


class DateTime(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = DateTime().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if value != DateTime.__parse(value):
            return False

        return True

    @staticmethod
    def sanitize(value):
        value = DateTime.__parse(value)
        return GenericType().sanitize(value)

    @staticmethod
    def __parse(value):
        try:
            return utils.decode(DateTime.__parse_utc_isoformat(value))
        except ValueError:
            pass

        try:
            value = dateutil.parser.parse(value, fuzzy=True)
            value = value.astimezone(pytz.utc)
            value = value.isoformat()
        except ValueError:
            return None
        return utils.decode(value)

    @staticmethod
    def __parse_utc_isoformat(value):
        """
        Parse format generated by datetime.isoformat() method with UTC timezone.
        It is much faster than universal dateutil parser.
        """
        try:
            datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+00:00')
        except ValueError:
            # With microseconds
            datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f+00:00')

        return value

    @staticmethod
    def from_timestamp(tstamp, tzone='UTC'):
        """
        Returns ISO formated datetime from given timestamp.
        You can give timezone for given timestamp, UTC by default.
        """
        dtime = (datetime.datetime(1970, 1, 1, tzinfo=pytz.utc) +
                 datetime.timedelta(seconds=tstamp))
        localized = pytz.timezone(tzone).normalize(dtime)
        return str(localized.isoformat())

    @staticmethod
    def generate_datetime_now():
        value = datetime.datetime.now(pytz.timezone('UTC'))
        value = value.replace(microsecond=0)
        value = value.isoformat()
        # Is byte string in 2 and unicode string in 3, make unicode string
        return utils.decode(value)


class Float(GenericType):
    """
    Float type. Without sanitation only python float/integer/long is
    accepted. Boolean is excplicitly denied.

    Sanitation accepts strings and everything float() accepts.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
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
    def sanitize(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


class Accuracy(GenericType):
    """
    Accuracy type. A Float between 0 and 100.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
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
    def sanitize(value):
        try:
            if isinstance(value, bool):
                return float(value) * 100

            value = float(value)
            if value >= 0 or value <= 100:
                return value
        except (ValueError, TypeError):
            return None


class FQDN(GenericType):
    """
    Fully qualified domain name type.

    All valid lowercase domains are accepted, no IP addresses or URLs. Trailing
    dot is not allowed.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = FQDN().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if value.rstrip('.') != value or value != value.lower():
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
    def sanitize(value):
        value = value.rstrip('.')
        if value:
            return value.encode('idna').decode().lower()

    @staticmethod
    def to_ip(value):
        try:
            value = str(dns.resolver.query(value, 'A')[0])
        except dns.resolver.NXDOMAIN:  # domain not found
            value = None
        return value


class Integer(GenericType):
    """
    Integer type. Without sanitation only python integer/long is accepted.
    Bool is excplicitly denied.

    Sanitation accepts strings and everything int() accepts.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
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
    def sanitize(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None


class IPAddress(GenericType):
    """
    Type for IP addresses, all families. Uses the ipaddress module.

    Sanitation accepts strings and objects of ipaddress.IPv4Address and ipaddress.IPv4Address.

    Valid values are only strings. 0.0.0.0 is explictly not allowed.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = IPAddress().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            return False

        if address == ipaddress.ip_address('0.0.0.0'):
            return False

        return True

    @staticmethod
    def sanitize(value):

        try:
            network = ipaddress.ip_network(str(value))
        except ValueError:
            return None

        if network.num_addresses == 1:
            value = str(network.network_address)
        else:
            return None

        return GenericType().sanitize(value)

    @staticmethod
    def to_int(value):
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
    def version(value):
        return ipaddress.ip_address(value).version

    @staticmethod
    def to_reverse(ip_addr):
        return str(dns.reversename.from_address(ip_addr))


class IPNetwork(GenericType):
    """
    Type for IP networks, all families. Uses the ipaddress module.

    Sanitation accepts strings and objects of ipaddress.IPv4Network and ipaddress.IPv4Network.
    If host bits in strings are set, they will be ignored (e.g 127.0.0.1/32).

    Valid values are only strings.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = IPNetwork().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        try:
            ipaddress.ip_network(value)
        except ValueError:
            return False

        return True

    @staticmethod
    def sanitize(value):

        try:
            value = str(ipaddress.ip_network(str(value), strict=False))
        except ValueError:
            return None

        return GenericType().sanitize(value)

    @staticmethod
    def version(value):
        return ipaddress.ip_network(str(value)).version


class JSON(GenericType):
    """
    JSON type.

    Sanitation accepts pythons dictionaries and JSON strings.

    Valid values are only unicode strings with JSON dictionaries.
    """

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = JSON().sanitize(value)

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
    def sanitize(value):
        if not value:
            return None
        if isinstance(value, (str, bytes)):
            sanitized = GenericType.sanitize(value)
            if JSON.is_valid(sanitized):
                return sanitized
        try:
            return GenericType().sanitize(json.dumps(value, sort_keys=True))
        except TypeError:
            return None


class LowercaseString(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = String().sanitize(value)
            value = LowercaseString().sanitize(value)

        if not String().is_valid(value):
            return False

        if value != value.lower():
            return False

        return True

    @staticmethod
    def sanitize(value):
        value = value.lower()
        return String().sanitize(value)


class String(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = String().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if type(value) is not str:
            return False

        if len(value) == 0:
            return False

        return True


class URL(GenericType):
    """
    URI type. Local and remote.

    Sanitation converts hxxp and hxxps to http and https.
    For local URIs (file) a missing host is replaced by localhost.

    Valid values must have the host (network location part).
    """

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = URL().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        result = parse.urlsplit(value)
        if result.netloc == "":
            return False

        return True

    @staticmethod
    def sanitize(value):
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
            return GenericType().sanitize(value)

    @staticmethod
    def to_ip(url):
        value = parse.urlsplit(url)
        if value.netloc != "":
            return FQDN().to_ip(value.netloc)
        return None

    @staticmethod
    def to_domain_name(url):
        value = parse.urlsplit(url)
        if value.netloc != "" and not IPAddress.is_valid(value.netloc):
            return value.netloc
        return None


class UppercaseString(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = UppercaseString().sanitize(value)

        if not String().is_valid(value):
            return False

        if value != value.upper():
            return False

        return True

    @staticmethod
    def sanitize(value):
        value = value.upper()
        return String().sanitize(value)


class Registry(UppercaseString):
    """
    Registry type. Derived from UppercaseString.

    Only valid values: AFRINIC, APNIC, ARIN, LACNIC, RIPE.
    RIPE-NCC and RIPENCC are normalized to RIPE.
    """
    ENUM = ['AFRINIC', 'APNIC', 'ARIN', 'LACNIC', 'RIPE']

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = Registry.sanitize(value)

        if not UppercaseString.is_valid(value):
            return False

        if value not in Registry.ENUM:
            return False

        return True

    @staticmethod
    def sanitize(value):
        value = UppercaseString.sanitize(value)
        if value in ['RIPENCC', 'RIPE-NCC']:
            value = 'RIPE'
        return value
