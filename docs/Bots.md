# Bots Documentation

**Table of Contents:**
- [Bots Documentation](#bots-documentation)
- [General remarks](#general-remarks)
- [Initialization parameters](#initialization-parameters)
- [Common parameters](#common-parameters)
- [Collectors](#collectors)
  - [Generic URL Fetcher](#generic-url-fetcher)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Generic URL Stream Fetcher](#generic-url-stream-fetcher)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Generic Mail URL Fetcher](#generic-mail-url-fetcher)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Generic Mail Attachment Fetcher](#generic-mail-attachment-fetcher)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Fileinput](#fileinput)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [MISP Generic](#misp-generic)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Request Tracker](#request-tracker)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Shodan Stream](#shodan-stream)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [TCP](#tcp)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [XMPP collector](#xmpp-collector)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Alien Vault OTX](#alien-vault-otx)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Blueliv Crimeserver](#blueliv-crimeserver)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Microsoft Azure](#microsoft-azure)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Microsoft Interflow](#microsoft-interflow)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
    - [Additional functionalities](#additional-functionalities)
  - [Stomp](#stomp)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Twitter](#twitter)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
- [Parsers](#parsers)
  - [Generic CSV Parser](#generic-csv-parser)
    - [Configuration parameters](#configuration-parameters)
  - [Cymru CAP Program](#cymru-cap-program)
    - [Information:](#information)
  - [Cymru Full Bogons](#cymru-full-bogons)
    - [Information:](#information)
  - [Twitter](#twitter)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Shodan](#shodan)
    - [Information](#information)
    - [Configuration Parameters:](#configuration-parameters)
- [Experts](#experts)
  - [Abusix](#abusix)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [ASN Lookup](#asn-lookup)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Cymru Whois](#cymru-whois)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Domain Suffix](#domain-suffix)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
    - [Rule processing](#rule-processing)
  - [Deduplicator](#deduplicator)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Field Reducer Bot](#field-reducer-bot)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
      - [Whitelist](#whitelist)
      - [Blacklist](#blacklist)
  - [Filter](#filter)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Generic DB Lookup](#generic-db-lookup)
  - [Gethostbyname](#gethostbyname)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [IDEA](#idea)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [MaxMind GeoIP](#maxmind-geoip)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Modify](#modify)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Configuration File](#configuration-file)
    - [Actions](#actions)
    - [Examples](#examples)
    - [Types](#types)
  - [National CERT contact lookup by CERT.AT](#national-cert-contact-lookup-by-certat)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Reverse DNS](#reverse-dns)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [RFC1918](#rfc1918)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [RipeNCC Abuse Contact](#ripencc-abuse-contact)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Sieve](#sieve)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Taxonomy](#taxonomy)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Tor Nodes](#tor-nodes)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Url2FQDN](#url2fqdn)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [Wait](#wait)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
- [Outputs](#outputs)
  - [File](#file)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
      - [Filename formatting](#filename-formatting)
  - [Files](#files)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [MongoDB](#mongodb)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
    - [Installation Requirements](#installation-requirements)
  - [PostgreSQL](#postgresql)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
    - [Installation Requirements](#installation-requirements)
    - [PostgreSQL Installation](#postgresql-installation)
  - [REST API](#rest-api)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
- [SMTP Output Bot](#smtp-output-bot)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)
  - [TCP](#tcp)
    - [Information:](#information)
    - [Configuration Parameters:](#configuration-parameters)


## General remarks

By default all of the bots are started when you start the whole botnet, however there is a possibility to
*disable* a bot. This means that the bot will not start every time you start the botnet, but you can start
and stop the bot if you specify the bot explicitly. To disable a bot, add the following to your
`runtime.conf`: `"enabled": false`. Be aware that this is **not** a normal parameter (like the others
described in this file). It is set outside of the `parameters` object in `runtime.conf`. Check the
[User-Guide](./User-Guide.md) for an example.

There are two different types of parameters: The initialization parameters are need to start the bot. The runtime parameters are needed by the bot itself during runtime.

The initialization parameters are in the first level, the runtime parameters live in the `parameters` sub-dictionary:

```json
{
    "bot-id": {
        "parameters": {
            runtime parameters...
        },
        initialization parameters...
    }
}
```
For example:
```json
{
    "abusech-feodo-domains-collector": {
        "parameters": {
            "provider": "Abuse.ch",
            "feed": "Abuse.ch Feodo Domains",
            "http_url": "http://example.org/feodo-domains.txt"
        },
        "name": "Generic URL Fetcher",
        "group": "Collector",
        "module": "intelmq.bots.collectors.http.collector_http",
        "description": "collect report messages from remote hosts using http protocol",
        "enabled": true,
        "run_mode": "scheduled"
    }
}
```

This configuration resides in the file `runtime.conf` in your intelmq's configuration directory for each configured bot.

## Initialization parameters

* `name` and `description`: The name and description of the bot as can be found in BOTS-file, not used by the bot itself.
* `group`: Can be `"Collector"`, `"Parser"`, `"Expert"` or `"Output"`. Only used for visualization by other tools.
* `module`: The executable (should be in `$PATH`) which will be started.
* `enabled`: If the parameter is set to `true` (which is NOT the default value if it is missing as a protection) the bot will start when the botnet is started (`intelmqctl start`). If the parameter was set to `false`, the Bot will not be started by `intelmqctl start`, however you can run the bot independently using `intelmqctl start <bot_id>`. Check the [User-Guide](./User-Guide.md) for more details.
* `run_mode`: There are two run modes, "continuous" (default run mode) or "scheduled". In the first case, the bot will be running forever until stopped or exits because of errors (depending on configuration). In the latter case, the bot will stop after one successful run. This is especially useful when scheduling bots via cron or systemd. Default is `continuous`. Check the [User-Guide](./User-Guide.md) for more details.

## Common parameters

**Feed parameters**: Common configuration options for all collectors.

* `feed`: Name for the feed (`feed.name`).
* `accuracy`: Accuracy for the data of the feed (`feed.accuracy`).
* `code`: Code for the feed (`feed.code`).
* `documentation`: Link to documentation for the feed (`feed.documentation`).
* `provider`: Name of the provider of the feed (`feed.provider`).
* `rate_limit`: time interval (in seconds) between fetching data if applicable.

**HTTP parameters**: Common URL fetching parameters used in multiple bots.

* `http_timeout_sec`: A tuple of floats or only one float describing the timeout of the http connection. Can be a tuple of two floats (read and connect timeout) or just one float (applies for both timeouts). The default is 30 seconds in default.conf, if not given no timeout is used. See also https://requests.readthedocs.io/en/master/user/advanced/#timeouts
* `http_timeout_max_tries`: An integer depciting how often a connection is retried, when a timeout occured. Defaults to 3 in default.conf.
* `http_username`: username for basic authentication.
* `http_password`: password for basic authentication.
* `http_proxy`: proxy to use for http
* `https_proxy`: proxy to use for https
* `http_user_agent`: user agent to use for the request.
* `http_verify_cert`: path to trusted CA bundle or directory, `false` to ignore verifying SSL certificates,  or `true` (default) to verify SSL certificates
* `ssl_client_certificate`: SSL client certificate to use.
* `http_header`: HTTP request headers

**Cache parameters**: Common redis cache parameters used in multiple bots (mainly lookup experts):

* `redis_cache_host`: Hostname of the redis database.
* `redis_cache_port`: Port of the redis database.
* `redis_cache_db`: Database number.
* `redis_cache_ttl`: TTL used for caching.
* `redis_cache_password`: Optional password for the redis database (default: none).

## Collectors


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
* `extract_files`: To extract the archive:
  * `true` for auto-detection / all files
  * a string of file names separated by `,`
  * otherwise `null` or `false` for no extraction
* `http_url`: location of information resource (e.g. https://feodotracker.abuse.ch/blocklist/?download=domainblocklist)
* `http_url_formatting`: If `True` (default `False`) `{time[format]}` will be replaced by the current time formatted by the given format. E.g. if the URL is `http://localhost/{time[%Y]}`, then the resulting URL is `http://localhost/2018` for the year 2018. Currently only the time in local timezone is available. Python's [Format Specification Mini-Language¶](https://docs.python.org/3/library/string.html) is used for this.


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
* `strip_lines`: boolean, if single lines should be stripped (removing whitespace from the beginning and the end of the line)

If the stream is interrupted, the connection will be aborted using the timeout parameter. Then, an error will be thrown and rate_limit applies if not null.
The parameter `http_timeout_max_tries` is of no use in this collector.


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
* `sent_from`: filter messages by sender
* `sent_to`: filter messages by recipient

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
* `description:` Request Tracker Collector fetches attachments from an RTIR instance.

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

The parameter `http_timeout_max_tries` is of no use in this collector.

* * *

### Shodan Stream

Requires the shodan library to be installed:
 * https://github.com/achillean/shodan-python/
 * https://pypi.org/project/shodan/

#### Information:
* `name:` intelmq.bots.collectors.shodan.collector_stream
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Queries the Shodan Streaming API

#### Configuration Parameters:

* **Feed parameters** (see above)
* **HTTP parameters** (see above). Only the proxy is used (requires shodan-python > 1.8.1). Certificate is always verified.
* `countries`: A list of countries to query for. If it is a string, it will be spit by `,`.

* * *

### TCP

#### Information:
* `name:` intelmq.bots.collectors.tcp.collector
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` TCP is the bot responsible to receive events on a TCP port (ex: from TCP Output of another IntelMQ instance). Might not be working on Python3.4.6.

#### Configuration Parameters:

* `ip`: IP of destination server
* `port`: port of destination server
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
* `xmpp_room_password`: FIXME
* `ca_certs`: FIXME (default: `/etc/ssl/certs/ca-certificates.crt`)
* `strip_message`: FIXME (default: `true`)
* `pass_full_xml`: FIXME (default: `false`)

* * *


### Alien Vault OTX

See the README.md

#### Information:
* `name:` intelmq.bots.collectors.alienvault_otx.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect report messages from Alien Vault OTX API

#### Configuration Parameters:

* **Feed parameters** (see above)
* `api_key`: location of information resource (e.g. FIXME)

* * *

### Blueliv Crimeserver

See the README.md

#### Information:
* `name:` intelmq.bots.collectors.blueliv.collector_crimeserver
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect report messages from Blueliv API

#### Configuration Parameters:

* **Feed parameters** (see above)
* `api_key`: location of information resource

* * *

### Microsoft Azure

Iterates over all blobs in all containers in an Azure storage.

#### Information:
* `name:` intelmq.bots.collectors.microsoft.collector_azure
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect blobs from microsoft azure using their library

#### Configuration Parameters:

* **Feed parameters** (see above)
* `account_name`: account name as give by Microsoft
* `account_key`: account key as give by Microsoft
* `delete`: boolean, delete containers and blobs after fetching

* * *

### Microsoft Interflow

Iterates over all files available by this API. Make sure to limit the files to be downloaded with the parameters, otherwise you will get a lot of data!
The cache is used to remember which files have already been downloaded. Make sure the TTL is high enough, higher than `not_older_than`.

#### Information:
* `name:` intelmq.bots.collectors.microsoft.collector_interflow
* `lookup:` yes
* `public:` no
* `cache (redis db):` 5
* `description:` collect files from microsoft interflow using their API

#### Configuration Parameters:

* **Feed parameters** (see above)
* `api_key`: API generate in their portal
* `file_match`: an optional regular expression to match file names
* `not_older_than`: an optional relative (minutes) or absolute time (UTC is assumed) expression to determine the oldest time of a file to be downloaded
* `redis_cache_*` and especially `redis_cache_ttl`: Settings for the cache where file names of downloaded files are saved. The cache's TTL must always be bigger than `not_older_than`.

#### Additional functionalities

* Files are automatically ungzipped if the filename ends with `.gz`.

* * *

### Stomp

See the README.md in `intelmq/bots/collectors/stomp/`

#### Information:
* `name:` intelmq.bots.collectors.stomp.collector
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect messages from a stomp server

#### Configuration Parameters:

* **Feed parameters** (see above)
* `exchange`: exchange point
* `port`: 61614
* `server`: hostname e.g. "n6stream.cert.pl"
* `ssl_ca_certificate`: path to CA file
* `ssl_client_certificate`: path to client cert file
* `ssl_client_certificate_key`: path to client cert key file

* * *

### Twitter

Collects tweets from target_timelines. Up to tweet_count tweets from each user and up to timelimit back in time. The tweet text is sent separately and if allowed, links to pastebin are followed and the text sent in a separate report 

#### Information:
* `name:` intelmq.bots.collectors.twitter.collector_twitter
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Collects tweets
#### Configuration Parameters:

* **Feed parameters** (see above)
* `target_timelines`: screen_names of twitter accounts to be followed
* `tweet_count`: number of tweets to be taken from each account
* `timelimit`: maximum age of the tweets collected in seconds
* `follow_urls`: list of screen_names for which urls will be followed
* `exclude_replies`: exclude replies of the followed screen_names
* `include_rts`: whether to include retweets by given screen_name 
* `consumer_key`: Twitter api login data
* `consumer_secret`: Twitter api login data
* `acces_token_key`: Twitter api login data
* `access_token_secret`: Twitter api login data

## Parsers

TODO

### Generic CSV Parser

Lines starting with `'#'` will be ignored. Headers won't be interpreted.

#### Configuration parameters

 * `"columns"`: A list of strings or a string of comma-separated values with field names. The names must match the harmonization's field names. Empty column specifications and columns named `"__IGNORE__"` are ignored. E.g.
   ```json
   "columns": [
        "",
        "source.fqdn",
        "extra.http_host_header",
        "__IGNORE__"
   ],
   ```
   is equivalent to:
   ```json
   "columns": ",source.fqdn,extra.http_host_header,"
   ```
   The first and the last column are not used in this example.
    It is possible to specify multiple columns using the `|` character. E.g.
    ```
        "columns": "source.url|source.fqdn|source.ip"
    ```
    First, bot will try to parse the value as url, if it fails, it will try to parse it as FQDN, if that fails, it will try to parse it as IP, if that fails, an error wil be raised.
    Some use cases - 
    
        - mixed data set, e.g. URL/FQDN/IP/NETMASK  `"columns": "source.url|source.fqdn|source.ip|source.network"`
    
        - parse a value and ignore if it fails  `"columns": "source.url|__IGNORE__"`
        
 * `"column_regex_search"`: Optional. A dictionary mapping field names (as given per the columns parameter) to regular expression. The field is evaulated using `re.search`. Eg. to get the ASN out of `AS1234` use: `{"source.asn": "[0-9]*"}`.
 * `"default_url_protocol"`: For URLs you can give a defaut protocol which will be pretended to the data.
 * `"delimiter"`: separation character of the CSV, e.g. `","`
 * `"skip_header"`: Boolean, skip the first line of the file, optional. Lines starting with `#` will be skipped additionally, make sure you do not skip more lines than needed!
 * `time_format`: Optional. If `"timestamp"`, `"windows_nt"` or `"epoch_millis"` the time will be converted first. With the default `null` fuzzy time parsing will be used.
 * `"type"`: set the `classification.type` statically, optional
 * `"data_type"`: sets the data of specific type, currently only `"json"` is supported value. An example
 
        ```{
            "columns": [ "source.ip", "source.url", "extra.tags"],
            "data_type": "{\"extra.tags\":\"json\"}"
        }```
        
        It will ensure `extra.tags` is treated as `json`.
 * `"filter_text"`: only process the lines containing or not containing specified text, to be used in conjection with `filter_type`
 * `"filter_type"`: value can be whitelist or blacklist. If `whitelist`, only lines containing the text in `filter_text` will be processed, if `blacklist`, only lines NOT containing the text will be processed.
 
     To process ipset format files use
     ```
        {
            "filter_text": "ipset add ",
            "filter_type": "whitelist",
            "columns": [ "__IGNORE__", "__IGNORE__", "__IGNORE__", "source.ip"]
        }
     ```
 * `"type_translation"`: If the source does have a field with information for `classification.type`, but it does not correspond to intelmq's types,
you can map them to the correct ones. The `type_translation` field can hold a JSON field with a dictionary which maps the feed's values to intelmq's.


### Cymru CAP Program

#### Information:
* `name:` intelmq.bots.parsers.cymru.parser_cap_program
* `public:` no
* `cache (redis db):` none
* `description:` Parses data from cymru's cap program feed.

As little information on the format is available, the mappings might not be correct in all cases.
Some reports are not implemented at all as there is no data available to check if the parsing is correct at all. If you do get errors like `Report ... not implement` or similar please open an issue and report the (anonymized) example data. Thanks.

The information about the event could be better in many cases but as Cymru does not want to be associated with the report, we can't add comments to the events in the parser, because then the source would be easily identifiable for the recipient.

### Cymru Full Bogons

http://www.team-cymru.com/bogon-reference.html

#### Information:
* `name:` intelmq.bots.parsers.cymru.parser_full_bogons
* `public:` no
* `cache (redis db):` none
* `description:` Parses data from full bogons feed.

### Twitter

#### Information:
* `name:` intelmq.bots.parsers.twitter.parser
* `public:` no
* `cache (redis db):` none
* `description:` Extracts urls from text, fuzzy, aimed at parsing tweets
#### Configuration Parameters:

* `domain_whitelist`: domains to be filetered out
* `substitutions`: semicolon delimited list of even length of pairs of substitutions (for example: '[.];.;,;.' substitutes '[.]' for '.' and ',' for '.')
* `classification_type: string with a valid classification type as defined in data harmonization
* `default_scheme`: Default scheme for URLs if not given. See also the next section.

##### Default scheme

The dependency `url-normalize` changed it's behavior in version 1.4.0 from using `http://` as default scheme to `https://`. Version 1.4.1 added the possibility to specify it. Thus you can only use the `default_scheme` parameter with a current version of this library >= 1.4.1, with 1.4.0 you will always get `https://` as default scheme and for older versions < 1.4.0 `http://` is used.

This does not affect URLs which already include the scheme.

### Shodan

#### Information
* `name:` intelmq.bots.parsers.shodan.parser
* `public:` yes
* `description:` Parses data from shodan (search, stream etc).

The parser is by far not complete as there are a lot of fields in a big nested structure. There is a minimal mode available which only parses the important/most useful fields and also saves everything in `extra.shodan` keeping the original structure. When not using the minimal mode if may be useful to ignore errors as many parsing errors can happen with the incomplete mapping.

#### Configuration Parameters:

* `ignore_errors`: Boolean (default true)
* `minimal_mode`: Boolean (default false)


## Experts

### Abusix

See the README.md

#### Information:
* `name:` abusix
* `lookup:` dns
* `public:` yes
* `cache (redis db):` 5
* `description:` FIXME
* `notes`: https://abusix.com/contactdb.html

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))
FIXME

* * *

### ASN Lookup

See the README.md

#### Information:
* `name:` ASN lookup
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` IP to ASN

#### Configuration Parameters:

FIXME

* * *

### Cymru Whois

#### Information:
* `name:` cymru-whois
* `lookup:` cymru dns
* `public:` yes
* `cache (redis db):` 5
* `description:` IP to geolocation, ASN, BGP prefix

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))
FIXME

* * *

### Domain Suffix

This bots adds the public suffix to the event, derived by a domain.
See or information on the public suffix list: https://publicsuffix.org/list/
Only rules for ICANN domains are processed. The list can (and should) contain
Unicode data, punycode conversion is done during reading.

Note that the public suffix is not the same as the top level domain (TLD). E.g.
`co.uk` is a public suffix, but the TLD is `uk`.
Privatly registered suffixes (such as `blogspot.co.at`) which are part of the
public suffix list too, are ignored.

#### Information:
* `name:` deduplicator
* `lookup:` redis cache
* `public:` yes
* `cache (redis db):` 6
* `description:` message deduplicator

#### Configuration Parameters:

* `field`: either `"fqdn"` or `"reverse_dns"`
* `suffix_file`: path to the suffix file

#### Rule processing

A short summary how the rules are processed:

The simple ones:
```
com
at
gv.at
```
`example.com` leads to `com`, `example.gv.at` leads to `gv.at`.

Wildcards:
```
*.example.com
```
`www.example.com` leads to `www.example.com`.

And additionally the exceptions, together with the above wildcard rule:
```
!www.example.com
```
`www.example.com` does now not lead to `www.example.com`, but to `example.com`.

* * *

### Deduplicator

See the README.md

#### Information:
* `name:` deduplicator
* `lookup:` redis cache
* `public:` yes
* `cache (redis db):` 6
* `description:` message deduplicator

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))
Please check this [README](../intelmq/bots/experts/deduplicator/README.md) file.

* * *

### Field Reducer Bot

#### Information:
* `name:` reducer
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` The field reducer bot is capable of removing fields from events.

#### Configuration Parameters:
* `type` - either `"whitelist"` or `"blacklist"`
* `keys` - Can be a JSON-list of field names (`["raw", "source.account"]`) or a string with a comma-separated list of field names (`"raw,source.account"`).

##### Whitelist

Only the fields in `keys` will passed along.

##### Blacklist

The fields in `keys` will be removed from events.

* * *

### Filter

See the README.md

#### Information:
* `name:` filter
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` filter messages (drop or pass messages) FIXME

#### Configuration Parameters:

FIXME

* * *

### Generic DB Lookup

See the README.md

* * *

### Gethostbyname

#### Information:
* `name:` gethostbyname
* `lookup:` dns
* `public:` yes
* `cache (redis db):` none
* `description:` DNS name (FQDN) to IP

#### Configuration Parameters:

none

* * *

### IDEA

Converts the event to IDEA format and saves it as JSON in the field `output`. All other fields are not modified.

Documentation about IDEA: https://idea.cesnet.cz/en/index

#### Information:
* `name:` idea
* `lookup:` local config
* `public:` yes
* `cache (redis db):` none
* `description:` The bot does a best effort translation of events into the IDEA format.

#### Configuration Parameters:

* `test_mode`: add `Test` category to mark all outgoing IDEA events as informal (meant to simplify setting up and debugging new IDEA producers) (default: `true`)

* * *

### MaxMind GeoIP

See the README.md

#### Information:
* `name:` maxmind-geoip
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` IP to geolocation

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

* `configuration_path`: filename
* `case_sensitive`: boolean, default: true

### Configuration File

The modify expert bot allows you to change arbitrary field values of events just using a configuration file. Thus it is possible to adapt certain values or adding new ones only by changing JSON-files without touching the code of many other bots.

The configuration is called `modify.conf` and looks like this:

```json
[
    {
        "rulename": "Standard Protocols http",
        "if": {
            "source.port": "^(80|443)$"
        },
        "then": {
            "protocol.application": "http"
        }
    },
    {
        "rulename": "Spamhaus Cert conficker",
        "if": {
            "malware.name": "^conficker(ab)?$"
        },
        "then": {
            "classification.identifier": "conficker"
        }
    },
    {
        "rulename": "bitdefender",
        "if": {
            "malware.name": "bitdefender-(.*)$"
        },
        "then": {
            "malware.name": "{matches[malware.name][1]}"
        }
    },
    {
        "rulename": "urlzone",
        "if": {
            "malware.name": "^urlzone2?$"
        },
        "then": {
            "classification.identifier": "urlzone"
        }
    },
    {
        "rulename": "default",
        "if": {
            "feed.name": "^Spamhaus Cert$"
        },
        "then": {
            "classification.identifier": "{msg[malware.name]}"
        }
    }
]
```

In our example above we have five groups labeled `Standard Protocols http`,
`Spamhaus Cert conficker`, `bitdefender`, `urlzone` and `default`.
All sections will be considered, in the given order (from top to bottom).

Each rule consists of *conditions* and *actions*.
Conditions and actions are dictionaries holding the field names of events
and regex-expressions to match values (selection) or set values (action).
All matching rules will be applied in the given order.
The actions are only performed if all selections apply.

If the value for a condition is an empty string, the bot checks if the field does not exist.
This is useful to apply default values for empty fields.


#### Actions

You can set the value of the field to a string literal or number.

In addition you can use the [standard Python string format syntax](https://docs.python.org/3/library/string.html#format-string-syntax)
to access the values from the processed event as `msg` and the match groups
of the conditions as `matches`, see the bitdefender example above.
Group 0 (`[0]`) contains the full matching string. See also the documentation on [`re.Match.group`](https://docs.python.org/3/library/re.html?highlight=re%20search#re.Match.group).

Note that `matches` will also contain the match groups
from the default conditions if there were any.

#### Examples

We have an event with `feed.name = Spamhaus Cert` and `malware.name = confickerab`. The expert loops over all sections in the file and eventually enters section `Spamhaus Cert`. First, the default condition is checked, it matches! OK, going on. Otherwise the expert would have selected a different section that has not yet been considered. Now, go through the rules, until we hit the rule `conficker`. We combine the conditions of this rule with the default conditions, and both rules match! So we can apply the action: `classification.identifier` is set to `conficker`, the trivial name.

Assume we have an event with `feed.name = Spamhaus Cert` and `malware.name = feodo`. The default condition matches, but no others. So the default action is applied. The value for `classification.identifier` will be set to `feodo` by `{msg[malware.name]}`.

#### Types

If the rule is a string, a regex-search is performed, also for numeric values (`str()` is called on them). If the rule is numeric for numeric values, a simple comparison is done. If other types are mixed, a warning will be thrown.

* * *

### National CERT contact lookup by CERT.AT

#### Information:
* `name:` `national_cert_contact_certat`
* `lookup:` https
* `public:` yes
* `cache (redis db):` none
* `description:` https://contacts.cert.at offers an IP address to national CERT contact (and cc) mapping. See https://contacts.cert.at for more info.

#### Configuration Parameters:

* `filter`: (true/false) act as a a filter for AT.
* `overwrite_cc`: set to true if you want to overwrite any potentially existing cc fields in the event.

* * *

### Reverse DNS

For both `source.ip` and `destination.ip` the PTR record is fetched and the first valid result is used for `source.reverse_dns`/`destination.reverse_dns`.

#### Information:
* `name:` reverse-dns
* `lookup:` dns
* `public:` yes
* `cache (redis db):` 8
* `description:` IP to domain

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))
* `cache_ttl_invalid_response`: The TTL for cached invalid responses.

* * *

### RFC1918

Several RFCs define IP addresses and Hostnames (and TLDs) reserved for documentation:

Sources:
* https://tools.ietf.org/html/rfc1918
* https://tools.ietf.org/html/rfc2606
* https://tools.ietf.org/html/rfc3849
* https://tools.ietf.org/html/rfc4291
* https://tools.ietf.org/html/rfc5737
* https://en.wikipedia.org/wiki/IPv4

#### Information:
* `name:` rfc1918
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` removes events or single fields with invalid data

#### Configuration Parameters:

* `fields`: list of fields to look at. e.g. "destination.ip,source.ip,source.url"
* `policy`: list of policies, e.g. "del,drop,drop". `drop` drops the entire event, `del` removes the field.

* * *

### RipeNCC Abuse Contact

RIPE NCC online Abuse Contact Finder for IP addresses and Autonomous Systems.

#### Information:
* `name:` ripencc-abuse-contact
* `lookup:` https api
* `public:` yes
* `cache (redis db):` 10
* `description:` IP to abuse contact

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))
* `mode`: either `append` (default) or `replace`
* `query_ripe_db_asn`: Query for IPs at `http://rest.db.ripe.net/abuse-contact/%s.json`, default `true`
* `query_ripe_db_ip`: Query for ASNs at `http://rest.db.ripe.net/abuse-contact/as%s.json`, default `true`
* `query_ripe_stat_asn`: Query for ASNs at `https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=%s`, default `true`
* `query_ripe_stat_ip`: Query for IPs at `https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=%s`, default `true`

* * *

### Sieve

See intelmq/bots/experts/sieve/README.md

#### Information:
* `name:` sieve
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` Filtering with a sieve-based configuration language

#### Configuration Parameters:

* `file`: Path to sieve file. Syntax can be validated with `intelmq_sieve_expert_validator`.

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

See the README.md

#### Information:
* `name:` tor-nodes
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` check if IP is tor node

#### Configuration Parameters:

FIXME

### Url2FQDN

#### Information:
* `name:` url2fqdn
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` writes domain name from URL to FQDN

#### Configuration Parameters:

* `overwrite`: boolean, replace existing FQDN?

### Wait

#### Information:
* `name:` wait
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` Waits for a some time or until a queue size is lower than a given numer.

#### Configuration Parameters:

* `queue_db`: Database number of the database, default `2`. Converted to integer.
* `queue_host`: Host of the database, default `localhost`.
* `queue_name`: Name of the queue to be watched, default `null`. This is not the name of a bot but the queue's name.
* `queue_password`: Password for the database, default `None`.
* `queue_polling_interval`: Interval to poll the list length in seconds. Converted to float.
* `queue_port`: Port of the database, default `6379`. Converted to integer.
* `queue_size`: Maximum size of the queue, default `0`. Compared by <=. Converted to integer.
* `sleep_time`: Time to sleep before sending the event.

Only one of the two modes is possible.
If a queue name is given, the queue mode is active. If the sleep_time is a number, sleep mode is active.
Otherwise the dummy mode is active, the events are just passed without an additional delay.

Note that SIGHUPs and reloads interrupt the sleeping.

## Outputs

### File

#### Information:
* `name:` file
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` output messages (reports or events) to file

#### Configuration Parameters:

* `encoding_errors_mode`: By default `'strict'`, see for more details and options: https://docs.python.org/3/library/functions.html#open For example with `'backslashreplace'` all characters which cannot be properly encoded will be written escaped with backslashes.
* `file`: file path of output file. Missing directories will be created if possible with the mode 755.
* `format_filename`: Boolean if the filename should be formatted (default: `false`).
* `hierarchial_output`: If true, the resulting dictionary will be hierarchical (field names split by dot).
* `single_key`: if `none`, the whole event is saved (default); otherwise the bot saves only contents of the specified key. In case of `raw` the data is base64 decoded.

##### Filename formatting
The filename can be formatted using pythons string formatting functions if `format_filename` is set. See https://docs.python.org/3/library/string.html#formatstrings

For example:
 * The filename `.../{event[source.abuse_contact]}.txt` will be (for example) `.../abuse@example.com.txt`.
 * `.../{event[time.source]:%Y-%m-%d}` results in the date of the event used as filename.

If the field used in the format string is not defined, `None` will be used as fallback.

* * *


### Files

#### Information:
* `name:` files
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` saving of messages as separate files

#### Configuration Parameters:

* `dir`: output directory (default `/opt/intelmq/var/lib/bots/files-output/incoming`)
* `tmp`: temporary directory (must reside on the same filesystem as `dir`) (default: `/opt/intelmq/var/lib/bots/files-output/tmp`)
* `suffix`: extension of created files (default `.json`)
* `hierarchical_output`: if `true`, use nested dictionaries; if `false`, use flat structure with dot separated keys (default)
* `single_key`: if `none`, the whole event is saved (default); otherwise the bot saves only contents of the specified key


* * *


### MongoDB

Saves events in a MongoDB either as hierarchical structure or flat with full key names. `time.observation` and `time.source` are saved as datetime objects, not as ISO formatted string.

#### Information:
* `name:` mongodb
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` MongoDB is the bot responsible to send events to a MongoDB database

#### Configuration Parameters:

* `collection`: MongoDB collection
* `database`: MongoDB database
* `db_user` : Database user that should be used if you enabled authentication
* `db_pass` : Password associated to `db_user`
* `host`: MongoDB host (FQDN or IP)
* `port`: MongoDB port
* `hierarchical_output`: Boolean (default true) as mongodb does not allow saving keys with dots, we split the dictionary in sub-dictionaries.
* `replacement_char`: String (default `'_'`) used as replacement character for the dots in key names if hierarchical output is not used.

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
* `jsondict_as_string`: save JSONDict fields as JSON string, boolean. Default: true (like in versions before 1.1)
* `port`: PostgreSQL port
* `user`: PostgreSQL user
* `password`: PostgreSQL password
* `sslmode`: PostgreSQL sslmode, can be `'disable'`, `'allow'`, `'prefer'` (default), `'require'`, `'verify-ca'` or `'verify-full'`. See postgresql docs: https://www.postgresql.org/docs/current/static/libpq-connect.html#libpq-connect-sslmode
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

* `auth_token`: the user name / http header key
* `auth_token_name`: the password / http header value
* `auth_type`: one of: `"http_basic_auth"`, `"http_header"`
* `hierarchical_output`: boolean
* `host`: destination URL
* `use_json`: boolean


* * *

### SMTP Output Bot

Sends a MIME Multipart message containing the text and the event as CSV for every single event.

#### Information:
* `name:` smtp
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Sends events via SMTP

#### Configuration Parameters:

* `fieldnames`: a list of field names to be included in the email, comma separated string or list of strings
* `mail_from`: string. Supports formatting, see below
* `mail_to`: string of email addresses, comma separated. Supports formatting, see below
* `smtp_host`: string
* `smtp_password`: string or null, Password for authentication on your SMTP server
* `smtp_port`: port
* `smtp_username`: string or null, Username for authentication on your SMTP server
* `ssl`: boolean
* `starttls`: boolean
* `subject`: string. Supports formatting, see below
* `text`: string or null. Supports formatting, see below

For several strings you can use values from the string using the
[standard Python string format syntax](https://docs.python.org/3/library/string.html#format-string-syntax).
Access the event's values with `{ev[source.ip]}` and similar.

Authentication is optional. If both username and password are given, these
mechanism are tried: CRAM-MD5, PLAIN, and LOGIN.

Client certificates are not supported. If `http_verify_cert` is true, TLS certificates are checked.

* * *


### TCP

#### Information:
* `name:` intelmq.bots.outputs.tcp.collector
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` TCP is the bot responsible to send events to a TCP port (Splunk, ElasticSearch, another IntelMQ, etc..).

#### Configuration Parameters:

* `ip`: IP of destination server
* `hierarchical_output`: true for a nested JSON, false for a flat JSON (when sending to a TCP collector).
* `port`: port of destination server
* `separator`: separator of messages, eg. "\n", optional. When sending to a TCP collector, parameter shouldn't be present. 
    In that case, the output waits every message is acknowledged by "Ok" message the tcp.collector bot implements.

