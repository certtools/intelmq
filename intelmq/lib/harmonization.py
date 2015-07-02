import sys
import dns
import DNS
import pytz
import time
import json
import ipaddr
import base64
import inspect
import urlparse
import binascii
import datetime
import dateutil.parser
import socket

class GenericType():

    @staticmethod
    def is_valid(key, value):
        if not value:
            return False

        if type(value) is not unicode:
            return False

        if len(value) == 0:
            return False

        return True
        
    @staticmethod
    def sanitize(value):
        if not value:
            return None

        if type(value) is unicode:
            return value.strip()

        if type(value) is str:
            try:
                value = value.decode('utf-8')
            except UnicodeDecodeError:
                value = value.decode('utf-8', 'ignore')
            return value.strip()

        return None


class String(GenericType):

    @staticmethod
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
            return False

        if type(value) is not unicode:
            return False

        if len(value) == 0:
            return False

        return True
        
    @staticmethod
    def sanitize(value):
        return GenericType().sanitize(value)


class FeedName(GenericType):

    @staticmethod
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
            return False

        return True
        
    @staticmethod
    def sanitize(value):
        return GenericType().sanitize(value)


class DateTime(GenericType):

    @staticmethod
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
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
        except:
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
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
            return False

        try:
            ipaddr.IPNetwork(value)
        except:
            return False

        return True
            
    @staticmethod
    def sanitize(value):
        
        try:
            ipaddr.IPNetwork(value)
        except:
            return None
                
        return GenericType().sanitize(value)

    @staticmethod
    def version(value):
        return int(ipaddr.IPNetwork(value).version)


class IPAddress(GenericType):

    @staticmethod
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
            return False

        try:
            ipaddr.IPAddress(value)
        except:
            return False

        return True
            
    @staticmethod
    def sanitize(value):
        
        try:
            network = ipaddr.IPNetwork(value)
        except:
            return None
        
        if network.numhosts == 1:
            value = str(network.network)
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
        return int(ipaddr.IPAddress(value).version)

    @staticmethod
    def to_reverse(ip):
        return unicode(dns.reversename.from_address(ip))


class FQDN(GenericType):

    @staticmethod
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
            return False

        if IPAddress().is_valid(key, value):
            return False
            
        if URL().is_valid(key, value):
            return False
        
        if not len(value.split('.')) > 1:
            return False

        return True
        
    @staticmethod
    def sanitize(value):
        return GenericType().sanitize(value)
    
    @staticmethod
    def to_ip(value):
        try:
            value = DNS.dnslookup(value, 'A')
        except:
            value = None
        return value


class MalwareName(GenericType):

    @staticmethod
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
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
    def is_valid(key, value):
        try:
            base64.b64decode(value)
        except:
            return False

        if not GenericType().is_valid(key, value):
            return False

        return True
        
    @staticmethod
    def sanitize(value):
        value = base64.b64encode(value)
        return GenericType().sanitize(value)


class URL(GenericType):

    @staticmethod
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
            return False

        result = urlparse.urlparse(value)
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
            result = urlparse.urlparse(value)
            if result.netloc != "":
                return GenericType().sanitize(value)

        return None
    
    @staticmethod
    def to_ip(url):
        value = urlparse.urlparse(url)
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

    __allowed_values = ['spam',
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
    def is_valid(key, value):
        if not GenericType().is_valid(key, value):
            return False

        if type(value) is not unicode:
            return False
            
        if not value in ClassificationType().__allowed_values:
            return False

        return True

    @staticmethod
    def sanitize(value):
        return GenericType().sanitize(value)        
