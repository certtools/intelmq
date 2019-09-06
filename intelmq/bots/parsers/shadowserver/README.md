# Shadowserver-Parser README

This bot parses multiple reports from Shadowserver.

## Structure of this Parser Bot:
The parser consists of two files:
 * config.py
 * parser.py

Both files are required for the parser to work properly.

## Requirements

The report to be processed MUST have `extra.file_name` set and it has to be
valid. A valid value has the following structure:
`%Y-%m-%d-${report_name}[-suffix].csv` where suffix can be something like `country-geo`. For example, some possible filenames are `2019-01-01-scan_http-country-geo.csv` or `2019-01-01-scan_tftp.csv`. The important part here ${report_name}, between the date and the suffix.


## Parameters

**Parameters**
 * `keep_feedname`: If report's `feed.name` should be kept instead of being
    overwritten by the bot with the value defined in config.py

## How this bot works?

When processing a report, this bot takes `extra.file_name` from the report and
looks in config.py how the report should be parsed.

## Supported reports:

These are the supported filenames (${report_name}) and their corresponding feed names:

| Filename             | Feed name |
|----------------------| ----------|            
| blacklist  | Blacklist |
| botnet_drone  | Drone |
| cisco_smart_install  | Accessible Cisco Smart Install |
| cwsandbox_url  | Sandbox URL |
| ddos_amplification  | Amplification DDoS Victim |
| drone_brute_force  | Drone Brute Force |
| microsoft_sinkhole  | Microsoft Sinkhole |
| scan_adb  | Accessible ADB |
| scan_afp  | Accessible AFP |
| scan_chargen  | Open Chargen |
| scan_cwmp  | Accessible CWMP |
| scan_dns  | DNS Open Resolvers |
| scan_elasticsearch  | Open Elasticsearch |
| scan_ftp  | Accessible FTP |
| scan_http  | Accessible HTTP |
| scan_ipmi  | Open IPMI |
| scan_isakmp  | Vulnerable ISAKMP |
| scan_ldap  | Open LDAP |
| scan_ldap_tcp  | Open LDAP |
| scan_mdns  | Open mDNS |
| scan_memcached  | Open Memcached |
| scan_mongodb  | Open mongoDB |
| scan_mssql  | Open MSSQL |
| scan_nat_pmp  | Open NATPMP |
| scan_netbios  | Open NetBIOS Nameservice |
| scan_ntp  | NTP Version |
| scan_ntpmonitor  | NTP Monitor |
| scan_portmapper  | Open Portmapper |
| scan_qotd  | Open QOTD |
| scan_rdp  | Accessible RDP |
| scan_redis  | Open Redis |
| scan_rsync  | Accessible Rsync |
| scan_smb  | Accessible SMB |
| scan_snmp  | Open SNMP |
| scan_ssdp  | Open SSDP |
| scan_ssl_freak  |  SSL FREAK Vulnerable Servers |
| scan_ssl_poodle  | SSL POODLE Vulnerable Servers |
| scan_telnet  | Accessible Telnet |
| scan_tftp  | Open TFTP |
| scan_ubiquiti  |  Open Ubiquiti |
| scan_vnc  | Accessible VNC |
| sinkhole_http_drone  | Sinkhole HTTP Drone |

## Add new Feedformats:
Add a new feedformat and conversions if required to the file
`config.py`. Don't forget to update the `feed_idx` dict.
It is required to look up the correct configuration.

### Configuration

In the following, *intelmqkey* are arbitrary keys from intelmq's harmonization
and *shadowkey* is a column name from shadowserver's data.

Every bot-type is defined by a dictionary with three values:
- `required_fields`: A list of tuples containing intelmq's field name, field
  name from data and an optional conversion function. Errors are raised, if the
  field does not exists in data.
- `optional_fields`: Same format as above, but does not raise errors if the
  field does not exist. If there's no mapping to an intelmq field, you can set
  the intelmqkey to `extra.` and the field will be added to the extra field
  using the original field name. See section below for possible tuple-values.
- `constant_fields`: A dictionary with a static mapping of field name to data,
  e.g. to set classifications or protocols.

The tuples can be of following format:

- `('intelmqkey', 'shadowkey')`, the data from the column *shadowkey* will be
  saved in the event's field *intelmqkey*. Logically equivalent to:
  `event[`*intelmqkey*`] = row[`*shadowkey*`]`.
- `('intelmqkey', 'shadowkey', conversion_function)`, the given function will be
  used to convert and/or validate the data. Logically equivalent to:
  `event[`*intelmqkey*`] = conversion_function(row[`*shadowkey*`)]`.
- `('intelmqkey', 'shadowkey', conversion_function, True)`, the function gets
  two parameters here, the second one is the full row (as dictionary). Logically
  equivalent to:
  `event[`*intelmqkey*`] = conversion_function(row[`*shadowkey*`, row)]`.
- `('extra.', 'shadowkey', conversion_function)`, the data will be added to
  extra in this case, the resulting name is `extra.[shadowkey]`. The
  `conversion_function` is optional. Logically equivalent to:
  `event[extra.`*intelmqkey*`] = conversion_function(row[`*shadowkey*`)]`.
