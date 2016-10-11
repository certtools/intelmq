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
* `description:` collect messages from mailboxes, extract URLs from that messages and download the report messages from the URLs.

#### Configuration Parameters:

* `feed`: Name for the feed, usually found in collector bot configuration.
* `rate_limit`: time interval (in seconds) between messages processing
* `mail_host`: FQDN or IP of mail server
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
* `description:` FIXME
* `notes`: https://abusix.com/contactdb.html

#### Configuration Parameters:

FIXME

* * *

### ASN Lookup

#### Information:
* `name:` ASN lookup
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` IP to ASN

#### Configuration Parameters:

FIXME

* * *

### CERT.AT Contact

#### Information:
* `name:` certat-contact
* `lookup:` https
* `public:` yes
* `cache (redis db):` none
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
* `description:` IP to geolocation, ASN, BGP prefix

#### Configuration Parameters:

FIXME

* * *

### Deduplicator

#### Information:
* `name:` deduplicator
* `lookup:` redis cache
* `public:` yes
* `cache (redis db):` 7
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
* `description:` IP to geolocation

#### Configuration Parameters:

FIXME

* * *

### Reverse DNS

#### Information:
* `name:` reverse-dns
* `lookup:` dns
* `public:` yes
* `cache (redis db):` 8
* `description:` IP to domain

#### Configuration Parameters:

FIXME

* * *

### RipeNCC Abuse Contact

#### Information:
* `name:` ripencc-abuse-contact
* `lookup:` https api
* `public:` yes
* `cache (redis db):` 9
* `description:` IP to abuse contact

#### Configuration Parameters:

FIXME

* * *

### Taxonomy

#### Information:
* `name:` taxonomy
* `lookup:` local config
* `public:` yes
* `cache (redis db):` none
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
* `description:` check if IP is tor node

#### Configuration Parameters:

FIXME

* * *

### Modify

#### Information:
* `name:` modify
* `lookup:` local config
* `public:` yes
* `cache (redis db):` none
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
        }],
    "bitdefender" : [{
            "malware.name": "bitdefender-(.*)$"
        }, {
            "malware.name": "{matches[malware.name][1]}"
        }]
    },
"Standard Protocols": {
    "http": [{
            "source.port": "^(80|443)$"
        }, {
            "protocol.application": "http"
        }]
    }
}
```

The dictionary on the first level holds sections to group the rules.
In our example above we have two sections labeled `Spamhaus Cert` and `Standard Protocols`.
All sections will be considered, but in undefined order.

Each section holds a dictionary of rules, consisting of *conditions* and *actions*.
`__default` indicates an optional default rule. If a default rule exist, the section
will only be entered, if its conditions match. Actions are optional for the default rule.

Conditions and actions are again dictionaries holding the field names of events
and regex-expressions to match values (condition) or set values (action).
All matching rules will be applied in no particular order.
Matching checks if all joined conditions of the rule and the default rule
are true before performing the actions.
If no rule within a section matches, existing actions of the default rule for the section are applied.

If the value for a condition is an empty string, the bot checks if the field does not exist.
This is useful to apply default values for empty fields.

**Attention**: Because the order of execution is undefined,
you need to take care that no rule depends on values modified by another rule.
Otherwise the results of the bot may be different from one run to the other.
(A redesign is [under discussion](https://github.com/certtools/intelmq/issues/662)
to improve the situation for future versions.)

#### Actions

You can set the value of the field to a string literal or number.

In addition you can use the [standard Python string format syntax](https://docs.python.org/3/library/string.html#format-string-syntax)
to access the values from the processed event as `msg` and the match groups
of the conditions as `matches`, see the bitdefender example above.
Note that `matches` will also contain the match groups
from the default conditions if there were any.

#### Examples

We have an event with `feed.name = Spamhaus Cert` and `malware.name = confickerab`. The expert loops over all sections in the file and eventually enters section `Spamhaus Cert`. First, the default condition is checked, it matches! Ok, going on. Otherwise the expert would have selected a different section that has not yet been considered. Now, go through the rules, until we hit the rule `conficker`. We combine the conditions of this rule with the default conditions, and both rules match! So we can apply the action: `classification.identifier` is set to `conficker`, the trivial name.

Assume we have an event with `feed.name = Spamhaus Cert` and `malware.name = feodo`. The default condition matches, but no others. So the default action is applied. The value for `classification.identifier` will be set to `feodo` by `{msg[malware.name]}`.

#### Types

If the rule is a string, a regex-search is performed, also for numeric values (`str()` is called on them). If the rule is numeric for numeric values, a simple comparison is done. If other types are mixed, a warning will be thrown.


<a name="outputs"></a>
## Outputs

### File

#### Information:
* `name:` file
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` output messages (reports or events) to file

#### Configuration Parameters:

* `file`: file path of output file


* * *


### MongoDB

#### Information:
* `name:` mongodb
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` MongoDB is the bot responsible to send events to a MongoDB database

#### Configuration Parameters:

* `collection`: MongoDB collection
* `database`: MongoDB database
* `host`: MongoDB host (FQDN or IP)
* `port`: MongoDB port

#### Installation Requirements

```
pip3 install pymongo>=2.7.1
```

* * *


### PostgreSQL

#### Information:
* `name:` postgresql
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` PostgreSQL is the bot responsible to send events to a PostgreSQL Database
* `notes`: When activating autocommit, transactions are not used: http://initd.org/psycopg/docs/connection.html#connection.autocommit

#### Configuration Parameters:

The parameters marked with 'PostgreSQL' will be sent
to libpq via psycopg2. Check the
[libpq parameter documentation] (https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS)
for the versions you are using.

* `autocommit`: [psycopg's autocommit mode](http://initd.org/psycopg/docs/connection.html?#connection.autocommit), optional, default True
* `connect_timeout`: PostgreSQL connect_timeout, optional, default 5 seconds
* `database`: PostgreSQL database
* `host`: PostgreSQL host
* `port`: PostgreSQL port
* `user`: PostgreSQL user
* `password`: PostgreSQL password
* `sslmode`: PostgreSQL sslmode
* `table`: name of the database table into which events are to be inserted

#### Installation Requirements

See [REQUIREMENTS.txt](../intelmq/bots/outputs/postgresql/REQUIREMENTS.txt)
from your installation.

#### PostgreSQL Installation

See [outputs/postgresql/README.md](../intelmq/bots/outputs/postgresql/README.md)
from your installation.

* * *


### REST API

#### Information:
* `name:` restapi
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
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
* `description:` TCP is the bot responsible to send events to a tcp port (Splunk, ElasticSearch, etc..)

#### Configuration Parameters:

* `ip`: FIXME
* `port`: FIXME
