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
 - ipaddressess
 - IPNetwork
 - MalwareName
 - String
 - URL
"""
import base64
import binascii
import datetime
import dateutil.parser
import dns.resolver
try:
    import ipaddress
except ImportError:
    import ipaddr as ipaddress
import pytz
import six
import socket
try:
    from urlparse import urlparse
except ImportError:
    from urllib import parse as urlparse


def ip_address(value):
    try:
        return ipaddress.ip_address(value)
    except AttributeError:
        return ipaddress.IPAddress(value)


def ip_network(value):
    try:
        return ipaddress.ip_network(value)
    except AttributeError:
        return ipaddress.IPNetwork(value)


class GenericType(object):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)

        if not value:
            return False

        if not isinstance(value, six.text_type):
            return False

        if len(value) == 0:
            return False

        return True

    @staticmethod
    def sanitize(value):
        if not value:
            return None

        if isinstance(value, six.text_type):
            return value.strip()

        if isinstance(value, six.binary_type):
            try:
                value = value.decode('utf-8')
            except UnicodeDecodeError:
                value = value.decode('utf-8', 'ignore')
            return value.strip()

        return None


class String(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = String().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if not isinstance(value, six.text_type):
            return False

        if len(value) == 0:
            return False

        return True


class FeedName(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = FeedName().sanitize(value)

        if not GenericType().is_valid(value):
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
            value = dateutil.parser.parse(value)
            value = value.astimezone(pytz.utc)
            value = value.isoformat()
        except ValueError:
            return None
        return value.decode("utf-8")

    @staticmethod
    def generate_datetime_now():
        value = datetime.datetime.now(pytz.timezone('UTC'))
        value = value.replace(microsecond=0)
        value = value.isoformat()
        return value.decode("utf-8")


class IPNetwork(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = IPNetwork().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        try:
            ip_network(value)
        except ValueError:
            return False

        return True

    @staticmethod
    def sanitize(value):

        try:
            ip_network(value)
        except ValueError:
            return None

        return GenericType().sanitize(value)

    @staticmethod
    def version(value):
        return int(ip_network(value).version)


class IPAddress(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = IPAddress().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        try:
            ip_address(value)
        except ValueError:
            return False

        return True

    @staticmethod
    def sanitize(value):

        try:
            network = ip_network(value)
        except ValueError:
            return None

        if network.numhosts == 1:
            value = bytes(network.network)
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
        return int(ip_address(value).version)

    @staticmethod
    def to_reverse(ip_addr):
        return six.text_type(dns.reversename.from_address(ip_addr))


class FQDN(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = FQDN().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if IPAddress().is_valid(value):
            return False

        if URL().is_valid(value):
            return False

        if not len(value.split('.')) > 1:
            return False

        return True

    @staticmethod
    def to_ip(value):
        try:
            value = str(dns.resolver.query(value, 'A')[0])
        except Exception:  # TODO: More specific Exception
            value = None
        return value


class MalwareName(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = MalwareName().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if value != value.lower():
            return False

        return True

    @staticmethod
    def sanitize(value):
        value = value.lower()
        return GenericType().sanitize(value)


class Base64(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = Base64().sanitize(value)

        try:
            base64.b64decode(value)
        except TypeError:
            return False

        if not GenericType().is_valid(value):
            return False

        return True

    @staticmethod
    def sanitize(value):
        value = base64.b64encode(value)
        return GenericType().sanitize(value)


class URL(GenericType):

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = URL().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        result = urlparse(value)
        if result.netloc == "":
            return False

        return True

    @staticmethod
    def sanitize(value):
        if "hxxp://" in value:
            value = value.replace('hxxp://', 'http://')

        if "hxxps://" in value:
            value = value.replace('hxxps://', 'https://')

        tests = [
                    value,
                    "http://" + value,
                    "http://" + value + "/"
                ]

        for value in tests:
            result = urlparse(value)
            if result.netloc != "":
                return GenericType().sanitize(value)

        return None

    @staticmethod
    def to_ip(url):
        value = urlparse(url)
        if value.netloc != "":
            return FQDN().to_ip(value.netloc)
        return None

    @staticmethod
    def to_domain_name(url):
        value = urlparse(url)
        if value.netloc != "" and not IPAddress.is_valid(value.netloc):
            return value.netloc
        return None


class ClassificationType(GenericType):

    allowed_values = ['spam',
                      'malware',
                      'botnet drone',
                      'ransomware',
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
                      'vulnerable service',
                      'blacklist',
                      'unknown'
                      ]

    @staticmethod
    def is_valid(value, sanitize=False):
        if sanitize:
            value = GenericType().sanitize(value)
            value = ClassificationType().sanitize(value)

        if not GenericType().is_valid(value):
            return False

        if not isinstance(value, six.text_type):
            return False

        if value not in ClassificationType().allowed_values:
            return False

        return True
