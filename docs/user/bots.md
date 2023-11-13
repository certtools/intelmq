<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Bots Inventory

This document contains complete reference of bots implemented by IntelMQ and how to configure them from the users perspective (meaning via IntelMQ Manager). Some of the bots are intended for general use and some of them are for processing particular data sources.

## Individual Bot Configuration

Each bot has it's own configuration. The configuration consists of two types of parameters:

- **Generic parameters** that are common to all the bots and need to be set for each bot.
  
- **Runtime parameters** are needed by the bot itself during runtime. Some of these parameters can be inherited from the [global configuration](../admin/configuration/intelmq.md#runtimeyaml) (which is applied to all the bots), but can be overridden in the individual bot configuration.

## Generic Parameters

These parameters must be set for each bot (at least the required ones).

### `id`

(required, string) This must be a unique identifier. Commonly it looks something like this: `abusech-feodo-tracker-collector`. It is safer to avoid using spaces.

### `name`

(required, string) Human readable name of the bot.

### `description`

(required, string) The description of the bot.

### `module`

(required, string) The executable (should be in `PATH` environment variable) which will be started.

### `group`

(optional, string) The group of the bot. Can be `Collector`, `Parser`, `Expert` or `Output`. Only used for visualization by other tools.

### `enabled`

(optional, boolean) Whether the bot will start when the whole botnet is started. You can still start a disabled bot explicitly. Defaults to `true`.

### `run_mode`

(optional, string) There are two run modes, `continuous` or `scheduled`. In the first case, the bot will be running
forever until stopped or exits because of errors (depending on the configuration). In the latter case, the bot will stop
after one successful run. This is especially useful when scheduling bots via cron or systemd.
Check [Configuration](../admin/configuration/intelmq.md) section for more details. Defaults to `continuous`.

## HTTP Parameters

Common HTTP runtime parameters used in multiple bots.

### `http_timeout_sec`

(optional, float) A tuple of floats or only one float describing the timeout (seconds) of the HTTP connection. Can be a
tuple of two floats (read and connect timeout) or just one float (applies for both timeouts). See
also <https://requests.readthedocs.io/en/master/user/advanced/#timeouts>. Defaults to 30.

### `http_timeout_max_tries`

(optional, integer) An integer depicting how many times a connection is retried, when a timeout occurred. Defaults to 3.

### `http_username`

(optional, string) Username for basic HTTP authentication.

### `http_password`

(optional, string) Password for basic HTTP authentication.

### `http_proxy`

(optional, string) Proxy to use for HTTP.

### `https_proxy`

(optional, string) Proxy to use for HTTPS.

### `http_user_agent`

(optional, string) User-Agent to be used for HTTP requests.

### `http_verify_cert`

(optional, boolean/string) Path to trusted CA bundle or directory, `false` to ignore verifying SSL certificates,
or `true` to verify SSL certificates. Defaults to `true`.

### `ssl_client_certificate`

(optional, string) Path to client certificate to use for TLS connections.

### `ssl_ca_certificate`

(optional, string) Path to trusted CA certificate. Only used by some bots.

## Cache Parameters

Common Redis cache runtime parameters used in multiple bots (mainly lookup experts).

### `redis_cache_host`

(required, string) Hostname of the Redis database.

### `redis_cache_port`

(required, string) Port of the Redis database.

### `redis_cache_db`

(required, integer) Database number.

### `redis_cache_ttl`

(required, integer) TTL used for caching.

### `redis_cache_password`

(optional, string) Password for the Redis database.

## Collector Bots

Multihreading is disabled for all Collectors, as this would lead to duplicated data.

### Feed Parameters

These runtime parameters must be set for each collector bot (at least the required ones).

#### `name`

(required, string) Name of the feed ([feed.name](<>)).

#### `accuracy`

(optional, float) Accuracy of the data from the feed ([feed.accuracy](<>)).

#### `code`

(optional, string) Code for the feed ([feed.code](<>)).

#### `documentation`

(optional, string) Link to documentation for the feed ([feed.documentation](<>)).

#### `provider`

(optional, string) Name of the provider of the feed ([feed.provider](<>)).

#### `rate_limit`

(optional, integer) Time interval (in seconds) between fetching data if applicable. Defaults to 0.

### Alien Vault OTX <div id="intelmq.bots.collectors.alienvault_otx.collector" />

Collects report messages from Alien Vault OTX.

**Module:** `intelmq.bots.collectors.alienvault_otx.collector`

**Requirements**

Install the library from GitHub, as there is no package in PyPi:

```bash
pip3 install -r intelmq/bots/collectors/alienvault_otx/REQUIREMENTS.txt
```

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`api_key`**

(required, string) API Key

**`modified_pulses_only`**

(optional, boolean) Whether to get only modified pulses instead of all. Defaults to false.

**`interval`**

(optional, integer) When `modified_pulses_only` is set, define the time in hours (integer value) to get modified pulses
since then. Defaults to 24 (hours).

---

### AMQP <div id="intelmq.bots.collectors.amqp.collector_amqp" />

This bot collects data from (remote) AMQP servers, for both IntelMQ as well as external data. Currently only fetching
from a queue is supported can be extended in the future. Messages will be acknowledge at AMQP after it is sent to the
pipeline. Requires the [pika](https://pypi.org/project/pika/) library, minimum version 1.0.0.

**Module:** `intelmq.bots.collectors.amqp.collector_amqp`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`connection_host`**

(optional, string) Hostname of the AMQP server. Defaults to 127.0.0.1.

**`connection_port`**

(optional, integer) Port of the AMQP server. Defaults to 5672.

**`connection_attempts`**

(optional, integer) The number of connection attempts to the defined server. Defaults to 3.

**`connection_heartbeat`**

(optional, integer) Heartbeat to server (seconds). Defaults to 3600.

**`connection_vhost`**

(optional, string) Virtual host to connect, on an HTTP(S) connection would be <http:/IP/><your virtual host>.

**`expect_intelmq_message`**

(optional, boolean) This parameter denotes whether the the data is from IntelMQ or not. If true, then the data can be
any Report or Event and will be passed to the next bot as is. Otherwise a new Report is created with the raw data.
Defaults to false.

**`queue_name`**

(optional, string) The name of the queue to fetch the data from.

**`username`**

(optional, string) Username for authentication to the AMQP server.

**`password`**

(optional, string) Password for authentication to the AMQP server.

**`use_ssl`**

(optional, boolean) Use of TLS for the connection. Make sure to also set the correct port. Defaults to false.

---

### API <div id="intelmq.bots.collectors.api.collector" />

This bot collects data from HTTP or Socket REST API. The API is available at `/intelmq/push` when the HTTP interface is
used. Requires the [tornado](https://pypi.org/project/tornado/) library.

**Module:** `intelmq.bots.collectors.api.collector`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`port`**

(optional, integer) The local port at which the API is available. Defaults to 5000.

**`use_socket`**

(optional, boolean) If true, the socket will be opened at the location given with `socket_path`. Defaults to false.

**`socket_path`**

(optional, string) Location of the socket. Defaults to `/tmp/imq_api_default_socket`.

---

### Generic URL Fetcher <div id="intelmq.bots.collectors.http.collector_http" />

This bot collects data from remote hosts using HTTP protocol. If the HTTP response' status code is not 2xx, this is
treated as error. In Debug logging level, the request's and response's headers and body are logged for further
inspection.

**Module:** `intelmq.bots.collectors.http.collector_http`

**Parameters (also expects [feed parameters](#feed-parameters) and [HTTP parameters](#http-parameters)):**

**`http_url`**

(required, string) Location of the resource to download.

**`http_url_formatting`**

(optional, boolean/object) When true, `{time[format]}` will be replaced by the current time in local timezone formatted
by the given format. E.g. if the URL is `http://localhost/{time[%Y]}`, then the resulting URL is `http://localhost/2019`
for the year 2019. (
Python's [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec) is used for
this.). You may use a JSON specifying [time-delta](https://docs.python.org/3/library/datetime.html#datetime.timedelta)
parameters to shift the current time accordingly. For example use `days: -1` for the yesterday's date; the
URL `http://localhost/{time[%Y-%m-%d]}` will get translated to `http://localhost/2018-12-31` for the 1st Jan of 2019.
Defaults to false.

**`extract_files`**

(optional, boolean/array of strings) If true, the retrieved (compressed) file or archived will be uncompressed/unpacked
and the files are extracted. If the parameter is a list of strings, only the files matching the filenames are extracted.
Extraction handles gzipped files and both compressed and uncompressed tar-archives as well as zip archives. For
extracted files, every extracted file is sent in it's own report. Every report has a field named `extra.file_name` with
the file name in the archive the content was extracted from. Defaults to false.

**`verify_pgp_signatures`**

(optional, boolean) When true, signature file is downloaded and report file is checked. On error (missing signature,
mismatch, ...), the error is logged and the report is not processed. Public key has to be imported in local keyring.
This requires the [python-gnupg](https://pypi.org/project/python-gnupg/) library. Defaults to false.

**`signature_url`**

(optional, string) Location of the signature file for the downloaded content.

**`signature_url_formatting`**

(optional, boolean/object) Same as `http_url_formatting`. Defaults to false.

**`gpg_keyring`**

(optional, string) If specified, the string represents path to keyring file. Otherwise the PGP keyring file of the
current `intelmq` user is used.

---

### Generic URL Stream Fetcher <div id="intelmq.bots.collectors.http.collector_http_stream" />

Opens a streaming connection to the URL and collects the received lines.

If the stream is interrupted, the connection will be aborted using the timeout parameter. No error will be logged if the
number of consecutive connection fails does not reach the parameter `error_max_retries`. Instead of errors, an INFO
message is logged. This is a measurement against too frequent ERROR logging messages. The consecutive connection fails
are reset if a data line has been successfully transferred. If the consecutive connection fails reaches the
parameter `error_max_retries`, an exception will be thrown and `rate_limit` applies, if not null.

**Module:** `intelmq.bots.collectors.http.collector_http_stream`

**Parameters (also expects [feed parameters](#feed-parameters) and [HTTP parameters](#http-parameters)):**

Uses the same parameters as [Generic URL Fetcher](#intelmq.bots.collectors.http.collector_http). The
parameter `http_timeout_max_tries` is of no use in this collector.

**`strip_lines`**

(optional, boolean) Whether the single lines should be stripped (removing whitespace from the beginning and the end of
the line) or not. Defaults to true.

---

### Generic Mail URL Fetcher <div id="intelmq.bots.collectors.mail.collector_mail_url" />

Extracts URLs from e-mail messages and downloads the content from the URLs.

The resulting reports contain the following special fields:

- `feed.url`: The URL the data was downloaded from.
- `extra.email_date`: The content of the email's `Date` header.
- `extra.email_subject`: The subject of the email.
- `extra.email_from`: The email's from address.
- `extra.email_message_id`: The email's message ID.
- `extra.file_name`: The file name of the downloaded file (extracted from the HTTP Response Headers if possible).

**Chunking**

For line-based inputs the bot can split up large reports into smaller chunks. This is particularly important for setups
that use Redis as a message queue which has a per-message size limitation of 512 MB. To configure chunking,
set `chunk_size` to a value in bytes. `chunk_replicate_header` determines whether the header line should be repeated for
each chunk that is passed on to a parser bot. Specifically, to configure a large file input to work around Redis size
limitation set `chunk_size` to something like 384000000 (~384 MB).

**Module:** `intelmq.bots.collectors.mail.collector_mail_url`

**Parameters (also expects [feed parameters](#feed-parameters) and [HTTP parameters](#http-parameters)):**

**`mail_host`**

(required, string) Hostname of the mail server.

**`mail_port`**

(optional, integer) IMAP server port: 143 without TLS, 993 with TLS. Defaults to 143.

**`mail_user`**

(required, string) Username of the email account.

**`mail_password`**

(required, string) Password associated with the user account.

**`mail_ssl`**

(optional, boolean) Whether the mail server uses TLS or not. Defaults to true.

**`folder`**

(optional, string) Folder in which to look for e-mail messages. Defaults to INBOX.

**`subject_regex`**

(optional, string) Regular expression to look for in the e-mail subject.

**`url_regex`**

(optional, string) Regular expression of the feed URL to look for in the e-mail body.

**`sent_from`**

(optional, string) Filter messages by the sender.

**`sent_to`**

(optional, string) Filter messages by the recipient.

**`ssl_ca_certificate`**

(optional, string) Path to trusted CA certificate. Applies only to IMAP connections, not HTTP. If the provided
certificate is not found, the IMAP connection will fail on handshake. Defaults to no certificate.

---

### Generic Mail Attachment Fetcher <div id="intelmq.bots.collectors.mail.collector_mail_attach" />

This bot collects messages from mailboxes and downloads the attachments.

The resulting reports contains the following special fields:

- `extra.email_date`: The content of the email's `Date` header
- `extra.email_subject`: The subject of the email
- `extra.email_from`: The email's from address
- `extra.email_message_id`: The email's message ID
- `extra.file_name`: The file name of the attachment or the file name in the attached archive if attachment is to
  uncompress.

**Module:** `intelmq.bots.collectors.mail.collector_mail_attach`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`mail_host`**

(required, string) Hostname of the mail server.

**`mail_port`**

(optional, integer) IMAP server port: 143 without TLS, 993 with TLS. Defaults to 143.

**`mail_user`**

(required, string) Username of the email account.

**`mail_password`**

(required, string) Password associated with the user account.

**`mail_ssl`**

(optional, boolean) Whether the mail server uses TLS or not. Defaults to true.

**`folder`**

(optional, string) Folder in which to look for e-mail messages. Defaults to INBOX.

**`subject_regex`**

(optional, string) Regular expression to look for in the e-mail subject.

**`attach_regex`**

(optional, string) Regular expression of the name of the attachment. Defaults to csv.zip.

**`extract_files`**

(optional, boolean) Whether to extract compress files from the attachment. Defaults to true.

**`sent_from`**

(optional, string) Only process messages sent from this address. Defaults to null (any sender).

**`sent_to`**

(optional, string) Only process messages sent to this address. Defaults to null (any recipient).

**`ssl_ca_certificate`**

(optional, string) Path to trusted CA certificate. Applies only to IMAP connections, not HTTP. If the provided
certificate is not found, the IMAP connection will fail on handshake. By default, no certificate is used.

---

### Generic Mail Body Fetcher <div id="intelmq.bots.collectors.mail.collector_mail_body" />

This bot collect messages from mailboxes, forwards the bodies as reports. Each non-empty body with the matching content
type is sent as individual report.

The resulting reports contains the following special fields:

- `extra.email_date`: The content of the email's `Date` header
- `extra.email_subject`: The subject of the email
- `extra.email_from`: The email's from address
- `extra.email_message_id`: The email's message ID

**Module:** `intelmq.bots.collectors.mail.collector_mail_body`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`mail_host`**

(required, string) Hostname of the mail server.

**`mail_port`**

(optional, integer) IMAP server port: 143 without TLS, 993 with TLS. Defaults to 143.

**`mail_user`**

(required, string) Username of the email account.

**`mail_password`**

(required, string) Password associated with the user account.

**`mail_ssl`**

(optional, boolean) Whether the mail server uses TLS or not. Defaults to true.

**`folder`**

(optional, string) Folder in which to look for e-mail messages. Defaults to INBOX.

**`subject_regex`**

(optional, string) Regular expression to look for in the e-mail subject.

**`url_regex`**

(optional, string) Regular expression of the feed URL to look for in the e-mail body.

**`sent_from`**

(optional, string) Filter messages by the sender.

**`sent_to`**

(optional, string) Filter messages by the recipient.

**`ssl_ca_certificate`**

(optional, string) Path to trusted CA certificate. Applies only to IMAP connections, not HTTP. If the provided
certificate is not found, the IMAP connection will fail on handshake. Defaults to no certificate.

**`content_types`**

(optional, boolean/array of strings) Which bodies to use based on the content_type. Defaults to `true` (same
as `['html', 'plain']`) for all:

- string with comma separated values, e.g. `['html', 'plain']`
- `true`, `false`, `null`: Same as default value - `string`, e.g. `plain`

---

### Github API <div id="intelmq.bots.collectors.github_api.collector_github_contents_api" />

Collects files matched by regular expression from GitHub repository via the GitHub API. Optionally with GitHub
credentials, which are used as the Basic HTTP authentication.

**Workflow**

The optional authentication parameters provide a high limit of the GitHub API requests. With the git hub user
authentication, the requests are rate limited to 5000 per hour, otherwise to 60 requests per hour.

The collector recursively searches for `regex`-defined files in the provided `repository`. Additionally it adds extra
file metadata defined by the `extra_fields`.

The bot always sets the url, from which downloaded the file, as `feed.url`.

**Module:** `intelmq.bots.collectors.github_api.collector_github_contents_api`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`personal_access_token`**

(required, string) GitHub account personal access
token [GitHub documentation: Creating a personal access token](<https://developer.github.com/changes/2020-02-14-deprecating-password-auth/#removal>)

**`repository`**

(required, string) GitHub target repository (`<USER>/<REPOSITORY>`)

**`regex`**

(optional, string) Valid regular expression of target files within the repository. Defaults to `.*.json`.

**`extra_fields`**

(optional, array of strings) Comma-separated list of extra fields
from [GitHub contents API](https://developer.github.com/v3/repos/contents/).

---

### File <div id="intelmq.bots.collectors.file.collector_file" />

This bot is capable of reading files from the local file-system. This is handy for testing purposes, or when you need to
react to spontaneous events. In combination with the Generic CSV parser this should work great.

The resulting reports contains the following special fields:

- `feed.url`: The URI using the `file://` scheme and localhost, with the full path to the processed file.
- `extra.file_name`: The file name (without path) of the processed file.

**Chunking**

Additionally, for line-based inputs the bot can split up large reports into smaller chunks.

This is particularly important for setups that use Redis as a message queue which has a per-message size limitation of
512 MB.

To configure chunking, set `chunk_size` to a value in bytes. `chunk_replicate_header` determines whether the header line
should be repeated for each chunk that is passed on to a parser bot.

Specifically, to configure a large file input to work around Redis' size limitation set `chunk_size` to something like
384000, i.e., ~384 MB.

**Workflow**

The bot loops over all files in `path` and tests if their file name matches *postfix, e.g. `*.csv`. If yes, the file
will be read and inserted into the queue.

If `delete_file` is set, the file will be deleted after processing. If deletion is not possible, the bot will stop.

To prevent data loss, the bot also stops when no `postfix` is set and `delete_file` was set. This cannot be overridden.

The bot always sets the file name as `feed.url`.

**Module:** `intelmq.bots.collectors.file.collector_file`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`path`**

(required, string) Path to file.

**`postfix`**

(required, string) The postfix (file ending) of the files to look for. For example [.csv].

**`delete_file`**

(optional, boolean) Whether to delete the file after reading. Defaults to false.

---

### FireEye <div id="intelmq.bots.collectors.fireeye.collector_mas" />

This bot is capable of collecting hashes and URLs from a FireEye MAS appliance.

The Python library `xmltodict` is required to run this bot.

**Workflow**

The bot collects all alerts which occurred during specified duration. After this we make a second call and check if
there is additional information like domains and hashes available. After collecting the openioc data we send this
information to the Fireeye parser.

**Module:** `intelmq.bots.collectors.fireeye.collector_fireeye`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`host`**

(required, string) DNS name of the target appliance.

**`request_duration`**

(required, string) Allowed values: `24_hours` or `48_hours`. Length of the query in past eg. collect alerts from last 24hours/48hours.

**`http_username`**

(required, string) Password for authentication.

**`http_password`**

(required, string) Username for authentication.

---

### Kafka <div id="intelmq.bots.collectors.kafka.collector" />

Requires the [kafka python library](https://pypi.org/project/kafka/).

**Module:** `intelmq.bots.collectors.kafka.collector`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`topic`**

(required, string) Kafka topic the collector should get messages from.

**`bootstrap_servers`**

(required, string) Kafka server(s) and port the collector should connect to. Defaults to `localhost:9092`

**`ssl_check_hostname`**

(optional, boolean) Whether to verify TLS certificates. Defaults to true.

**`ssl_client_certificate`**

(optional, string) Path to client certificate to use for TLS connections.

**`ssl_ca_certificate`**

(optional, string) Path to trusted CA certificate.

---

### MISP Generic <div id="intelmq.bots.collectors.misp.collector" />

Collects messages from [MISP](https://github.com/MISP), a malware information sharing platform server.

**Workflow**

This collector will search for events on a MISP server that have a [to_process] tag attached to them (see
the [misp_tag_to_process] parameter) and collect them for processing by IntelMQ. Once the MISP event has been processed
the [to_process] tag is removed from the MISP event and a [processed] tag is then attached (see the [misp_tag_processed]
parameter).

**NB.** The MISP tags must be configured to be 'exportable' otherwise they will not be retrieved by the collector.

**Module:** `intelmq.bots.collectors.misp.collector`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`misp_url`**

(required, string) URL of MISP server (with trailing '/').

**`misp_key`**

(required, string) MISP Authkey.

**`misp_tag_to_process`**

(required, string) MISP tag for events to be processed.

**`misp_tag_processed`**

(optional, string) MISP tag for processed events.

**`http_verify_cert`**

(optional, boolean) Verify the TLS certificate of the server. Defaults to true.

---

### Request Tracker <div id="intelmq.bots.collectors.rt.collector_rt" />

Request Tracker Collector fetches attachments from an RTIR instance.

This rt bot will connect to RT and inspect the given `search_queue` for tickets matching all criteria in `search_*`, Any
matches will be inspected. For each match, all (RT-) attachments of the matching RT tickets are iterated over and within
this loop, the first matching filename in the attachment is processed. If none of the filename matches apply, the
contents of the first (RT-) "history" item is matched against the regular expression for the URL (`url_regex`).

The parameter `http_timeout_max_tries` is of no use in this collector.

**Search**

The parameters prefixed with `search_` allow configuring the ticket search.

Empty strings and null as value for search parameters are ignored.

**File downloads**

Attachments can be optionally unzipped, remote files are downloaded with the `http_*` settings applied.

If `url_regex` or `attachment_regex` are empty strings, false or null, they are ignored.

**Ticket processing**

Optionally, the RT bot can "take" RT tickets (i.e. the `user` is assigned this ticket now) and/or the status can be changed (leave `set_status` empty in case you don't want to change the status). Please note however that you **MUST** do one of the following: either "take" the ticket or set the status (`set_status`). Otherwise, the search will find the ticket every time and get stuck in an endless loop.

In case a resource needs to be fetched and this resource is permanently not available (status code is 4xx), the ticket
status will be set according to the configuration to avoid processing the ticket over and over. For temporary failures
the status is not modified, instead the ticket will be skipped in this run.

**Time search**

To find only tickets newer than a given absolute or relative time, you can use the `search_not_older_than` parameter. Absolute time specification can be anything parseable by dateutil, best use a ISO format.

Relative must be in this format: `[NUMBER] [TIMESPAN]s`, e.g. `3 days`. Timespan can be hour, day, week, month or year. Trailing 's' is supported for all timespans. Relative times are subtracted from the current time directly before the search is performed.

The resulting reports contains the following special fields:

- `rtir_id`: The ticket ID
- `extra.email_subject` and `extra.ticket_subject`: The subject of the ticket
- `extra.email_from` and `extra.ticket_requestors`: Comma separated list of the ticket's requestor's email addresses.
- `extra.ticket_owner`: The ticket's owner name
- `extra.ticket_status`: The ticket's status
- `extra.ticket_queue`: The ticket's queue
- `extra.file_name`: The name of the extracted file, the name of the downloaded file or the attachments' filename without `.gz` postfix.
- `time.observation`: The creation time of the ticket or attachment.

**Requirements**

You need the rt-library >= 1.9 and < 3.0 from from nic.cz, available via [pypi](https://pypi.org/project/rt/): `pip3 install rt<3`

**Module:** `intelmq.bots.collectors.rt.collector_rt`

**Parameters (also expects [feed parameters](#feed-parameters) and [HTTP parameters](#http-parameters)):**

**`extract_attachment`**

(optional, boolean/array of strings) See documentation of the Generic URL Fetcher parameter `extract_files` for more details.

**`extract_download`**

(optional, boolean/array of strings) See documentation of the Generic URL Fetcher parameter `extract_files` for more details.

**`uri`**

(optional, string) URL of the REST interface of the RT. Defaults to `http://localhost/rt/REST/1.0`.

**`user`**

(optional, string) RT username. Defaults to intelmq.

**`password`**

(optional, string) RT password. Defaults to password.

**`search_not_older_than`**

(optional, string) Absolute time (use ISO format) or relative time, e.g. `3 days`.

**`search_owner`**

(optional, string) Owner of the ticket to search for. Defaults to nobody.

**`search_queue`**

(optional, string) Queue of the ticket to search for. Defaults to Incident Reports.

**`search_requestor`**

(optional, string) E-mail address of the requestor.

**`search_status`**

(optional, string) Status of the ticket to search for. Defaults to new.

**`search_subject_like`**

(optional, string/array of strings) Part of the subject of the ticket to search for. Defaults to "Report".


**`search_subject_notlike`**

(optional, string/array of strings) Exclude subject containing given value, use list for multiple excluding values.

**`set_status`**

(optional, string) Status to set the ticket to after processing. Use false or null to keep current status. Defaults to open.

**`take_ticket`**

(optional, boolean) Whether to take the ticket. Defaults to true.

**`url_regex`**

(optional, string) Regular expression of an URL to search for in the ticket. Defaults to `https://dl.shadowserver.org/[a-zA-Z0-9?_-]*`.

**`attachment_regex`**

(optional, string) Eegular expression of an attachment in the ticket. Defaults to `\.csv\.zip$`.

---

### Rsync <div id="intelmq.bots.collectors.rsync.collector_rsync" />

This bot downloads a file via rsync and then load data from downloaded file. Downloaded file is located in
`var/lib/bots/rsync_collector`.

Requires the rsync executable.

**Module:** `intelmq.bots.collectors.rsync.collector_rsync`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`file`**

(required, string) The filename to process, combined with `rsync_path`.

**`rsync_path`**

(required, string) Path to the directory of the file. Allowed values are local directory (such as `/home/username/`) or remote directory (such as `<username@remote_host>:/home/username/directory`).

**`rsync_file_path_formatting`**

(optional, boolean) Whether the file and rsync_path should be formatted by the given format. E.g. if the path is `/path/to_file/{time[%Y]}`, then the resulting path is `/path/to/file/2023` for the year 2023. (Python's `Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>`_ is used for this.). You may use a `JSON` specifying `time-delta <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`_ parameters to shift the current time accordingly. For example use `{"days": -1}` for the yesterday's date; the path `/path/to/file/{time[%Y-%m-%d]}` will get translated to "/path/to/file/2018-12-31" for the 1st Jan of 2023. Defaults to false.

**`extra_params`**

(optional, array of strings) A list of extra parameters to pass to rsync.

**`private_key`**

(optional, string) Private key to use for rsync authentication.

**`private_key_path`**

(optional, string) Path to private key to use for rsync authentication. Use `private_key` or `private_key_path`, not both.

**`strict_host_key_checking`**

(optional, boolean) Whether the host key should be checked. Defaults to false.

**`temp_directory`**

(optional, string) The temporary directory for rsync to use for collected files. Defaults to `/opt/intelmq/var/run/{BOT-ID}` or `/var/run/intelmq/{BOT-ID}`.

---

### Shadowserver Reports API <div id="intelmq.bots.collectors.shadowserver.collector_reports_api" />

Connects to the [Shadowserver API](https://www.shadowserver.org/what-we-do/network-reporting/api-documentation/),
requests a list of all the reports for a specific country and processes the ones that are new.

The Cache is required to memorize which files have already been processed (TTL needs to be high enough to cover the
oldest files available!).

The resulting reports contain the following special field:

- `extra.file_name`: The name of the downloaded file, with fixed filename extension. The API returns file names with the
  extension `.csv`, although the files are JSON, not CSV. Therefore, for clarity and better error detection in the parser, the file name in `extra.file_name` uses `.json` as extension.

**Module:** `intelmq.bots.collectors.shadowserver.collector_reports_api`

**Parameters (also expects [feed parameters](#feed-parameters) and [cache parameters](#cache-parameters)):**

**`apikey`**

(required, string) Your Shadowserver API key.

**`secret`**

(required, string) Your Shadowserver API secret.

**`reports`**

(required, string/array of strings) An array of strings (or a list of comma-separated values) of the mailing lists you want to process.

**`types`**

(optional, string/array of strings) An array of strings (or a list of comma-separated values) with the names of report types you want to process. If you leave this empty, all the available reports will be downloaded and processed (i.e. 'scan', 'drones', 'intel', 'sandbox_connection', 'sinkhole_combined'). The possible report types are equivalent to the file names given in the section Supported Reports of the [Shadowserver parser](#intelmq.bots.parsers.shadowserver.parser).

**Sample configuration**

```yaml

  shadowserver-collector:
    description: Our bot responsible for getting reports from Shadowserver
    enabled: true
    group: Collector
    module: intelmq.bots.collectors.shadowserver.collector_reports_api
    name: Shadowserver_Collector
    parameters:
      destination_queues:
        _default: [shadowserver-parser-queue]
      file_format: csv
      api_key: "$API_KEY_received_from_the_shadowserver_foundation"
      secret: "$SECRET_received_from_the_shadowserver_foundation"
    run_mode: continuous

```

---

### Shodan Stream <div id="intelmq.bots.collectors.shodan.collector_stream" />

Queries the Shodan Streaming API.

Requires the shodan library to be installed:

- <https://github.com/achillean/shodan-python/>

- <https://pypi.org/project/shodan/>

**Module:** `intelmq.bots.collectors.shodan.collector_stream`

**Parameters (also expects [feed parameters](#feed-parameters) and [HTTP parameters](#http-parameters)):**

Only the proxy is used (requires `shodan-python > 1.8.1`). Certificate is always verified.

**`countries`**

() A list of countries to query for. If it is a string, it will be spit by `,`.

If the stream is interrupted, the connection will be aborted using the timeout parameter. No error will be logged if the
number of consecutive connection fails does not reach the parameter
`error_max_retries`. Instead of errors, an INFO message is logged. This is a measurement against too frequent ERROR
logging messages. The consecutive connection fails are reset if a data line has been successfully transferred. If the
consecutive connection fails reaches the parameter `error_max_retries`, an exception will be thrown and `rate_limit`
applies, if not null.

---

### TCP <div id="intelmq.bots.collectors.tcp.collector" />

TCP is the bot responsible to receive events on a TCP port (ex: from TCP Output of another IntelMQ instance). Might not
be working on Python 3.4.6.

**Response**

TCP collector just sends an "OK" message after every received message, this should not pose a problem for an arbitrary
input. If you intend to link two IntelMQ instance via TCP, have a look at the TCP output bot documentation.

**Module:** `intelmq.bots.collectors.tcp.collector`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`ip`**

(required, string) IP of the destination server.

**`port`**

(required, integer) Port of destination server.

---

### Blueliv Crimeserver <div id="intelmq.bots.collectors.blueliv.collector_crimeserver" />

Collects report messages from Blueliv API.

For more information visit <https://github.com/Blueliv/api-python-sdk>

**Module:** `intelmq.bots.collectors.blueliv.collector_crimeserver`

**Requirements**

Install the required library:

```bash
pip3 install -r intelmq/bots/collectors/blueliv/REQUIREMENTS.txt
```

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`api_key`**

(required, string) location of information resource, see <https://map.blueliv.com/?redirect=get-started#signup>

**`api_url`**

(optional, string) The optional API endpoint. Defaults to `https://freeapi.blueliv.com`.

---

### Calidog Certstream <div id="intelmq.bots.collectors.calidog.collector_certstream" />

A Bot to collect data from the Certificate Transparency Log (CTL). This bot works based on certstream library
(<https://github.com/CaliDog/certstream-python>)

**Module:** `intelmq.bots.collectors.calidog.collector_certstream`

**Parameters (also expects [feed parameters](#feed-parameters)):**

---

### ESET ETI <div id="intelmq.bots.collectors.eset.collector" />

Collects data from ESET ETI TAXII server.

For more information visit <https://www.eset.com/int/business/services/threat-intelligence/>.

**Module:** `intelmq.bots.collectors.eset.collector`

**Requirements**

Install the required `cabby` library:

```bash
pip3 install -r intelmq/bots/collectors/eset/REQUIREMENTS.txt
```

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`username`**

(required, string) Your username.

**`password`**

(required, string) Your password.

**`endpoint`**

(optional, string) Defaults to `eti.eset.com`.

**`time_delta`**

(optional, integer) The time (in seconds) span to look back. Default to 3600.

**`collection`**

(required, string) The collection to fetch.

---

### McAfee openDXL <div id="intelmq.bots.collectors.opendxl.collector" />

Collects messages via McAfee openDXL.

**Module:** `intelmq.bots.collectors.opendxl.collector`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`dxl_config_file`**

(required, string) Path to the the configuration file containing required information to connect.

**`dxl_topic`**

(optional, string) Name of the DXL topic to subscribe to. Defaults to `/mcafee/event/atd/file/report`.

---

### Microsoft Azure <div id="intelmq.bots.collectors.microsoft.collector_azure" />

Collects blobs from Microsoft Azure using their library.

Iterates over all blobs in all containers in an Azure storage. The Cache is required to memorize which files have
already been processed (TTL needs to be high enough to cover the oldest files available!).

This bot significantly changed in a backwards-incompatible way in IntelMQ Version 2.2.0 to support current versions of
the Microsoft Azure Python libraries. `azure-storage-blob>=12.0.0` is required.

**Module:** `intelmq.bots.collectors.microsoft.collector_azure`

**Parameters (also expects [feed parameters](#feed-parameters) and [cache parameters](#cache-parameters)):**

**`connection_string`**

(required, string) Connection string as given by Microsoft.

**`container_name`**

(required, string) Name of the container to connect to.

---

### Microsoft Interflow <div id="intelmq.bots.collectors.microsoft.collector_interflow" />

This bot collects files from Microsoft Interflow API.

Iterates over all files available by this API. Make sure to limit the files to be downloaded with the parameters,
otherwise you will get a lot of data! The cache is used to remember which files have already been downloaded. Make sure
the TTL is high enough, higher than `not_older_than`.

**Module:** `intelmq.bots.collectors.microsoft.collector_interflow`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`api_key`**

(required, string) API generated in their portal.

**`file_match`**

(optional, string) Regular expression to match file names.

**`not_older_than`**

(optional, integer/datetime) an optional relative (minutes) or absolute time (UTC is assumed) expression to determine
the oldest time of a file to be downloaded.

**`redis_cache_*` and especially `redis_cache_ttl`**

Settings for the cache where file names of downloaded files are saved. The cache's TTL must always be bigger than
`not_older_than`.

**Additional functionalities**

Files are automatically ungzipped if the filename ends with `.gz`.

---

### STOMP <div id="intelmq.bots.collectors.stomp.collector" />

Collects messages from a STOMP server.

**Module:** `intelmq.bots.collectors.stomp.collector`

**Requirements**

Install the `stomp.py` library from PyPI:

```bash
pip3 install -r intelmq/bots/collectors/stomp/REQUIREMENTS.txt
```

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`server`**

(required, string) Hostname of the STOMP server.

**`port`**

(optional, integer) Defaults to 61614.

**`exchange`**

(required, string) STOMP *destination* to subscribe to, e.g. "/exchange/my.org/*.*.*.*"

**`username`**

(optional, string) Username to use.

**`password`**

(optional, string) Password to use.

**`ssl_ca_certificate`**

(optional, string) Path to trusted CA certificate.

**`auth_by_ssl_client_certificate`**

(optional, boolean) Whether to authenticate using TLS certificate. (Set to false for new *n6* auth.) Defaults to true.

**`ssl_client_certificate`**

(optional, string) Path to client certificate to use for TLS connections.

**`ssl_client_certificate_key`**

(optional, string) Path to client private key to use for TLS connections.

---

### Twitter (REMOVE?) <div id="intelmq.bots.collectors.twitter.collector_twitter" />

Collects tweets.

Collects tweets from target_timelines. Up to tweet_count tweets from each user and up to timelimit back in time. The
tweet text is sent separately and if allowed, links to pastebin are followed and the text sent in a separate report

**Module:** `intelmq.bots.collectors.twitter.collector_twitter`

**Parameters (also expects [feed parameters](#feed-parameters)):**

**`target_timelines`**

() screen_names of twitter accounts to be followed

**`tweet_count`**

() number of tweets to be taken from each account

**`timelimit`**

() maximum age of the tweets collected in seconds

**`follow_urls`**

() list of screen_names for which URLs will be followed

**`exclude_replies`**

() exclude replies of the followed screen_names

**`include_rts`**

() whether to include retweets by given screen_name

**`consumer_key`**

() Twitter API login data

**`consumer_secret`**

() Twitter API login data

**`access_token_key`**

() Twitter API login data

**`access_token_secret`**

() Twitter API login data

## Parser Bots

### Common parameters

#### `default_fields`

(optional, object) Map of statically added fields to each event (only applied if parsing the event doesn't set the
value).

example usage:

```yaml
defaults_fields:
  classification.type: c2-server
  protocol.transport: tcp
```

---

### Abuse.ch Feodo Tracker <div id="intelmq.bots.parsers.abusech.parser_feodotracker" />

Parses data from Abuse.ch Feodo Tracker (JSON format).

**Module:** `intelmq.bots.parsers.abusech.parser_feodotracker`

No additional parameters.

---

### AlienVault API

Parses data from AlienVault API.

**Module:** `intelmq.bots.parsers.alienvault.parser`

No additional parameters.

---

### AlienVault OTX

Parses data from AlientVault Open Threat Exchange (OTX).

**Module:** `intelmq.bots.parsers.alienvault.parser_otx`

No additional parameters.

---

### AnubisNetworks Cyberfeed Stream <div id="intelmq.bots.parsers.anubisnetworks.parser" />

Parses data from AnubisNetworks Cyberfeed Stream.

The feed format changes over time. The parser supports at least data from 2016 and 2020.

Events with the Malware "TestSinkholingLoss" are ignored, as they are for the feed provider's internal purpose only and
should not be processed at all.

**Module:** `intelmq.bots.parsers.anubisnetworks.parser`

**Parameters:**

**`use_malware_family_as_classification_identifier`**

(optional, boolean) Use the `malw.family` field as `classification.type`. If false, check if the same
as `malw.variant`. If it is the same, it is ignored. Otherwise saved as `extra.malware.family`. Defaults to true.

---

### Bambenek <div id="intelmq.bots.parsers.bambenek.parser" />

Parses data from Bambenek DGA, Domain, and IP feeds.

**Module:** `intelmq.bots.parsers.bambenek.parser`

No additional parameters.

---

### Blocklist.de <div id="intelmq.bots.parsers.blocklistde.parser" />

Parses data from Blocklist.de feeds.

**Module:** `intelmq.bots.parsers.blocklistde.parser`

No additional parameters.

---

### Blueliv Crimeserver <div id="intelmq.bots.parsers.blueliv.parser_crimeserver" />

Parses data from Blueliv Crimeserver feed.

**Module:** `intelmq.bots.parsers.blueliv.parser_crimeserver`

No additional parameters.

---

### Calidog Certstream <div id="intelmq.bots.parsers.calidog.parser_certstream" />

Parses data from Certificate Transparency Log.

For each domain in the `leaf_cert.all_domains` object one event with the domain in `source.fqdn` (and `source.ip` as fallback) is produced. The seen-date is saved in `time.source` and the classification type is `other`.

**Module:** `intelmq.bots.parsers.calidog.parser_certstream`

No additional parameters.

---

### CERT-EU <div id="intelmq.bots.parsers.certeu.parser_csv" />

Parses data from CERT-EU feed (CSV).

**Module:** `intelmq.bots.parsers.certeu.parser_csv`

No additional parameters.

---

### CI Army <div id="intelmq.bots.parsers.ci_army.parser" />

Parses data from CI Army feed.

**Module:** `intelmq.bots.parsers.ci_army.parser`

No additional parameters.

---

### CleanMX <div id="intelmq.bots.parsers.cleanmx.parser" />

Parses data from CleanMX feed.

**Module:** `intelmq.bots.parsers.cleanmx.parser`

No additional parameters.

---

### Team Cymru CAP <div id="intelmq.bots.parsers.cymru.parser_cap_program" />

Parses data from Team Cymru's CSIRT Assistance Program (CAP) feed.

There are two different feeds available:

- `infected_$date.txt` ("old")
- `$certname_$date.txt` ("new")

The new will replace the old at some point in time, currently you need to fetch both. The parser handles both formats.

**Old feed**

As little information on the format is available, the mappings might not be correct in all cases. Some reports are not
implemented at all as there is no data available to check if the parsing is correct at all. If you do get errors
like `Report ... not implement` or similar please open an issue and report the (anonymized) example data. Thanks.

The information about the event could be better in many cases but as Cymru does not want to be associated with the
report, we can't add comments to the events in the parser, because then the source would be easily identifiable for the
recipient.

**Module:** `intelmq.bots.parsers.cymru.parser_cap_program`

No additional parameters.

---

### Team Cymru Full Bogons <div id="intelmq.bots.parsers.cymru.parser_full_bogons" />

Parses data from full bogons feed.

<http://www.team-cymru.com/bogon-reference.html>

**Module:** `intelmq.bots.parsers.cymru.parser_full_bogons`

No additional parameters.

---

### CZ.NIC HaaS <div id="intelmq.bots.parsers.cznic.parser_haas" />

Parses data from CZ.NIC Honeypot as a service (HaaS) feed.

**Module:** `intelmq.bots.parsers.cznic.parser_haas`

No additional parameters.

---

### CZ.NIC PROKI <div id="intelmq.bots.parsers.cznic.parser_proki" />

Parses data from CZ.NIC PROKI API.

**Module:** `intelmq.bots.parsers.cznic.parser_proki`

No additional parameters.

---

### Danger Rulez <div id="intelmq.bots.parsers.danger_rulez.parser" />

Parses data from Danger Rulez SSH blocklist.

**Module:** `intelmq.bots.parsers.danger_rulez.parser`

No additional parameters.

---

### Dataplane <div id="intelmq.bots.parsers.dataplane.parser" />

Parses data from Dataplane feed.

**Module:** `intelmq.bots.parsers.dataplane.parser`

No additional parameters.

---

### DShield ASN <div id="intelmq.bots.parsers.dshield.parser_asn" />

Parses data from DShield ASN feed.

**Module:** `intelmq.bots.parsers.dshield.parser_asn`

No additional parameters.

---

### DShield Block <div id="intelmq.bots.parsers.dshield.parser_block" />

Parses data from DShield Block feed.

**Module:** `intelmq.bots.parsers.dshield_parser_block`

No additional parameters.

---

### ESET <div id="intelmq.bots.parsers.eset.parser" />

Parses data from ESET ETI TAXII server.

Supported collections:

- "ei.urls (json)"
- "ei.domains v2 (json)"

**Module:** `intelmq.bots.parsers.eset.parser`

No additional parameters.

---

### Dyn (TODO)

---

### FireEye <div id="intelmq.bots.parsers.fireeye.parser" />

Parses data from FireEye MAS appliance.

**Module:** `intelmq.bots.parsers.fireeye.parser`

No additional parameters.

---

### Fraunhofer DGA <div id="intelmq.bots.parsers.fraunhofer.parser_dga" />

Parses data from Fraunhofer DGA feed.

**Module:** `intelmq.bots.parsers.fraunhofer.parser_dga`

No additional parameters.

---

### Generic CSV <div id="intelmq.bots.parsers.generic.parser_csv" />

Parses CSV data.

Lines starting with `#` are skipped. Headers won't be interpreted.

**Module:** `intelmq.bots.parsers.generic.parser_csv`

**Parameters**

**`columns`**

(required, string/array of strings) A list of strings or a string of comma-separated values with field names. The names
must match the IntelMQ Data Format field names. Empty column specifications and columns named `__IGNORE__` are ignored.
E.g.

```yaml
columns:
  - "source.ip"
  - "source.fqdn"
  - "extra.http_host_header"
  - "__IGNORE__"
```

is equivalent to:

```yaml
columns: "source.ip,source.fqdn,extra.http_host_header,__IGNORE__"
```

The fourth column is not used in this example.

It is possible to specify multiple columns using the `|` character. E.g.

```yaml
columns:
  - "source.url|source.fqdn|source.ip"
  - "source.fqdn"
  - "extra.http_host_header"
  - "__IGNORE__"
```

First, the bot will try to parse the value as URL, if it fails, it will try to parse it as FQDN, if that fails, it will
try to parse it as IP, if that fails, an error will be raised. Some use cases:

- Mixed data set, e.g. URL/FQDN/IP/NETMASK:

```yaml
columns:
  - "source.url|source.fqdn|source.ip|source.network"
```

- Parse a value and ignore if it fails:

```yaml
columns:
  - "source.url|__IGNORE__"
```

**`column_regex_search`**

(optional, object) A dictionary mapping field names (as given per the columns parameter) to regular expression. The
field is evaluated using `re.search`. Eg. to get the ASN out of `AS1234` use: `{"source.asn":
"[0-9]*"}`. Make sure to properly escape any backslashes in your regular expression (see also
this [issue](https://github.com/certtools/intelmq/issues/1579)).

**`compose_fields`**

(optional, object) Compose fields from multiple columns, e.g. with data like this:

```csv
# Host,Path
example.com,/foo/
example.net,/bar/
```

Using this parameter:

```yaml
compose_fields:
  source.url: "http://{0}{1}"
```

You get:

```
http://example.com/foo/
http://example.net/bar/
```

in the respective `source.url` fields. The value in the dictionary mapping is formatted whereas the columns are
available with their index.

**`default_url_protocol`**

(optional, string) For URLs you can give a default protocol which will be prepended to the data. Defaults to null.

**`delimiter`**

(optional, string) Character used for columns separation. Defaults to `,` (comma).

**`skip_header`**

(optional, boolean/integer) Whether to skip the first N lines of the input (True -> 1, False -> 0). Lines starting
with `#` will be skipped additionally, make sure you do not skip more lines than needed!

**`time_format`**

(optional, string) Allowed values: `timestamp`, `windows_nt` or `epoch_millis`. When `null` then fuzzy time parsing is
used. Defaults to null.

**`type`**

(optional, string) Set the `classification.type` statically. Deprecated in favour of [`default_fields`](#default_fields)
. Will be removed in IntelMQ 4.0.0.

**`data_type`**

(optional, object) Sets the data of specific type, currently only `json` is a supported value.

Example:

```yaml
columns:
  - source.ip
  - source.url
  - extra.tags
data_type:
  extra.tags: json
```

It will ensure that `extra.tags` is treated as JSON.

**`filter_text`**

(optional, string) Only process the lines containing or not containing specified text. It is expected to be used in
conjunction with `filter_type`.

**`filter_type`**

(optional, string) Allowed values: `whitelist` or `blacklist`. When `whitelist` is used, only lines containing the text
specified in `filter_text` option will be processed. When `blacklist` is used, only lines NOT containing the text will
be processed.

Example (processing ipset format files):

```yaml
filter_text: 'ipset add '
filter_type: whitelist
columns:
  - __IGNORE__
  - __IGNORE__
  - __IGNORE__
  - source.ip
```

**`type_translation`**

(optional, object) If the source does have a field with information for `classification.type`, but it does not
correspond to IntelMQ's types, you can map them to the correct ones. The `type_translation` field can hold a dictionary,
or a string with a JSON dictionary which maps the feed's values to IntelMQ's.

Example:

```yaml
type_translation:
  malware_download: "malware-distribution"
```

**`columns_required`**

(optional, array of booleans) An array of true/false for each column. By default, it is true for every column.

---

### Github Feed <div id="intelmq.bots.parsers.github_feed.parser" />

Parses data publicly available on GitHub (should receive from `github_api` collector).

**Module:** `intelmq.bots.parsers.github_feed.parser`

No additional parameters.

---

### Have I Been Pwned Callback <div id="intelmq.bots.parsers.hibp.parser_callback" />

Parsers data from the callback of Have I Been Pwned Enterprise Subscription.

Parses breaches and pastes and creates one event per e-mail address. The e-mail address is stored in `source.account`
. `classification.type` is `leak` and `classification.identifier` is `breach` or `paste`.

**Module:** `intelmq.bots.parsers.hibp.parser_callback`

No additional parameters.

---

### HTML Table <div id="intelmq.bots.parsers.html_table.parser" />

Parses tables in HTML documents.

**Module:** `intelmq.bots.parsers.html_table.parser`

**Parameters:**

(required, string/array of strings) A list of strings or a string of comma-separated values with field names. The names
must match the IntelMQ Data Format field names. Empty column specifications and columns named `__IGNORE__` are ignored.
E.g.

```yaml
columns:
  - "source.ip"
  - "source.fqdn"
  - "extra.http_host_header"
  - "__IGNORE__"
```

is equivalent to:

```yaml
columns: "source.ip,source.fqdn,extra.http_host_header,__IGNORE__"
```

The fourth column is not used in this example.

It is possible to specify multiple columns using the `|` character. E.g.

```yaml
columns:
  - "source.url|source.fqdn|source.ip"
  - "source.fqdn"
  - "extra.http_host_header"
  - "__IGNORE__"
```

First, the bot will try to parse the value as URL, if it fails, it will try to parse it as FQDN, if that fails, it will
try to parse it as IP, if that fails, an error will be raised. Some use cases:

- Mixed data set, e.g. URL/FQDN/IP/NETMASK:

```yaml
columns:
  - "source.url|source.fqdn|source.ip|source.network"
```

- Parse a value and ignore if it fails:

```yaml
columns:
  - "source.url|__IGNORE__"
```

**`ignore_values`**

(optional, string/array of strings) A list of strings or a string of comma-separated values which are ignored when
encountered.

Example:

```yaml
ignore_values:
  - ""
  - "unknown"
  - "Not listed"
```

The following configuration will lead to assigning all values to `malware.name` and `extra.SBL` except `unknown`
and `Not listed` respectively.

```yaml
columns:
  - source.url
  - malware.name
  - extra.SBL
ignore_values:
  - ''
  - unknown
  - Not listed
```

Parameters `columns` and `ignore_values` **must have same length!**

**`attribute_name`**

(optional, string) Filtering table with table attributes. To be used in conjunction with `attribute_value`. E.g. `class`, `id`, `style`.

**`attribute_value`**

(optional, string) To filter all tables with attribute `class='details'` use

```yaml
attribute_name: "class"
attribute_value: "details"
```

**`table_index`**

(optional, integer) Index of the table if multiple tables present. If `attribute_name` and `attribute_value` given,
index according to tables remaining after filtering with table attribute. Defaults to 0.

**`split_column`**

(optional, ) Padded column to be split to get values, to be used in conjunction with `split_separator` and `split_index`, optional.

**`split_separator`**

(optional, string) Delimiter string for padded column.

**`split_index`**

(optional, integer) Index of unpadded string in returned list from splitting `split_column` with `split_separator` as
delimiter string. Defaults to 0.

Example:

```yaml
split_column: "source.fqdn"
split_separator: " "
split_index: 1
```

With above configuration, column corresponding to `source.fqdn` with value `D lingvaworld.ru` will be assigned
as `source.fqdn: lingvaworld.ru`.

**`skip_table_head`**

(optional, boolean) Skip the first row of the table. Defaults to true.

**`default_url_protocol`**

(optional, string) For URLs you can give a default protocol which will be pretended to the data. Defaults to `http://`.

**`time_format`**

(optional, string) Allowed values: `timestamp`, `windows_nt` or `epoch_millis`. When `null` then fuzzy time parsing is
used. Defaults to null.

**`html_parser`**

(optional, string) The HTML parser to use. Allowed values: `html.parser` or `lxml` (see
also <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>). Defaults to `html.parser`.

---

### JSON (TODO) <div id="intelmq.bots.parsers.json.parser" />

TODO

**Module:** `intelmq.bots.parsers.json.parser`

---

### Key=Value Parser <div id="intelmq.bots.parsers.key_value.parser" />

Parses text lines in key=value format, for example FortiGate firewall logs.

**Parsing limitations**

The input must not have (quoted) occurrences of the separator in the values. For example, this is not parsable (with
space as separator):

```
key="long value" key2="other value"
```

In firewall logs like FortiGate, this does not occur. These logs usually look like:

```
srcip=192.0.2.1 srcmac="00:00:5e:00:17:17"
```

**Module:** `intelmq.bots.parsers.key_value.parser`

**Parameters:**

**`pair_separator`**

(optional, string) String separating key=value pairs. Defaults to space.

**`kv_separator`**

(optional, string) String separating the key and the value. Defaults to `=`.

**`keys`**

(optional, object) Mapping of original key names to IntelMQ Data Format.

Example:

```yaml
keys:
  srcip: source.ip
  dstip: destination.ip
```

The value mapped to `time.source` is parsed. If the value is numeric, it is interpreted. Otherwise, or if it fails, it
is parsed fuzzy with dateutil. If the value cannot be parsed, a warning is logged per line.

**`strip_quotes`**

(optional, boolean) Whether to remove opening and closing quotes from values. Defaults to true.

---

### MalwarePatrol <div id="intelmq.bots.parsers.malwarepatrol.parser_dansguardian" />

Parses data from MalwarePatrol feed.

**Module:** `intelmq.bots.parsers.malwarepatrol.parser_dansguardian`

No additional parameters.

---

### MalwareURL <div id="intelmq.bots.parsers.malwareurl.parser" />

Parses data from MalwareURL feed.

**Module:** `intelmq.bots.parsers.malwareurl.parser`

No additional parameters.

---

### McAfee Advanced Threat Defense File <div id="intelmq.bots.parsers.mcafee.parser_atd" />

Parse IoCs from McAfee Advanced Threat Defense reports (hash, IP, URL).

**Module:** `intelmq.bots.parsers.mcafee.parser_atd`

**Parameters:**

**`verdict_severity`**

(optional, integer) Minimum report severity to parse. Defaults to 4.

---

### Microsoft CTIP <div id="intelmq.bots.parsers.microsoft.parser_ctip" />

Parses data from the Microsoft CTIP feed.

Can parse the JSON format provided by the Interflow interface (lists of dictionaries) as well as the format provided by
the Azure interface (one dictionary per line). The provided data differs between the two formats/providers.

The parser is capable of parsing both feeds:

- `ctip-c2`
- `ctip-infected-summary` The feeds only differ by a few fields, not in the format.

The feeds contain a field called `Payload` which is nearly always a base64 encoded JSON structure. If decoding works,
the contained fields are saved as `extra.payload.*`, otherwise the field is saved as `extra.payload.text`.

**Module:** `intelmq.bots.parsers.microsoft.parser_ctip`

**Parameters:**

**`overwrite`**

(optional, boolean) Overwrite an existing field `feed.name` with `DataFeed` of the source. Defaults to false.

---

### MISP <div id="intelmq.bots.parsers.misp.parser" />

Parses MISP events.

MISP events collected by the MISPCollectorBot are passed to this parser for processing. Supported MISP event categories
and attribute types are defined in the `SUPPORTED_MISP_CATEGORIES` and `MISP_TYPE_MAPPING` class constants.

**Module:** `intelmq.bots.parsers.misp.parser`

No additional parameters.

---

### N6 <div id="intelmq.bots.parsers.n6.parser_n6stomp" />

Parses n6 data into IntelMQ format.

Test messages are ignored, this is logged with debug logging level. Also contains a mapping for the classification (
results in taxonomy, type and identifier). The `name` field is normally used as `malware.name`, if that fails due to
disallowed characters, these characters are removed and the original value is saved as `event_description.text`. This
can happen for names like `further iocs: text with invalid ' char`.

If a n6 message contains multiple IP addresses, multiple events are generated, resulting in events only differing in the
address information.

**Module:** `intelmq.bots.parsers.n6.parser_n6stomp`

No additional parameters.

---

### OpenPhish Free <div id="intelmq.bots.parsers.openphish.parser" />

Parses data from OpenPhish Free feed.

**Module:** `intelmq.bots.parsers.openphish.parser`

No additional parameters.

---

### OpenPhish Premium <div id="intelmq.bots.parsers.openphish.parser_commercial" />

Parses data from OpenPhish Premium feed (JSON).

**Module:** `intelmq.bots.parsers.openphish.parser_commercial`

No additional parameters.

---

### Phishtank <div id="intelmq.bots.parsers.phishtank.parser" />

Parses data from Phishtank feed.

**Module:** `intelmq.bots.parsers.phishtank.parser`

No additional parameters.

---

### Shadowserver <div id="intelmq.bots.parsers.shadowserver.parser" /> 

The Shadowserver parser operates on CSV formatted data.


**How this bot works?**

There are two possibilities for the bot to determine which report type the data belongs to in order to determine the
correct mapping of the columns:

1. **Automatic report type detection**

   Since IntelMQ version 2.1 the parser can detect the feed based on metadata provided by the collector.

   When processing a report, this bot takes `extra.file_name` from the report and looks in `config.py` how the report
   should be parsed. If this lookup is not possible, and the `feedname` is not given as parameter, the feed cannot be
   parsed.

   The field `extra.file_name` has the following structure: `%Y-%m-%d-${report_name}[-suffix].csv` where the optional
   suffix can be something like `country-geo`. For example, some possible filenames
   are `2019-01-01-scan_http-country-geo.csv` or `2019-01-01-scan_tftp.csv`. The important part is the `report_name`,
   between the date and the suffix. Since version 2.1.2 the date in the filename is optional, so filenames
   like `scan_tftp.csv` are also detected.

2. **Fixed report type**

   If the method above is not possible and for upgraded instances, the report type can be set with the `feedname`
   parameter. Report type is derived from the subject of Shadowserver e-mails. A list of possible values of
   the `feedname` parameter can be found in the table below in the column "Report Type".

**Module:**

`intelmq.bots.parsers.shadowserver.parser`

**Parameters:**

**`feedname`**

(optional, string) Name of the Shadowserver report, see list below for possible values.

**`overwrite`**

(optional, boolean) If an existing `feed.name` should be overwritten.

**Supported reports:**

The report configuration is stored in a `shadowserver-schema.json` file downloaded from https://interchange.shadowserver.org/intelmq/v1/schema.

The parser will attempt to download a schema update on startup when the *auto_update* option is enabled.

Schema downloads can also be scheduled as a cron job for the `intelmq` user:

```bash
  02  01 *   *   *     intelmq.bots.parsers.shadowserver.parser --update-schema
```

For air-gapped systems automation will be required to download and copy the file to VAR_STATE_PATH/shadowserver-schema.json.

The parser will automatically reload the configuration when the file changes.


**Schema contract**

Once set in the schema, the `classification.identifier`, `classification.taxonomy`, and `classification.type` fields will remain static for a specific report.

The schema revision history is maintained at https://github.com/The-Shadowserver-Foundation/report_schema/.


**Sample configuration**

```yaml
  shadowserver-parser:
    bot_id: shadowserver-parser
    name: Shadowserver Parser
    enabled: true
    group: Parser
    groupname: parsers
    module: intelmq.bots.parsers.shadowserver.parser
    parameters:
      destination_queues:
        _default: [file-output-queue]
      auto_update: true
    run_mode: continuous
```
---

### Shodan <div id="intelmq.bots.parsers.shodan.parser" />

Parses data from Shodan (search, stream etc).

The parser is by far not complete as there are a lot of fields in a big nested structure. There is a minimal mode
available which only parses the important/most useful fields and also saves everything in `extra.shodan` keeping the original structure. When not using the minimal mode if may be useful to ignore errors as many
parsing errors can happen with the incomplete mapping.

**Module:** `intelmq.bots.parsers.shodan.parser`

**Parameters:**

**`ignore_errors`**

(optional, boolean) Defaults to true.

**`minimal_mode`**

(optional, boolean) Defaults to false.

---

### Spamhaus DROP <div id="intelmq.bots.parsers.spamhaus.parser_drop" />

Parses data from Spamhaus DROP feed.

**Module:** `intelmq.bots.parsers.spamhaus.parser_drop`

No additional parameters.

---

### Spamhaus CERT <div id="intelmq.bots.parsers.spamhaus.parser_cert" />

Parses data from Spamhaus CERT feed.

**Module:** `intelmq.bots.parsers.spamhaus.parser_cert`

No additional parameters.

---

### Surbl <div id="intelmq.bots.parsers.surbl.parser" />

Parses data from surbl feed.

**Module:** `intelmq.bots.parsers.surbl.parser`

No additional parameters.

---

### Threatminer <div id="intelmq.bots.parsers.threatminer.parser" />

Parses data from Threatminer feed.

**Module:** `intelmq.bots.parsers.threatminer.parser`

No additional parameters.

---

### Turris <div id="intelmq.bots.parsers.turris.parser" />

Parses data from Turris Greylist feed.

**Module:** `intelmq.bots.parsers.turris.parser`

No additional parameters.

---

### Twitter <div id="intelmq.bots.parsers.twitter.parser" />

Extracts URLs from text, fuzzy, aimed at parsing tweets.

**Module:** `intelmq.bots.parsers.twitter.parser`

**Parameters:**

**`domain_whitelist`**

(optional, array of strings) domains to be filtered out

**`substitutions`**

(optional, string) Semicolon delimited list of even length of pairs of substitutions (for example: `.;.;,;.`
substitutes `.` for `.` and `,` for `.`).

**`classification_type`**

(optional, string) Statically set `classification.type`.

**`default_scheme`**

(optional, string) Default scheme for URLs if not given. See also the next section.

**Default scheme**

The dependency `url-normalize` changed it's behavior in version 1.4.0 from using `http://` as default scheme to
`https://`. Version 1.4.1 added the possibility to specify it. Thus you can only use the `default_scheme`
parameter with a current version of this library >= 1.4.1, with 1.4.0 you will always get `https://`
as default scheme and for older versions < 1.4.0 `http://` is used.

This does not affect URLs which already include the scheme.

---

### VxVault <div id="intelmq.bots.parsers.vxvault.parser" />

Parses data from VxVault feed.

**Module:** `intelmq.bots.parsers.vxvault.parser`

No additional parameters.

---

### ZoneH <div id="intelmq.bots.parsers.zoneh.parser" />

Parses data from ZoneH.

This bot is designed to consume defacement reports from zone-h.org. It expects fields normally present in CSV files
distributed by email.

**Module:** `intelmq.bots.parsers.zoneh.parser`

No additional parameters.

## Expert Bots

Expert bots are used for enriching, filtering and/or other data manipulation.

### Abusix <div id="intelmq.bots.experts.abusix.expert" />

This bot adds `source.abuse_contact` and `destination.abuse_contact` e-mail addresses. They are obtained via DNS TXT
queries to Abusix servers.

**Requirements**

This bot can optionally use the python module *querycontacts* by Abusix itself: <https://pypi.org/project/querycontacts/>

```bash
pip3 install querycontacts
```

If the package is not installed, our own routines are used.

**Module:** `intelmq.bots.experts.abusix.expert`

**Parameters (also expects [cache parameters](#cache-parameters)):**

No additional parameters.

---

### Aggregate <div id="intelmq.bots.experts.aggregate.expert" />

Aggregates events based upon given fields & timespan.

Define specific fields to filter incoming events and aggregate them. Also set the timespan you want the events to get
aggregated.

The "cleanup" procedure, sends out the aggregated events or drops them based upon the given threshold value. It is
called on every incoming message and on the bot's initialization. If you're potentially running on low traffic ( no
incoming events within the given timestamp ) it is recommended to reload or restart the bot via cronjob each 30
minutes (adapt to your configured timespan). Otherwise you might loose information.

I. e.:

```bash
crontab -e

0,30 * * * * intelmqctl reload my-aggregate-bot
```

For reloading/restarting please check the `intelmqctl` documentation.

**Module:** `intelmq.bots.experts.aggregate.expert`

**Parameters (also expects [cache parameters](#cache-parameters)):**

!!! warning
    `redis_cache_ttl` is not used at it would result in data loss.

**`fields`**

(required, string) Given fields which are used to aggregate like `classification.type`, `classification.identifier`.

**`threshold`**

(required, integer) If the aggregated event is lower than the given threshold after the timespan, the event will get
dropped.

**`timespan`**

(required, string) Timespan to aggregate events during the given time. I. e. `1 hour`

---

### ASN Lookup <div id="intelmq.bots.experts.asn_lookup.expert" />

This bot uses an offline database to add `source.asn` and `destination.asn` based on the respective IP address.

**Requirements**

Install `pyasn` module.

```bash
pip3 install pyasn
```

**Module:** `intelmq.bots.experts.asn_lookup.expert`

**Parameters:**

**`database`**

(required, string) Path to the downloaded database.

**Database**

Use this command to create/update the database and reload the bot:

```bash
intelmq.bots.experts.asn_lookup.expert --update-database
```

The database is fetched from [routeviews.org](http://www.routeviews.org/routeviews/) and licensed under the Creative
Commons Attribution 4.0 International license (see
the [routeviews FAQ](http://www.routeviews.org/routeviews/index.php/faq/#faq-6666)).

---

### CSV Converter <div id="intelmq.bots.experts.csv_converter.expert" />

Converts an event to CSV format, saved in the `output` field.

To use the CSV-converted data in an output bot - for example in a file output, use the configuration
parameter `single_key` of the output bot and set it to `output`.

**Module:** `intelmq.bots.experts.csv_converter.expert`

**Parameters:**

**`delimiter`**

(optional, string) Defaults to `,`.

**`fieldnames`**

(required, string) Comma-separated list of field names, e.g. `"time.source,classification.type,source.ip"`.

---

### Team Cymru Whois <div id="intelmq.bots.experts.cymru_whois.expert" />

This bot adds geolocation, ASN and BGP prefix based on IP address.

Public documentation: <https://www.team-cymru.com/IP-ASN-mapping.html#dns>

**Module:** `intelmq.bots.experts.cymru_whois.expert`

**Parameters (also expects [cache parameters](#cache-parameters)):**

**`overwrite`**

(optional, boolean) Whether to overwrite existing fields. Defaults to true.

---

### Remove Affix <div id="intelmq.bots.experts.remove_affix.expert" />

Remove part of string from string fields, example: `www.` from `source.fqdn`.

**Module:** `intelmq.bots.experts.remove_affix.expert`

**Parameters:**

**`remove_prefix`**

(optional, boolean) True - cut from start, False - cut from end. Defaults to true.

**`affix`**

(required, string) example 'www.'

**`field`**

(required, string) Which field to modify. 'source.fqdn'

---

### Domain Suffix <div id="intelmq.bots.experts.domain_suffix.expert" />

This bots uses an offline database to add the public suffix to the event, derived by a domain. See or information on the
public suffix list: <https://publicsuffix.org/list/>. Only rules for ICANN domains are processed. The list can (and
should) contain Unicode data, punycode conversion is done during reading.

Note that the public suffix is not the same as the top level domain (TLD). E.g. `co.uk` is a public suffix, but the TLD
is `uk`. Privately registered suffixes (such as `blogspot.co.at`) which are part of the public suffix list too, are
ignored.

**Rule processing**

A short summary how the rules are processed:

The simple ones:

```
com
at
gv.at
```

`example.com` leads to `com`,
`example.gv.at` leads to `gv.at`.

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

**Module:** `intelmq.bots.experts.domain_suffix.expert`

**Parameters:**

**`field`**

(required, string) Allowed values: `fqdn` or `reverse_dns`.

**`suffix_file`**

(required, string) path to the suffix file

**Database**

Use this command to create/update the database and reload the bot:

```bash
intelmq.bots.experts.domain_suffix.expert --update-database
```

---

### Domain Valid <div id="intelmq.bots.experts.domain_valid.expert" />

Checks if a domain is valid by performing multiple validity checks (see below).

If the field given in `domain_field` does not exist in the event, the event is dropped. If the domain contains
underscores (`_`), the event is dropped. If the domain is not valid according to
the [validators library](https://pypi.org/project/validators/), the event is dropped. If the domain's last part (the
TLD) is not in the TLD-list configured by parameter `tlds_domains_list`, the field is dropped. Latest TLD
list: <https://data.iana.org/TLD/>

**Module:** `intelmq.bots.experts.domain_valid.expert`

**Parameters:**

**`domain_field`**

(required, string) The name of the field to be validated.

**`tlds_domains_list`**

(required, string) Path to a local file with all valid TLDs. Defaults to `/opt/intelmq/var/lib/bots/domain_valid/tlds-alpha-by-domain.txt`


---

### Deduplicator <div id="intelmq.bots.experts.deduplicator.expert" />

Bot responsible for dropping duplicate events. Deduplication can be performed based on an arbitrary set of fields.

**Module:** `intelmq.bots.experts.deduplicator.expert`

**Parameters (also expects [cache parameters](#cache-parameters)):**

**`bypass`**

(optional, boolean) Whether to bypass the deduplicator or not. When set to true, messages will not be deduplicated.
Defaults to false.

**`filter_type`**

(optional, string) Allowed values: `blacklist` or `whitelist`. The filter type will be used to define how Deduplicator
bot will interpret the parameter `filter_keys` in order to decide whether an event has already been seen or not, i.e.,
duplicated event or a completely new event.

- `whitelist` configuration: only the keys listed in `filter_keys` will be considered to verify if an event is
  duplicated or not.
- `blacklist` configuration: all keys except those in `filter_keys` will be considered to verify if an event is
  duplicated or not.

**`filter_keys`**

(optional, string) string with multiple keys separated by comma. Please note that `time.observation` key will not be
considered even if defined, because the system always ignore that key.

When using a whitelist field pattern and a small number of fields (keys), it becomes more important, that these fields
exist in the events themselves. If a field does not exist, but is part of the hashing/deduplication, this field will be
ignored. If such events should not get deduplicated, you need to filter them out before the deduplication process, e.g.
using a sieve expert. See
also [this discussion thread](https://lists.cert.at/pipermail/intelmq-users/2021-July/000370.html) on the mailing-list.

**Configuration Example**

*Example 1*

The bot with this configuration will detect duplication only based on `source.ip` and `destination.ip` keys.

```yaml
parameters:
  redis_cache_db: 6
  redis_cache_host: "127.0.0.1"
  redis_cache_password: null
  redis_cache_port: 6379
  redis_cache_ttl: 86400
  filter_type: "whitelist"
  filter_keys: "source.ip,destination.ip"
```

*Example 2*

The bot with this configuration will detect duplication based on all keys, except `source.ip` and `destination.ip` keys.

```yaml
parameters:
  redis_cache_db: 6
  redis_cache_host: "127.0.0.1"
  redis_cache_password: null
  redis_cache_port: 6379
  redis_cache_ttl: 86400
  filter_type: "blacklist"
  filter_keys: "source.ip,destination.ip"
```

**Flushing the cache**

To flush the deduplicator's cache, you can use the `redis-cli` tool. Enter the database used by the bot and submit
the `flushdb` command:

```bash
redis-cli -n 6
flushdb
```

---

### DO Portal <div id="intelmq.bots.experts.do_portal.expert" />

The DO portal retrieves the contact information from a DO portal instance:
<http://github.com/certat/do-portal/>

**Module:** `intelmq.bots.experts.do_portal.expert`

**Parameters:**

**`mode`**

(required, string) Allowed values: `replace` or `append`. How to handle new abuse contacts in case there are existing
ones.

**`portal_url`**

(required, string) The URL to the portal, without the API-path. The used URL
is `$portal_url + '/api/1.0/ripe/contact?cidr=%s'`.

**`portal_api_key`**

(required, string) The API key of the user to be used. Must have sufficient privileges.

---

### Field Reducer <div id="intelmq.bots.experts.field_reducer.expert" />

The field reducer bot is capable of removing fields from events.

**Module:** `intelmq.bots.experts.field_reducer.expert`

**Parameters:**

**`type`**

(required, string) Allowed values: `whitelist` or `blacklist`. When `whitelist` is set, tnly the fields in `keys` will
passed along. When `blacklist` is set then the fields in `keys` will be removed from events.

**`keys`**

(required, array of strings) Can be an array of field names or a string with a comma-separated list of field names.

---

### Filter <div id="intelmq.bots.experts.filter.expert" />

The filter bot is capable of filtering specific events.

A simple filter for messages (drop or pass) based on a exact string comparison or regular expression.

**Module:** `intelmq.bots.experts.filter.expert`

**Parameters:**

*Parameters for filtering with key/value attributes*

**`filter_key`**

() - key from data format

**`filter_value`**

() - value for the key

**`filter_action`**

() - action when a message match to the criteria
(possible actions: keep/drop)

**`filter_regex`**

() - attribute determines if the `filter_value` shall be treated as regular expression or not.

If this attribute is not empty (can be `true`, `yes` or whatever), the bot uses python's `` `re.search ``
<<https://docs.python.org/3/library/re.html#re.search>>`_ function to evaluate the filter with regular expressions. If
this attribute is empty or evaluates to false, an exact string comparison is performed. A check on string *
inequality* can be achieved with the usage of *Paths* described below.

*Parameters for time based filtering*

**`not_before`**

(optional, string) Events before this time will be dropped. Example: `1 week`.

**`not_after`**

(optional, string) - Events after this time will be dropped.

Both parameters accept string values describing absolute or relative time:

- absolute
- basically anything parseable by datetime parser, eg.

```
2015-09-12T06:22:11+00:00
```

**`time.source`**

(optional, string) Taken from the event will be compared to this value to decide the filter behavior.

- relative
- accepted string formatted like this "<integer> <epoch>", where epoch could be any of following strings (could
  optionally end with trailing 's'): hour, day, week, month, year
- time.source taken from the event will be compared to the value (now - relative) to decide the filter behavior

*Examples of time filter definition*

- `not_before: "2015-09-12T06:22:11+00:00"` - events older than the specified time will be dropped
- `not_after: "6 months"` - just events older than 6 months will be passed through the pipeline

**Possible paths**

- `_default`: default path, according to the configuration
- `action_other`: Negation of the default path
- `filter_match`: For all events the filter matched on
- `filter_no_match`: For all events the filter does not match

| action | match | \_default | action_other | filter_match | filter_no_match |
| ------ | ----- | --------- | ------------ | ------------ | --------------- |
| keep   | ✓     | ✓         | ✗            | ✓            | ✗               |
| keep   | ✗     | ✗         | ✓            | ✗            | ✓               |
| drop   | ✓     | ✗         | ✓            | ✓            | ✗               |
| drop   | ✗     | ✓         | ✗            | ✗            | ✓               |

In `DEBUG` logging level, one can see that the message is sent to both matching paths, also if one of the paths is not
configured. Of course the message is only delivered to the configured paths.

---

### Format Field <div id="intelmq.bots.experts.format_field.expert" />

String method operations on column values.

**Module:** `intelmq.bots.experts.format_field.expert`

**Parameters:**

*Parameters for stripping chars*

**`strip_columns`**
(optional, string/array of strings) A list of strings or a string of comma-separated values with field names. The names
must match the IntelMQ Data Format field names.

For example:

```yaml
columns:
  - malware.name
  - extra.tags
```

is equivalent to:

```yaml
columns: "malware.name,extra.tags"
```

**`strip_chars`**

(optional, string) Set of characters to remove as leading/trailing characters. Defaults to space.

*Parameters for replacing chars*

**`replace_column`**

() key from data format

**`old_value`**

() the string to search for

**`new_value`**

() the string to replace the old value with

**`replace_count`**
() number specifying how many occurrences of the old value you want to replace(default: [1])

*Parameters for splitting string to list of string*

**`split_column`**

() key from data format

**`split_separator`**

() specifies the separator to use when splitting the string(default: `,`)

Order of operation: `strip -> replace -> split`. These three methods can be combined such as first strip and then split.

---

### Generic DB Lookup <div id="intelmq.bots.experts.generic_db_lookup.expert" />

This bot is capable for enriching intelmq events by lookups to a database. Currently only PostgreSQL and SQLite are
supported.

If more than one result is returned, a ValueError is raised.

**Module:** `intelmq.bots.experts.generic_db_lookup.expert`

**Parameters:**

*Connection*

**`engine`**

(required, string) Allowed values: `postgresql` or `sqlite`.

**`database`**

(optional, string) Database name or the SQLite filename. Defaults to `intelmq`.

**`table`**

(optional, string) Name of the table. Defaults to `contacts`.

*PostgreSQL specific parameters*

**`host`**

(optional, string) Hostname of the PostgreSQL server. Defaults to `localhost`.

**`port`**

(optional, integer) Port of the PostgreSQL server. Defaults to 5432.

**`user`**

(optional, string) Username for accessing PostgreSQL. Defaults to `intelmq`.

**`password`**

(optional, string) Password for accessing PostgreSQL. Defaults to ?.

**`sslmode`**

(optional, string) Type of TLS mode to use. Defaults to `require`.

*Lookup*

**`match_fields`**

(optional, object) The value is a key-value mapping an arbitrary number IntelMQ field names to table column names. The
values are compared with `=` only. Defaults to `source.asn: "asn"`.

*Replace fields*

**`overwrite`**

(optional, boolean) Whether to overwrite existing fields. Defaults to false.

**`replace_fields`**

(optional, object) Key-value mapping an arbitrary number of table column names to IntelMQ field names. Defaults
to `{"contact": "source.abuse_contact"}`.

---

### Gethostbyname <div id="intelmq.bots.experts.gethostbyname.expert" />

This bot resolves to IP address (`source.ip` and `destination.ip`). Can possibly use also the `source.url`
and `destination.url` for extracting FQDN.

This bot resolves the DNS name (`source.fqdn` and `destination.fqdn`) using the `gethostbyname` syscall to an IP
address (`source.ip` and `destination.ip`). The following gaierror resolution errors are ignored and treated as if the
hostname cannot be resolved:

* `-2`/`EAI_NONAME`: NAME or SERVICE is unknown
* `-4`/`EAI_FAIL`: Non-recoverable failure in name res.
* `-5`/`EAI_NODATA`: No address associated with NAME.
* `-8`/`EAI_SERVICE`: SERVICE not supported for `ai_socktype'.
* `-11`/`EAI_SYSTEM`: System error returned in `errno'.

Other errors result in an exception if not ignored by the parameter `gaierrors_to_ignore`. All gaierrors can be found here: <http://www.castaglia.org/proftpd/doc/devel-guide/src/lib/glibc-gai_strerror.c.html>

**Module:** `intelmq.bots.experts.gethostbyname.expert`

**Parameters:**

**`fallback_to_url`**

(optional, boolean) When true and no `source.fqdn` present, use `source.url` instead for producing `source.ip`.

**`gaierrors_to_ignore`**

(optional, array of integers) Gaierror codes to ignore, e.g. `-3` for EAI_AGAIN (Temporary failure in name resolution).
Only accepts the integer values, not the names.

**`overwrite`**

(optional, boolean) Whether to overwrite existing `source.ip` and/or `source.destination` fields. Defaults to false.

---

### HTTP Status <div id="intelmq.bots.experts.http.expert_status" />

The bot fetches the HTTP status for a given URL and saves it in the event.

**Module:** `intelmq.bots.experts.http.expert_status`

**Parameters:**

**`field`**

(required, string) The name of the field containing the URL to be checked.

**`success_status_codes`**

(optional, array of integers) An array of success status codes. If this parameter is omitted or the list is empty,
successful status codes are the ones between 200 and 400.

**`overwrite`**

(optional, boolean) Whether to overwrite existing `status` field. Defaults to false.

---

### HTTP Content <div id="intelmq.bots.experts.http.expert_content" />

Fetches an HTTP resource and checks if it contains a specific string.

The bot fetches an HTTP resource and checks if it contains a specific string.

**Module:** `intelmq.bots.experts.http.expert_content`

**Parameters:**

**`field`**

(optional, string) The name of the field containing the URL to be checked. Defaults to `source.url`.

**`needle`**

(optional, string) The string that the content available on URL is checked for.

**`overwrite`**

(optional, boolean) Whether to overwrite existing `status` field. Defaults to false.

---

### IDEA Converter <div id="intelmq.bots.experts.idea.expert" />

Converts the event to IDEA format and saves it as JSON in the field `output`. All other fields are not modified.

Documentation about IDEA: <https://idea.cesnet.cz/en/index>

**Module:** `intelmq.bots.experts.idea.expert`

**Parameters:**

**`test_mode`**

(optional, boolean) Adds `Test` category to mark all outgoing IDEA events as informal (meant to simplify setting up and
debugging new IDEA producers). Defaults to true.

---

### Jinja2 Template <div id="intelmq.bots.experts.jinja.expert" />

This bot lets you modify the content of your IntelMQ message fields using Jinja2 templates.

Documentation about Jinja2 templating language: <https://jinja.palletsprojects.com/>

**Module:** `intelmq.bots.experts.jinja.expert`

**Parameters:**

**`fields`**

(required, object) a dict containing as key the name of the field where the result of the Jinja2 template should be
written to and as value either a Jinja2 template or a filepath to a Jinja2 template file (starting with `file:///`).
Because the experts decides if it is a filepath based on the value starting with `file:///` it is not possible to simply
write values starting with `file:///` to fields. The object containing the existing message will be passed to the Jinja2
template with the name `msg`.

```yaml
fields:
  output: The provider is {{ msg['feed.provider'] }}!
  feed.url: "{{ msg['feed.url'] | upper }}"
  extra.somejinjaoutput: file:///etc/intelmq/somejinjatemplate.j2
```

---

### Lookyloo <div id="intelmq.bots.experts.lookyloo.expert" />

Lookyloo is a website screenshotting and analysis tool. For more information and installation instructions visit
<https://www.lookyloo.eu/>

The bot sends a request for `source.url` to the configured Lookyloo instance and saves the retrieved website screenshot
link in the field `screenshot_url`. Lookyloo only *queues* the website for screenshotting, therefore the screenshot may
not be directly ready after the bot requested it. The `pylookyloo` library is required for this bot.
The `http_user_agent` parameter is passed on, but not other HTTP-related parameter like proxies.

Events without `source.url` are ignored.

**Module:** `intelmq.bots.experts.lookyloo.expert`

**Parameters:**

**`instance_url`**

(required, string) LookyLoo instance to connect to.

---

### MaxMind GeoIP <div id="intelmq.bots.experts.maxmind_geoip.expert" />

This bot uses an offline database for adding geolocation information based on the IP address (`source.ip` and `destination.ip`).

**Requirements**

The bot requires the MaxMind's `geoip2` Python library, version 2.2.0 has been tested.

To download the database a free license key is required. More information can be found
at <https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/>.

**Module:** `intelmq.bots.experts.maxmind_geoip.expert`

**Parameters:**

**`database`**

(required, string) Path to the local database file.

**`overwrite`**

(optional, boolean) Whether to overwrite existing fields. Defaults to true.

**`use_registered`**

(optional, boolean) MaxMind has two country ISO codes: One for the physical location of the address and one for the
registered location. See also <https://github.com/certtools/intelmq/pull/1344> for a short explanation. Defaults
to `false` (backwards-compatibility).

**`license_key`**

(required, string) MaxMind license key is necessary for downloading the GeoLite2 database.

**Database**

Use this command to create/update the database and reload the bot:

```bash
intelmq.bots.experts.maxmind_geoip.expert --update-database
```

---

### MISP <div id="intelmq.bots.experts.misp.expert" />

Queries a MISP instance for the `source.ip` and adds the MISP Attribute UUID and MISP Event ID of the newest attribute
found.

**Module:** `intelmq.bots.experts.misp.expert`

**Parameters:**

**`misp_key`**

(required, string) MISP Authkey.

**`misp_url`**

(required, string) URL of MISP server (with trailing '/')

**`http_verify_cert`**

(optional, boolean) Verify the TLS certificate of the server. Default to `true`.

---

### McAfee Active Response Lookup <div id="intelmq.bots.experts.mcafee.expert_mar" />

Queries DXL bus for hashes, IP addresses or FQDNs.

**Module:** `intelmq.bots.experts.mcafee.expert_mar`

**Parameters:**

**`dxl_config_file`**

(required, string) Location of the file containing required information to connect to DXL bus.

**`lookup_type`**

(required, string) Allowed values:

- `Hash` - Looks up `malware.hash.md5`, `malware.hash.sha1` and `malware.hash.sha256`.
- `DestSocket` - Looks up `destination.ip` and `destination.port`.
- `DestIP` - Looks up `destination.ip`.
- `DestFQDN` - Looks up in `destination.fqdn`.

---

### Modify <div id="intelmq.bots.experts.modify.expert" />

This bots allows you to change arbitrary field values of events using a configuration file.

**Module:** `intelmq.bots.experts.modify.expert`

**Parameters:**

**`configuration_path`**

(required, string) Location of the configuration file.

**`case_sensitive`**

(optional, boolean) Defaults to true.

**`maximum_matches`**

(optional, boolean) Maximum number of matches. Processing stops after the limit is reached. Defaults to null (no limit).

**`overwrite`**

(optional, boolean) Overwrite any existing fields by matching rules. Defaults to false.

**Configuration File**

The modify expert bot allows you to change arbitrary field values of events just using a configuration file. Thus it is
possible to adapt certain values or adding new ones only by changing JSON-files without touching the code of many other
bots.

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

In our example above we have five groups labeled `Standard Protocols http`, `Spamhaus Cert conficker`,
`bitdefender`, `urlzone` and `default`. All sections will be considered, in the given order (from top to bottom).

Each rule consists of *conditions* and *actions*. Conditions and actions are dictionaries holding the field names of
events and regular expressions to match values (selection) or set values (action). All matching rules will be applied in
the given order. The actions are only performed if all selections apply.

If the value for a condition is an empty string, the bot checks if the field does not exist. This is useful to apply
default values for empty fields.

**Actions**

You can set the value of the field to a string literal or number.

In addition you can use the [standard Python string format syntax](https://docs.python.org/3/library/string.html#format-string-syntax) to access the values from the processed event as `msg` and the match groups of the conditions as `matches`, see the bitdefender example above. Group 0 ([`0`]) contains the full matching string. See also the documentation on [re.Match.group](https://docs.python.org/3/library/re.html?highlight=re%20search#re.Match.group).

Note that `matches` will also contain the match groups from the default conditions if there were any.

**Examples**

We have an event with `feed.name = Spamhaus Cert` and `malware.name = confickerab`. The expert loops over all sections
in the file and eventually enters section `Spamhaus Cert`. First, the default condition is checked, it matches!
OK, going on. Otherwise the expert would have selected a different section that has not yet been considered. Now, go
through the rules, until we hit the rule `conficker`. We combine the conditions of this rule with the default
conditions, and both rules match! So we can apply the action: `classification.identifier` is set to `conficker`, the
trivial name.

Assume we have an event with `feed.name = Spamhaus Cert` and `malware.name = feodo`. The default condition matches, but
no others. So the default action is applied. The value for `classification.identifier` will be set to `feodo`
by `{msg[malware.name]}`.

**Types**

If the rule is a string, a regular expression search is performed, also for numeric values (`str()` is called on them).
If the rule is numeric for numeric values, a simple comparison is done. If other types are mixed, a warning will be
thrown.

For boolean values, the comparison value needs to be `true` or `false` as in JSON they are written all-lowercase.

---

### National CERT Contact Lookup by CERT.AT <div id="intelmq.bots.experts.national_cert_contact_certat.expert" />

<https://contacts.cert.at> offers an IP address to national CERT contact (and cc) mapping.

**Module:** `intelmq.bots.experts.national_cert_contact_certat.expert`

**Parameters:**

**`filter`**

(optional, boolean) Whether to act as a filter for AT.

**`overwrite_cc`**

(optional, boolean) Set to true if you want to overwrite any potentially existing cc fields in the event. Defaults to
false.

---

### RDAP <div id="intelmq.bots.experts.rdap.expert" />

This bot queries RDAP servers for additional information about a domain.

**Module:** `intelmq.bots.experts.rdap.expert`

**Parameters:**

**`rdap_order`**

(optional, array of strings) Search order of contacts with these roles. Defaults to `["abuse", "technical"]`.

**`rdap_bootstrapped_servers`**

(optional, object) Customized RDAP servers. Do not forget the trailing slash. For example:

```json
{
  "at": {
    "url": "rdap.server.at/v1/",
    "auth": {
      "type": "jwt",
      "token": "ey..."
    }
  },
  "de": "rdap.service:1337/v1/"
}
```

---

### RecordedFuture IP Risk <div id="intelmq.bots.experts.recordedfuture_iprisk.expert" />

This bot tags events with the score found in RecordedFuture large IP risklist.

Record risk score associated to source and destination IP if they are present. Assigns 0 to IP addresses not in the RF
list.

For both `source.ip` and `destination.ip` the corresponding risk score is fetched from a local database created from
RecordedFuture's API. The score is recorded in `extra.rf_iprisk.source` and `extra.rf_iprisk.destination`. If a lookup
for an IP fails a score of 0 is recorded.

See <https://www.recordedfuture.com/products/api/> and speak with your RecordedFuture representative for more
information.

The list is obtained from recorded future API and needs a valid API TOKEN The large list contains all IP's with a risk
score of 25 or more. If IP's are not present in the database a risk score of 0 is given.

**Module:** `intelmq.bots.experts.recordedfuture_iprisk.expert`

**Parameters:**

**`database`**

(required, string) Path to the local database file.

**`api_token`**

(required, string) This needs to contain valid API token to download the latest database data.

**`overwrite`**

(optional, boolean) Whether to overwrite existing fields. Defaults to false.

**Database**

Use this command to create/update the database and reload the bot:

```bash
intelmq.bots.experts.recordedfuture_iprisk.expert --update-database
```

---

### Reverse DNS <div id="intelmq.bots.experts.reverse_dns.expert" />

For both `source.ip` and `destination.ip` the PTR record is fetched and the first valid result is used
for `source.reverse_dns` or `destination.reverse_dns`.

**Module:** `intelmq.bots.experts.reverse_dns.expert`

**Parameters (also expects [cache parameters](#cache-parameters)):**

**`cache_ttl_invalid_response`**

(required, integer) The TTL for cached invalid responses.

**`overwrite`**

(optional, boolean) Whether to overwrite existing fields. Defaults to false.

---

### RFC1918 <div id="intelmq.bots.experts.rfc1918.expert" />

Several RFCs define ASNs, IP Addresses and Hostnames (and TLDs) reserved for *documentation*. Events or fields of events
can be dropped if they match the criteria of either being reserved for documentation (e.g. AS 64496,
Domain `example.com`) or belonging to a local area network (e.g. `192.168.0.0/24`). These checks can applied to URLs, IP
Addresses, FQDNs and ASNs.

It is configurable if the whole event should be dropped ("policies") or just the field removed, as well as which fields
should be checked.

Sources:

- `1918`
- `2606`
- `3849`
- `4291`
- `5737`
- <https://en.wikipedia.org/wiki/IPv4>
- <https://en.wikipedia.org/wiki/Autonomous_system_(Internet)>

**Module:** `intelmq.bots.experts.rfc1918.expert`

**Parameters:**

**`fields`**

(required, string) Comma-separated list of fields. Allowed values:

- `destination.asn` & `source.asn`
- `destination.fqdn` & `source.fqdn`
- `destination.ip` & `source.ip`
- `destination.url` & `source.url`

**`policy`**

(required, string) Comma-separated list of policies. Allowed values:

- `drop` - the entire events is dropped
- `del` - the affected field is removed

With the example parameter values given above, this means that:

- If a `destination.ip` value is part of a reserved network block, the field will be removed (policy `del`).
- If a `source.asn` value is in the range of reserved AS numbers, the event will be removed altogether (policy `drop`).
- If a `source.url` value contains a host with either an IP address part of a reserved network block, or a reserved
  domain name (or with a reserved TLD), the event will be dropped (policy `drop`).

---

### RIPE <div id="intelmq.bots.experts.ripe.expert" />

Online RIPE Abuse Contact and Geolocation Finder for IP addresses and Autonomous Systems.

**Module:** `intelmq.bots.experts.ripe.expert`

**Parameters (also expects [cache parameters](#cache-parameters)):**

**`mode`**

(optional, string) Allowed values: `append` or `replace`. Defaults to `append`.

**`query_ripe_db_asn`**

(optional, boolean) Query for IPs at `http://rest.db.ripe.net/abuse-contact/%s.json`. Defaults to true.

**`query_ripe_db_ip`**

(optional, boolean) Query for ASNs at `http://rest.db.ripe.net/abuse-contact/as%s.json`. Defaults to true.

**`query_ripe_stat_asn`**

(optional, boolean) Query for ASNs at `https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=%s`. Defaults
to true.

**`query_ripe_stat_ip`**

(optional, boolean) Query for IPs at `https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=%s`. Defaults
to true.

**`query_ripe_stat_geolocation`**

(optional, boolean) Query for IPs at `https://stat.ripe.net/data/maxmind-geo-lite/data.json?resource=%s`. Defaults to
true.

---

### Sieve <div id="intelmq.bots.experts.sieve.expert" />

This bot is used to filter and/or modify events based on a set of rules. The rules are specified in an external
configuration file and with a syntax *similar* to the [Sieve language](http://sieve.info) used for mail filtering.

Each rule defines a set of matching conditions on received events. Events can be matched based on keys and values in the
event. Conditions can be combined using parenthesis and the boolean operators `&&` and `||`. If the processed event
matches a rule's conditions, the corresponding actions are performed. Actions can specify whether the event should be
kept or dropped in the pipeline (filtering actions) or if keys and values should be changed (modification actions).

**Requirements**

To use this bot, you need to install the required dependencies:

```bash
pip3 install -r intelmq/bots/experts/sieve/REQUIREMENTS.txt
```

**Module:** `intelmq.bots.experts.sieve.expert`

**Parameters:**

**`file`**

(required, string) Path to sieve file. Syntax can be validated with `intelmq_sieve_expert_validator`.

**Examples**

The following excerpts illustrate some of the basic features of the sieve file format:

```
if :exists source.fqdn {
 keep // aborts processing of subsequent rules and forwards the event.
}


if :notexists source.abuse_contact || source.abuse_contact =~ '.*@example.com' {
 drop // aborts processing of subsequent rules and drops the event.
}

if source.ip << '192.0.0.0/24' {
 add! comment = 'bogon' // sets the field comment to this value and overwrites existing values
 path 'other-path' // the message is sent to the given path
}

if classification.type :in ['phishing', 'malware-distribution'] && source.fqdn =~ '.*.(ch|li)$' {
 add! comment = 'domainabuse'
 keep
} elif classification.type == 'scanner' {
 add! comment = 'ignore'
 drop
} else {
 remove comment
}
```

**Reference**

*Sieve File Structure*

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

Nested if-statements and mixed if statements and rules in the same scope are possible.

*Expressions*

Each rule specifies on or more expressions to match an event based on its keys and values. Event keys are specified as
strings without quotes. String values must be enclosed in single quotes. Numeric values can be specified as integers or
floats and are unquoted. IP addresses and network ranges (IPv4 and IPv6) are specified with quotes. List values for use
with list/set operators are specified as string, float, int, bool and string literals separated by commas and enclosed
in square brackets. Expression statements can be combined and chained using parentheses and the boolean operators `&&`
and `||`. The following operators may be used to match events:

- `:exists` and `:notexists` match if a given key exists, for example:

```
if :exists source.fqdn { ... }
```

- `==` and `!=` match for equality of strings, numbers, and booleans, for example:

```
if feed.name != 'acme-security' || feed.accuracy == 100 || extra.false_positive == false { ... }
```

- `:contains` matches on substrings.

- `=~` matches strings based on the given regular expression. `!~` is the inverse regular expression match.

- Numerical comparisons are evaluated with `<`, `<=`, `>`, `>=`.

- `<<` matches if an IP address is contained in the specified network range:

```
if source.ip << '10.0.0.0/8' { ... }
```

- String values to match against can also be specified as lists of strings, which have separate operators. For example:

```
if source.ip :in ['8.8.8.8', '8.8.4.4'] { ... }
```

In this case, the event will match if it contains a key `source.ip` with either value `8.8.8.8` or `8.8.4.4`.

There are also `:containsany` to match at least one of a list of substrings, and `:regexin` to match at least one of a
list of regular expressions, similar to the `:contains` and `=~` operators.

- Lists of numeric values support `:in` to check for inclusion in a list of numbers:

```
if source.port :in [80, 443] { ... }
```

- `:equals` tests for equality between lists, including order. Example for checking a hostname-port pair:

```
if extra.host_tuple :equals ['dns.google', 53] { ... }
```

- `:setequals` tests for set-based equality (ignoring duplicates and value order) between a list of given values.
  Example for checking for the first nameserver of two domains, regardless of the order they are given in the list:

```
if extra.hostnames :setequals ['ns1.example.com', 'ns1.example.mx'] { ... }
```

- `:overlaps` tests if there is at least one element in common between the list specified by a key and a list of values.
  Example for checking if at least one of the ICS, database or vulnerable tags is given:

```
if extra.tags :overlaps ['ics', 'database', 'vulnerable'] { ... }
```

- `:subsetof` tests if the list of values from the given key only contains values from a set of values specified as the
  argument. Example for checking for a host that has only ns1.example.com and/or ns2.* as its apparent hostname:

```
if extra.hostnames :subsetof ['ns1.example.com', 'ns2.example.com'] { ... }
```

- `:supersetof` tests if the list of values from the given key is a superset of the values specified as the argument.
  Example for matching hosts with at least the IoT and vulnerable tags:

```
if extra.tags :supersetof ['iot', 'vulnerable'] { ... }
```

* `:before` tests if the date value occurred before given time ago. The time might be absolute (basically anything parseable by pendulum parser, eg. “2015-09-12T06:22:11+00:00”) or relative (accepted string formatted like this “<integer> <epoch>”, where epoch could be any of following strings (could optionally end with trailing ‘s’): hour, day, week, month, year)

```
if time.observation :before '1 week' { ... }
```
  
* `:after`  tests if the date value occurred after given time ago; see `:before`
  
```
if time.observation :after '2015-09-12' { ... }  # happened after midnight the 12th Sep
```

- Boolean values can be matched with `==` or `!=` followed by `true` or `false`. Example:

```
if extra.has_known_vulns == true { ... }
```

- The combination of multiple expressions can be done using parenthesis and boolean operators:

```
if (source.ip == '127.0.0.1') && (comment == 'add field' || classification.taxonomy == 'vulnerable') { ... }
```

- Any single expression or a parenthesised group of expressions can be negated using `!`:

```
if ! source.ip :contains '127.0.0.' || ! ( source.ip == '172.16.0.5' && source.port == 25 ) { ... }
```

!!! note Since 3.0.0, list-based operators are used on list values, such as `foo :in [1, 2, 3]` instead
of `foo == [1, 2, 3]` and `foo :regexin ['.mx', '.zz']` rather than `foo =~ ['.mx', '.zz']`, and similarly
for `:containsany` vs `:contains`. Besides that, `:notcontains` has been removed, with
e.g `foo :notcontains ['.mx', '.zz']` now being represented using negation as `! foo :contains ['.mx', '.zz']`.

*Actions*

If part of a rule matches the given conditions, the actions enclosed in `{` and `}` are applied. By default, all events
that are matched or not matched by rules in the sieve file will be forwarded to the next bot in the pipeline, unless
the `drop` action is applied.

- `add` adds a key value pair to the event. It can be a string, number, or boolean. This action only applies if the key
  is not yet defined in the event. If the key is already defined, the action is ignored. Example:

```
add comment = 'hello, world'
```

Some basic mathematical expressions are possible, but currently support only relative time specifications objects are
supported. For example:

```
add time.observation += '1 hour'
add time.observation -= '10 hours'
```

- `add!` same as above, but will force overwrite the key in the event.

- `update` modifies an existing value for a key. Only applies if the key is already defined. If the key is not defined
  in the event, this action is ignored. This supports mathematical expressions like above. Example:

```
update feed.accuracy = 50
```

Some basic mathematical expressions are possible, but currently support only relative time specifications objects are
supported. For example:

```
update time.observation += '1 hour'
update time.observation -= '10 hours'
```

- `remove` removes a key/value from the event. Action is ignored if the key is not defined in the event. Example:

```
remove extra.comments
```

- `keep` sends the message to the next bot in the pipeline (same as the default behaviour), and stops sieve rules
  processing.

- `path` sets the path (named queue) the message should be sent to (implicitly or with the command `keep`. The named
  queue needs to configured in the pipeline, see the User Guide for more information.

```
path 'named-queue'
```

You can as well set multiple destination paths with the same syntax as for value lists:

```
path ['one', 'two']
```

This will result in two identical message, one sent to the path `one` and the other sent to the path `two`.

If the path is not configured, the error looks like:

```
File "/path/to/intelmq/intelmq/lib/pipeline.py", line 353, in send for destination_queue in self.destination_queues path]: KeyError: 'one'
```

- `drop` marks the event to be dropped. The event will not be forwarded to the next bot in the pipeline. The sieve file
  processing is interrupted upon reaching this action. No other actions may be specified besides the `drop` action
  within `{` and `}`.

*Comments*

Comments may be used in the sieve file: all characters after `//` and until the end of the line will be ignored.

---

### Splunk Saved Search Lookup <div id="intelmq.bots.experts.splunk_saved_search.expert" />

Runs a saved search in Splunk using fields in an event, adding fields from the search result into the event.

Splunk documentation on saved
searches: <https://docs.splunk.com/Documentation/Splunk/latest/Report/Createandeditreports>

The saved search should take parameters according to the `search_parameters` configuration and deliver results according
to `result_fields`. The examples above match a saved search of this format:

```
index="dhcp" ipv4address="$ip$" | ... | fields _time username ether
```

The time window used is the one saved with the search.

Waits for Splunk to return an answer for each message, so slow searches will delay the entire botnet. If you anticipate
a load of more than one search every few seconds, consider running multiple load-balanced copies of this bot.

**Module:** `intelmq.bots.experts.splunk_saved_search.expert`

**Parameters (also expects [HTTP parameters](#http-parameters)):**

**`auth_token`**

(required, string) Splunk API authentication token.

**`url`**

(required, string) base URL of the Splunk REST API.

**`retry_interval`**

(optional, integer) Number of seconds to wait between polling for search results to be available. Defaults to 5.

**`saved_search`**

(required, string) Name of Splunk saved search to run.

**`search_parameters`**

(optional, object) Mapping of IntelMQ event fields containing the data to search for to parameters of the Splunk saved
search. Defaults to `{}`. Example:

```yaml
search_parameters:
  source.ip: ip
```

**`result_fields`**

(optional, object) Mapping of Splunk saved search result fields to IntelMQ event fields to store the results in.
Defaults to `{}`. Example:

```yaml
result_fields:
  username: source.account
```

**`not_found`**

(optional, array of strings) How to handle empty search results. Allowed values:

- `warn` - log a warning message
- `send` - send the event on unmodified
- `drop` - drop the message
- `send` - and `drop` are mutually exclusive

All specified actions are performed. Defaults to `[ "warn", "send" ]`.

**`multiple_result_handling`**

(optional, array of strings) How to handle more than one search result. Allowed values:

- `limit` - limit the search so that duplicates are impossible
- `warn` - log a warning message
- `use_first` - use the first search result
- `ignore` - do not modify the event
- `send` - send the event on
- `drop` - drop the message
- `limit` cannot be combined with any other value
- `send` and `drop` are mutually exclusive
- `ignore` and `use_first` are mutually exclusive

All specified actions are performed. Defaults to `["warn", "use_first", "send" ]`.

**`overwrite`**

(optional, boolean/null) Whether search results overwrite values already in the message or not. If null, attempting to add a field that already exists throws an exception. Defaults to null.

---

### Taxonomy <div id="intelmq.bots.experts.taxonomy.expert" />

This bot adds the `classification.taxonomy` field according to the RSIT taxonomy.

Please note that there is a slight mismatch of IntelMQ's taxonomy to the upstream taxonomy. See also this [issue](https://github.com/certtools/intelmq/issues/1409).

Information on the "Reference Security Incident Taxonomy" can be found here: <https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force>

For brevity, "type" means `classification.type` and "taxonomy" means `classification.taxonomy`.

- If taxonomy is missing, and type is given, the according taxonomy is set.
- If neither taxonomy, not type is given, taxonomy is set to "other" and type to "unknown".
- If taxonomy is given, but type is not, type is set to "unknown".

**Module:** `intelmq.bots.experts.taxonomy.expert`

No additional parameters.

---

### Threshold <div id="intelmq.bots.experts.threshold.expert" />

Check if the number of similar messages during a specified time interval exceeds a set value.

**Limitations**

This bot has certain limitations and is not a true threshold filter (yet). It works like this:

1. Every incoming message is hashed according to the `filter_*` parameters.
2. The hash is looked up in the cache and the count is incremented by 1, and the TTL of the key is (re-)set to the    timeout.
3. If the new count matches the threshold exactly, the message is forwarded. Otherwise it is dropped.

!!! note
    Even if a message is sent, any further identical messages are dropped, if the time difference to the last message is less than the timeout! The counter is not reset if the threshold is reached.

**Module:** `intelmq.bots.experts.threshold.expert`

**Parameters (also expects [cache parameters](#cache-parameters)):**

**`filter_keys`**

(required, string/array of strings) Array or comma-separated list of field names to consider or ignore when determining which messages are similar.

**`filter_type`**

(required, string) Allowed values: `whitelist` or `blacklist`. When `whitelist` is used, only lines containing the text
specified in `filter_text` option will be processed. When `blacklist` is used, only lines NOT containing the text will
be processed.

**`threshold`**

(required, integer) Number of messages required before propagating one. In forwarded messages, the threshold is saved in the message as `extra.count`.

**`add_keys`**

(optional, object) List of keys and their respective values to add to the propagated messages. Example:

```yaml
add_keys:
  classification.type: "spam"
  comment: "Started more than 10 SMTP connections"
```

---

### Tor Exit Node <div id="intelmq.bots.experts.tor_nodes.expert" />

This bot uses an offline database to determine whether the host is a Tor exit node.

**Module:** `intelmq.bots.experts.tor_nodes.expert`

**Parameters:**

**`database`**

(required, string) Path to the database file.

**Database**

Use this command to create/update the database and reload the bot:

```bash
intelmq.bots.experts.tor_nodes.expert --update-database
```

---

### Trusted Introducer Lookup <div id="intelmq.bots.experts.trusted_introducer_lookup.expert" />

Lookups data from Trusted Introducer public teams list.

**Module:** `intelmq.bots.experts.trusted_introducer_lookup.expert`

**Parameters:**

**`order`**

(required, string) Allowed values: `domain` and `asn`. You can set multiple values, so first match wins.

- When `domain` is set, it will lookup the `source.fqdn` field. It will go from high-order to low-order, i.e.
  `1337.super.example.com -> super.example.com -> example.com -> .com`
- If `asn` is set, it will lookup `source.asn`.

After a match, the abuse contact will be fetched from the trusted introducer teams list and will be stored in the event
as `source.abuse_contact`. If there is no match, the event will not be enriched and will be sent to the next configured
step.

---

### Tuency <div id="intelmq.bots.experts.tuency.expert" />

Queries the [IntelMQ API](https://gitlab.com/intevation/tuency/tuency/-/blob/master/backend/docs/IntelMQ-API.md)
of a [Tuency Contact Database](https://gitlab.com/intevation/tuency/tuency/) instance.

*Tuency* is a contact management database addressing the needs of CERTs. Users of *tuency* can configure contact
addresses and delivery settings for IP objects (addresses, netblocks), Autonomous Systems, and
(sub-)domains. This expert queries the information for `source.ip` and
`source.fqdn` using the following other fields:

- `classification.taxonomy`
- `classification.type`
- `feed.provider`
- `feed.name`

These fields therefore need to exist, otherwise the message is skipped.

The API parameter "feed_status" is currently set to "production" constantly, until IntelMQ supports this field.

The API answer is processed as following. For the notification interval:

- If *suppress* is true, then `extra.notify` is set to false.
- Otherwise:
- If the interval is *immediate*, then `extra.ttl` is set to 0.
- Otherwise the interval is converted into seconds and saved in
  `extra.ttl`.

For the contact lookup: For both fields *ip* and *domain*, the
*destinations* objects are iterated and its *email* fields concatenated to a comma-separated list
in `source.abuse_contact`.

The IntelMQ fields used by this bot may change in the next IntelMQ release, as soon as better suited fields are
available.

**Module:** `intelmq.bots.experts.tuency.expert`

**Parameters:**

**`url`**

(required, string) Tuency instance URL. Without the API path.

**`authentication_token`**

(required, string) The Bearer authentication token. Without the `Bearer` prefix.

**`overwrite`**

(optional, boolean) Whether the existing data in `source.abuse_contact` should be overwritten. Defaults to true.

---

### Truncate By Delimiter <div id="intelmq.bots.experts.truncate_by_delimiter.expert" />

Cut string if length is bigger than maximum length.

**Module:** `intelmq.bots.experts.truncate_by_delimiter.expert`

**Parameters:**

**`delimiter`**

(required, string) The delimiter to be used for truncating. Defaults to `.`.

**`max_length`**

(required, integer) The maximum string length.

**`field`**

(required, string) The field to be truncated, e.g. `source.fqdn`. The given field is truncated step-by-step using the delimiter from the beginning, until the field is shorter than `max_length`.

Example: Cut through a long domain with a dot. The string is truncated until the domain does not exceed the configured
maximum length.

- Input domain (e.g. `source.fqdn`): `www.subdomain.web.secondsubomain.test.domain.com`
- `delimiter`: `.`
- `max_length`: 20
- Resulting value `test.domain.com` (length: 15 characters)

---

### URL <div id="intelmq.bots.experts.url.expert" />

This bot extracts additional information from `source.url` and `destination.url` fields. It can fill the following
fields:

- `source.fqdn`
- `source.ip`
- `source.port`
- `source.urlpath`
- `source.account`
- `destination.fqdn`
- `destination.ip`
- `destination.port`
- `destination.urlpath`
- `destination.account`
- `protocol.application`
- `protocol.transport`

**Module:** `intelmq.bots.experts.url.expert`

**Parameters:**

**`overwrite`**

(optional, boolean) Whether to overwrite existing fields. Defaults to false.

**`skip_fields`**

(optional, array of string) An array of field names that shouldn't be extracted from the URL.

---

### Url2FQDN <div id="intelmq.bots.experts.url2fqdn.expert" />

This bot is deprecated and will be removed in version 4.0. Use [URL Expert](#intelmq.bots.experts.url.expert) bot instead.

This bot extracts the Host from the `source.url` and `destination.url` fields and writes it to `source.fqdn` or `destination.fqdn` if it is a hostname, or `source.ip` or `destination.ip` if it is an IP address.

**Module:** `intelmq.bots.experts.url2fqdn.expert`

**Parameters:**

**`overwrite`**

(optional, boolean) Whether to overwrite existing fields. Defaults to false.

---

### uWhoisd <div id="intelmq.bots.experts.uwhoisd.expert" />

[uWhoisd](https://github.com/Lookyloo/uwhoisd) is a universal Whois server that supports caching and stores whois
entries for historical purposes.

The bot sends a request for `source.url`, `source.fqdn`, `source.ip` or `source.asn` to the configured uWhoisd instance and saves the retrieved whois entry:

- If both `source.url` and `source.fqdn` are present, it will only do a request for `source.fqdn`, as the hostname of `source.url` should be the same as `source.fqdn`. The whois entry will be saved in `extra.whois.fqdn`.
- If `source.ip` is present, the whois entry will be saved in `extra.whois.ip`.
- If `source.asn` is present, he whois entry will be saved in `extra.whois.asn`.

Events without `source.url`, `source.fqdn`, `source.ip`, or `source.asn`, are ignored.

!!! note
    Requesting a whois entry for a fully qualified domain name (FQDN) only works if the request only contains the domain. uWhoisd will automatically strip the subdomain part if it is present in the request.

Example: `https://www.theguardian.co.uk`

- TLD: `co.uk` (uWhoisd uses the [Mozilla public suffix list](https://publicsuffix.org/list/) as a reference)
- Domain: `theguardian.co.uk`
- Subdomain: `www`

The whois request will be for `theguardian.co.uk`

**Module:** `intelmq.bots.experts.uwhoisd.expert`

**Parameters:**

**`server`**

(optional, string) Hostname of the uWhoisd server. Defaults to localhost.

**`port`**

(optional, integer) Port of the uWhoisd server. Defaults to 4243.

---

### Wait <div id="intelmq.bots.experts.wait.expert" />

Waits for a some time or until a queue size is lower than a given number.

Only one of the two modes is possible. If a queue name is given, the queue mode is active. If the sleep_time is a
number, sleep mode is active. Otherwise the dummy mode is active, the events are just passed without an additional
delay.

Note that SIGHUPs and reloads interrupt the sleeping.

**Module:** `intelmq.bots.experts.wait.expert`

**Parameters:**

**`queue_db`**

(optional, integer) Database number of the database. Defaults to 2.

**`queue_host`**

(optional, string) Hostname of the database. Defaults to localhost.

**`queue_name`**

(optional, string) Name of the queue to be watched. This is not the name of a bot but the queue's name. Defaults to null.

**`queue_password`**

(optional, string) Password for the database. Defaults to null.

**`queue_polling_interval`**

(required, float) Interval to poll the list length in seconds. Defaults to ?.

**`queue_port`**

(optional, integer) Port of the database. Defaults to 6379.

**`queue_size`**

(optional, integer) Maximum size of the queue. Defaults to 0.

**`sleep_time`**

(optional, integer) Time to sleep before sending the event. Defaults to null.

## Output Bots

### AMQP Topic <div id="intelmq.bots.outputs.amqptopic.output" />

Sends the event to a specified topic of an AMQP server

Sends data to an AMQP Server See
<https://www.rabbitmq.com/tutorials/amqp-concepts.html> for more details on amqp topic exchange.

Requires the [pika python library](https://pypi.org/project/pika/).

**Module:** `intelmq.bots.outputs.amqptopic.output`

**Parameters:**

**`connection_attempts`**

(optional, integer) The number of connection attempts to defined server. Defaults to 3.

**`connection_heartbeat`**

(optional, integer) Heartbeat to server (in seconds). Defaults to 3600.

**`connection_host`**

(optional, string) Hostname of the AMQP server. Defaults to 127.0.0.1.

**`connection_port`**

(optional, integer) Port of the AMQP server. Defaults to 5672.

**`connection_vhost`**

(optional, string) Virtual host to connect, on an http(s) connection would be `http://IP/<your virtual host>`.

**`content_type`**

(optional, string) Content type to deliver to AMQP server. Currently only supports `application/json`.

**`delivery_mode`**

(optional, integer) Allowed values:

- `1` - Non-persistent delivery.
- `2` - Persistent delivery. Messages are delivered to 'durable' queues and will be saved to disk.

**`exchange_durable`**

(optional, boolean) When set to true, the exchange will survive broker restart, otherwise will be a transient exchange.

**`exchange_name`**

(optional, string) The name of the exchange to use.

**`exchange_type`**

(optional, string) Type of the exchange, e.g. `topic`, `fanout` etc.

**`keep_raw_field`**

(optional, boolean) Whether to keep the `raw` field or not. Defaults to false.

**`password`**

(optional, boolean) Password for authentication on your AMQP server. Leave empty if authentication is not required.

**`require_confirmation`**

(optional, boolean) If set to True, an exception will be raised if a confirmation error is received.

**`routing_key`**

(required, string) The routing key for your amqptopic.

**`single_key`**

(optional, boolean) Only send the field instead of the full event (expecting a field name as string). Defaults to false.

**`username`**

(required, string) Username for authentication on your AMQP server.

**`use_ssl`**

(optional, boolean) Use ssl for the connection, make sure to also set the correct port, usually 5671. Defaults to false.

**`message_hierarchical_output`**

(optional, boolean) Convert the message to hierarchical JSON. Defaults to false.

**`message_with_type`**

(optional, boolean) Whether to include the type in the sent message. Defaults to false.

**`message_jsondict_as_string`**

(optional, boolean) Whether to convert JSON fields (`extra`) to string. Defaults to false.

**Examples of usage**

- Useful to send events to a RabbitMQ exchange topic to be further processed in other platforms.

**Confirmation**

If routing key or exchange name are invalid or non existent, the message is accepted by the server but we receive no
confirmation. If parameter require_confirmation is True and no confirmation is received, an error is raised.

**Common errors**

*Unroutable messages / Undefined destination queue*

The destination exchange and queue need to exist beforehand, with your preferred settings (e.g. durable, [lazy queue](https://www.rabbitmq.com/lazy-queues.html). If the error message says that the message is "unroutable", the queue doesn't exist.

---

### Blackhole <div id="intelmq.bots.outputs.blackhole.output" />

This bot discards all incoming messages.

**Module:** `intelmq.bots.outputs.blackhole.output`

No additional parameters.

---

### Bro File <div id="intelmq.bots.outputs.bro_file.output" />

This bot outputs to BRO (zeek) file.

File example:

```
#fields indicator indicator_type meta.desc meta.cif_confidence meta.source xxx.xxx.xxx.xxx Intel::ADDR phishing 100 MISP XXX www.testdomain.com Intel::DOMAIN apt 85 CERT
```

**Module:** `intelmq.bots.outputs.bro_file.output`

No additional parameters.

---

### CIFv3 API <div id="intelmq.bots.outputs.cif3.output" />

This bot outputs to a CIFv3 API instance and adds new indicator if not there already.

By default, CIFv3 does an upsert check and will only insert entirely new indicators. Otherwise,
upsert matches will have their count increased by 1. By default, the CIF3 output bot will batch indicators
up to 500 at a time prior to doing a single bulk send. If the output bot doesn't receive a full 500
indicators within 5 seconds of the first received indicator, it will send what it has so far.

CIFv3 should be able to process indicators as fast as IntelMQ can
send them.

**Module:** `intelmq.bots.outputs.cif3.output`

**Parameters:**

**`add_feed_provider_as_tag`**

(required, boolean) Use `false` when in doubt.

**`cif3_additional_tags`**

(required, array of strings) An array of tags to set on submitted indicator(s).

**`cif3_feed_confidence`**

(required, float) Used when mapping a feed's confidence fails or if static confidence parameter is true.

**`cif3_static_confidence`**

(required, boolean) Whether to always use `cif3_feed_confidence` value as confidence rather than dynamically interpret feed value (use `false` when in doubt).

**`cif3_token`**

(required, string) Token key for accessing CIFv3 API.

**`cif3_url`**

(required, string) URL of the CIFv3 instance.

**`fireball`**

(required, integer) Used to batch events before submitting to a CIFv3 instance, use 0 to disable batch and send each event as received. Defaults to 500.

**`http_verify_cert`**

(optional, boolean) Verify the TLS certificate of the server. Defaults to true.



---

### Elasticsearch <div id="intelmq.bots.outputs.elasticsearch.output" />

This bot outputs to Elasticsearch.

**Module:** `intelmq.bots.outputs.elasticsearch.output`

- `lookup`: yes
- `public`: yes
- `cache`: no
- `description`: Output Bot that sends events to Elasticsearch

Only ElasticSearch version 7 supported.

It is also possible to feed data into ElasticSearch using ELK-Stack via Redis and Logstash, see `ELK-Stack`
{.interpreted-text role="doc"} for more information. This methods supports various different versions of ElasticSearch.

**Parameters:**

**`elastic_host`**

(optional, string) Name/IP for the Elasticsearch server. Defaults to 127.0.0.1.

**`elastic_port`**

(optional, int) Port for the Elasticsearch server. Defaults to 9200.

**`elastic_index`**

(optional, string) Index for the Elasticsearch output. Defaults to intelmq.

**`rotate_index`**

(optional, string) Allowed values: `never`, `daily`, `weekly`, `monthly` or `yearly`. If set, will index events using the date information associated with the event. Defaults to never.

Using 'intelmq' as the `elastic_index`, the following are examples of the generated index names:

```
'never' --> intelmq
'daily' --> intelmq-2018-02-02
'weekly' --> intelmq-2018-42
'monthly' --> intelmq-2018-02
'yearly' --> intelmq-2018
```

**`http_username`**

(optional, string) HTTP basic authentication username.

**`http_password`**

(optional, string) HTTP basic authentication password.

**`use_ssl`**

(optional, boolean) Whether to use SSL/TLS when connecting to Elasticsearch. Defaults to false.

**`http_verify_cert`**

(optional, boolean) Whether to require verification of the server's certificate. Defaults to false.

**`ssl_ca_certificate`**

(optional, string) Path to trusted CA certificate.

**`ssl_show_warnings`**

(optional, boolean) Whether to show warnings if the server's certificate cannot be verified. Defaults to true.

**`replacement_char`**

(optional, string) If set, dots ('.') in field names will be replaced with this character prior to indexing. This is for backward compatibility with ES 2.X. Defaults to null. Recommended for Elasticsearch 2.X: `_`

**`flatten_fields`**

(optional, array of strings) In ES, some query and aggregations work better if the fields are flat and not JSON. Here you can provide a list of fields to convert. Defaults to `['extra']`.

Can be a list of strings (fieldnames) or a string with field names separated by a comma (,). eg `extra,field2` or `['extra', 'field2']`.

See `contrib/elasticsearch/elasticmapper` for a utility for creating Elasticsearch mappings and templates.

If using `rotate_index`, the resulting index name will be of the form `elastic_index`-`event date`. To query all intelmq
indices at once, use an alias (<https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html>), or a multi-index query.

The data in ES can be retrieved with the HTTP-Interface:

```bash
 curl -XGET 'http://localhost:9200/intelmq/events/_search?pretty=True'
```

---

### File <div id="intelmq.bots.outputs.file.output" />

This bot outputs messages (reports or events) to a file.

Multihreading is disabled for this bot, as this would lead to corrupted files.

**Module:** `intelmq.bots.outputs.file.output`

**Parameters:**

**`encoding_errors_mode`**

(optional, string) See for more details and options: <https://docs.python.org/3/library/functions.html#open> For example with `backslashreplace` all characters which cannot be properly encoded will be written escaped with backslashes. Defaults to `strict`.

**`file`**

(optional, string) Path to the output file. Missing directories will be created if possible with the mode 755. Defaults to `/opt/intelmq/var/lib/bots/file-output/events.txt`.

**`format_filename`**

(optional, boolean) Whether the file name should be formatted. Defaults to false.

Uses Python formatted strings. See: <https://docs.python.org/3/library/string.html#formatstrings>

Example:

- The filename `.../{event[source.abuse_contact]}.txt` will be (for example) `.../abuse@example.com.txt`.
- `.../{event[time.source]:%Y-%m-%d}` results in the date of the event used as filename.

If the field used in the format string is not defined, `None` will be used as fallback.

**`hierarchical_output`**

(optional, boolean) Whether the resulting dictionary should be hierarchical (field names split by a dot). Defaults to false.

**`single_key`**

(optional, string) Output only a single specified key. In case of `raw` key the data is base64 decoded. Defaults to null (output the whole message).

---

### Files <div id="intelmq.bots.outputs.files.output" />

This bot outputs each message to a separate file.

**Module:** `intelmq.bots.outputs.files.output`

**Parameters:**

**`dir`**

(optional, string) Path to the output directory. Defaults to `/opt/intelmq/var/lib/bots/files-output/incoming`.

**`tmp`**

(optional, string) Temporary directory to use (must reside on the same filesystem as `dir`). Defaults to `/opt/intelmq/var/lib/bots/files-output/tmp`.

**`suffix`**

(optional, strings) Extension of created files. Defaults to .json.

**`hierarchical_output`**

(optional, boolean) Whether the resulting dictionary should be hierarchical (field names split by a dot). Defaults to false.

**`single_key`**

(optional, string) Output only a single specified key. In case of `raw` key the data is base64 decoded. Defaults to null (output the whole message).

---

### McAfee Enterprise Security Manager <div id="intelmq.bots.outputs.mcafee.output_esm_ip" />

This bot outputs messages to McAfee Enterprise Security Manager watchlist.

**Module:** `intelmq.bots.outputs.mcafee.output_esm_ip`

**Parameters:**

- **Feed parameters** (see above)

**`esm_ip`**

(optional, string) Hostname of the ESM server. Defaults to 1.2.3.4.

**`esm_user`**

(optional, string) Username of user entitled to write to watchlist. Defaults to NGCP.

**`esm_pw`**

(required, string) Password of user entitled to write to watchlist.

**`esm_watchlist`**

(required, string) Name of the watchlist to write to.

**`field`**

(optional, string) Name of the IntelMQ field to be written to ESM. Defaults to source.ip.

---

### MISP Feed <div id="intelmq.bots.outputs.misp.output_feed" />

Create a directory layout in the MISP Feed format.

The PyMISP library >= 2.4.119.1 is required, see
[REQUIREMENTS.txt](https://github.com/certtools/intelmq/blob/master/intelmq/bots/outputs/misp/REQUIREMENTS.txt).

**Module:** `intelmq.bots.outputs.misp.output_feed`

**Parameters:**

- **Feed parameters** (see above)

**`misp_org_name`**

() Org name which creates the event, string

**`misp_org_uuid`**

() Org UUID which creates the event, string

**`output_dir`**

() Output directory path, e.g.
[/opt/intelmq/var/lib/bots/mispfeed-output]. Will be created if it does not exist and possible.

**`interval_event`**

() The output bot creates one event per each interval, all data in this time frame is part of this event. Default "1
hour", string.

**Usage in MISP**

Configure the destination directory of this feed as feed in MISP, either as local location, or served via a web server.
See [the MISP documentation on Feeds](https://www.circl.lu/doc/misp/managing-feeds)
for more information

---

### MISP API <div id="intelmq.bots.outputs.misp.output_api" />

**Module:** `intelmq.bots.outputs.misp.output_api`

Connect to a MISP instance and add event as MISPObject if not there already.

The PyMISP library >= 2.4.120 is required, see
[REQUIREMENTS.txt](https://github.com/certtools/intelmq/blob/master/intelmq/bots/outputs/misp/REQUIREMENTS.txt).

**Parameters:**

- **Feed parameters** (see above)

**`add_feed_provider_as_tag`**

() boolean (use [true] when in doubt)

**`add_feed_name_as_tag`**

() boolean (use [true] when in doubt)

**`misp_additional_correlation_fields`**

() list of fields for which the correlation flags will be enabled (in addition to those which are in significant_fields)

**`misp_additional_tags`**

() list of tags to set not be searched for when looking for duplicates

**`misp_key`**

() string, API key for accessing MISP

**`misp_publish`**

() boolean, if a new MISP event should be set to "publish".

Expert setting as MISP may really make it "public"! (Use
[false] when in doubt.)

**`misp_tag_for_bot`**

() string, used to mark MISP events

**`misp_to_ids_fields`**

() list of fields for which the
[to_ids] flags will be set

**`misp_url`**

() string, URL of the MISP server

**`significant_fields`**

() list of intelmq field names

The `significant_fields` values will be searched for in all MISP attribute values and if all values are found in the
same MISP event, no new MISP event will be created. Instead if the existing MISP events have the same feed.provider and
match closely, their timestamp will be updated.

If a new MISP event is inserted the `significant_fields` and the `misp_additional_correlation_fields`
will be the attributes where correlation is enabled.

Make sure to build the IntelMQ Botnet in a way the rate of incoming events is what MISP can handle, as IntelMQ can
process many more events faster than MISP (which is by design as MISP is for manual handling). Also remove the fields of
the IntelMQ events with an expert bot that you do not want to be inserted into MISP.

(More details can be found in the docstring of
[output_api.py](https://github.com/certtools/intelmq/blob/master/intelmq/bots/outputs/misp/output_api.py).

---

### MongoDB <div id="intelmq.bots.outputs.mongodb.output" />

MongoDB is the bot responsible to send events to a MongoDB database

Saves events in a MongoDB either as hierarchical structure or flat with full key names. `time.observation`
and `time.source` are saved as datetime objects, not as ISO formatted string.

**Module:** `intelmq.bots.outputs.mongodb.output`

**Requirements**

```bash
pip3 install pymongo>=2.7.1
```

The bot has been tested with pymongo versions 2.7.1, 3.4 and 3.10.1
(server versions 2.6.10 and 3.6.8).

**Parameters:**

**`host`**

(optional, string) Hostname of the MongoDB server. Defaults to localhost.

**`port`**

(optional, integer) Port of the MongoDB server. Defaults to 27017.

**`database`**

(required, string) Name of the MongoDB database to use.

**`db_user`**

(optional, string) User that should be used if authentication is required.

**`db_pass`**

(optional, string) Password.

**`collection`**

(required, string) Name of the MongoDB collection to use.

**`hierarchical_output`**

(optional, boolean) MongoDB does not allow saving keys with dots, we split the dictionary in sub-dictionaries. Defaults to true.

**`replacement_char`**

(optional, string) Replacement character for replacing the dots in key names if hierarchical output is not used. Defaults to `_`.

---

### Redis <div id="intelmq.bots.outputs.redis.output" />

This bot outputs events to a remote Redis server/queue.

**Examples of usage**

- Can be used to send events to be processed in another system. E.g.: send events to Logstash.
- In a multi tenant installation can be used to send events to external/remote IntelMQ instance. Any expert bot queue
  can receive the events.
- In a complex configuration can be used to create logical sets in IntelMQ-Manager.

**Module:** `intelmq.bots.outputs.redis.output`

**Parameters:**

**`redis_server_ip`**

(optional, string) Hostname of the Redis server. Defaults to 127.0.0.1.

**`redis_server_port`**

(optional, integer) Port of the Redis server. Defaults to 6379.

**`redis_db`**

(optional, integer) Redis database number. Defaults to 2.

**`redis_password`**

(optional, string) Redis server password. Defaults to null.

**`redis_queue`**

(required, string) Redis queue name (such as `remote-server-queue`).

**`redis_timeout`**

(optional, integer) Connection timeout, in milliseconds. Defaults to 5000.

**`hierarchical_output`**

(optional, boolean) Whether the resulting dictionary should be hierarchical (field names split by a dot). Defaults to false.

**`with_type`**

(optional, boolean) Whether to include `__type` field. Defaults to true.

---

### Request Tracker <div id="intelmq.bots.outputs.rt.output" />

Output Bot that creates Request Tracker tickets from events.

**Module:** `intelmq.bots.outputs.rt.output`

**Description**

The bot creates tickets in Request Tracker and uses event fields for the ticket body text. The bot follows the workflow
of the RTIR:

- create ticket in Incidents queue (or any other queue)
- all event fields are included in the ticket body,
- event attributes are assigned to tickets' CFs according to the attribute mapping,
- ticket taxonomy can be assigned according to the CF mapping. If you use taxonomy different
  from [ENISA RSIT](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force), consider using some
  extra attribute field and do value mapping with modify or sieve bot,
- create linked ticket in Investigations queue, if these conditions are met
- if first ticket destination was Incidents queue,
- if there is source.abuse_contact is specified,
- if description text is specified in the field appointed by configuration,
- RT/RTIR supposed to do relevant notifications by script working on condition "On Create",
- configuration option investigation_fields specifies which event fields has to be included in the investigation,
- Resolve Incident ticket, according to configuration (Investigation ticket status should depend on RT script
  configuration),

Take extra caution not to flood your ticketing system with enormous amount of tickets. Add extra filtering for that to
pass only critical events to the RT, and/or deduplicating events.

**Parameters:**

**`rt_uri`**

()

**`rt_user`**

()

**`rt_password`**

()

**`verify_cert`**

() RT API endpoint connection details, string.

**`queue`**

() ticket destination queue. If set to 'Incidents', 'Investigations' ticket will be created if create_investigation is set to true, string.

**`CF_mapping`**

(optional, object) Mapping event fields to ticket CFs. Defaults to:

```yaml
classification.taxonomy: Classification
classification.type: Incident Type
event_description.text: Description
extra.incident.importance: Importance
extra.incident.severity: Incident Severity
extra.organization.name: Customer
source.ip: IP
```

**`final_status`**

(optional, string) The final status for the created ticket. Defaults to resolved. The linked Investigation ticket will be resolved automatically by RTIR scripts.

**`create_investigation`**

(optional, boolean) Whether an Investigation ticket should be created (in case of RTIR workflow). Defaults to false.

**`investigation_fields`**

(optional, string) Comma-separated string of attributes to include in an Investigation ticket. Defaults to `time.source,source.ip,source.port,source.fqdn,source.url,classification.taxonomy,classification.type,classification.identifier,event_description.url,event_description.text,malware.name,protocol.application,protocol.transport`.

**`description_attr`**

(optional, string) Event field to be used as a text message being sent to the recipient. If it is not specified or not found in the event, the Investigation ticket is not going to be created. Defaults to `event_decription.text`.

---

### REST API <div id="intelmq.bots.outputs.restapi.output" />

REST API is the bot responsible to send events to a REST API listener through POST.

**Module:** `intelmq.bots.outputs.restapi.output`

**Parameters:**

**`host`**

(required, host) Destination URL of the POST request.

**`auth_type`**

(required, string) Allowed values: `http_basic_auth` or `http_header`. Type of authentication to use.

**`auth_token`**

(required, string) Username or HTTP header key.

**`auth_token_name`**

(required, string) Password or HTTP header value.

**`hierarchical_output`**

(optional, boolean) Whether the resulting dictionary should be hierarchical (field names split by a dot). Defaults to false.

**`use_json`**

(optional, boolean) Whether to use JSON. Defaults to true.

---

### RPZ File <div id="intelmq.bots.outputs.rpz_file.output" />

This bot outputs events into DNS RPZ blocklist file used for "DNS firewall".

The prime motivation for creating this feature was to protect users from badness on the Internet related to
known-malicious global identifiers such as host names, domain names, IP addresses, or nameservers. More
information: <https://dnsrpz.info>

Example:
```
$TTL 3600 @ SOA rpz.yourdomain.eu. hostmaster.rpz.yourdomain.eu. 2105260601 60 60 432000 60 NS localhost. ; ;
yourdomain.eu. CERT.XX Response Policy Zones (RPZ) ; Last updated: 2021-05-26 06:01:41 (UTC) ; ; Terms Of
Use: https://rpz.yourdomain.eu ; For questions please contact rpz [at] yourdomain.eu ; *.maliciousdomain.com CNAME
rpz.yourdomain.eu. *.secondmaliciousdomain.com CNAME rpz.yourdomain.eu.
```

**Module:** `intelmq.bots.outputs.rpz_file.output`

**Parameters:**

**`cname`**

(optional, string) example rpz.yourdomain.eu

**`organization_name`**

(optional, string) Your organisation name

**`rpz_domain`**

(optional, string) Information website about RPZ

**`hostmaster_rpz_domain`**

() Technical website

**`rpz_email`**

() Contact email

**`ttl`**

() Time to live

**`ncachttl`**

() DNS negative cache

**`serial`**

() Time stamp or another numbering

**`refresh`**

() Refresh time

**`retry`**

() Retry time

**`expire`**

() Expiration time

**`test_domain`**

() For test domain, it's added in first rpz file (after header)

---

### SMTP <div id="intelmq.bots.outputs.smtp.output" />

Sends a MIME Multipart message containing the text and the event as CSV for every single event.

**Module:** `intelmq.bots.outputs.smtp.output`

**Parameters:**

**`fieldnames`**

(optional, string/array of strings) Array of field names (or comma-separated list) to be included in the email. If empty, no attachment is sent - this can be useful if the actual data is already in the body (parameter `text`) or the `subject`.

**`mail_from`**

(optional, string) Sender's e-email address. Defaults to `cert@localhost`.

**`mail_to`**

(required, string) Comma-separated string of recipient email addresses. Supports formatting.

**`smtp_host`**

(optional, string) Hostname of the SMTP server. Defaults to `localhost`.

**`smtp_password`**

(optional, string) Password for authentication to your SMTP server. Defaults to `null`.

**`smtp_port`**

(optional, integer) Port of the SMTP server. Defaults to 25.

**`smtp_username`**

(optional, string) Username for authentication to your SMTP server. Defaults to `null`.

**`fail_on_errors`**

(optional, boolean) Whether any error should cause the bot to fail (raise an exception) or otherwise rollback. If false, the bot eventually waits and re-try (e.g. re-connect) etc. to solve the issue. If true, the bot raises an exception and - depending on the IntelMQ error handling configuration - stops. Defaults to false.

**`ssl`**

(optional, boolean) Defaults to false.

**`starttls`**

(optional, boolean) Defaults to true.

**`subject`**

(optional, string) Subject of the e-mail message. Supports formatting. Defaults to `Incident in your AS {ev[source.asn]}`.

**`text`**

(optional, string) Body of the e-mail message. Supports formatting. Defaults to
```
Dear network owner,

We have been informed that the following device might have security problems.

Your localhost CERT
```

For several strings you can use values from the string using the [standard Python string format syntax](https://docs.python.org/3/library/string.html#format-string-syntax). Access the event's values with `{ev[source.ip]}` and similar. Any not existing fields will result in `None`. For example, to set the recipient(s) to the value given in the event's `source.abuse_contact` field, use this as `mail_to` parameter: `{ev[source.abuse_contact]}`

Authentication is optional. If both username and password are given, these mechanism are tried: CRAM-MD5, PLAIN, and LOGIN.

Client certificates are not supported. If `http_verify_cert` is true, TLS certificates are checked.

---

### SQL <div id="intelmq.bots.outputs.sql.output" />

SQL is the bot responsible to send events to a PostgreSQL, SQLite, or MSSQL Database.

!!! note
    When activating autocommit, transactions are not used. See: <http://initd.org/psycopg/docs/connection.html#connection.autocommit>

**Module:** `intelmq.bots.outputs.sql.output`

**Parameters:**

The parameters marked with 'PostgreSQL' will be sent to libpq via psycopg2. Check the [libpq parameter documentation](https://www.postgresql.org/docs/current/static/images/libpq-connect.html#LIBPQ-PARAMKEYWORDS) for the versions you are using.

**`autocommit`**

(optional, boolean) [Psycopg's autocommit mode](http://initd.org/psycopg/docs/connection.html?#connection.autocommit). Defaults to true.

**`engine`**

(required, string) Allowed values are `postgresql`, `sqlite`, or `mssql`.

**`database`**

(optional, string) Database name or SQLite database file. Defaults to intelmq-events.

**`host`**

(optional, string) Hostname of the database server. Defaults to localhost.

**`jsondict_as_string`**

(optional, boolean) Whether to save JSON fields as JSON string. Defaults to true.

**`message_jsondict_as_string`**

(optional, boolean) Whether to save JSON fields as JSON string. Defaults to true.

**`port`**

(optional, integer) Port of the database server. Defaults to 5432.

**`user`**

(optional, string) Username for connecting to the database system. Defaults to intelmq.

**`password`**

(optional, string) Password for connecting to the database system. Defaults to null.

**`sslmode`**

(optional, string) Database sslmode, Allowed values: `disable`, `allow`, `prefer`, `require`, `verify-ca` or `verify-full`. See: <https://www.postgresql.org/docs/current/static/images/libpq-connect.html#libpq-connect-sslmode>. Defaults to `require`.

**`table`**

(optional, string) Name of the database table to use. Defaults to events.

**`fields`**

(optional, array) Array of event fields to output to the database. Defaults to null (use all fields).

**`reconnect_delay`**

(optional, integer) Number of seconds to wait before reconnecting in case of an error. Defaults to 0.

**`fail_on_errors`**

(optional, boolean) Whether an error should cause the bot to fail (raise an exception) or otherwise rollback. If false, the bot eventually waits and re-try (e.g. re-connect) etc. to solve the issue. If true, the bot raises an exception and - depending on the IntelMQ error handling configuration - stops. Defaults to false.


### STOMP

This bot pushes data to any STOMP stream. STOMP stands for Streaming Text Oriented Messaging Protocol. See: <https://en.wikipedia.org/wiki/Streaming_Text_Oriented_Messaging_Protocol>

**Module:** `intelmq.bots.outputs.stomp.output`

**Requirements**

Install the stomp.py library, e.g. [apt install python3-stomp.py] or [pip install stomp.py].

You need a CA certificate, client certificate and key file from the organization / server you are connecting to. Also
you will need a so called "exchange point".

**Parameters:**

**`exchange`**

(optional, string) The exchange to push to. Defaults to `/exchange/_push`.

**`username`**

(optional, string) Username to use.

**`password`**

(optional, string) Password to use.

**`ssl_ca_certificate`**

(optional, string) Path to trusted CA certificate.

**`auth_by_ssl_client_certificate`**

(optional, boolean) Whether to authenticate using TLS certificate. (Set to false for new *n6* auth.) Defaults to true.

**`heartbeat`**

(optional, integer) Defaults to 60000.

**`message_hierarchical_output`**

(optional, boolean) Defaults to false.

**`message_jsondict_as_string`**

(optional, boolean) Defaults to false.

**`message_with_type`**

(optional, boolean) Defaults to false.

**`port`**

(optional, integer) Defaults to 61614.

**`server`**

(optional, string) Hostname of the STOMP server.

**`single_key`**

(optional, string) Output only a single specified key. In case of `raw` key the data is base64 decoded. Defaults to null (output the whole message).

**`ssl_ca_certificate`**

(optional, string) Path to trusted CA certificate.

**`ssl_client_certificate`**

(optional, string) Path to client certificate to use for TLS connections.

**`ssl_client_certificate_key`**

(optional, string) Path to client private key to use for TLS connections.

---

### TCP <div id="intelmq.bots.outputs.tcp.output" />

TCP is the bot responsible to send events to a TCP port (Splunk, another IntelMQ, etc..).

Multihreading is disabled for this bot.

**Sending to an IntelMQ TCP collector**

If you intend to link two IntelMQ instance via TCP, set the parameter `counterpart_is_intelmq` to true. The bot then awaits an "Ok" message to be received after each message is sent. The TCP collector just sends "Ok" after every message it gets.

**Module:** `intelmq.bots.outputs.tcp.output`

**Parameters:**

**`counterpart_is_intelmq`**

(optional, boolean) Whether the receiver is an IntelMQ TCP collector bot. Defaults to true.

**`ip`**

(required, string) Hostname of the destination server.

**`hierarchical_output`**

(optional, boolean) True for a nested JSON, false for a flat JSON (when sending to a TCP collector).

**`port`**

(required, integer) Port of destination server.

**`separator`**

(optional, string) Separator of messages, e.g. "n", optional. When sending to a TCP collector, parameter shouldn't be present. In that case, the output waits every message is acknowledged by "Ok" message the TCP collector bot implements.

---

### Templated SMTP <div id="intelmq.bots.outputs.templated_smtp.output" />

Sends a MIME Multipart message built from an event and static text using Jinja2 templates.

See the Jinja2 documentation at <https://jinja.palletsprojects.com/>.

Authentication is attempted only if both username and password are specified.

Templates are in Jinja2 format with the event provided in the variable `event`. E.g.:

```yaml
mail_to: "{{ event['source.abuse_contact'] }}"
```

As an extension to the Jinja2 environment, the function `from_json` is available for parsing JSON strings into Python
structures. This is useful if you want to handle complicated structures in the `output` field of an event. In that case,
you would start your template with a line like:

```
{%- set output = from_json(event['output']) %}
```

and can then use `output` as a regular Python object in the rest of the template.

Attachments are templated strings, especially useful for sending structured data. E.g. to send a JSON document including
`malware.name` and all other fields starting with `source.`:

```yaml
attachments:
  - content-type: application/json
    text: |
      {
        "malware": "{{ event['malware.name'] }}",
        {%- set comma = joiner(", ") %}
        {%- for key in event %}
           {%- if key.startswith('source.') %}
        {{ comma() }}"{{ key }}": "{{ event[key] }}"
           {%- endif %}
        {%- endfor %}
      }
    name: report.json
```

You are responsible for making sure that the text produced by the template is valid according to the content-type.

If you are migrating from the SMTP output bot that produced CSV format attachments, use the following configuration to
produce a matching format:

```yaml
attachments:
  - content-type: text/csv
    text: |
      {%- set fields = ["classification.taxonomy", "classification.type", "classification.identifier", "source.ip","source.asn", "source.port"] %}
      {%- set sep = joiner(";") %}
      {%- for field in fields %}{{ sep() }}{{ field }}{%- endfor %}
      {% set sep = joiner(";") %}
      {%- for field in fields %}{{ sep() }}{{ event[field] }}{%- endfor %}
    name: event.csv
```

**Module:** `intelmq.bots.outputs.templated_smtp.output`

**Requirements**

Install the required `jinja2` library:

```bash
pip3 install -r intelmq/bots/collectors/templated_smtp/REQUIREMENTS.txt
```

**Parameters:**

**`attachments`**

(required, array of objects) Each object must have `content-type`, `text` (attachment text) and `name` (filename of the attachment) fields.

```yaml
- content-type: simple string/jinja template
  text: simple string/jinja template
  name: simple string/jinja template
```

**`body`**

(optional, string) Simple string or Jinja template. The default body template prints every field in the event except `raw`, in undefined order, one field per line, as "field: value".

**`mail_from`**

(optional, string) Simple string or Jinja template. Sender's address.

**`mail_to`**

(required, string) Simple string or Jinja template. Comma-separated array of recipient addresses.

**`smtp_host`**

(optional, string) Hostname of the SMTP server. Defaults to localhost.

**`smtp_password`**

(optional, string) Password (if any) for authenticated SMTP. Defaults to null.

**`smtp_port`**

(optional, integer) TCP port to connect to. Defaults to 25.

**`smtp_username`**

(optional, string)  Username (if any) for authenticated SMTP. Defaults to null.

**`tls`**

(optional, boolean) Whether to use use SMTPS. When true, also set smtp_port to the SMTPS port. Defaults to false.

**`starttls`**

(optional, boolean) Whether to use opportunistic STARTTLS over SMTP. Defaults to true.

**`subject`**

(optional, string) Simple string or Jinja template. E-mail subject line. Defaults to "IntelMQ event".

**`verify_cert`**

(optional, boolean) Whether to verify the server certificate in STARTTLS or SMTPS. Defaults to true.

---

### Touch <div id="intelmq.bots.outputs.touch.output" />

Touches a file for every event received. Does not output the event!

**Module:** `intelmq.bots.outputs.touch.output`

**Parameters:**

**`path`**

(optional, string) Path to the file to touch.

---

### UDP <div id="intelmq.bots.outputs.udp.output" />

Output Bot that sends events to a remote UDP server.

Multihreading is disabled for this bot.

**Module:** `intelmq.bots.outputs.udp.output`

**Parameters:**

**`format`**

(optional, string) Allowed values: `json` or `delimited`. The JSON format outputs the event 'as-is'. Delimited will deconstruct the event and print each field:value separated by the field delimit. See examples below.

**`field_delimiter`**

(optional, string) If the `format` is `delimited` then this parameter is used as a delimiter between fields. Defaults to `|`.

**`header`**

(required, string) Header text to be sent in the UDP datagram.

**`keep_raw_field`**

(optional, boolean) Whether to keep `raw` field. Defaults to false.

**`udp_host`**

(optional, string) Hostname of the destination server.

**`udp_port`**

(required, integer) Port of the destination server.

**Examples of usage**

Consider the following event:

```json
{
  "raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=",
  "source.asn": 8972,
  "source.ip": "85.25.160.114",
  "source.url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/",
  "source.reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com",
  "classification.type": "malware-distribution",
  "event_description.text": "Angler EK",
  "feed.url": "http://www.malwaredomainlist.com/updatescsv.php",
  "feed.name": "Malware Domain List",
  "feed.accuracy": 100,
  "time.observation": "2016-04-29T10:59:34+00:00",
  "time.source": "2016-04-25T11:39:00+00:00"
}
```

With the following parameters:

```yaml
format: json
header: header example
keep_raw_field: true
ip: 127.0.0.1
port: 514
```

Resulting line in syslog:

```
Apr 29 11:01:29 header example {"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware-distribution"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}
```

With the following Parameters:

```yaml
field_delimiter: |
format: delimited
header: IntelMQ-event
keep_raw_field: false
ip: 127.0.0.1
port: 514
```


Resulting line in syslog:

```
Apr 29 11:17:47 localhost IntelMQ-event|source.ip: 85.25.160.114|time.source:2016-04-25T11:39:00+00:00|feed.url:http://www.malwaredomainlist.com/updatescsv.php|time.observation:2016-04-29T11:17:44+00:00|source.reverse_dns:static-ip-85-25-160-114.inaddr.ip-pool.com|feed.name:Malware Domain List|event_description.text:Angler EK|source.url:http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/|source.asn:8972|classification.type:malware-distribution|feed.accuracy:100.0
```
