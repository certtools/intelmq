# Shadowserver-Parser README

## Structure of this Parser Bot:
The parser consists of two files:
 * config.py
 * parser.py

Both files are required for the parser to work properly.


## How to use the Parser:
Add the Shadowserver parser to your Botnet.

**Parameters**
 * feedname: The Name of the feed, see list below for possible values.
 * overwrite: If an existing `feed.name` should be overwritten.

Set at least the parameter `feedname`. it is required to find the correct
configuration. If this parameter is not set or not correct, the bot fail!
Feed-names are the subjects of the Shadowserver E-Mails.
They are different from the wiki page names!

Possible feednames:
* `Accessible-ADB`
* `Accessible-AFP`
* `Accessible-Cisco-Smart-Install`
* `Accessible-CWMP`
* `Accessible-Hadoop`
* `Accessible-HTTP`
* `Accessible-RDP`
* `Accessible-Rsync`
* `Accessible-SMB`
* `Accessible-Telnet`
* `Accessible-Ubiquiti-Discovery-Service`
* `Accessible-VNC`
* `Amplification-DDoS-Victim`
* `Blacklisted-IP`
* `Compromised-Website`
* `Darknet`
* `DNS-Open-Resolvers`
* `Drone`
* `Drone-Brute-Force`
* `HTTP-Scanners`
* `ICS-Scanners`
* `IPv6-Sinkhole-HTTP-Drone`
* `Microsoft-Sinkhole`
* `NTP-Monitor`
* `NTP-Version`
* `Open-Chargen`
* `Open-DB2-Discovery-Service`
* `Open-Elasticsearch`
* `Open-IPMI`
* `Open-LDAP` (also parses the `Open-LDAP-TCP` feed)
* `Open-mDNS`
* `Open-Memcached`
* `Open-MongoDB`
* `Open-MSSQL`
* `Open-NATPMP`
* `Open-NetBIOS-Nameservice`
* `Open-Netis`
* `Open-Portmapper`
* `Open-QOTD`
* `Open-Redis`
* `Open-SNMP`
* `Open-SSDP`
* `Open-TFTP`
* `Open-XDMCP`
* `Outdated-DNSSEC-Key`
* `Outdated-DNSSEC-Key-IPv6`
* `Sandbox-URL`
* `Sinkhole-HTTP-Drone`
* `Spam-URL`
* `SSL-FREAK-Vulnerable-Servers`
* `SSL-POODLE-Vulnerable-Servers`
* `Vulnerable-ISAKMP`

Additionally these deprecated names can still be used until removed in version 1.3:
* `Botnet-Drone-Hadoop` for `Drone`
* `DNS-open-resolvers` for `DNS-Open-Resolvers`
* `Open-NetBIOS` for `Open-NetBIOS-Nameservice`
* `Ssl-Freak-Scan` for `SSL-FREAK-Vulnerable-Servers`
* `Ssl-Scan` for `SSL-POODLE-Vulnerable-Servers`

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
