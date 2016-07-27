# Shadowserver-Parser Readme

## Structure of this Parser Bot:
The parser consists of two files:
 * config.py
 * parser.py

Both files are required for the parser to work properly.


## How to use the Parser:
Add the Shadowserver parser to your Botnet.

**Parameters**
 * feedname: The Name of the feed, see list below for possible values.
 * override: If an existing `feed.name` should be overriden.

Set at least the parameter `feedname`. it is required to find the correct
configuration. If this parameter is not set or not correct, the bot fail!
Feed-names are the Names of the Shadowserver Format specification pages.
E.g. `Botnet-Drone-Hadoop` for the feed corresponding to:
https://www.shadowserver.org/wiki/pmwiki.php/Services/Botnet-Drone-Hadoop

Possible feednames:
* DNS-open-resolvers
* Open-Mongo DB
* Open-Elasticsearch
* Open-SNMP
* Ssl-Scan
* Open-Redis
* Open-Memcached
* Open-m DNS
* Open-TFTP
* Open-NetBIOS
* NTP-Monitor
* Open-SSDP
* Open-Chargen
* Open-Portmapper
* Botnet-Drone-Hadoop
* Open-IPMI
* Open-MSSQL
* Sinkhole-HTTP-Drone
* Microsoft-Sinkhole


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
