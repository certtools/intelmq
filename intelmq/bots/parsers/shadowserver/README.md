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
* Open-Net BIOS
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

Every bot-type is defined by a dictionary with three values:
- `required_fields`: A list of tuples containing intelmq's field name, field
  name from data and an optional conversion function. Errors are raisen, when
  field does not exists in data.
- `optional_fields`: Same format as above, but does not raise errors of field
  does not exist. If there's no mapping to an intelmq field, you can give a
  tuple of showserver key and conversion function or not mention it at all.
  In both cases, the data will be added to extra.
- `additional_fields`: A dictionary with a static mapping of field name to
  data, e.g. to set classifications or protocols.

The tuples can be of following format:

- `('intelmqkey', 'shadowkey')`
- `('intelmqkey', 'shadowkey', conversion_function)`
- `('shadowkey', conversion_function)`, data will be added to extra in this case
- `('intelmqkey', 'shadowkey', conversion_function, True)`, the function gets two parameters here, the second one is the full row (as dictionary)
