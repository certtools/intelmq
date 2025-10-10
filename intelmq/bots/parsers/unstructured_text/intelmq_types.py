"""
Full IntelMQ-compatible type definitions using Pydantic.

This module implements the complete IntelMQ harmonization type system
using Pydantic validators and custom types.
"""

from datetime import datetime, timezone
from typing import Optional, Literal, Annotated, Any
from pydantic import BaseModel, Field, field_validator, model_validator
import ipaddress
import re
import urllib.parse as parse
from dateutil import parser as dateutil_parser


# Literal types matching IntelMQ exactly
ClassificationTaxonomyLiteral = Literal[
    'abusive-content',
    'availability',
    'fraud',
    'information-content-security',
    'information-gathering',
    'intrusion-attempts',
    'intrusions',
    'malicious-code',
    'other',
    'test',
    'vulnerable'
]

ClassificationTypeLiteral = Literal[
    'application-compromise',
    'blacklist',
    'brute-force',
    'burglary',
    'c2-server',
    'copyright',
    'data-leak',
    'data-loss',
    'ddos',
    'ddos-amplifier',
    'dga-domain',
    'dos',
    'exploit',
    'harmful-speech',
    'ids-alert',
    'infected-system',
    'information-disclosure',
    'malware',
    'malware-configuration',
    'malware-distribution',
    'masquerade',
    'misconfiguration',
    'other',
    'outage',
    'phishing',
    'potentially-unwanted-accessible',
    'privileged-account-compromise',
    'proxy',
    'sabotage',
    'scanner',
    'sniffing',
    'social-engineering',
    'spam',
    'system-compromise',
    'test',
    'tor',
    'unauthorised-information-access',
    'unauthorised-information-modification',
    'unauthorized-use-of-resources',
    'undetermined',
    'unprivileged-account-compromise',
    'violence',
    'vulnerable-system',
    'weak-crypto'
]

RegistryLiteral = Literal['AFRINIC', 'APNIC', 'ARIN', 'LACNIC', 'RIPE']
TLPLiteral = Literal['WHITE', 'GREEN', 'AMBER', 'RED']


class GeolocationInfo(BaseModel):
    """Geolocation information"""
    cc: Optional[str] = Field(None, description="Country code (2 chars)", max_length=2)
    city: Optional[str] = Field(None, description="City name")
    country: Optional[str] = Field(None, description="Country name")
    latitude: Optional[float] = Field(None, description="Latitude", ge=-90, le=90)
    longitude: Optional[float] = Field(None, description="Longitude", ge=-180, le=180)
    region: Optional[str] = Field(None, description="Region")
    state: Optional[str] = Field(None, description="State")

    @field_validator('cc')
    @classmethod
    def validate_cc(cls, v):
        if v:
            return v.upper()
        return v


class SourceInfo(BaseModel):
    """Source information for an event (complete IntelMQ fields)"""
    # Network identifiers
    ip: Optional[str] = Field(None, description="Source IP address")
    port: Optional[int] = Field(None, description="Source port", ge=0, le=65535)
    fqdn: Optional[str] = Field(None, description="Fully qualified domain name")
    url: Optional[str] = Field(None, description="Source URL")

    # ASN and registry
    asn: Optional[int] = Field(None, description="Autonomous System Number")
    registry: Optional[RegistryLiteral] = Field(None, description="Regional Internet Registry")

    # Network details
    network: Optional[str] = Field(None, description="Network in CIDR notation")
    allocated: Optional[str] = Field(None, description="Allocation date")

    # DNS
    reverse_dns: Optional[str] = Field(None, description="Reverse DNS lookup result")

    # Account
    account: Optional[str] = Field(None, description="Account identifier")

    # Local information
    local_ip: Optional[str] = Field(None, description="Local IP address")
    local_hostname: Optional[str] = Field(None, description="Local hostname")

    # Geolocation
    geolocation: Optional[GeolocationInfo] = Field(None, description="Geolocation information")

    # Tor
    tor_node: Optional[bool] = Field(None, description="Is a Tor node")

    @field_validator('ip', mode='before')
    @classmethod
    def validate_ip(cls, v):
        if not v:
            return v
        try:
            # Handle integers
            if isinstance(v, int):
                v = str(ipaddress.ip_address(v))
            # Handle strings with potential CIDR
            addr = str(v).strip()
            # Remove IPv6 scope ID
            if '%' in addr:
                addr = addr.split('%')[0]
            # Try parsing as network to handle CIDR
            try:
                network = ipaddress.ip_network(addr, strict=False)
                if network.num_addresses == 1:
                    addr = str(network.network_address)
                else:
                    # It's a network, not a single IP
                    return None
            except ValueError:
                # Try as plain IP
                ipaddress.ip_address(addr)

            # Reject 0.0.0.0
            if addr == '0.0.0.0':
                return None

            return addr
        except (ValueError, AttributeError):
            return None

    @field_validator('fqdn', mode='before')
    @classmethod
    def validate_fqdn(cls, v):
        if not v:
            return v
        v = str(v).strip('.').lower()

        # Check if it's an IP (not allowed for FQDN)
        try:
            ipaddress.ip_address(v)
            return None  # It's an IP, not a FQDN
        except ValueError:
            pass

        # Check for port notation
        if ':' in v and not v.startswith('['):  # Allow IPv6 format [::1]
            return None

        # Check for URL components
        url = parse.urlsplit(v)
        if url.scheme or url.netloc or url.query or url.fragment or '/' in url.path:
            return None

        # IDNA encoding
        try:
            return v.encode('idna').decode().lower()
        except (UnicodeError, UnicodeDecodeError):
            return None

    @field_validator('url', mode='before')
    @classmethod
    def validate_url(cls, v):
        if not v:
            return v
        v = str(v).strip()

        # Normalize hxxp/hxxps
        v = v.replace('hxxp://', 'http://')
        v = v.replace('hxxps://', 'https://')

        # Parse URL
        result = parse.urlsplit(v)

        # Add localhost for file:// URLs without netloc
        if result.scheme == "file" and result.netloc == '':
            result_split = list(result)
            result_split[1] = 'localhost'
            v = parse.urlunsplit(result_split)
            result = parse.urlsplit(v)

        # Must have netloc
        if result.netloc == "":
            return None

        return v

    @field_validator('asn', mode='before')
    @classmethod
    def validate_asn(cls, v):
        if v is None:
            return v
        # Strip 'AS' prefix if present
        if isinstance(v, str) and v.upper().startswith('AS'):
            v = v[2:]
        try:
            asn = int(v)
            if 0 < asn <= 4294967295:
                return asn
        except (ValueError, TypeError):
            pass
        return None

    @field_validator('registry', mode='before')
    @classmethod
    def validate_registry(cls, v):
        if not v:
            return v
        v = str(v).upper()
        # Normalize RIPE variants
        if v in ['RIPENCC', 'RIPE-NCC']:
            return 'RIPE'
        return v


class DestinationInfo(BaseModel):
    """Destination information for an event (complete IntelMQ fields)"""
    # Network identifiers
    ip: Optional[str] = Field(None, description="Destination IP address")
    port: Optional[int] = Field(None, description="Destination port", ge=0, le=65535)
    fqdn: Optional[str] = Field(None, description="Fully qualified domain name")
    url: Optional[str] = Field(None, description="Destination URL")

    # ASN and registry
    asn: Optional[int] = Field(None, description="Autonomous System Number")
    registry: Optional[RegistryLiteral] = Field(None, description="Regional Internet Registry")

    # Network details
    network: Optional[str] = Field(None, description="Network in CIDR notation")
    allocated: Optional[str] = Field(None, description="Allocation date")

    # DNS
    reverse_dns: Optional[str] = Field(None, description="Reverse DNS lookup result")

    # Account
    account: Optional[str] = Field(None, description="Account identifier")

    # Local information
    local_ip: Optional[str] = Field(None, description="Local IP address")
    local_hostname: Optional[str] = Field(None, description="Local hostname")

    # Geolocation
    geolocation: Optional[GeolocationInfo] = Field(None, description="Geolocation information")

    # Tor
    tor_node: Optional[bool] = Field(None, description="Is a Tor node")

    # Use same validators as SourceInfo
    _validate_ip = field_validator('ip', mode='before')(SourceInfo.validate_ip.__func__)
    _validate_fqdn = field_validator('fqdn', mode='before')(SourceInfo.validate_fqdn.__func__)
    _validate_url = field_validator('url', mode='before')(SourceInfo.validate_url.__func__)
    _validate_asn = field_validator('asn', mode='before')(SourceInfo.validate_asn.__func__)
    _validate_registry = field_validator('registry', mode='before')(SourceInfo.validate_registry.__func__)


class ClassificationInfo(BaseModel):
    """Classification information"""
    identifier: Optional[str] = Field(None, description="Classification identifier")
    taxonomy: Optional[ClassificationTaxonomyLiteral] = Field(None, description="Classification taxonomy")
    type: Optional[ClassificationTypeLiteral] = Field(None, description="Classification type")

    @field_validator('taxonomy', mode='before')
    @classmethod
    def validate_taxonomy(cls, v):
        if not v:
            return v
        v = str(v).lower().replace(' ', '-')

        # Map old values to new ones
        mappings = {
            'abusive content': 'abusive-content',
            'information gathering': 'information-gathering',
            'intrusion attempts': 'intrusion-attempts',
            'malicious code': 'malicious-code',
        }
        return mappings.get(v, v)

    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, v):
        if not v:
            return v

        original = str(v).lower()
        v_normalized = original.replace(' ', '-')

        # Map old values to new ones (use both space and dash versions as keys)
        mappings = {
            'botnet drone': 'infected-system',
            'botnet-drone': 'infected-system',
            'ids alert': 'ids-alert',
            'ids-alert': 'ids-alert',  # Already normalized
            'c&c': 'c2-server',
            'c2server': 'c2-server',
            'infected system': 'infected-system',
            'infected-system': 'infected-system',  # Already normalized
            'malware configuration': 'malware-configuration',
            'malware-configuration': 'malware-configuration',  # Already normalized
            'Unauthorised-information-access': 'unauthorised-information-access',
            'unauthorised-information-access': 'unauthorised-information-access',
            'vulnerable client': 'vulnerable-system',
            'vulnerable-client': 'vulnerable-system',
            'vulnerable service': 'vulnerable-system',
            'vulnerable-service': 'vulnerable-system',
            'leak': 'data-leak',
            'ransomware': 'infected-system',
            'unknown': 'undetermined',
            'dga domain': 'dga-domain',
            'dga-domain': 'dga-domain',
            'unauthorized-login': 'system-compromise',
            'unauthorized-command': 'system-compromise',
            'compromised': 'system-compromise',
            'defacement': 'unauthorised-information-modification',
            'backdoor': 'system-compromise',
            'dropzone': 'other',
        }

        # Try original first, then normalized
        return mappings.get(original, mappings.get(v_normalized, v_normalized))


class MalwareInfo(BaseModel):
    """Malware-related information"""
    name: Optional[str] = Field(None, description="Malware name")
    version: Optional[str] = Field(None, description="Malware version")
    hash: Optional[str] = Field(None, description="Generic hash")
    md5: Optional[str] = Field(None, description="MD5 hash", min_length=32, max_length=32)
    sha1: Optional[str] = Field(None, description="SHA1 hash", min_length=40, max_length=40)
    sha256: Optional[str] = Field(None, description="SHA256 hash", min_length=64, max_length=64)

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if v:
            return str(v).lower()
        return v

    @field_validator('md5', 'sha1', 'sha256', mode='before')
    @classmethod
    def validate_hash(cls, v):
        if v:
            return str(v).lower()
        return v


class FeedInfo(BaseModel):
    """Feed source information"""
    accuracy: Optional[float] = Field(None, description="Feed accuracy", ge=0, le=100)
    code: Optional[str] = Field(None, description="Feed code")
    documentation: Optional[str] = Field(None, description="Feed documentation URL")
    name: Optional[str] = Field(None, description="Feed name")
    provider: Optional[str] = Field(None, description="Feed provider")
    url: Optional[str] = Field(None, description="Feed URL")

    @field_validator('accuracy', mode='before')
    @classmethod
    def validate_accuracy(cls, v):
        if v is None:
            return v
        # Handle boolean (True=100, False=0)
        if isinstance(v, bool):
            return 100.0 if v else 0.0
        try:
            val = float(v)
            if 0 <= val <= 100:
                return val
        except (ValueError, TypeError):
            pass
        return None


class EventDescriptionInfo(BaseModel):
    """Event description details"""
    target: Optional[str] = Field(None, description="Event target description")
    text: Optional[str] = Field(None, description="Event description text")
    url: Optional[str] = Field(None, description="Event description URL")


class ProtocolInfo(BaseModel):
    """Protocol information"""
    application: Optional[str] = Field(None, description="Application protocol (e.g., http, ssh)")
    transport: Optional[str] = Field(None, description="Transport protocol (e.g., tcp, udp)")

    @field_validator('application', 'transport', mode='before')
    @classmethod
    def validate_protocol(cls, v):
        if v:
            return str(v).lower()
        return v


class IntelMQEvent(BaseModel):
    """
    Complete IntelMQ Event with full field compatibility.

    This implements the complete IntelMQ harmonization specification
    with all standard fields and proper validation.
    """

    # Time fields
    time_source: Optional[datetime] = Field(
        None,
        description="Time when the event occurred according to the source"
    )
    time_observation: Optional[datetime] = Field(
        None,
        description="Time when the event was observed/collected"
    )

    # Source information
    source: Optional[SourceInfo] = Field(
        None,
        description="Information about the source of the attack/event"
    )

    # Destination information
    destination: Optional[DestinationInfo] = Field(
        None,
        description="Information about the target/destination of the attack/event"
    )

    # Classification
    classification: Optional[ClassificationInfo] = Field(
        None,
        description="Classification of the security event"
    )

    # Event description
    event_description: Optional[EventDescriptionInfo] = Field(
        None,
        description="Human-readable event description"
    )
    event_hash: Optional[str] = Field(None, description="Hash of the event for deduplication")

    # Feed information
    feed: Optional[FeedInfo] = Field(None, description="Feed source information")

    # Protocol information
    protocol: Optional[ProtocolInfo] = Field(None, description="Protocol details")

    # Malware information
    malware: Optional[MalwareInfo] = Field(None, description="Malware-related information")

    # Additional fields
    comment: Optional[str] = Field(None, description="Free-form comment")
    extra: Optional[dict[str, Any]] = Field(None, description="Additional data as JSON")

    # Output/Raw data
    output: Optional[str] = Field(None, description="Output data (for collectors)")
    raw: Optional[str] = Field(None, description="Base64-encoded original data")

    # Screenshot
    screenshot_url: Optional[str] = Field(None, description="URL to screenshot")

    # Status and confidence
    status: Optional[str] = Field(None, description="Status of the event")
    tlp: Optional[TLPLiteral] = Field(None, description="Traffic Light Protocol level")

    # RTIR integration
    rtir_id: Optional[int] = Field(None, description="RTIR ticket ID")

    # Notification
    notification_email: Optional[str] = Field(None, description="Notification email address")
    notification_interval: Optional[int] = Field(None, description="Notification interval in seconds")

    @field_validator('time_source', 'time_observation', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime with IntelMQ compatibility"""
        if v is None or isinstance(v, datetime):
            return v

        if isinstance(v, str):
            try:
                # Try ISO format first (fast path)
                if 'T' in v:
                    dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
                else:
                    # Fuzzy parsing
                    dt = dateutil_parser.parse(v, fuzzy=True)

                # Ensure UTC timezone
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                else:
                    dt = dt.astimezone(timezone.utc)

                return dt
            except (ValueError, TypeError):
                return None

        return v

    @field_validator('tlp', mode='before')
    @classmethod
    def validate_tlp(cls, v):
        if not v:
            return v
        v = str(v).upper()
        # Remove TLP: prefix if present
        v = re.sub(r'^(TLP:?)?\s*', '', v)
        # Map YELLOW to AMBER
        if v == 'YELLOW':
            return 'AMBER'
        return v

    @field_validator('extra', mode='before')
    @classmethod
    def validate_extra(cls, v):
        """Ensure extra is a dict"""
        if v is None:
            return v
        if isinstance(v, dict):
            return v
        # Try to parse as JSON string
        if isinstance(v, str):
            import json
            try:
                parsed = json.loads(v)
                if isinstance(parsed, dict):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
        return None

    class Config:
        # Allow extra fields to be stored in 'extra'
        extra = 'allow'
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class IntelMQEventList(BaseModel):
    """List of extracted IntelMQ events"""
    events: list[IntelMQEvent] = Field(
        description="List of security events extracted from text, using complete IntelMQ harmonization format. See https://docs.intelmq.org/latest/user/event/ for a description of the IntelMQ harmonization format."
    )
