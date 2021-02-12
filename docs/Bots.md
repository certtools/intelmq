# Bots Documentation

**Table of Contents:**
- [Bots Documentation](#bots-documentation)
- [General remarks](#general-remarks)
- [Initialization parameters](#initialization-parameters)
- [Common parameters](#common-parameters)
- [Collectors](#collectors)
  - [API](#api)
  - [Generic URL Fetcher](#generic-url-fetcher)
  - [Generic URL Stream Fetcher](#generic-url-stream-fetcher)
  - [Generic Mail URL Fetcher](#generic-mail-url-fetcher)
  - [Generic Mail Attachment Fetcher](#generic-mail-attachment-fetcher)
  - [Fileinput](#fileinput)
  - [MISP Generic](#misp-generic)
  - [Request Tracker](#request-tracker)
  - [Rsync](#rsync)
  - [Shodan Stream](#shodan-stream)
  - [TCP](#tcp)
  - [XMPP collector](#xmpp-collector)
  - [Alien Vault OTX](#alien-vault-otx)
  - [Blueliv Crimeserver](#blueliv-crimeserver)
  - [Calidog Certstream](#calidog-certstream)
  - [McAfee openDXL](#mcafee-opendxl)
  - [Microsoft Azure](#microsoft-azure)
  - [Microsoft Interflow](#microsoft-interflow)
    - [Additional functionalities](#additional-functionalities)
  - [Stomp](#stomp)
  - [Twitter](#twitter)
- [Parsers](#parsers)
  - [Not complete](#not-complete)
  - [Generic CSV Parser](#generic-csv-parser)
  - [Calidog Certstream](#calidog-certstream)
  - [Cymru CAP Program](#cymru-cap-program)
  - [Cymru Full Bogons](#cymru-full-bogons)
  - [HTML Table Parser](#html-table-parser)
  - [Twitter](#twitter)
  - [Shadowserver](#shadowserver)
  - [Shodan](#shodan)
- [Experts](#experts)
  - [Abusix](#abusix)
  - [ASN Lookup](#asn-lookup)
  - [CSV Converter](#csv-converter)
  - [Copy Extra](#copy-extra)
  - [Cymru Whois](#cymru-whois)
  - [Deduplicator](#deduplicator)
  - [Domain Suffix](#domain-suffix)
    - [Rule processing](#rule-processing)
  - [DO-Portal](#do-portal)
  - [Field Reducer Bot](#field-reducer-bot)
      - [Whitelist](#whitelist)
      - [Blacklist](#blacklist)
  - [Filter](#filter)
  - [Format Field](#format-field)
  - [Generic DB Lookup](#generic-db-lookup)
  - [Gethostbyname](#gethostbyname)
  - [IDEA](#idea)
  - [MaxMind GeoIP](#maxmind-geoip)
  - [MISP](#misp)
  - [Modify](#modify)
    - [Configuration File](#configuration-file)
      - [Actions](#actions)
      - [Examples](#examples)
      - [Types](#types)
  - [McAfee Active Response Hash lookup](#mcafee-active-response-hash-lookup)
  - [McAfee Active Response IP lookup](#mcafee-active-response-ip-lookup)
  - [McAfee Active Response URL lookup](#mcafee-active-response-url-lookup)
  - [National CERT contact lookup by CERT.AT](#national-cert-contact-lookup-by-certat)
  - [Recorded Future IP Risk](#recorded-future-ip-risk)
  - [Reverse DNS](#reverse-dns)
  - [RFC1918](#rfc1918)
  - [RipeNCC Abuse Contact](#ripencc-abuse-contact)
  - [Sieve](#sieve)
  - [Taxonomy](#taxonomy)
  - [Tor Nodes](#tor-nodes)
  - [Url2FQDN](#url2fqdn)
  - [Wait](#wait)
- [Outputs](#outputs)
  - [AMQP Topic](#amqp-topic)
  - [Blackhole](#blackhole)
  - [Elasticsearch](#elasticsearch)
  - [File](#file)
      - [Filename formatting](#filename-formatting)
  - [Files](#files)
  - [McAfee Enterprise Security Manager](#mcafee-enterprise-security-manager)
  - [MISP Feed](#misp-feed)
  - [MISP API](#misp-api)
  - [MongoDB](#mongodb)
    - [Installation Requirements](#installation-requirements)
  - [Redis](#redis)
  - [REST API](#rest-api)
  - [SMTP Output Bot](#smtp-output-bot)
  - [SQL](#sql)
    - [Installation Requirements](#installation-requirements)
    - [PostgreSQL Installation](#postgresql-installation)
  - [TCP](#tcp)
  - [Touch](#touch)
  - [UDP](#tcp)
  - [XMPP](#xmpp)


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
            "name": "Abuse.ch Feodo Domains",
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

* `name`: Name for the feed (`feed.name`). In IntelMQ versions smaller than 2.2 the parameter name `feed` is also supported.
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
* `ssl_ca_certificate`: Optional string of path to trusted CA certificate. Only used by some bots.
* `http_header`: HTTP request headers

**Cache parameters**: Common redis cache parameters used in multiple bots (mainly lookup experts):

* `redis_cache_host`: Hostname of the redis database.
* `redis_cache_port`: Port of the redis database.
* `redis_cache_db`: Database number.
* `redis_cache_ttl`: TTL used for caching.
* `redis_cache_password`: Optional password for the redis database (default: none).

## Collectors

Multihreading is disabled for all Collectors, as this would lead to duplicated data.

### AMQP

Requires the [`pika` python library](https://pypi.org/project/pika/), minimum version 1.0.0.

#### Information:
* `name`: intelmq.bots.collectors.amqp.collector_amqp
* `lookup`: yes
* `public`: yes
* `cache (redis db)`: none
* `description`: collect data from (remote) AMQP servers, for both IntelMQ as well as external data

#### Configuration Parameters:

* **Feed parameters** (see above)
* `connection_attempts`: The number of connection attempts to defined server, defaults to 3
* `connection_heartbeat`: Heartbeat to server, in seconds, defaults to 3600
* `connection_host`: Name/IP for the AMQP server, defaults to 127.0.0.1
* `connection_port`: Port for the AMQP server, defaults to 5672
* `connection_vhost`: Virtual host to connect, on an http(s) connection would be http:/IP/<your virtual host>
* `expect_intelmq_message`: Boolean, if the data is from IntelMQ or not. Default: `false`. If true, then the data can be any Report or Event and will be passed to the next bot as is. Otherwise a new report is created with the raw data.
* `password`: Password for authentication on your AMQP server
* `queue_name`: The name of the queue to fetch data from
* `username`: Username for authentication on your AMQP server
* `use_ssl`: Use ssl for the connection, make sure to also set the correct port, usually 5671 (`true`/`false`)

Currently only fetching from a queue is supported can be extended in the future. Messages will be acknowledge at AMQP after it is sent to the pipeline.

* * *

### API

#### Information:
* `name:` intelmq.bots.collectors.api.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect report messages from an HTTP REST API

#### Configuration Parameters:

* **Feed parameters** (see above)
* `port`: Optional, integer. Default: 5000. The local port, the API will be available at.

The API is available at `/intelmq/push`.
The `tornado` library is required.

* * *


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
* `extract_files`: Optional, boolean or list of strings. If it is true, the retrieved (compressed) file or archived will be uncompressed/unpacked and the files are extracted. If the parameter is a list for strings, only the files matching the filenames are extracted. Extraction handles gziped files and both compressed and uncompressed tar-archives as well as zip archives.
* `http_url`: location of information resource (e.g. https://feodotracker.abuse.ch/blocklist/?download=domainblocklist)
* `http_url_formatting`: (`bool|JSON`, default: `false`) If `true`, `{time[format]}` will be replaced by the current time in local timezone formatted by the given format. E.g. if the URL is `http://localhost/{time[%Y]}`, then the resulting URL is `http://localhost/2019` for the year 2019. (Python's [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec) is used for this.)
You may use a `JSON` specifying [time-delta](https://docs.python.org/3/library/datetime.html#datetime.timedelta) parameters to shift the current time accordingly. For example use `{"days": -1}` for the yesterday's date; the URL `http://localhost/{time[%Y-%m-%d]}` will get translated to "http://localhost/2018-12-31" for the 1st Jan of 2019.

Zipped files are automatically extracted if detected.

For extracted files, every extracted file is sent in its own report. Every report has a field named `extra.file_name` with the file name in the archive the content was extracted from.

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
* `mail_port`: IMAP server port, optional (default: 143 without SSL, 993 for SSL)
* `mail_ssl`: whether the mail account uses SSL (default: `true`)
* `folder`: folder in which to look for mails (default: `INBOX`)
* `subject_regex`: regular expression to look for a subject
* `url_regex`: regular expression of the feed URL to search for in the mail body
* `sent_from`: filter messages by sender
* `sent_to`: filter messages by recipient
* `ssl_ca_certificate`: Optional string of path to trusted CA certificate. Applies only to IMAP connections, not HTTP. If the provided certificate is not found, the IMAP connection will fail on handshake. By default, no certificate is used.

The resulting reports contains the following special fields:
 * `feed.url`: The URL the data was downloaded from
 * `extra.email_subject`: The subject of the email
 * `extra.email_from`: The email's from address
 * `extra.email_message_id`: The email's message ID
 * `extra.file_name`: The file name of the downloaded file (extracted from the HTTP Response Headers if possible).

##### Chunking

For line-based inputs the bot can split up large reports into smaller chunks.

This is particularly important for setups that use Redis as a message queue
which has a per-message size limitation of 512 MB.

To configure chunking, set `chunk_size` to a value in bytes.
`chunk_replicate_header` determines whether the header line should be repeated
for each chunk that is passed on to a parser bot.

Specifically, to configure a large file input to work around Redis' size
limitation set `chunk_size` to something like `384000000`, i.e., ~384 MB.

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
* `extract_files`: Optional, boolean or list of strings. See documentation of the Generic URL Fetcher for more details.
* `mail_host`: FQDN or IP of mail server
* `mail_user`: user account of the email account
* `mail_password`: password associated with the user account
* `mail_port`: IMAP server port, optional (default: 143 without SSL, 993 for SSL)
* `mail_ssl`: whether the mail account uses SSL (default: `true`)
* `folder`: folder in which to look for mails (default: `INBOX`)
* `subject_regex`: regular expression to look for a subject
* `attach_regex`: regular expression of the name of the attachment
* `attach_unzip`: whether to unzip the attachment. Only extracts the first file. Deprecated, use `extract_files` instead.
* `sent_from`: filter messages by sender
* `sent_to`: filter messages by recipient
* `ssl_ca_certificate`: Optional string of path to trusted CA certificate. Applies only to IMAP connections, not HTTP. If the provided certificate is not found, the IMAP connection will fail on handshake. By default, no certificate is used.

The resulting reports contains the following special fields:
 * `extra.email_subject`: The subject of the email
 * `extra.email_from`: The email's from address
 * `extra.email_message_id`: The email's message ID
 * `extra.file_name`: The file name of the attachment or the file name in the attached archive if attachment is to uncompress.
* * *

### Generic Mail Body Fetcher


#### Information:
* `name:` intelmq.bots.collectors.mail.collector_mail_body
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from mailboxes, forwards the bodies as reports. Each non-empty body with the matching content type is sent as individual report.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `mail_host`: FQDN or IP of mail server
* `mail_user`: user account of the email account
* `mail_password`: password associated with the user account
* `mail_port`: IMAP server port, optional (default: 143 without SSL, 993 for SSL)
* `mail_ssl`: whether the mail account uses SSL (default: `true`)
* `folder`: folder in which to look for mails (default: `INBOX`)
* `subject_regex`: regular expression to look for a subject
* `sent_from`: filter messages by sender
* `sent_to`: filter messages by recipient
* `ssl_ca_certificate`: Optional string of path to trusted CA certificate. Applies only to IMAP connections, not HTTP. If the provided certificate is not found, the IMAP connection will fail on handshake. By default, no certificate is used.
* `content_types`: Which bodies to use based on the content_type. Default: `true`/`['html', 'plain']` for all:
  - string with comma separated values, e.g. `['html', 'plain']`
  - `true`, `false`, `null`: Same as default value
  - `string`, e.g. `'plain'`

The resulting reports contains the following special fields:
 * `extra.email_subject`: The subject of the email
 * `extra.email_from`: The email's from address
 * `extra.email_message_id`: The email's message ID

* * *

### GithubAPI


#### Information:
* `name:` intelmq.bots.collectors.github_api.collector_github_contents_api
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Collects files matched by regex from github repository via the Github API.
  Optionally with github credentials, which are used as the Basic HTTP authetication.
  
#### Configuration Parameters:

* **Feed parameters** (see above)
* `basic_auth_username:` Github account username (optional)
* `basic_auth_password:` Github account password (optional)
* `repository:` Github target repository (`<USER>/<REPOSITORY>`)
* `regex:` Valid regex of target files within the repository (defaults to `.*.json`)
* `extra_fields:` Comma-separated list of extra fields from [github contents API](https://developer.github.com/v3/repos/contents/)

#### Workflow

The optional authentication parameters provide a high limit of the github API requests.
With the github user authentication, the requests are rate limited to 5000 per hour, otherwise to 60 requests per hour. 

The collector recursively searches for `regex`-defined files in the provided `repository`.
Additionally it adds extra file metadata defined by the `extra_fields`.

The bot always sets the url, from which downloaded the file, as `feed.url`.

* * *

### Fileinput

#### Information:
* `name:` intelmq.bots.collectors.file.collector_file
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` This bot is capable of reading files from the local file-system.
  This is handy for testing purposes, or when you need to react to spontaneous
  events. In combination with the Generic CSV Parser this should work great.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `path`: path to file
* `postfix`: FIXME
* `delete_file`: whether to delete the file after reading (default: `false`)

The resulting reports contains the following special fields:
 * `feed.url`: The URI using the `file://` scheme and localhost, with the full path to the processed file.
 * `extra.file_name`: The file name (without path) of the processed file.

#### Chunking

Additionally, for line-based inputs the bot can split up large reports into
smaller chunks.

This is particularly important for setups that use Redis as a message queue
which has a per-message size limitation of 512 MB.

To configure chunking, set `chunk_size` to a value in bytes.
`chunk_replicate_header` determines whether the header line should be repeated
for each chunk that is passed on to a parser bot.

Specifically, to configure a large file input to work around Redis' size
limitation set `chunk_size` to something like `384000`, i.e., ~384 MB.

#### Workflow

The bot loops over all files in `path` and tests if their file name matches
*postfix, e.g. `*.csv`. If yes, the file will be read and inserted into the
queue.

If `delete_file` is set, the file will be deleted after processing. If deletion
is not possible, the bot will stop.

To prevent data loss, the bot also stops when no `postfix` is set and
`delete_file` was set. This cannot be overridden.

The bot always sets the file name as feed.url

* * *

### Rsync

Requires the rsync executable

#### Information:
* `name:` intelmq.bots.collectors.rsync.collector_rsync
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Bot download file by rsync and then load data from downloaded file. Downloaded file is located in var/lib/bots/rsync_collector.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `file`: Name of downloaded file.
* `rsync_path`: Path to file. It can be "/home/username/directory" or "username@remote_host:/home/username/directory"
* `temp_directory`: Path of a temporary state directory to use for rsync'd files. Optional. Default: `/opt/intelmq/var/run/rsync_collector/`.

* * *

### MISP Generic


#### Information:
* `name:` intelmq.bots.collectors.misp.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from [MISP](https://github.com/MISP), a malware information sharing platform server.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `misp_url`: URL of MISP server (with trailing '/')
* `misp_key`: MISP Authkey
* `misp_tag_to_process`: MISP tag for events to be processed
* `misp_tag_processed`: MISP tag for processed events, optional

Generic parameters used in this bot:
* `http_verify_cert`: Verify the TLS certicate of the server, boolean (default: `true`)

#### Workflow
This collector will search for events on a MISP server that have a
`to_process` tag attached to them (see the `misp_tag_to_process` parameter)
and collect them for processing by IntelMQ. Once the MISP event has been
processed the `to_process` tag is removed from the MISP event and a
`processed` tag is then attached (see the `misp_tag_processed` parameter).

**NB.** The MISP tags must be configured to be 'exportable' otherwise they will
not be retrieved by the collector.

* * *

### Request Tracker


#### Information:
* `name:` intelmq.bots.collectors.rt.collector_rt
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Request Tracker Collector fetches attachments from an RTIR instance.

You need the rt-library >= 1.9 from nic.cz, available via [pypi](https://pypi.org/project/rt/): `pip3 install rt`

This rt bot will connect to RT and inspect the given `search_queue` for tickets matching all criteria in `search_*`, 
Any matches will be inspected. For each match, all (RT-) attachments of the matching RT tickets are iterated over and within this loop, the first matching filename in the attachment is processed.
If none of the filename matches apply, the contents of the first (RT-) "history" item is matched against the URL-regex.

#### Configuration Parameters:

* **Feed parameters** (see above)
* **HTTP parameters** (see above)
* `extract_attachment`: Optional, boolean or list of strings. See documentation of the Generic URL Fetcher parameter `extract_files` for more details.
* `extract_download`: Optional, boolean or list of strings. See documentation of the Generic URL Fetcher parameter `extract_files` for more details.
* `uri`: url of the REST interface of the RT
* `user`: RT username
* `password`: RT password
* `search_not_older_than`: Absolute time (use ISO format) or relative time, e.g. `3 days`.
* `search_owner`: owner of the ticket to search for (default: `nobody`)
* `search_queue`: queue of the ticket to search for (default: `Incident Reports`)
* `search_status`: status of the ticket to search for (default: `new`)
* `search_subject_like`: part of the subject of the ticket to search for (default: `Report`)
* `set_status`: status to set the ticket to after processing (default: `open`). `false` or `null` to not set a different status.
* `take_ticket`: whether to take the ticket (default: `true`)
* `url_regex`: regular expression of an URL to search for in the ticket
* `attachment_regex`: regular expression of an attachment in the ticket
* `unzip_attachment`: whether to unzip a found attachment. Only the first file in the archive is used. Deprecated in favor of `extract_attachment`.

The parameter `http_timeout_max_tries` is of no use in this collector.

The resulting reports contains the following special fields:
 * `rtir_id`: The ticket ID
 * `extra.email_subject` and `extra.ticket_subject`: The subject of the ticket
 * `extra.email_from` and `extra.ticket_requestors`: Comma separated list of requestor's email addresses.
 * `extra.ticket_owner`: The ticket's owner name
 * `extra.ticket_status`: The ticket's status
 * `extra.ticket_queue`: The ticket's queue
 * `extra.file_name`: The name of the extracted file, the name of the downloaded file or the attachments' filename without `.gz` postfix.
 * `time.observation`: The creation time of the ticket or attachment.

##### Search

The parameters prefixed with `search_` allow configuring the ticket search.

Empty strings and `null` as value for search parameters are ignored.

##### File downloads

Attachments can be optionally unzipped, remote files are downloaded with the `http_*` settings applied (see `defaults.conf`).

If `url_regex` or `attachment_regex` are empty strings, false or null, they are ignored.

##### Ticket processing

Optionally, the RT bot can "take" RT tickets (i.e. the `user` is assigned this ticket now) and/or the status can be changed (leave `set_status` empty in case you don't want to change the status). Please note however that you **MUST** do one of the following: either "take" the ticket  or set the status (`set_status`). Otherwise, the search will find the ticket every time and we will have generated an endless loop.

In case a resource needs to be fetched and this resource is permanently not available (status code is 4xx), the ticket status will be set according to the configuration to avoid processing the ticket over and over.
For temporary failures the status is not modified, instead the ticket will be skipped in this run.

##### Time search

To find only tickets newer than a given absolute or relative time, you can use the `search_not_older_than` parameter. Absolute time specification can be anything parseable by dateutil, best use a ISO format.

Relative must be in this format: `[number] [timespan]s`, e.g. `3 days`. Timespan can be hour, day, week, month, year. Trailing 's' is supported for all timespans. Relative times are subtracted from the current time directly before the search is performed.

* * *

### Rsync

#### Information:

* `name:` intelmq.bots.collectors.rsync.collector_rsync
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Syncs a file via rsync and reads the file.

#### Configuration Parameters:

* **Feed parameters** (see above)
* `file`: The filename to process, combine with `rsync_path`.
* `temp_directory`: The temporary directory for rsync, by default `$VAR_STATE_PATH/rsync_collector`. `$VAR_STATE_PATH` is `/var/run/intelmq/` or `/opt/intelmq/var/run/`.
* `rsync_path`: The path of the file to process

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

#### Requirements
The Sleekxmpp - Library needs to be installed on your System
```bash
pip3 install -r intelmq/bots/collectors/xmpp/REQUIREMENTS.txt
```

#### Configuration Parameters:

* **Feed parameters** (see above)
* `xmpp_server`: The domain name of the server of the XMPP-Account (part after the @ sign)
* `xmpp_user`: The username of the XMPP-Account the collector shall use (part before the @ sign)
* `xmpp_password`: The password of the XMPP-Account
* `xmpp_room`: The room which has to be joined by the XMPP-Collector (full address room@conference.server.tld)
* `xmpp_room_nick`: The username / nickname the collector shall use within the room
* `xmpp_room_password`: The password which might be required to join a room
 - `use_muc` : If this parameter is `true`, the bot will join the room `xmpp_room`.
 - `xmpp_userlist`: An array of usernames whose messages will (not) be processed.
 - `xmpp_whitelist_mode`: If `true` the list provided in `xmpp_userlist` is a whitelist. Else it is a blacklist.
    In case of a whitelist, only messages from the configured users will be processed, else their messages are not
    processed. Default is `false` / blacklist.
* `ca_certs`: A path to a file containing the CA's which should be used (default: `/etc/ssl/certs/ca-certificates.crt`)
* `strip_message`: If `true` trailing white space will be removed from the message. Does not happen if `pass_full_xml` is set to `true` (default: `true`)
* `pass_full_xml`: If this parameter is set to `true` the collector will read the full-xmpp-xml message and add it to the pipeline.
   this is useful if other systems like AbuseHelper should be processed. (default: `false`)

* * *


### Alien Vault OTX

#### Information:
* `name:` intelmq.bots.collectors.alienvault_otx.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect report messages from Alien Vault OTX API

#### Requirements

Install the library from GitHub, as there is no package in PyPi:
```bash
pip3 install -r intelmq/bots/collectors/alienvault_otx/REQUIREMENTS.txt
```

#### Configuration Parameters:

* **Feed parameters** (see above)
* `api_key`: API Key
* `modified_pulses_only`: get only modified pulses instead of all, set to it to true or false, default false
* `interval`: if "modified_pulses_only" is set, define the time in hours (integer value) to get modified pulse since then, default 24 hours

* * *

### Blueliv Crimeserver

#### Information:
* `name:` intelmq.bots.collectors.blueliv.collector_crimeserver
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect report messages from Blueliv API

For more information visit https://github.com/Blueliv/api-python-sdk

#### Requirements

Install the required library:
```bash
pip3 install -r intelmq/bots/collectors/blueliv/REQUIREMENTS.txt
```

#### Configuration Parameters:

* **Feed parameters** (see above)
* `api_key`: location of information resource, see https://map.blueliv.com/?redirect=get-started#signup
* `api_url`: The optional API endpoint, by default `https://freeapi.blueliv.com`.

* * *

### Calidog Certstream

A Bot to collect data from the Certificate Transparency Log (CTL)
This bot works based on certstream library (https://github.com/CaliDog/certstream-python)

#### Information:
* `name:` intelmq.bots.collectors.calidog.collector_certstream
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect data from Certificate Transparency Log

#### Configuration Parameters:

* **Feed parameters** (see above)

* * *

### McAfee openDXL

#### Information:
* `name:` intelmq.bots.collectors.opendxl.collector
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect messages via openDXL

#### Configuration Parameters:

* **Feed parameters** (see above)
* `dxl_config_file`: location of the config file containing required information to connect $
* `dxl_topic`: the name of the DXL topic to subscribe

* * *

### Microsoft Azure

Iterates over all blobs in all containers in an Azure storage.
The Cache is required to memorize which files have already been processed (TTL needs to be high enough to cover the oldest files available!).

This bot significantly changed in a backwards-incompatible way in IntelMQ Version 2.2.0 to support current versions of the Microsoft Azure Python libraries.

#### Information:
* `name`: intelmq.bots.collectors.microsoft.collector_azure
* `lookup`: yes
* `public`: no
* `cache (redis db)`: 5
* `description`: collect blobs from Microsoft Azure using their library

#### Configuration Parameters:

* **Cache parameters** (see above)
* **Feed parameters** (see above)
* `connection_string`: connection string as given by Microsoft
* `container_name`: name of the container to connect to

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

#### Information:
* `name:` intelmq.bots.collectors.stomp.collector
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect messages from a stomp server

#### Requirements

Install the stomp.py library from pypi:
```bash
pip3 install -r intelmq/bots/collectors/stomp/REQUIREMENTS.txt
```

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
* `access_token_key`: Twitter api login data
* `access_token_secret`: Twitter api login data

### API collector bot

#### Information:
* `name:` intelmq.bots.collectors.api.collector_api
* `lookup:` no
* `public:` no
* `cache (redis db):` none
* `description:` Bot for collecting data using API, you need to post JSON to /intelmq/push endpoint

example usage:
```
curl -X POST http://localhost:5000/intelmq/push -H 'Content-Type: application/json' --data '{"source.ip": "127.0.0.101", "classification.type": "backdoor"}'
```

#### Configuration Parameters:

* **Feed parameters** (see above)
* `port`: 5000

## Parsers

### Not complete

This list is not complete. Look at `intelmq/bots/BOTS` or the list of parsers shown in the manager. But most parsers do not need configuration parameters.

TODO

### AnubisNetworks Cyberfeed Stream

#### Information
* `name`: `intelmq.bots.parsers.anubisnetworks.parser`
* `lookup`: no
* `public`: yes
* `cache (redis db)`: none
* `description`: parsers data from AnubisNetworks Cyberfeed Stream

#### Description

The feed format changes over time. The parser supports at least data from 2016 and 2020.

#### Configuration parameters

* `use_malware_familiy_as_classification_identifier`: default: `true`. Use the `malw.family` field as `classification.type`. If `false`, check if the same as `malw.variant`. If it is the same, it is ignored. Otherwise saved as `extra.malware.family`.

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

 * `"column_regex_search"`: Optional. A dictionary mapping field names (as given per the columns parameter) to regular expression. The field is evaluated using `re.search`. Eg. to get the ASN out of `AS1234` use: `{"source.asn": "[0-9]*"}`.
 * `"default_url_protocol"`: For URLs you can give a default protocol which will be pretended to the data.
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
 * `"columns_required"`: A list of true/false for each column. By default, it is true for every column.

* * *

### Calidog Certstream


#### Information:
* `name:` intelmq.bots.parsers.calidog.parser_certstream
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` parsers data from Certificate Transparency Log

#### Description

For each domain in the `leaf_cert.all_domains` object one event with the domain in `source.fqdn` (and `source.ip` as fallback) is produced.
The seen-date is saved in `time.source` and the classification type is `other`.

* **Feed parameters** (see above)

* * *

### Fraunhofer DDos Attack Parser

#### Information:
* `name:` `intelmq.bots.parsers.fraunhofer.parser_ddosattack_cnc` and `intelmq.bots.parsers.fraunhofer.parser_ddosattack_target`
* `public:` no
* `cache (redis db):` none
* `description:` Parses data from Fraunhofer's DDoS Attack feed.

#### Description

The parser bots generate c&c events and ddos events, depending on the
information retrieved from the feed. The feed delivers reports with different
message types and different C&C types based on the type of tracked C&C servers
and the type of commands received. If the c&c parser bot receives a report with
a known C&C type but with an unknown message type, it generates a C&C event
with an adjusted feed.accuracy given by the parameter
unknown_messagetype_accuracy, if set. This feature can be used to lower the
accuracy of events in case of unknown behavior of the tracked C&Cs, while
keeping a high accuracy otherwise. For this feature to work, set the default
feed.accuracy of the collector bot feeding this parser bot to a high value,
while setting the value of the c&c parser bot's unknown_messagetype_accuracy
to a lower value. The c&c parser bot will not change the feed.accuracy value
if the tracker was able to interpret the C&C communication, giving a high
chance, that the tracked server is actually a real live C&C server.
If the tracker was not able to completely interpret the C&C communication, the
feed.accuracy will be set to the lower value of the
unknown_messagetype_accuracy parameter. There is still a certain probability
that the tracked server is a real C&C, but it could not be confirmed.
The target parser bot generates one ddos event for every target found in the
attack commands of the tracked C&C server, which could be more than one for a
single event from the tracker feed. 

#### Configuration

* `unknown_messagetype_accuracy`: A float between 0 an 100 representing the
  accuracy of a c&c event for reports with unknown message types. Replaces the
  feed.accuracy with the given value for these events.

* * *

### Cymru CAP Program

#### Information:
* `name:` intelmq.bots.parsers.cymru.parser_cap_program
* `public:` no
* `cache (redis db):` none
* `description:` Parses data from cymru's cap program feed.

#### Description

There are two different feeds available:
 * infected_$date.txt ("old")
 * $certname_$date.txt ("new")

The new will replace the old at some point in time, currently you need to fetch both. The parser handles both formats.

##### Old feed

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

* * *

### Github Feed

#### Information

* `name:` intelmq.bots.parsers.github_feed.parser
* `description:` Parses Feeds available publicly on github (should receive from github_api collector)

* * *

### Have I Been Pwned Callback Parser

#### Information:
* `name:` intelmq.bots.parsers.hibp.parser_callback
* `public:` no
* `cache (redis db):` none
* `description:` Parses data from Have I Been Pwned feed.

#### Description

Parsers the data from a Callback of a Have I Been Pwned Enterprise Subscription.

Parses breaches and pastes and creates one event per e-mail address. The e-mail address is stored in `source.account`.
`classification.type` is `leak` and `classification.identifier` is `breach` or `paste`.

* * *

### HTML Table Parser

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

 * `"ignore_values"`:  A list of strings or a string of comma-separated values which will not considered while assigning to the corresponding fields given in `columns`. E.g.
   ```json
   "ignore_values": [
        "",
        "unknown",
        "Not listed",
   ],
   ```
   is equivalent to:
   ```json
   "ignore_values": ",unknown,Not listed,"
   ```
   The following configuration will lead to assigning all values to malware.name and extra.SBL except `unknown` and `Not listed` respectively.
   ```json
   "columns": [
        "source.url",
        "malware.name",
        "extra.SBL",
   ],
   "ignore_values": [
        "",
        "unknown",
        "Not listed",
   ],
   ```
   Parameters **columns and ignore_values must have same length**
 * `"attribute_name"`: Filtering table with table attributes, to be used in conjunction with `attribute_value`, optional. E.g. `class`, `id`, `style`.
 * `"attribute_value"`: String.
    To filter all tables with attribute `class='details'` use
    ```json
    "attribute_name": "class",
    "attribute_value": "details"
    ```
 * `"table_index"`: Index of the table if multiple tables present. If `attribute_name` and `attribute_value` given, index according to tables remaining after filtering with table attribute. Default: `0`.
 * `"split_column"`: Padded column to be split to get values, to be used in conjunction with `split_separator` and `split_index`, optional.
 * `"split_separator"`: Delimiter string for padded column.
 * `"split_index"`: Index of unpadded string in returned list from splitting `split_column` with `split_separator` as delimiter string. Default: `0`.
    E.g.
    ```json
    "split_column": "source.fqdn",
    "split_separator": " ",
    "split_index": 1,
    ```
    With above configuration, column corresponding to `source.fqdn` with value `[D] lingvaworld.ru` will be assigned as `"source.fqdn": "lingvaworld.ru"`.
 * `"skip_table_head"`: Boolean, skip the first row of the table, optional. Default: `true`.
 * `"default_url_protocol"`: For URLs you can give a default protocol which will be pretended to the data. Default: `"http://"`.
 * `"time_format"`: Optional. If `"timestamp"`, `"windows_nt"` or `"epoch_millis"` the time will be converted first. With the default `null` fuzzy time parsing will be used.
 * `"type"`: set the `classification.type` statically, optional
 * `"html_parser"`: The html parser to use, by default "html.parser", can also be e.g. "lxml", have a look at https://www.crummy.com/software/BeautifulSoup/bs4/doc/

* * *

### McAfee Advanced Threat Defense File

#### Information:
* `name:` intelmq.bots.parsers.mcafee.parser_atd_file
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` parses file hash information off ATD reports

#### Configuration Parameters:

* **Feed parameters** (see above)
* `verdict_severity`: min report severity to parse

* * *

### McAfee Advanced Threat Defense IP

#### Information:
* `name:` intelmq.bots.parsers.mcafee.parser_atd_file
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` parses IP addresses off ATD reports

#### Configuration Parameters:

* **Feed parameters** (see above)
* `verdict_severity`: min report severity to parse

* * *

### McAfee Advanced Threat Defense URL

#### Information:
* `name:` intelmq.bots.parsers.mcafee.parser_atd_file
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` parses URLs off ATD reports

#### Configuration Parameters:

* **Feed parameters** (see above)
* `verdict_severity`: min report severity to parse

* * *

### Microsoft CTIP Parser

* `name`: `intelmq.bots.parsers.microsoft.parser_ctip`
* `public`: no
* `cache (redis db)`: none
* `description`: Parses data from the Microsoft CTIP Feed

#### Description

Can parse the JSON format provided by the Interflow interface (lists of dictionaries) as well as the format provided by the Azure interface (one dictionary per line).
The provided data differs between the two formats/providers.

* * *

### MISP

* `name:` intelmq.bots.parsers.misp.parser
* `public:` no
* `cache (redis db):` none
* `description:` Parses MISP events

#### Description

MISP events collected by the MISPCollectorBot are passed to this parser
for processing. Supported MISP event categories and attribute types are
defined in the `SUPPORTED_MISP_CATEGORIES` and `MISP_TYPE_MAPPING` class
constants.

* * *

### Twitter

#### Information:
* `name:` intelmq.bots.parsers.twitter.parser
* `public:` no
* `cache (redis db):` none
* `description:` Extracts urls from text, fuzzy, aimed at parsing tweets

#### Configuration Parameters:

* `domain_whitelist`: domains to be filtered out
* `substitutions`: semicolon delimited list of even length of pairs of substitutions (for example: '[.];.;,;.' substitutes '[.]' for '.' and ',' for '.')
* `classification_type`: string with a valid classification type as defined in data harmonization
* `default_scheme`: Default scheme for URLs if not given. See also the next section.

##### Default scheme

The dependency `url-normalize` changed it's behavior in version 1.4.0 from using `http://` as default scheme to `https://`. Version 1.4.1 added the possibility to specify it. Thus you can only use the `default_scheme` parameter with a current version of this library >= 1.4.1, with 1.4.0 you will always get `https://` as default scheme and for older versions < 1.4.0 `http://` is used.

This does not affect URLs which already include the scheme.

* * *

### Shadowserver

#### Information
* `name:` intelmq.bots.parsers.shadowserver.parser
* `public:` yes
* `description:` Parses different reports from shadowserver.

#### Configuration Parameters

 * `feedname`: Optional, the Name of the feed, see list below for possible values.
 * `overwrite`: If an existing `feed.name` should be overwritten.

#### How this bot works?

There are two possibilities for the bot to determine which feed the data belongs to in order to determine the correct mapping of the columns:

#### Automatic feed detection
Since IntelMQ version 2.1 the parser can detect the feed based on metadata provided by the collector.

When processing a report, this bot takes `extra.file_name` from the report and
looks in config.py how the report should be parsed.

If this lookup is not possible, and the feed name is not given as parameter, the feed cannot be parsed.

The field `extra.file_name` has the following structure:
`%Y-%m-%d-${report_name}[-suffix].csv` where suffix can be something like `country-geo`. For example, some possible filenames are `2019-01-01-scan_http-country-geo.csv` or `2019-01-01-scan_tftp.csv`. The important part is `${report_name}`, between the date and the suffix.
Since version 2.1.2 the date in the filename is optional, so filenames like `scan_tftp.csv` are also detected.

#### Fixed feed name
If the method above is not possible and for upgraded instances, the feed can be set with the `feedname` parameter.
Feed-names are derived from the subjects of the Shadowserver E-Mails.
A list of possible feeds can be found in the table below in the column "feed name".

#### Supported reports:

These are the supported feed name and their corresponding file name for automatic detection:

| feed name            | file name |
|----------------------| ----------|
| Accessible-ADB | `scan_adb` |
| Accessible-AFP | `scan_afp` |
| Accessible-Cisco-Smart-Install | `cisco_smart_install` |
| Accessible-CWMP | `scan_cwmp` |
| Accessible-FTP | `scan_ftp` |
| Accessible-Hadoop | `scan_hadoop` |
| Accessible-HTTP | `scan_http` |
| Accessible-RDP | `scan_rdp` |
| Accessible-Rsync | `scan_rsync` |
| Accessible-SMB | `scan_smb` |
| Accessible-Telnet | `scan_telnet` |
| Accessible-Ubiquiti-Discovery-Service | `scan_ubiquiti` |
| Accessible-VNC | `scan_vnc` |
| Amplification-DDoS-Victim | `ddos_amplification` |
| Blacklisted-IP | `blacklist` |
| Compromised-Website | `compromised_website` |
| Darknet | `darknet` |
| DNS-Open-Resolvers | `scan_dns` |
| Drone | `botnet_drone` |
| Drone-Brute-Force | `drone_brute_force` |
| HTTP-Scanners | `hp_http_scan` |
| ICS-Scanners | `hp_ics_scan` |
| IPv6-Sinkhole-HTTP-Drone | `sinkhole6_http` |
| Microsoft-Sinkhole | `microsoft_sinkhole` |
| NTP-Monitor | `scan_ntpmonitor` |
| NTP-Version | `scan_ntp` |
| Open-Chargen | `scan_chargen` |
| Open-DB2-Discovery-Service | `scan_db2` |
| Open-Elasticsearch | `scan_elasticsearch` |
| Open-IPMI | `scan_ipmi` |
| Open-IPP | `scan_ipp` |
| Open-LDAP | `scan_ldap ` |
| Open-LDAP-TCP | `scan_ldap_tcp` |
| Open-mDNS | `scan_mdns` |
| Open-Memcached | `scan_memcached` |
| Open-MongoDB | `scan_mongodb` |
| Open-MQTT | `scan_mqtt` |
| Open-MSSQL | `scan_mssql` |
| Open-NATPMP | `scan_nat_pmp` |
| Open-NetBIOS-Nameservice | `scan_netbios` |
| Open-Netis | ? |
| Open-Portmapper | `scan_portmapper` |
| Open-QOTD | `scan_qotd` |
| Open-Redis | `scan_redis` |
| Open-SNMP | `scan_snmp` |
| Open-SSDP | `scan_ssdp` |
| Open-TFTP | `scan_tftp` |
| Open-XDMCP | `scan_xdmcp` |
| Outdated-DNSSEC-Key | `outdated_dnssec_key` |
| Outdated-DNSSEC-Key-IPv6 | `outdated_dnssec_key_v6` |
| Sandbox-URL | `cwsandbox_url` |
| Sinkhole-HTTP-Drone | `sinkhole_http_drone` |
| Spam-URL | `spam_url` |
| SSL-FREAK-Vulnerable-Servers | `scan_ssl_freak` |
| SSL-POODLE-Vulnerable-Servers | `scan_ssl_poodle` |
| Vulnerable-ISAKMP | `scan_isakmp` |

#### Development

##### Structure of this Parser Bot:
The parser consists of two files:
 * config.py
 * parser.py

Both files are required for the parser to work properly.

##### Add new Feedformats:
Add a new feedformat and conversions if required to the file
`config.py`. Don't forget to update the `feed_idx` dict.
It is required to look up the correct configuration.

Look at the documentation in the bots's `config.py` file for more information.

* * *


### Shodan

#### Information
* `name:` intelmq.bots.parsers.shodan.parser
* `public:` yes
* `description:` Parses data from shodan (search, stream etc).

The parser is by far not complete as there are a lot of fields in a big nested structure. There is a minimal mode available which only parses the important/most useful fields and also saves everything in `extra.shodan` keeping the original structure. When not using the minimal mode if may be useful to ignore errors as many parsing errors can happen with the incomplete mapping.

#### Configuration Parameters:

* `ignore_errors`: Boolean (default true)
* `minimal_mode`: Boolean (default false)

* * *

### ZoneH

#### Information
* `name:` intelmq.bots.parsers.zoneh.parser
* `public:` yes
* `description:` Parses data from zoneh.

#### Description
This bot is designed to consume defacement reports from zone-h.org. It expects
fields normally present in CSV files distributed by email.

* * *

## Experts

### Abusix

#### Information:
* `name:` abusix
* `lookup:` dns
* `public:` yes
* `cache (redis db):` 5
* `description:` RIPE abuse contacts resolving through DNS TXT queries
* `notes`: https://abusix.com/contactdb.html

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))

#### Requirements
This bot can optionally use the python module *querycontacts* by abusix itself:
https://pypi.org/project/querycontacts/

```bash
pip3 install querycontacts
```
If the package is not installed, our own routines are used.

* * *

### ASN Lookup


#### Information:
* `name:` ASN lookup
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` IP to ASN

#### Configuration Parameters:

* `database`: Path to the downloaded database.

#### Requirements

Install pyasn module
```bash
pip3 install pyasn 
```

#### Database
* Download database and convert:
```
# cd /tmp/
# pyasn_util_download.py --latest
# pyasn_util_convert.py --single <downloaded_filename.bz2>  ipasn.dat
```

Note: the '<' '>' characters only are syntactic markings, no shell redirection is necessary.

* Copy database to IntelMQ:
```
# mkdir /opt/intelmq/var/lib/bots/asn_lookup
# mv /tmp/ipasn.dat /opt/intelmq/var/lib/bots/asn_lookup/
# chown -R intelmq.intelmq /opt/intelmq/var/lib/bots/asn_lookup
```

* * *

### CSV Converter


#### Information:
* `name`: `intelmq.bots.experts.csv_converter.expert
* `lookup`: no
* `public`: yes
* `cache (redis db)`: none
* `description`: Converts an event to CSV format, saved in the `output` field.

#### Configuration Parameters:

 * `delimiter`: String, default `","`
 * `fieldnames`: Comma-separated list of field names, e.g. `"time.source,classification.type,source.ip"`

#### Usage

To use the CSV-converted data in an output bot - for example in a file output,
use the configuration parameter `single_key` of the output bot and set it to `output`.

* * *

### Copy Extra

#### Information:
* `name:` `intelmq.bots.experts.national_cert_contact_certat.expert
* `lookup:` to https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl
* `public:` yes
* `cache (redis db):` none
* `description:` Queries abuse contact based on the country.

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))
FIXME

* * *

### Cymru Whois

#### Information:
* `name:` cymru-whois
* `lookup:` cymru dns
* `public:` yes
* `cache (redis db):` 5
* `description:` IP to geolocation, ASN, BGP prefix

Public documentation: https://www.team-cymru.com/IP-ASN-mapping.html#dns

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))
* `overwrite`: Overwrite existing fields. Default: `True` if not given (for backwards compatibility, will change in version 3.0.0)

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
* `name:` domain suffix
* `lookup:` no
* `public:` yes
* `cache (redis db):` -
* `description:` extracts the domain suffix from the FQDN

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


#### Information:
* `name:` deduplicator
* `lookup:` redis cache
* `public:` yes
* `cache (redis db):` 6
* `description:` Bot responsible for ignore duplicated messages. The bot can be configured to perform deduplication just looking to specific fields on the message.

#### Configuration Parameters:

* **Cache parameters** (see in section [common parameters](#common-parameters))
* `bypass`- true or false value to bypass the deduplicator. When set to true, messages will not be deduplicated. Default: false

##### Parameters for "fine-grained" deduplication

* `filter_type`: type of the filtering which can be "blacklist" or "whitelist". The filter type will be used to define how Deduplicator bot will interpret the parameter `filter_keys` in order to decide whether an event has already been seen or not, i.e., duplicated event or a completely new event.
  * "whitelist" configuration: only the keys listed in `filter_keys` will be considered to verify if an event is duplicated or not.
  * "blacklist" configuration: all keys except those in `filter_keys` will be considered to verify if an event is duplicated or not.
* `filter_keys`: string with multiple keys separated by comma. Please note that `time.observation` key will not be considered even if defined, because the system always ignore that key.

##### Parameters Configuration Example

###### Example 1

The bot with this configuration will detect duplication only based on `source.ip` and `destination.ip` keys.

```
"parameters": {
    "redis_cache_db": 6,
    "redis_cache_host": "127.0.0.1",
    "redis_cache_password": null,
    "redis_cache_port": 6379,
    "redis_cache_ttl": 86400,
    "filter_type": "whitelist",
    "filter_keys": "source.ip,destination.ip",
}
```

###### Example 2

The bot with this configuration will detect duplication based on all keys, except `source.ip` and `destination.ip` keys.

```
"parameters": {
    "redis_cache_db": 6,
    "redis_cache_host": "127.0.0.1",
    "redis_cache_password": null,
    "redis_cache_port": 6379,
    "redis_cache_ttl": 86400,
    "filter_type": "blacklist",
    "filter_keys": "source.ip,destination.ip",
}
```

#### Flushing the cache

To flush the deduplicator's cache, you can use the `redis-cli` tool. Enter the database used by the bot and submit the `flushdb` command:
```
redis-cli -n 6
flushdb
```

* * *

### DO Portal Expert Bot

#### Information:
* `name:` do_portal
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` The DO portal retrieves the contact information from a DO portal instance: http://github.com/certat/do-portal/

#### Configuration Parameters:
* `mode` - Either `replace` or `append` the new abuse contacts in case there are existing ones.
* `portal_url` - The URL to the portal, without the API-path. The used URL is `$portal_url + '/api/1.0/ripe/contact?cidr=%s'`.
* `portal_api_key` - The API key of the user to be used. Must have sufficient privileges.

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

The filter bot is capable of filtering specific events.

#### Information:
* `name:` filter
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` filter messages (drop or pass messages) FIXME

#### Configuration Parameters:

##### Parameters for filtering with key/value attributes:
* `filter_key` - key from data harmonization
* `filter_value` - value for the key
* `filter_action` - action when a message match to the criteria (possible actions: keep/drop)
* `filter_regex` - attribute determines if the `filter_value` shall be treated as regular expression or not.
   If this attribute is not empty, the bot uses python's "search" function to evaluate the filter.

##### Parameters for time based filtering:
* `not_before` - events before this time will be dropped
* `not_after` - events after this time will be dropped

Both parameters accept string values describing absolute or relative time:
* absolute
 * basically anything parseable by datetime parser, eg. "2015-09-012T06:22:11+00:00"
 * `time.source` taken from the event will be compared to this value to decide the filter behavior
* relative
 * accepted string formatted like this "<integer> <epoch>", where epoch could be any of following strings (could optionally end with trailing 's'): hour, day, week, month, year
 * time.source taken from the event will be compared to the value (now - relative) to decide the filter behavior

Examples of time filter definition:
* ```"not_before" : "2015-09-012T06:22:11+00:00"``` events older than the specified time will be dropped
* ```"not_after" : "6 months"``` just events older than 6 months will be passed through the pipeline

#### Possible paths

 * `_default`: default path, according to the configuration
 * `action_other`: Negation of the default path
 * `filter_match`: For all events the filter matched on
 * `filter_no_match`: For all events the filter does not match

| action | match |  `_default` | `action_other` | `filter_match` | `filter_no_match` |
| ------ | ----- | ----------- | -------------- | -------------- | ----------------- |
| keep   | ✓     | ✓           | ✗              | ✓              | ✗                 |
| keep   | ✗     | ✗           | ✓              | ✗              | ✓                 |
| drop   | ✓     | ✗           | ✓              | ✓              | ✗                 |
| drop   | ✗     | ✓           | ✗              | ✗              | ✓                 |

In `DEBUG` logging level, one can see that the message is sent to both matching paths, also if one of the paths is not configured. Of course the message is only delivered to the configured paths.

* * *

### Format Field

#### Information:
* `name:` Format Field
* `lookup:` none
* `cache (redis db):` none
* `description:` String method operations on column values

#### Configuration Parameters:

##### Parameters for stripping chars:
* `strip_columns` -  A list of strings or a string of comma-separated values with field names. The names must match the harmonization's field names. E.g.
   ```json
   "columns": [
        "malware.name",
        "extra.tags"
   ],
   ```
   is equivalent to:
   ```json
   "columns": "malware.name,extra.tags"
   ```
* `strip_chars` -  a set of characters to remove as leading/trailing characters(default: ` ` or whitespace)

##### Parameters for replacing chars:
* `replace_column` - key from data harmonization
* `old_value` - the string to search for
* `new_value` - the string to replace the old value with
* `replace_count` - number specifying how many occurrences of the old value you want to replace(default: `1`)

##### Parameters for splitting string to list of string:
* `split_column` - key from data harmonization
* `split_separator` - specifies the separator to use when splitting the string(default: `,`)

Order of operation: `strip -> replace -> split`. These three methods can be combined such as first strip and then split.

* * *

### Generic DB Lookup

This bot is capable for enriching intelmq events by lookups to a database.
Currently only PostgreSQL and SQLite are supported.

If more than one result is returned, a ValueError is raised.

#### Information:
* `name:` `intelmq.bots.experts.generic_db_lookup.expert`
* `lookup:` database
* `public:` yes
* `cache (redis db):` none
* `description:` This bot is capable for enriching intelmq events by lookups to a database.

#### Configuration Parameters:

##### Connection

* `engine`: `postgresql` or `sqlite`
* `database`: string, defaults to "intelmq", database name or the SQLLite filename
* `table`: defaults to "contacts"

##### PostgreSQL specific
* `host`: string, defaults to "localhost"
* `password`: string
* `port`: integer, defaults to 5432
* `sslmode`: string, defaults to "require"
* `user`: defaults to "intelmq"

##### Lookup

* `match_fields`: defaults to `{"source.asn": "asn"}`

The value is a key-value mapping an arbitrary number **intelmq** field names **to table** column names.
The values are compared with `=` only.

##### Replace fields.

* `overwrite`: defaults to `false`. Is applied per field
* `replace_fields`: defaults to `{"contact": "source.abuse_contact"}`

`replace_fields` is again a key-value mapping an arbitrary number of **table** column names **to intelmq** field names 

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

### IDEA Converter

Converts the event to IDEA format and saves it as JSON in the field `output`. All other fields are not modified.

Documentation about IDEA: https://idea.cesnet.cz/en/index

#### Information:
* `name:` intelmq.bots.experts.idea.expert
* `lookup:` local config
* `public:` yes
* `cache (redis db):` none
* `description:` The bot does a best effort translation of events into the IDEA format.

#### Configuration Parameters:

* `test_mode`: add `Test` category to mark all outgoing IDEA events as informal (meant to simplify setting up and debugging new IDEA producers) (default: `true`)

* * *

### MaxMind GeoIP

#### Information:
* `name:` intelmq.bots.experts.maxmind_geoip.expert
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` IP to geolocation

#### Setup

The bot requires the maxmind's `geoip2` Python library, version 2.2.0 has been tested.

To download the database a free license key is required. More information can be found at https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/

You may want to use a shell script provided in the contrib directory to keep the database up to date: `contrib/cron-jobs/update-geoip-data`

#### Configuration Parameters:

* `database`: Path to the local database, e.g. `"/opt/intelmq/var/lib/bots/maxmind_geoip/GeoLite2-City.mmdb"`
* `overwrite`: boolean
* `use_registered`: boolean. MaxMind has two country ISO codes: One for the physical location of the address and one for the registered location. Default is `false` (backwards-compatibility). See also https://github.com/certtools/intelmq/pull/1344 for a short explanation.

### MISP

Queries a MISP instance for the `source.ip` and adds the MISP Attribute UUID and MISP Event ID of the newest attribute found.

#### Information:
* `name:` intelmq.bots.experts.misp.expert
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` IP address to MISP attribute and event

#### Configuration Parameters:

* `misp_key`: MISP Authkey
* `misp_url`: URL of MISP server (with trailing '/')

Generic parameters used in this bot:
* `http_verify_cert`: Verify the TLS certicate of the server, boolean (default: `true`)

* * *

### McAfee Active Response Hash lookup

#### Information:
* `name:` intelmq.bots.experts.mcafee.expert_mar
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Queries occurrences of hashes within local environment

#### Configuration Parameters:

* **Feed parameters** (see above)
* `dxl_config_file`: location of file containing required information to connect to DXL bus
* `lookup_type`: One of:
  - `Hash`: looks up `malware.hash.md5`, `malware.hash.sha1` and `malware.hash.sha256`
  - `DestSocket`: looks up `destination.ip` and `destination.port`
  - `DestIP`: looks up `destination.ip`
  - `DestFQDN`: looks up in `destination.fqdn`

* * *

### McAfee Active Response IP lookup

#### Information:
* `name:` intelmq.bots.experts.mcafee.expert_mar_ip
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Queries occurrences of connection attempts to destination ip/port within local environment

#### Configuration Parameters:

* **Feed parameters** (see above)
* `dxl_config_file`: location of file containing required information to connect to DXL bus

* * *

### McAfee Active Response URL lookup

#### Information:
* `name:` intelmq.bots.experts.mcafee.expert_mar_url
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Queries occurrences of FQDN lookups within local environment

#### Configuration Parameters:

* **Feed parameters** (see above)
* `dxl_config_file`: location of file containing required information to connect to DXL bus

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
* `maximum_matches`: Maximum number of matches. Processing stops after the limit is reached. Default: no limit (`null`, `0`).
* `overwrite`: Overwrite any existing fields by matching rules. Default if the parameter is given: `true`, for backwards compatibility. Default will change to `false` in version 3.0.0.

#### Configuration File

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


##### Actions

You can set the value of the field to a string literal or number.

In addition you can use the [standard Python string format syntax](https://docs.python.org/3/library/string.html#format-string-syntax)
to access the values from the processed event as `msg` and the match groups
of the conditions as `matches`, see the bitdefender example above.
Group 0 (`[0]`) contains the full matching string. See also the documentation on [`re.Match.group`](https://docs.python.org/3/library/re.html?highlight=re%20search#re.Match.group).

Note that `matches` will also contain the match groups
from the default conditions if there were any.

##### Examples

We have an event with `feed.name = Spamhaus Cert` and `malware.name = confickerab`. The expert loops over all sections in the file and eventually enters section `Spamhaus Cert`. First, the default condition is checked, it matches! OK, going on. Otherwise the expert would have selected a different section that has not yet been considered. Now, go through the rules, until we hit the rule `conficker`. We combine the conditions of this rule with the default conditions, and both rules match! So we can apply the action: `classification.identifier` is set to `conficker`, the trivial name.

Assume we have an event with `feed.name = Spamhaus Cert` and `malware.name = feodo`. The default condition matches, but no others. So the default action is applied. The value for `classification.identifier` will be set to `feodo` by `{msg[malware.name]}`.

##### Types

If the rule is a string, a regex-search is performed, also for numeric values (`str()` is called on them). If the rule is numeric for numeric values, a simple comparison is done. If other types are mixed, a warning will be thrown.

For boolean values, the comparison value needs to be `true` or `false` as in JSON they are written all-lowercase.

* * *

### National CERT contact lookup by CERT.AT

#### Information:
* `name:` `national_cert_contact_certat`
* `lookup:` https
* `public:` yes
* `cache (redis db):` none
* `description:` https://contacts.cert.at offers an IP address to national CERT contact (and cc) mapping. See https://contacts.cert.at for more info.

#### Configuration Parameters:

* `filter`: (true/false) act as a filter for AT.
* `overwrite_cc`: set to true if you want to overwrite any potentially existing cc fields in the event.

* * *

### RecordedFuture IP risk

This Bot tags events with score found in recorded futures large IP risklist.

#### Information:
* `name:` recordedfuture_iprisk
* `lookup:` local database
* `public:` no
* `cache (redis db):` none
* `description:` Record risk score associated to source and destination IP if they are present. Assigns 0 to IP addresses not in the RF list.

#### Configuration Parameters:

* `database`: Location of csv file obtained from recorded future API (a script is provided to download the large IP set)
* `overwrite`: set to true if you want to overwrite any potentially existing risk score fields in the event.

#### Description

For both `source.ip` and `destination.ip` the corresponding risk score is fetched from a local database created from Recorded Future's API. The score is recorded in `extra.rf_iprisk.source` and `extra.rf_iprisk.destination`. If a lookup for an IP fails a score of 0 is recorded.

See https://www.recordedfuture.com/products/api/ and speak with your recorded future representative for more information.


The list is obtained from recorded future API and needs a valid API TOKEN
The large list contains all IP's with a risk score of 25 or more.
If IP's are not present in the database a risk score of 0 is given

A script is supplied that may be run as intelmq to update the database.
The script needs to be edited to use a valid API token.

Download database:

```bash
mkdir /opt/intelmq/var/lib/bots/recordedfuture_iprisk
cd /tmp/
curl -H "X-RFToken: [API Token]" --output rfiprisk.dat.gz "https://api.recordedfuture.com/v2/ip/risklist?format=csv%2Fsplunk&gzip=true&list=large"
bunzip rfiprisk.dat.gz
mv rfiprisk.dat /opt/intelmq/var/lib/bots/recordedfuture_iprisk/rfiprisk.dat
chown intelmq.intelmq -R /opt/intelmq/var/lib/bots/recordedfuture_iprisk
```

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
* `overwrite`: Overwrite existing fields. Default: `True` if not given (for backwards compatibility, will change in version 3.0.0)

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

### Ripe

Online RIPE Abuse Contact and Geolocation Finder for IP addresses and Autonomous Systems.

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
* `query_ripe_stat_geolocation`: Query for IPs at `https://stat.ripe.net/data/maxmind-geo-lite/data.json?resource=%s`, default `true`

* * *

### Sieve

#### Information:
* `name:` sieve
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` Filtering with a sieve-based configuration language

#### Configuration Parameters:

* `file`: Path to sieve file. Syntax can be validated with `intelmq_sieve_expert_validator`.


#### Description

The sieve bot is used to filter and/or modify events based on a set of rules. The
rules are specified in an external configuration file and with a syntax similar
to the [Sieve language](http://sieve.info/) used for mail filtering.

Each rule defines a set of matching conditions on received events. Events can be
matched based on keys and values in the event. If the processed event matches a
rule's conditions, the corresponding actions are performed. Actions can specify
whether the event should be kept or dropped in the pipeline (filtering actions)
or if keys and values should be changed (modification actions).

#### Requirements

To use this bot, you need to install the required dependencies:
```
pip3 install -r intelmq/bots/experts/sieve/REQUIREMENTS.txt
```

#### Examples

The following excerpts illustrate some of the basic features of the sieve file
format:

```
if :exists source.fqdn {
  keep  // aborts processing of subsequent rules and forwards the event.
}


if :notexists source.abuse_contact || source.abuse_contact =~ '.*@example.com' {
  drop  // aborts processing of subsequent rules and drops the event.
}

if source.ip << '192.0.0.0/24' {
    add! comment = 'bogon'
}

if classification.type == ['phishing', 'malware'] && source.fqdn =~ '.*\.(ch|li)$' {
  add! comment = 'domainabuse'
  keep
} elif classification.type == 'scanner' {
  add! comment = 'ignore'
  drop
} else {
  remove comment
}
```


#### Reference

##### Sieve File Structure

The sieve file contains an arbitrary number of rules of the form:

```
if EXPRESSION {
    ACTIONS
} elif EXPRESSION {
    ACTIONS
} else {
    ACTIONS
}
```


#####  Expressions

Each rule specifies on or more expressions to match an event based on its keys
and values. Event keys are specified as strings without quotes. String values
must be enclosed in single quotes. Numeric values can be specified as integers
or floats and are unquoted. IP addresses and network ranges (IPv4 and IPv6) are
specified with quotes. Following operators may be used to match events:

 * `:exists` and `:notexists` match if a given key exists, for example:

    ```if :exists source.fqdn { ... }```

 * `==` and `!=` match for equality of strings and numbers, for example:

   ```if feed.name != 'acme-security' || feed.accuracy == 100 { ... }```

 * `:contains` matches on substrings.

 * `=~` matches strings based on the given regex. `!~` is the inverse regex
 match.

 * Numerical comparisons are evaluated with `<`, `<=`, `>`, `>=`.

 * `<<` matches if an IP address is contained in the specified network range:

   ```if source.ip << '10.0.0.0/8' { ... }```

 * Values to match against can also be specified as list, in which case any one
 of the values will result in a match:

   ```if source.ip == ['8.8.8.8', '8.8.4.4'] { ... }```

  In this case, the event will match if it contains a key `source.ip` with
  either value `8.8.8.8` or `8.8.4.4`.

  With inequality operators, the behavior is the same, so it matches if any expression does not match:

  ```if source.ip != ['8.8.8.8', '8.8.4.4'] { ... }```

  Events with values like `8.8.8.8` or `8.8.4.4` will match, as they are always unequal to the other value.
  The result is *not* that the field must be unequal to all given values.


##### Actions

If part of a rule matches the given conditions, the actions enclosed in `{` and
`}` are applied. By default, all events that are matched or not matched by rules
in the sieve file will be forwarded to the next bot in the pipeline, unless the
`drop` action is applied.

 * `add` adds a key value pair to the event. This action only applies if the key
 is not yet defined in the event. If the key is already defined, the action is
 ignored. Example:

   ```add comment = 'hello, world'```

 * `add!` same as above, but will force overwrite the key in the event.

 * `update` modifies an existing value for a key. Only applies if the key is
already defined. If the key is not defined in the event, this action is ignored.
Example:

   ```update feed.accuracy = 50```

 * `remove` removes a key/value from the event. Action is ignored if the key is
 not defined in the event. Example:

    ```remove extra.comments```

 * `keep` sends the message to the next bot in the pipeline
 (same as the default behaviour), and stops sieve file processing.

   ```keep```

 * `path` sets the path (named queue) the message should be sent to (implicitly
   or with the command `keep`. The named queue needs to configured in the
   pipeline, see the User Guide for more information.

   ```path 'named-queue'```

 * `drop` marks the event to be dropped. The event will not be forwarded to the
 next bot in the pipeline. The sieve file processing is interrupted upon
 reaching this action. No other actions may be specified besides the `drop`
 action within `{` and `}`.


##### Comments

Comments may be used in the sieve file: all characters after `//` and until the end of the line will be ignored.


##### Validating a sieve file

Use the following command to validate your sieve files:
```
$ intelmq.bots.experts.sieve.validator
usage: intelmq.bots.experts.sieve.validator [-h] sievefile

Validates the syntax of sievebot files.

positional arguments:
  sievefile   Sieve file

optional arguments:
  -h, --help  show this help message and exit
```

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

* `database`: Path to the database

#### Database
Use the included script `update-tor-nodes` to download the database.

### Url2FQDN

This bot extracts the Host from the `source.url` and `destination.url` fields and
writes it to `source.fqdn` or `destination.fqdn` if it is a hostname, or
`source.ip` or `destination.ip` if it is an IP address.

#### Information:
* `name:` url2fqdn
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` writes domain name from URL to FQDN or IP address

#### Configuration Parameters:

* `overwrite`: boolean, replace existing FQDN / IP address?

### Wait

#### Information:
* `name:` wait
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` Waits for a some time or until a queue size is lower than a given number.

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

* * *

## Outputs

### AMQP Topic

Sends data to an AMQP Server
See https://www.rabbitmq.com/tutorials/amqp-concepts.html for more details on amqp topic exchange.

Requires the [`pika` python library](https://pypi.org/project/pika/).

#### Information
* `name`: `intelmq.bots.outputs.amqptopic.output`
* `lookup`: to the amqp server
* `public`: yes
* `cache`: no
* `description`: Sends the event to a specified topic of an AMQP server

#### Configuration parameters:

* connection_attempts   : The number of connection attempts to defined server, defaults to 3
* connection_heartbeat  : Heartbeat to server, in seconds, defaults to 3600
* connection_host       : Name/IP for the AMQP server, defaults to 127.0.0.1
* connection_port       : Port for the AMQP server, defaults to 5672
* connection_vhost      : Virtual host to connect, on an http(s) connection would be http:/IP/<your virtual host>
* content_type          : Content type to deliver to AMQP server, currently only supports "application/json"
* delivery_mode         : 1 - Non-persistent, 2 - Persistent. On persistent mode, messages are delivered to 'durable' queues and will be saved to disk.
* exchange_durable      : If set to True, the exchange will survive broker restart, otherwise will be a transient exchange.
* exchange_name         : The name of the exchange to use
* exchange_type         : Type of the exchange, e.g. `topic`, `fanout` etc.
* keep_raw_field        : If set to True, the message 'raw' field will be sent
* password              : Password for authentication on your AMQP server
* require_confirmation  : If set to True, an exception will be raised if a confirmation error is received
* routing_key           : The routing key for your amqptopic
* `single_key`          : Only send the field instead of the full event (expecting a field name as string)
* username              : Username for authentication on your AMQP server
* `use_ssl`             : Use ssl for the connection, make sure to also set the correct port, usually 5671 (`true`/`false`)
* message_hierarchical_output: Convert the message to hierarchical JSON, default: false
* message_with_type     : Include the type in the sent message, default: false
* message_jsondict_as_string: Convert fields of type JSONDict (extra) as string, default: false

If no authentication should be used, leave username or password empty or `null`.

#### Examples of usage:

* Useful to send events to a RabbitMQ exchange topic to be further processed in other platforms.

#### Confirmation

If routing key or exchange name are invalid or non existent, the message is
accepted by the server but we receive no confirmation.
If parameter require_confirmation is True and no confirmation is received, an
error is raised.

#### Common errors

##### Unroutable messages / Undefined destination queue

The destination exchange and queue need to exist beforehand,
with your preferred settings (e.g. durable, [lazy queue](https://www.rabbitmq.com/lazy-queues.html).
If the error message says that the message is "unroutable", the queue doesn't exist.

* * *

### Blackhole

This output bot discards all incoming messages.

#### Information
* `name`: blackhole
* `lookup`: no
* `public`: yes
* `cache`: no
* `description`: discards messages

* * *

### Elasticsearch Output Bot

#### Information
* `name`: `intelmq.bots.outputs.elasticsearch.output`
* `lookup`: yes
* `public`: yes
* `cache`: no
* `description`: Output Bot that sends events to Elasticsearch

Only ElasticSearch version 7 supported.

#### Configuration parameters:

* `elastic_host`: Name/IP for the Elasticsearch server, defaults to 127.0.0.1
* `elastic_port`: Port for the Elasticsearch server, defaults to 9200
* `elastic_index`: Index for the Elasticsearch output, defaults to intelmq
* `rotate_index`: If set, will index events using the date information associated with the event.
                       Options: 'never', 'daily', 'weekly', 'monthly', 'yearly'. Using 'intelmq' as the elastic_index, the following are examples of the generated index names:

                       'never' --> intelmq
                       'daily' --> intelmq-2018-02-02
                       'weekly' --> intelmq-2018-42
                       'monthly' --> intelmq-2018-02
                       'yearly' --> intelmq-2018
* `http_username`: HTTP basic authentication username
* `http_password`: HTTP basic authentication password
* `use_ssl`: Whether to use SSL/TLS when connecting to Elasticsearch. Default: False
* `http_verify_cert`: Whether to require verification of the server's certificate. Default: False
* `ssl_ca_certificate`: An optional path to a certificate bundle to use for verifying the server
* `ssl_show_warnings`: Whether to show warnings if the server's certificate cannot be verified. Default: True
* `replacement_char`: If set, dots ('.') in field names will be replaced with this character prior to indexing. This is for backward compatibility with ES 2.X. Default: null. Recommended for ES2.X: '_'
* `flatten_fields`: In ES, some query and aggregations work better if the fields are flat and not JSON. Here you can provide a list of fields to convert.
                       Can be a list of strings (fieldnames) or a string with field names separated by a comma (,). eg `extra,field2` or `['extra', 'field2']`
                       Default: ['extra']

See contrib/elasticsearch/elasticmapper for a utility for creating Elasticsearch mappings and templates.

If using `rotate_index`, the resulting index name will be of the form [elastic_index]-[event date].
To query all intelmq indices at once, use an alias (https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html), or a multi-index query.

The data in ES can be retrieved with the HTTP-Interface:

```bash
> curl -XGET 'http://localhost:9200/intelmq/events/_search?pretty=True'
```

* * *

### File

#### Information:
* `name:` file
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` output messages (reports or events) to file

Multihreading is disabled for this bot, as this would lead to corrupted files.

#### Configuration Parameters:

* `encoding_errors_mode`: By default `'strict'`, see for more details and options: https://docs.python.org/3/library/functions.html#open For example with `'backslashreplace'` all characters which cannot be properly encoded will be written escaped with backslashes.
* `file`: file path of output file. Missing directories will be created if possible with the mode 755.
* `format_filename`: Boolean if the filename should be formatted (default: `false`).
* `hierarchical_output`: If true, the resulting dictionary will be hierarchical (field names split by dot).
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

### McAfee Enterprise Security Manager

#### Information:
* `name:` intelmq.bots.outputs.mcafee.output_esm_ip
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Writes information out to McAfee ESM watchlist

#### Configuration Parameters:

* **Feed parameters** (see above)
* `esm_ip`: IP address of ESM instance
* `esm_user`: username of user entitled to write to watchlist
* `esm_pw`: password of user
* `esm_watchlist`: name of the watchlist to write to
* `field`: name of the IntelMQ field to be written to ESM

* * *

### MISP Feed

#### Information:
* `name:` `intelmq.bots.outputs.misp.output_feed`
* `lookup:` no
* `public:` no
* `cache (redis db):` none
* `description:` Create a directory layout in the MISP Feed format

The PyMISP library >= 2.4.119.1 is required, see
[REQUIREMENTS.txt](../intelmq/bots/outputs/misp/REQUIREMENTS.txt).

#### Configuration Parameters:

* **Feed parameters** (see above)
* `misp_org_name`: Org name which creates the event, string
* `misp_org_uuid`: Org UUID which creates the event, string
* `output_dir`: Output directory path, e.g. `/opt/intelmq/var/lib/bots/mispfeed-output`. Will be created if it does not exist and possible.
* `interval_event`: The output bot creates one event per each interval, all data in this time frame is part of this event. Default "1 hour", string.

#### Usage in MISP

Configure the destination directory of this feed as feed in MISP, either as local location, or served via a web server. See [the MISP documentation on Feeds](https://www.circl.lu/doc/misp/managing-feeds/) for more information

* * *

### MISP API

#### Information:
* `name:` `intelmq.bots.outputs.misp.output_api`
* `lookup:` no
* `public:` no
* `cache (redis db):` none
* `description:` Connect to a MISP instance and add event as MISPObject if not there already.

The PyMISP library >= 2.4.120 is required, see
[REQUIREMENTS.txt](../intelmq/bots/outputs/misp/REQUIREMENTS.txt).

#### Configuration Parameters:

* **Feed parameters** (see above)
* `add_feed_provider_as_tag`: bool (use `true` when in doubt)
* `add_feed_name_as_tag`: bool (use `true` when in doubt)
* `misp_additional_correlation_fields`: list of fields for which
      the correlation flags will be enabled (in addition to those which are
      in significant_fields)
* `misp_additional_tags`: list of tags to set not be searched for
      when looking for duplicates
* `misp_key`: str, API key for accessing MISP
* `misp_publish`: bool, if a new MISP event should be set to "publish".
      Expert setting as MISP may really make it "public"!
      (Use `false` when in doubt.)
* `misp_tag_for_bot`: str, used to mark MISP events
* `misp_to_ids_fields`: list of fields for which the `to_ids` flags will be set
* `misp_url`: str, URL of the MISP server
* `significant_fields`: list of intelmq field names

The `significant_fields` values
will be searched for in all MISP attribute values
and if all values are found in the same MISP event, no new MISP event
will be created.
Instead if the existing MISP events have the same feed.provider
and match closely, their timestamp will be updated.

If a new MISP event is inserted the `significant_fields` and the
`misp_additional_correlation_fields` will be the attributes
where correlation is enabled.

Make sure to build the IntelMQ Botnet in a way the rate of incoming
events is what MISP can handle, as IntelMQ can process many more events faster
than MISP (which is by design as MISP is for manual handling).
Also remove the fields of the IntelMQ events with an expert bot
that you do not want to be inserted into MISP.

(More details can be found in the docstring of
[`output_api.py`](../intelmq/bots/outputs/misp/output_api.py)).

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
* `port`: MongoDB port, default: 27017
* `hierarchical_output`: Boolean (default true) as mongodb does not allow saving keys with dots, we split the dictionary in sub-dictionaries.
* `replacement_char`: String (default `'_'`) used as replacement character for the dots in key names if hierarchical output is not used.

#### Installation Requirements

```
pip3 install pymongo>=2.7.1
```

The bot has been tested with pymongo versions 2.7.1, 3.4 and 3.10.1 (server versions 2.6.10 and 3.6.8).

* * *

### Redis

#### Information:
* `name:` `intelmq.bots.outputs.redis.output`
* `lookup:` to the redis server
* `public:` yes
* `cache (redis db):` none
* `description:` Output Bot that sends events to a remote Redis server/queue.

#### Configuration Parameters:

* `redis_db`: remote server database, e.g.: 2
* `redis_password`: remote server password
* `redis_queue`: remote server list (queue), e.g.: "remote-server-queue"
* `redis_server_ip`: remote server IP address, e.g.: 127.0.0.1
* `redis_server_port`: remote server Port, e.g.: 6379
* `redis_timeout`: Connection timeout, in msecs, e.g.: 50000
* `hierarchical_output`: whether output should be sent in hierarchical json format (default: false)
* `with_type`: Send the `__type` field (default: true)

#### Examples of usage:

* Can be used to send events to be processed in another system. E.g.: send events to Logstash.
* In a multi tenant installation can be used to send events to external/remote IntelMQ instance. Any expert bot queue can receive the events.
* In a complex configuration can be used to create logical sets in IntelMQ-Manager. 

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
Access the event's values with `{ev[source.ip]}` and similar. Any not existing fields will result in `None`.

Authentication is optional. If both username and password are given, these
mechanism are tried: CRAM-MD5, PLAIN, and LOGIN.

Client certificates are not supported. If `http_verify_cert` is true, TLS certificates are checked.

* * *

### SQL

#### Information:
* `name:` sql
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` SQL is the bot responsible to send events to a PostgreSQL or SQLite Database
* `notes`: When activating autocommit, transactions are not used: http://initd.org/psycopg/docs/connection.html#connection.autocommit

#### Configuration Parameters:

The parameters marked with 'PostgreSQL' will be sent
to libpq via psycopg2. Check the
[libpq parameter documentation] (https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS)
for the versions you are using.

* `autocommit`: [psycopg's autocommit mode](http://initd.org/psycopg/docs/connection.html?#connection.autocommit), optional, default True
* `connect_timeout`: Database connect_timeout, optional, default 5 seconds
* `engine`: 'postgresql' or 'sqlite'
* `database`: PostgreSQL database or SQLite file
* `host`: PostgreSQL host
* `jsondict_as_string`: save JSONDict fields as JSON string, boolean. Default: true (like in versions before 1.1)
* `port`: PostgreSQL port
* `user`: PostgreSQL user
* `password`: PostgreSQL password
* `sslmode`: PostgreSQL sslmode, can be `'disable'`, `'allow'`, `'prefer'` (default), `'require'`, `'verify-ca'` or `'verify-full'`. See postgresql docs: https://www.postgresql.org/docs/current/static/libpq-connect.html#libpq-connect-sslmode
* `table`: name of the database table into which events are to be inserted

#### SQL
Similarly to PostgreSQL, you can use `intelmq_psql_initdb` to create initial sql-statements
from Harmonization.conf. The script will create the required table layout
and save it as /tmp/initdb.sql

Create the new database (you can ignore all errors since SQLite doesn't know all SQL features generated for PostgreSQL):

```bash
sqlite3 your-db.db
sqlite> .read /tmp/initdb.sql
```

#### PostgreSQL

You have two basic choices to run PostgreSQL:
1. on the same machine as intelmq, then you could use unix-sockets if available on your platform
2. on a different machine. In which case you would need to use a TCP connection and make sure you give the right connection parameters to each psql or client call.

Make sure to consult your PostgreSQL documentation 
about how to allow network connections and authentication in case 2.

##### PostgreSQL Version
Any supported version of PostgreSQL should work 
(v>=9.2 as of Oct 2016)[[1](https://www.postgresql.org/support/versioning/)].

If you use PostgreSQL server v >= 9.4, it gives you the possibility 
to use the time-zone [formatting string](https://www.postgresql.org/docs/9.4/static/functions-formatting.html) "OF" for date-times 
and the [GiST index for the cidr type](https://www.postgresql.org/docs/9.4/static/release-9-4.html#AEN120769). This may be useful depending on how 
you plan to use the events that this bot writes into the database.

##### How to install:

Use `intelmq_psql_initdb` to create initial sql-statements
from Harmonization.conf. The script will create the required table layout
and save it as /tmp/initdb.sql

You need a postgresql database-user to own the result database.
The recommendation is to use the name `intelmq`.
There may already be such a user for the postgresql database-cluster
to be used by other bots. (For example from setting up
the expert/certbund_contact bot.)

Therefore if still necessary: create the database-user
as postgresql superuser, which usually is done via the system user `postgres`:
```
createuser --no-superuser --no-createrole --no-createdb --encrypted --pwprompt intelmq
```

Create the new database:
```
createdb --encoding='utf-8' --owner=intelmq intelmq-events
```

(The encoding parameter should ensure the right encoding on platform
where this is not the default.)

Now initialize it as database-user `intelmq` (in this example
a network connection to localhost is used, so you would get to test
if the user `intelmq` can authenticate):
```
psql -h localhost intelmq-events intelmq </tmp/initdb.sql
```

* * *

### STOMP

#### Information:
* `name`: intelmq.bots.outputs.stomp.output
* `lookup`: yes
* `public`: yes
* `cache (redis db)`: none
* `description`: This collector will push data to any STOMP stream. STOMP stands for Streaming Text Oriented Messaging Protocol. See: https://en.wikipedia.org/wiki/Streaming_Text_Oriented_Messaging_Protocol

#### Requirements:

Install the stomp.py library, e.g. `apt install python3-stomp.py` or `pip install stomp.py`.

You need a CA certificate, client certificate and key file from the organization / server you are connecting to.
Also you will need a so called "exchange point".

#### Configuration Parameters:

* `exchange`: The exchange to push at
* `heartbeat`: default: 60000
* `message_hierarchical_output`: Boolean, default: false
* `message_jsondict_as_string`: Boolean, default: false
* `message_with_type`: Boolean, default: false
* `port`: Integer, default: 61614
* `server`: Host or IP address of the STOMP server
* `single_key`: Boolean or string (field name), default: false
* `ssl_ca_certificate`: path to CA file
* `ssl_client_certificate`: path to client cert file
* `ssl_client_certificate_key`: path to client cert key file

* * *

### TCP

#### Information:
* `name:` intelmq.bots.outputs.tcp.output
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` TCP is the bot responsible to send events to a TCP port (Splunk, another IntelMQ, etc..).

Multihreading is disabled for this bot.

#### Configuration Parameters:

* `counterpart_is_intelmq`: Boolean. If you are sending to an IntelMQ TCP collector, set this to True, otherwise e.g. with filebeat, set it to false.
* `ip`: IP of destination server
* `hierarchical_output`: true for a nested JSON, false for a flat JSON (when sending to a TCP collector).
* `port`: port of destination server
* `separator`: separator of messages, eg. "\n", optional. When sending to a TCP collector, parameter shouldn't be present.
    In that case, the output waits every message is acknowledged by "Ok" message the tcp.collector bot implements.

* * *

### Touch

#### Information:
* `name:` intelmq.bots.outputs.touch.output
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Touches a file for every event received.

#### Configuration Parameters:

* `path`: Path to the file to touch.

* * *

### UDP

#### Information:
* `name:` intelmq.bots.outputs.udp.output
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Output Bot that sends events to a remote UDP server.

Multihreading is disabled for this bot.

#### Configuration Parameters:

* `field_delimiter`: If the format is 'delimited' this will be added between fields. String, default: `"|"`
* `format`: Can be `'json'` or `'delimited'`. The Json format outputs the event 'as-is'. Delimited will deconstruct the event and print each field:value separated by the field delimit. See examples bellow.
* `header`: Header text to be sent in the udp datagram, string.
* `keep_raw_field`: boolean, default: false
* `udp_host`: Destination's server's Host name or IP address
* `udp_port`: Destination port

#### Examples of usage:

Consider the following event:
```json
{"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}
```
With the following Parameters:

* field_delimiter   : |
* format            : json
* Header            : header example
* keep_raw_field    : true
* ip                : 127.0.0.1
* port              : 514

Resulting line in syslog:

```
Apr 29 11:01:29 header example {"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}
```
With the following Parameters:

* field_delimiter   : |
* format            : delimited
* Header            : IntelMQ-event
* keep_raw_field    : false
* ip                : 127.0.0.1
* port              : 514

Resulting line in syslog:

```
Apr 29 11:17:47 localhost IntelMQ-event|source.ip: 85.25.160.114|time.source:2016-04-25T11:39:00+00:00|feed.url:http://www.malwaredomainlist.com/updatescsv.php|time.observation:2016-04-29T11:17:44+00:00|source.reverse_dns:static-ip-85-25-160-114.inaddr.ip-pool.com|feed.name:Malware Domain List|event_description.text:Angler EK|source.url:http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/|source.asn:8972|classification.type:malware|feed.accuracy:100.0
```

* * *

### XMPP

#### Information:
* `name:` intelmq.bots.outputs.xmpp.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` The XMPP Output is capable of sending Messages to XMPP Rooms and as direct messages.

#### Requirements
The Sleekxmpp - Library needs to be installed on your System
```bash
pip3 install -r intelmq/bots/collectors/xmpp/REQUIREMENTS.txt
```

#### Configuration Parameters:

- `xmpp_user` : The username of the XMPP-Account the output shall use (part before the @ sign)
- `xmpp_server` : The domain name of the server of the XMPP-Account (part after the @ sign)
- `xmpp_password` : The password of the XMPP-Account
- `xmpp_to_user` : The username of the receiver
- `xmpp_to_server` : The domain name of the receiver
- `xmpp_room` : The room which has to be joined by the output (full address a@conference.b.com)
- `xmpp_room_nick` : The username / nickname the output shall use within the room.
- `xmpp_room_password` : The password which might be required to join a room
- `use_muc` : If this parameter is `true`, the bot will join the room `xmpp_room`.
- `ca_certs` : A path to a file containing the CA's which should be used
