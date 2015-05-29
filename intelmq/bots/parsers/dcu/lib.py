from datetime import datetime, timedelta
from dateutil.tz import tzutc
import types

def convert_windows_timestamp(windows_ts):
    """Convert a windows file utc timestamp to a datetime object"""
    us = int(windows_ts)/10
    dt = datetime(1601,1,1, tzinfo=tzutc()) + timedelta(microseconds=us)
    return dt

def filetimeutc_as_source_time(ts):
    """Convert the given FileTimeUTC timestamp to a UTC datetime object """
    parts = ("reported_source_time", str(convert_windows_timestamp(ts)))
    return parts

def convert_malware_field(malware_name):
    return ("reported_malware", malware_name.lower())

INTELMQ_TX = {"SourcedFrom": None,  # TBD
              "FileTimeUtc": filetimeutc_as_source_time,
              "Botnet": convert_malware_field, 
              "SourceIp": "reported_source_ip", 
              "SourcePort": "reported_source_port", 
              "SourceIpAsnNr": "reported_source_asn", 
              "TargetIp": "reported_destination_ip", 
              "TargetPort": "reported_destination_port", 
              "Payload": None,  # TBD
              "SourceIpCountryCode": "reported_source_cc", 
              "SourceIpRegion": None, # TBD
              "SourceIpCity": "reported_source_city", 
              "SourceIpPostalCode": None, # TBD
              "SourceIpLatitude": "reported_source_latitude",
              "SourceIpLongitude": "reported_source_longitude",
              "SourceIpMetroCode": None, # TBD
              "SourceIpAreaCode": None, # TBD
              "HttpRequest": "reported_http_request",  # TBD
              "HttpReferrer": "reported_http_referrer",  # TBD 
              "HttpUserAgent": "reported_http_user_agent", 
              "HttpMethod": "reported_http_method",   # TBD
              "HttpVersion": "reported_http_version",  # TBD
              "HttpHost": "reported_http_host",  # TBD 
              "Custom Field 1": None,  # TBD 
              "Custom Field 2": None,  # TBD
              "Custom Field 3": None,  # TBD
              "Custom Field 4": None,  # TBD
              "Custom Field 5": None}  # TBD

def convert_dcu_field(dcu_field, value):
    # Converts the given dcu field to intelMQ field
    converter = INTELMQ_TX[dcu_field]
    if isinstance(converter, types.FunctionType):
        return converter(value)
    elif isinstance(converter, types.StringType):
        return (converter, value)
    else:
        return None
