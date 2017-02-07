# Bots Documentation

1. [Collectors](#collectors)
2. [Parsers](#parsers)
3. [Experts](#experts)
4. [Outputs](#outputs)

By default all of the bots are started when you start the whole botnet, however there is a possibility to 
*disable* a bot. This means that the bot will not start every time you start the botnet, but you can start 
and stop the bot if you specify the bot explicitly. To disable a bot, add the following to your 
`runtime.conf`: `"enabled": false`. Be aware that this is **not** a normal parameter (like the others 
described in this file). It is set outside of the `parameters` object in `runtime.conf`. Check the 
[User-Guide](./User-Guide.md) for an example.


<a name="collectors"></a>
## Collectors

**Feed parameters**: Common configuration options for all collectors

* `feed`: Name for the feed.
* `code`: Code for the feed.
* `provider`: Name of the provider of the feed.
* `rate_limit`: time interval (in seconds) between messages processing.

**HTTP parameters**: Common URL fetching parameters used in multiple collectors

* `http_username`: username for basic authentication.
* `http_password`: password for basic authentication.
* `http_proxy`: proxy to use for http
* `https_proxy`: proxy to use for https
* `http_user_agent`: user agent to use for the request.
* `http_verify_cert`: path to trusted CA bundle or directory, `false` to ignore verifying SSL certificates,  or `true` (default) to verify SSL certificates
* `ssl_client_certificate`: SSL client certificate to use.
* `http_header`: HTTP request headers
* `http_timeout`: Seconds for read and connect timeout. Can be one float (applies for both timeouts) or a tuple of two floats. Default: 60 seconds. See also https://requests.readthedocs.io/en/master/user/advanced/#timeouts



### Generic URL Fetcher


#### Information:
* `name:` intelmq.bots.collectors.http.collector_http
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect report messages from remote hosts using http protocol

#### Configuration Parameters:

* **Feed parameters** (see above)
* **HTTP parameters** (see above)
* `http_url`: location of information resource (e.g. https://feodotracker.abuse.ch/blocklist/?download=domainblocklist)


* * *

### Generic URL Stream Fetcher


#### Information:
* `name:` intelmq.bots.collectors.http.collector_http_stream
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Opens a streaming connection to the URL and sends the received lines.

#### Configuration Parameters:

* **Feed parameters** (see above)
* **HTTP parameters** (see above)
* `http_url`: location of HTTP streaming resource
* `strip_lines`: boolean, if single lines should be stripped (removing whitespace from the beginning and the end of the line)

If the stream is interrupted, the connection will be aborted using the timeout parameter. Then, an error will be thrown and rate_limit applies if not null.

* * *

### Generic Mail URL Fetcher


#### Information:
* `name:` intelmq.bots.collectors.mail.collector_mail_url
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from mailboxes, extract URLs from that messages and download the report messages from the URLs.

#### Configuration Parameters:

* **Feed parameters** (see above)
* **HTTP parameters** (see above)
* `mail_host`: FQDN or IP of mail server
* `mail_user`: user account of the email account
* `mail_password`: password associated with the user account
* `mail_ssl`: whether the mail account uses SSL (default: `true`)
* `folder`: folder in which to look for mails (default: `INBOX`)
* `subject_regex`: regular expression to look for a subject
* `url_regex`: regular expression of the feed URL to search for in the mail body 

* * *

### Generic Mail Attachment Fetcher


#### Information:
* `name:` intelmq.bots.collectors.mail.collector_mail_attach
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from mailboxes, download the report messages from the attachments.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `mail_host`: FQDN or IP of mail server
* `mail_user`: user account of the email account
* `mail_password`: password associated with the user account
* `mail_ssl`: whether the mail account uses SSL (default: `true`)
* `folder`: folder in which to look for mails (default: `INBOX`)
* `subject_regex`: regular expression to look for a subject
* `attach_regex`: regular expression of the name of the attachment
* `attach_unzip`: whether to unzip the attachment (default: `true`)

* * *

### Fileinput

#### Information:
* `name:` intelmq.bots.collectors.file.collector_file
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from a file.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `path`: path to file
* `postfix`: FIXME
* `delete_file`: whether to delete the file after reading (default: `false`)


* * *

### MISP Generic


#### Information:
* `name:` intelmq.bots.collectors.misp.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from a MISP server.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `misp_url`: url of MISP server (with trailing '/')
* `misp_key`: MISP Authkey
* `misp_verify`: (default: `true`)
* `misp_tag_to_process`: MISP tag for events to be processed
* `misp_tag_processed`: MISP tag for processed events

* * *

### Request Tracker

        
#### Information:
* `name:` intelmq.bots.collectors.rt.collector_rt
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Request Tracker Collector fetches attachments from an RTIR instance and optionally decrypts them with gnupg.

#### Configuration Parameters:

* **Feed parameters** (see above)
* **HTTP parameters** (see above)
* `uri`: url of the REST interface of the RT
* `user`: RT username
* `password`: RT password
* `search_owner`: owner of the ticket to search for (default: `nobody`)
* `search_queue`: queue of the ticket to search for (default: `Incident Reports`)
* `search_status`: status of the ticket to search for (default: `new`)
* `search_subject_like`: part of the subject of the ticket to search for (default: `Report`)
* `set_status`: status to set the ticket to after processing (default: `open`)
* `take_ticket`: whether to take the ticket (default: `true`)
* `url_regex`: regular expression of an URL to search for in the ticket
* `attachment_regex`: regular expression of an attachment in the ticket
* `unzip_attachment`: whether to unzip a found attachment
        
* * *

### XMPP collector


#### Information:
* `name:` intelmq.bots.collectors.xmpp.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` This bot can connect to an XMPP Server and one room, in order to receive reports from it. TLS is used by default. rate_limit is ineffective here. Bot can either pass the body or the whole event.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `xmpp_server`: FIXME
* `xmpp_user`: FIXME
* `xmpp_password`: FIXME
* `xmpp_room`: FIXME
* `xmpp_room_nick`: FIXME
* `xmpp_room_passsword`: FIXME
* `ca_certs`: FIXME (default: `/etc/ssl/certs/ca-certificates.crt`)
* `strip_message`: FIXME (default: `true`)
* `pass_full_xml`: FIXME (default: `false`)

* * *


### Alien Vault OTX


#### Information:
* `name:` intelmq.bots.collectors.alienvault_otx.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect report messages from Alien Vault OTX API

#### Configuration Parameters:

* **Feed parameters** (see above)
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
* `hierarchical_output`: Boolean (default true) as mongodb does not allow saving keys with dots, we split the dictionay in sub-dictionaries.

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
