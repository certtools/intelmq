# Bots Documentation

1. [Collectors](#collectors)
2. [Parsers](#parsers)
3. [Experts](#experts)
4. [Outputs](#outputs)


<a name="collectors"></a>
## Collectors

### HTTP

#### Information:
* `name:` http
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` collect report messages from remote hosts using http protocol

#### Configuration Parameters:
* `feed`: Name for the feed, usually found in collector bot configuration.
* `rate_limit`: time interval (in seconds) between messages processing
* `http_url`: location of information resource (e.g. https://feodotracker.abuse.ch/blocklist/?download=domainblocklist)
* `http_header`: FIXME
* `http_verify_cert`: FIXME
* `http_username`: FIXME
* `http_password`: FIXME
* `http_proxy`: FIXME
* `http_ssl_proxy`: FIXME


* * *

### Mail (URL)

#### Information:
* `name:` collector_mail_url
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` collect messages from mailboxes, extract urls from that messages and download the report messages from the urls.

#### Configuration Parameters:

* `feed`: Name for the feed, usually found in collector bot configuration.
* `rate_limit`: time interval (in seconds) between messages processing
* `mail_host`: fqdn or ip of mail server
* `mail_user`: user account of the email account
* `mail_password`: password associated to user account
* `mail_ssl`: FIXME
* `mail_folder`: FIXME
* `mail_subject_regex`: FIXME
* `mail_url_regex`: FIXME

* * *

### Mail (Attach)

#### Information:
* `name:` collector_mail_attach
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` -
* `description:` collect messages from mailboxes, download the report messages from the attachments.

#### Configuration Parameters:

* `feed`: Name for the feed, usually found in collector bot configuration.
* `rate_limit`: time interval (in seconds) between messages processing
* `mail_host`: FIXME
* `mail_user`: FIXME
* `mail_password`: FIXME
* `mail_ssl`: FIXME
* `mail_folder`: FIXME
* `mail_subject_regex`: FIXME
* `mail_folder`: FIXME
* `mail_attach_regex`: FIXME
* `mail_attach_unzip`: FIXME


* * *


### Alien Vault OTX

#### Information:
* `name:` http
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` -
* `description:` collect report messages from Alien Vault OTX API

#### Configuration Parameters:

* `feed`: Name for the feed, usually found in collector bot configuration.
* `rate_limit`: time interval (in seconds) between messages processing
* `api_key`: location of information resource (e.g. FIXME)




<a name="parsers"></a>
## Parsers

### \<ParserBot\>

#### Information:
* `name:` 
* `lookup:` 
* `public:` 
* `cache (redis db):` 
* `ipv6 support:` 
* `description:` 

#### Configuration Parameters:

* `<parameter>`: \<text\>




<a name="experts"></a>
## Experts

### Abusix

#### Information:
* `name:` abusix
* `lookup:` dns
* `public:` yes
* `cache (redis db):` 5
* `ipv6 support:` no (implementation missing)
* `description:` FIXME
* `notes`: https://abusix.com/contactdb.html

#### Configuration Parameters:

FIXME

* * *

### ASN Lookup

#### Information:
* `name:` asn-lookup
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` ip to asn

#### Configuration Parameters:

FIXME

* * *

### CERT.AT Contact

#### Information:
* `name:` certat-contact
* `lookup:` https
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` https://contacts.cert.at offers an IP address to national CERT contact (and cc) mapping. See https://contacts.cert.at for more info.

#### Configuration Parameters:

* `filter`: (true/false) act as a a filter for AT.
* `overwrite_cc`: set to true if you want to overwrite any potentially existing cc fields in the event.

* * *

### Cymru Whois

#### Information:
* `name:` cymru-whois
* `lookup:` cymru dns
* `public:` yes
* `cache (redis db):` 6
* `ipv6 support:` yes 
* `description:` ip to geolocation, asn, bgp prefix

#### Configuration Parameters:

FIXME

* * *

### Deduplicator

#### Information:
* `name:` deduplicator
* `lookup:` redis cache
* `public:` yes
* `cache (redis db):` 7
* `ipv6 support:` yes
* `description:` message deduplicator

#### Configuration Parameters:

FIXME

* * *

### Filter

#### Information:
* `name:` filter
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` filter messages (drop or pass messages) FIXME

#### Configuration Parameters:

FIXME

* * *

### MaxMind GeoIP

#### Information:
* `name:` maxmind-geoip
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` ip to geolocation

#### Configuration Parameters:

FIXME

* * *

### Reverse DNS

#### Information:
* `name:` reverse-dns
* `lookup:` dns
* `public:` yes
* `cache (redis db):` 8
* `ipv6 support:` no
* `description:` ip to domain

#### Configuration Parameters:

FIXME

* * *

### RipeNCC Abuse Contact

#### Information:
* `name:` ripencc-abuse-contact
* `lookup:` https api
* `public:` yes
* `cache (redis db):` 9
* `ipv6 support:` yes
* `description:` ip to abuse contact

#### Configuration Parameters:

FIXME

* * *

### Taxonomy

#### Information:
* `name:` taxonomy
* `lookup:` local config
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` -
* `description:` use eCSIRT taxonomy to classify events (classification type to classification taxonomy)

#### Configuration Parameters:

FIXME

* * *

### Tor Nodes

#### Information:
* `name:` tor-nodes
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` check if ip is tor node

#### Configuration Parameters:

FIXME

* * *

### Modify

#### Information:
* `name:` modify
* `lookup:` local config
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` -
* `description:` modify expert bot allows you to change arbitrary field values of events just using a configuration file

#### Configuration Parameters:

The modify expert bot allows you to change arbitrary field values of events just using a configuration file. Thus it is possible to adapt certain values or adding new ones only by changing JSON-files without touching the code of many other bots.

The configuration is called `modify.conf` and looks like this:

```json
{
"Spamhaus Cert": {
    "__default": [{
            "feed.name": "^Spamhaus Cert$"
        }, {
            "classification.identifier": "{msg[malware.name]}"
        }],
    "conficker": [{
            "malware.name": "^conficker(ab)?$"
        }, {
            "classification.identifier": "conficker"
        }],
    "urlzone": [{
            "malware.name": "^urlzone2?$"
        }, {
            "classification.identifier": "urlzone"
        }]
	}
}
```

The dictionary in the first level holds sections, here called `Spamhaus Cert` to group the rulessets and for easier navigation. It holds another dictionary of rules, consisting of *conditions* and *actions*. The first matching rule is used. Conditions and actions are again dictionaries holding the field names of harmonization and have regex-expressions to existing values (condition) or new values (action). The rule conditions are merged with the default condition and the default action is applied if no rule matches.

The default rule/action list may not exist. If the value is an empty string, the bot checks if the field does not exist. This is useful to apply default values for empty fields.

#### Examples

We have an event with `feed.name = Spamhaus Cert` and `malware.name = confickerab`. The expert loops over all sections in the file and enters section `Spamhaus Cert`. First, the default condition is checked, it matches! Ok, going on. Otherwise the expert would have continued to the next section. Now, iteration through the rules, the first is rule `conficker`. We combine the conditions of this rule with the default conditions, and both rules match! So we can apply the action, here `classification.identifier` is set to `conficker`, the trivial name.

Assume we have an event with `feed.name = Spamhaus Cert` and `malware.name = feodo`. The default condition matches, but no others. So the default action is applied. The value for `classification.identifier` is `{msg[malware.name]}`, this is [standard Python string format syntax](https://docs.python.org/3/library/string.html#formatspec). Thus you can use any value from the processed event, which is available as `msg`.




<a name="outputs"></a>
## Outputs

### File

#### Information:
* `name:` file
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` output messages (reports or events) to file

#### Configuration Parameters:

* `file`: filepath of output file


* * *


### MongoDB

#### Information:
* `name:` mongodb
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` MongoDB is the bot responsible to send events to a MongoDB database

#### Configuration Parameters:

* `collection`: MongoDB collection
* `database`: MongoDB database
* `host`: MongoDB host (fqdn or IP)
* `port`: MongoDB port

#### Installation Requirements

Using Python 3.4 (recommended):
```
pip3 install pymongo>=2.7.1
```

Using Python 2.7:
```
pip2 install pymongo>=2.7.1
```


* * *


### IntelMQ Mailer

#### Information:
* `name:` intelmqmailer
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` IntelMQ Mailer is the bot responsible to send events to a MongoDB database that supports IntelMQ Mailer platform

#### Configuration Parameters:

* `collection`: MongoDB collection
* `database`: MongoDB database
* `host`: MongoDB host (FQDN or IP)
* `port`: MongoDB port

#### Installation Requirements

Using Python 3.4 (recommended):
```
pip3 install pymongo>=2.7.1
```

Using Python 2.7:
```
pip2 install pymongo>=2.7.1
```


* * *


### PostgreSQL

#### Information:
* `name:` postgresql
* `lookup:` no 
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` PostgreSQL is the bot responsible to send events to a PostgreSQL Database
* `notes`: When activating autocommit, transactions are not used: http://initd.org/psycopg/docs/connection.html#connection.autocommit

#### Configuration Parameters:

* `autocommit`: FIXME
* `database`: PostgreSQL database
* `host`: PostgreSQL host
* `port`: PostgreSQL port
* `user`: PostgreSQL user
* `password`: PostgreSQL password
* `sslmode`: FIXME
* `autocommit`: FIXME
* `table`: FIXME

#### Installation Requirements

Using Python 3.4 (recommended):
```
pip3 install psycopg2>=2.5.5
```

Using Python 2.7:
```
pip2 install psycopg2>=2.5.5
```

#### PostgreSQL Installation

* Install PostgreSQL, at least version 9.4 is required.

```bash
> apt-get install postgresql-9.4 python-psycopg2 postgresql-server-dev-9.4
```

* Create a User and Database:

```shell
> su - postgres
> createuser intelmq -W
  Shall the new role be a superuser? (y/n) n
  Shall the new role be allowed to create databases? (y/n) y
  Shall the new role be allowed to create more new roles? (y/n) n
  Password: 

> createdb -O intelmq --encoding='utf-8' intelmq-events
```

* Please note the --encoding='utf-8' in the line above! Without it, the output but will not be able to insert utf-8 data into the table.

* Depending on your setup adjust `/etc/postgresql/9.4/main/pg_hba.conf` to allow network connections for the intelmq user.

* Restart PostgreSQL.

* Generate `initdb.sql` by using the [psql_initdb_generator.py](https://github.com/certtools/intelmq/blob/master/intelmq/bin/intelmq_psql_initdb.py) tool which extracts all field names and data types from `Data-Harmonization.md`.

* Create the `events` table:

```bash
> psql intelmq-events < /tmp/initdb.sql # as intelmq user
> psql -U intelmq intelmq-events -W < /tmp/initdb.sql # as other user
```


* * *


### REST API

#### Information:
* `name:` restapi
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` REST API is the bot responsible to send events to a REST API listener through POST

#### Configuration Parameters:

* `auth_token`: FIXME
* `auth_token_name`: FIXME
* `host`: FIXME


* * *


### TCP

#### Information:
* `name:` tcp
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `ipv6 support:` yes
* `description:` TCP is the bot responsible to send events to a tcp port (Splunk, ElasticSearch, etc..)

#### Configuration Parameters:

* `ip`: FIXME
* `port`: FIXME
