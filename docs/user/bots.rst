..
   SPDX-FileCopyrightText: 2015-2021 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

####
Bots
####

.. contents::

***************
General remarks
***************

By default all of the bots are started when you start the whole botnet, however there is a possibility to
*disable* a bot. This means that the bot will not start every time you start the botnet, but you can start
and stop the bot if you specify the bot explicitly. To disable a bot, add the following to your
`runtime.conf`: `"enabled": false`. Be aware that this is **not** a normal parameter (like the others
described in this file). It is set outside of the `parameters` object in `runtime.conf`. Check out
:doc:`configuration-management` for an example.

There are two different types of parameters: The initialization parameters are need to start the bot. The runtime parameters are needed by the bot itself during runtime.

The initialization parameters are in the first level, the runtime parameters live in the `parameters` sub-dictionary:

.. code-block:: yaml

    bot-id:
      parameters:
          runtime parameters...
      initialization parameters...

For example:

.. code-block:: yaml

   abusech-feodo-domains-collector:
     parameters:
       provider: Abuse.ch
       name: Abuse.ch Feodo Domains
       http_url: http://example.org/feodo-domains.txt
     name: Generic URL Fetcher
     group: Collector
     module: intelmq.bots.collectors.http.collector_http
     description: collect report messages from remote hosts using http protocol
     enabled: true
     run_mode: scheduled

This configuration resides in the file `runtime.yaml` in your IntelMQ's configuration directory for each configured bot.

*************************
Initialization parameters
*************************

* `name` and `description`: The name and description of the bot. See also ``intelmqctl list --configured bots``.
* `group`: Can be `"Collector"`, `"Parser"`, `"Expert"` or `"Output"`. Only used for visualization by other tools.
* `module`: The executable (should be in `$PATH`) which will be started.
* `enabled`: If the parameter is set to `true` (which is NOT the default value if it is missing as a protection) the bot will start when the botnet is started (`intelmqctl start`). If the parameter was set to `false`, the Bot will not be started by `intelmqctl start`, however you can run the bot independently using `intelmqctl start <bot_id>`. Check :doc:`configuration-management` for more details.
* `run_mode`: There are two run modes, "continuous" (default run mode) or "scheduled". In the first case, the bot will be running forever until stopped or exits because of errors (depending on configuration). In the latter case, the bot will stop after one successful run. This is especially useful when scheduling bots via cron or systemd. Default is `continuous`. Check :doc:`configuration-management` for more details.

.. _common-parameters:

*************************
Common parameters
*************************

Feed parameters
^^^^^^^^^^^^^^^

Common configuration options for all collectors.

* `name`: Name for the feed (`feed.name`). In IntelMQ versions smaller than 2.2 the parameter name `feed` is also supported.
* `accuracy`: Accuracy for the data of the feed (`feed.accuracy`).
* `code`: Code for the feed (`feed.code`).
* `documentation`: Link to documentation for the feed (`feed.documentation`).
* `provider`: Name of the provider of the feed (`feed.provider`).
* `rate_limit`: time interval (in seconds) between fetching data if applicable.

HTTP parameters
^^^^^^^^^^^^^^^

Common URL fetching parameters used in multiple bots.

* `http_timeout_sec`: A tuple of floats or only one float describing the timeout of the HTTP connection. Can be a tuple of two floats (read and connect timeout) or just one float (applies for both timeouts). The default is 30 seconds in default.conf, if not given no timeout is used. See also https://requests.readthedocs.io/en/master/user/advanced/#timeouts
* `http_timeout_max_tries`: An integer depicting how often a connection is retried, when a timeout occurred. Defaults to 3 in default.conf.
* `http_username`: username for basic authentication.
* `http_password`: password for basic authentication.
* `http_proxy`: proxy to use for HTTP
* `https_proxy`: proxy to use for HTTPS
* `http_user_agent`: user agent to use for the request.
* `http_verify_cert`: path to trusted CA bundle or directory, `false` to ignore verifying SSL certificates,  or `true` (default) to verify SSL certificates
* `ssl_client_certificate`: SSL client certificate to use.
* `ssl_ca_certificate`: Optional string of path to trusted CA certificate. Only used by some bots.
* `http_header`: HTTP request headers

Cache parameters
^^^^^^^^^^^^^^^^

Common Redis cache parameters used in multiple bots (mainly lookup experts):

* `redis_cache_host`: Hostname of the Redis database.
* `redis_cache_port`: Port of the Redis database.
* `redis_cache_db`: Database number.
* `redis_cache_ttl`: TTL used for caching.
* `redis_cache_password`: Optional password for the Redis database (default: none).

.. _collector bots:

**************
Collector Bots
**************

Multihreading is disabled for all Collectors, as this would lead to duplicated data.

.. _intelmq.bots.collectors.amqp.collector_amqp:

AMQP
^^^^

Requires the `pika python library <https://pypi.org/project/pika/>`_, minimum version 1.0.0.

**Information**

* `name`: intelmq.bots.collectors.amqp.collector_amqp
* `lookup`: yes
* `public`: yes
* `cache (redis db)`: none
* `description`: collect data from (remote) AMQP servers, for both IntelMQ as well as external data

**Configuration Parameters**

* **Feed parameters** (see above)
* `connection_attempts`: The number of connection attempts to defined server, defaults to 3
* `connection_heartbeat`: Heartbeat to server, in seconds, defaults to 3600
* `connection_host`: Name/IP for the AMQP server, defaults to 127.0.0.1
* `connection_port`: Port for the AMQP server, defaults to 5672
* `connection_vhost`: Virtual host to connect, on an HTTP(S) connection would be http:/IP/<your virtual host>
* `expect_intelmq_message`: Boolean, if the data is from IntelMQ or not. Default: `false`. If true, then the data can be any Report or Event and will be passed to the next bot as is. Otherwise a new report is created with the raw data.
* `password`: Password for authentication on your AMQP server
* `queue_name`: The name of the queue to fetch data from
* `username`: Username for authentication on your AMQP server
* `use_ssl`: Use ssl for the connection, make sure to also set the correct port, usually 5671 (`true`/`false`)

Currently only fetching from a queue is supported can be extended in the future. Messages will be acknowledge at AMQP after it is sent to the pipeline.


.. _intelmq.bots.collectors.api.collector:

API
^^^

**Information**

* `name:` intelmq.bots.collectors.api.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect report messages from an HTTP or Socket REST API

**Configuration Parameters**

* **Feed parameters** (see above)
* `port`: Optional, integer. Default: 5000. The local port, the API will be available at.
* `use_socket`: Optional, boolean. Default: false. If true, the socket will be opened at the location given with `socket_path`.
* `socket_path`: Optional, string. Default: ``/tmp/imq_api_default_socket``

The API is available at `/intelmq/push` if the HTTP interface is used (default).
The `tornado` library is required.


.. _intelmq.bots.collectors.http.collector_http:

Generic URL Fetcher
^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.http.collector_http
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect report messages from remote hosts using HTTP protocol

**Configuration Parameters**

* **Feed parameters** (see above)
* **HTTP parameters** (see above)
* `extract_files`: Optional, boolean or list of strings. If it is true, the retrieved (compressed) file or archived will be uncompressed/unpacked and the files are extracted. If the parameter is a list for strings, only the files matching the filenames are extracted. Extraction handles gzipped files and both compressed and uncompressed tar-archives as well as zip archives.
* `http_url`: location of information resource (e.g. https://feodotracker.abuse.ch/blocklist/?download=domainblocklist)
* `http_url_formatting`: (`bool|JSON`, default: `false`) If `true`, `{time[format]}` will be replaced by the current time in local timezone formatted by the given format. E.g. if the URL is `http://localhost/{time[%Y]}`, then the resulting URL is `http://localhost/2019` for the year 2019. (Python's `Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>`_ is used for this.). You may use a `JSON` specifying `time-delta <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`_ parameters to shift the current time accordingly. For example use `{"days": -1}` for the yesterday's date; the URL `http://localhost/{time[%Y-%m-%d]}` will get translated to "http://localhost/2018-12-31" for the 1st Jan of 2019.
* `verify_pgp_signatures`: `bool`, defaults to `false`. If `true`, signature file is downloaded and report file is checked. On error (missing signature, mismatch, ...), the error is logged and the report is not processed. Public key has to be imported in local keyring. This requires the `python-gnupg` library.
* `signature_url`: Location of signature file for downloaded content. For path `http://localhost/data/latest.json` this may be for example `http://localhost/data/latest.asc`.
* `signature_url_formatting`: (`bool|JSON`, default: `false`) The same as `http_url_formatting`, only for the signature file.
* `gpg_keyring`: `string` or `none` (default). If specified, the string represents path to keyring file, otherwise the PGP keyring file for current `intelmq` user is used.

Zipped files are automatically extracted if detected.

For extracted files, every extracted file is sent in its own report. Every report has a field named `extra.file_name` with the file name in the archive the content was extracted from.

**HTTP Response status code checks**

If the HTTP response' status code is not 2xx, this is treated as error.

In Debug logging level, the request's and response's headers and body are logged for further inspection.


.. _intelmq.bots.collectors.http.collector_http_stream:

Generic URL Stream Fetcher
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.http.collector_http_stream
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Opens a streaming connection to the URL and sends the received lines.

**Configuration Parameters**

* **Feed parameters** (see above)
* **HTTP parameters** (see above)
* `strip_lines`: boolean, if single lines should be stripped (removing whitespace from the beginning and the end of the line)

If the stream is interrupted, the connection will be aborted using the timeout parameter.
No error will be logged if the number of consecutive connection fails does not reach the parameter `error_max_retries`. Instead of errors, an INFO message is logged. This is a measurement against too frequent ERROR logging messages. The consecutive connection fails are reset if a data line has been successfully transferred.
If the consecutive connection fails reaches the parameter `error_max_retries`, an exception will be thrown and `rate_limit` applies, if not null.

The parameter `http_timeout_max_tries` is of no use in this collector.


.. _intelmq.bots.collectors.mail.collector_mail_url:

Generic Mail URL Fetcher
^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.mail.collector_mail_url
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from mailboxes, extract URLs from that messages and download the report messages from the URLs.

**Configuration Parameters**

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
* `extra.email_date`: The content of the email's `Date` header
* `extra.email_subject`: The subject of the email
* `extra.email_from`: The email's from address
* `extra.email_message_id`: The email's message ID
* `extra.file_name`: The file name of the downloaded file (extracted from the HTTP Response Headers if possible).

**Chunking**

For line-based inputs the bot can split up large reports into smaller chunks.

This is particularly important for setups that use Redis as a message queue
which has a per-message size limitation of 512 MB.

To configure chunking, set `chunk_size` to a value in bytes.
`chunk_replicate_header` determines whether the header line should be repeated
for each chunk that is passed on to a parser bot.

Specifically, to configure a large file input to work around Redis' size
limitation set `chunk_size` to something like `384000000`, i.e., ~384 MB.


.. _intelmq.bots.collectors.mail.collector_mail_attach:

Generic Mail Attachment Fetcher
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.mail.collector_mail_attach
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from mailboxes, download the report messages from the attachments.

**Configuration Parameters**

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

* `extra.email_date`: The content of the email's `Date` header
* `extra.email_subject`: The subject of the email
* `extra.email_from`: The email's from address
* `extra.email_message_id`: The email's message ID
* `extra.file_name`: The file name of the attachment or the file name in the attached archive if attachment is to uncompress.


.. _intelmq.bots.collectors.mail.collector_mail_body:

Generic Mail Body Fetcher
^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.mail.collector_mail_body
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from mailboxes, forwards the bodies as reports. Each non-empty body with the matching content type is sent as individual report.

**Configuration Parameters**

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

* `extra.email_date`: The content of the email's `Date` header
* `extra.email_subject`: The subject of the email
* `extra.email_from`: The email's from address
* `extra.email_message_id`: The email's message ID


.. _intelmq.bots.collectors.github_api.collector_github_contents_api:

Github API
^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.github_api.collector_github_contents_api
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Collects files matched by regular expression from GitHub repository via the GitHub API.
  Optionally with GitHub credentials, which are used as the Basic HTTP authentication.

**Configuration Parameters**

* **Feed parameters** (see above)
* `basic_auth_username:` GitHub account username (optional)
* `basic_auth_password:` GitHub account password (optional)
* `repository:` GitHub target repository (`<USER>/<REPOSITORY>`)
* `regex:` Valid regular expression of target files within the repository (defaults to `.*.json`)
* `extra_fields:` Comma-separated list of extra fields from `GitHub contents API <https://developer.github.com/v3/repos/contents/>`_.

**Workflow**

The optional authentication parameters provide a high limit of the GitHub API requests.
With the git hub user authentication, the requests are rate limited to 5000 per hour, otherwise to 60 requests per hour.

The collector recursively searches for `regex`-defined files in the provided `repository`.
Additionally it adds extra file metadata defined by the `extra_fields`.

The bot always sets the url, from which downloaded the file, as `feed.url`.


.. _intelmq.bots.collectors.file.collector_file:

Fileinput
^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.file.collector_file
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` This bot is capable of reading files from the local file-system.
  This is handy for testing purposes, or when you need to react to spontaneous
  events. In combination with the Generic CSV Parser this should work great.

**Configuration Parameters**

* **Feed parameters** (see above)
* `path`: path to file
* `postfix`: The postfix (file ending) of the files to look for. For example `.csv`.
* `delete_file`: whether to delete the file after reading (default: `false`)

The resulting reports contains the following special fields:

* `feed.url`: The URI using the `file://` scheme and localhost, with the full path to the processed file.
* `extra.file_name`: The file name (without path) of the processed file.

**Chunking**

Additionally, for line-based inputs the bot can split up large reports into
smaller chunks.

This is particularly important for setups that use Redis as a message queue
which has a per-message size limitation of 512 MB.

To configure chunking, set `chunk_size` to a value in bytes.
`chunk_replicate_header` determines whether the header line should be repeated
for each chunk that is passed on to a parser bot.

Specifically, to configure a large file input to work around Redis' size
limitation set `chunk_size` to something like `384000`, i.e., ~384 MB.

**Workflow**

The bot loops over all files in `path` and tests if their file name matches
*postfix, e.g. `*.csv`. If yes, the file will be read and inserted into the
queue.

If `delete_file` is set, the file will be deleted after processing. If deletion
is not possible, the bot will stop.

To prevent data loss, the bot also stops when no `postfix` is set and
`delete_file` was set. This cannot be overridden.

The bot always sets the file name as feed.url


.. _intelmq.bots.collectors.fireeye.collector_fireeye:

Fireeye
^^^^^^^

**Information**

* `name:` `intelmq.bots.collectors.fireeye.collector_fireeye`
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` This bot is capable of collecting hashes and URLs from a Fireeye MAS appliance.

The Python library `xmltodict` is required to run this bot.

**Configuration Parameters**

* **Feed parameters** (see above)
* `dns_name`: DNS name of the target appliance.
* `request_duration`: Length of the query in past eg. collect alerts from last 24hours/48hours.
* `http_username`: Password for authentication.
* `http_password`: Username for authentication.

**Workflow**

The bot collects all alerts which occurred during specified duration. After this we
make a second call and check if there is additional information like domains and hashes available.
After collecting the openioc data we send this information to the Fireeye parser.


.. _intelmq.bots.collectors.kafka.collector:

Kafka
^^^^^

Requires the `kafka python library <https://pypi.org/project/kafka/>`_.

**Information**

* `name:` intelmq.bots.collectors.kafka.collector

**Configuration parameters**

* `topic:` the kafka topic the collector should get messages from
* `bootstrap_servers:` the kafka server(s) the collector should connect to. Defaults to `localhost:9092`
* `ssl_check_hostname`: `false` to ignore verifying SSL certificates, or `true` (default) to verify SSL certificates
* `ssl_client_certificate`: SSL client certificate to use.
* `ssl_ca_certificate`: Optional string of path to trusted CA certificate. Only used by some bots.


.. _intelmq.bots.collectors.rsync.collector_rsync:

Rsync
^^^^^

Requires the rsync executable

**Information**

* `name:` intelmq.bots.collectors.rsync.collector_rsync
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Bot download file by rsync and then load data from downloaded file. Downloaded file is located in `var/lib/bots/rsync_collector.`

**Configuration Parameters**

* **Feed parameters** (see above)
* `file`: Name of downloaded file.
* `rsync_path`: Path to file. It can be "/home/username/directory" or "username@remote_host:/home/username/directory"
* `temp_directory`: Path of a temporary state directory to use for rsync'd files. Optional. Default: `/opt/intelmq/var/run/rsync_collector/`.


.. _intelmq.bots.collectors.misp.collector:

MISP Generic
^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.misp.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect messages from `MISP <https://github.com/MISP>`_, a malware information sharing platform server.

**Configuration Parameters**

* **Feed parameters** (see above)
* `misp_url`: URL of MISP server (with trailing '/')
* `misp_key`: MISP Authkey
* `misp_tag_to_process`: MISP tag for events to be processed
* `misp_tag_processed`: MISP tag for processed events, optional

Generic parameters used in this bot:

* `http_verify_cert`: Verify the TLS certificate of the server, boolean (default: `true`)

**Workflow**
This collector will search for events on a MISP server that have a
`to_process` tag attached to them (see the `misp_tag_to_process` parameter)
and collect them for processing by IntelMQ. Once the MISP event has been
processed the `to_process` tag is removed from the MISP event and a
`processed` tag is then attached (see the `misp_tag_processed` parameter).

**NB.** The MISP tags must be configured to be 'exportable' otherwise they will
not be retrieved by the collector.


.. _intelmq.bots.collectors.rt.collector_rt:

Request Tracker
^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.rt.collector_rt
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Request Tracker Collector fetches attachments from an RTIR instance.

You need the rt-library >= 1.9 from nic.cz, available via `pypi <https://pypi.org/project/rt/>`_: `pip3 install rt`

This rt bot will connect to RT and inspect the given `search_queue` for tickets matching all criteria in `search_*`,
Any matches will be inspected. For each match, all (RT-) attachments of the matching RT tickets are iterated over and within this loop, the first matching filename in the attachment is processed.
If none of the filename matches apply, the contents of the first (RT-) "history" item is matched against the regular expression for the URL (`url_regex`).

**Configuration Parameters**

* **Feed parameters** (see above)
* **HTTP parameters** (see above)
* `extract_attachment`: Optional, boolean or list of strings. See documentation of the Generic URL Fetcher parameter `extract_files` for more details.
* `extract_download`: Optional, boolean or list of strings. See documentation of the Generic URL Fetcher parameter `extract_files` for more details.
* `uri`: URL of the REST interface of the RT
* `user`: RT username
* `password`: RT password
* `search_not_older_than`: Absolute time (use ISO format) or relative time, e.g. `3 days`.
* `search_owner`: owner of the ticket to search for (default: `nobody`)
* `search_queue`: queue of the ticket to search for (default: `Incident Reports`)
* `search_requestor`: the e-mail address of the requestor
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
* `extra.email_from` and `extra.ticket_requestors`: Comma separated list of the ticket's requestor's email addresses.
* `extra.ticket_owner`: The ticket's owner name
* `extra.ticket_status`: The ticket's status
* `extra.ticket_queue`: The ticket's queue
* `extra.file_name`: The name of the extracted file, the name of the downloaded file or the attachments' filename without `.gz` postfix.
* `time.observation`: The creation time of the ticket or attachment.

**Search**

The parameters prefixed with `search_` allow configuring the ticket search.

Empty strings and `null` as value for search parameters are ignored.

**File downloads**

Attachments can be optionally unzipped, remote files are downloaded with the `http_*` settings applied.

If `url_regex` or `attachment_regex` are empty strings, false or null, they are ignored.

**Ticket processing**

Optionally, the RT bot can "take" RT tickets (i.e. the `user` is assigned this ticket now) and/or the status can be changed (leave `set_status` empty in case you don't want to change the status). Please note however that you **MUST** do one of the following: either "take" the ticket  or set the status (`set_status`). Otherwise, the search will find the ticket every time and we will have generated an endless loop.

In case a resource needs to be fetched and this resource is permanently not available (status code is 4xx), the ticket status will be set according to the configuration to avoid processing the ticket over and over.
For temporary failures the status is not modified, instead the ticket will be skipped in this run.

**Time search**

To find only tickets newer than a given absolute or relative time, you can use the `search_not_older_than` parameter. Absolute time specification can be anything parseable by dateutil, best use a ISO format.

Relative must be in this format: `[number] [timespan]s`, e.g. `3 days`. `timespan` can be hour, day, week, month, year. Trailing 's' is supported for all timespans. Relative times are subtracted from the current time directly before the search is performed.


.. _intelmq.bots.collectors.rsync.collector_rsync:

Rsync
^^^^^

**Information**


* `name:` intelmq.bots.collectors.rsync.collector_rsync
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Syncs a file via rsync and reads the file.

**Configuration Parameters**

* **Feed parameters** (see above)
* `file`: The filename to process, combine with `rsync_path`.
* `temp_directory`: The temporary directory for rsync, by default `$VAR_STATE_PATH/rsync_collector`. `$VAR_STATE_PATH` is `/var/run/intelmq/` or `/opt/intelmq/var/run/`.
* `rsync_path`: The path of the file to process


.. _intelmq.bots.collectors.shadowserver.collector_reports_api:

Shadowserver Reports API
^^^^^^^^^^^^^^^^^^^^^^^^

The Cache is required to memorize which files have already been processed (TTL needs to be high enough to cover the oldest files available!).

**Information**

* `name`: `intelmq.bots.collectors.shadowserver.collector_reports_api`
* `description`: Connects to the `Shadowserver API <https://www.shadowserver.org/what-we-do/network-reporting/api-documentation/>`_, requests a list of all the reports for a specific country and processes the ones that are new.

**Configuration Parameters**

* `country`: The country you want to download the reports for
* `apikey`: Your Shadowserver API key
* `secret`: Your Shadowserver API secret
* `types`: A list of strings or a string of comma-separated values with the names of report types you want to process. If you leave this empty, all the available reports will be downloaded and processed (i.e. 'scan', 'drones', 'intel', 'sandbox_connection', 'sinkhole_combined'). The possible report types are equivalent to the file names given in the section :ref:`Supported Reports <shadowserver-supported-reports>` of the Shadowserver parser.
* **Cache parameters** (see in section :ref:`common-parameters`, the default TTL is set to 10 days)

The resulting reports contain the following special field:

* `extra.file_name`: The name of the downloaded file, with fixed filename extension. The API returns file names with the extension `.csv`, although the files are JSON, not CSV. Therefore, for clarity and better error detection in the parser, the file name in `extra.file_name` uses `.json` as extension.


.. _intelmq.bots.collectors.shodan.collector_stream:

Shodan Stream
^^^^^^^^^^^^^

Requires the shodan library to be installed:
 * https://github.com/achillean/shodan-python/
 * https://pypi.org/project/shodan/

**Information**

* `name:` intelmq.bots.collectors.shodan.collector_stream
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Queries the Shodan Streaming API

**Configuration Parameters**

* **Feed parameters** (see above)
* **HTTP parameters** (see above). Only the proxy is used (requires `shodan-python > 1.8.1`). Certificate is always verified.
* `countries`: A list of countries to query for. If it is a string, it will be spit by `,`.

If the stream is interrupted, the connection will be aborted using the timeout parameter.
No error will be logged if the number of consecutive connection fails does not reach the parameter `error_max_retries`. Instead of errors, an INFO message is logged. This is a measurement against too frequent ERROR logging messages. The consecutive connection fails are reset if a data line has been successfully transferred.
If the consecutive connection fails reaches the parameter `error_max_retries`, an exception will be thrown and `rate_limit` applies, if not null.


.. _intelmq.bots.collectors.tcp.collector:

TCP
^^^

**Information**

* `name:` intelmq.bots.collectors.tcp.collector
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` TCP is the bot responsible to receive events on a TCP port (ex: from TCP Output of another IntelMQ instance). Might not be working on Python3.4.6.

**Configuration Parameters**

* `ip`: IP of destination server
* `port`: port of destination server

**Response**

TCP collector just sends an "Ok" message after every received message, this should not pose a problem for an arbitrary input.
If you intend to link two IntelMQ instance via TCP, have a look at the TCP output bot documentation.


.. _intelmq.bots.collectors.alienvault_otx.collector:

Alien Vault OTX
^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.alienvault_otx.collector
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` collect report messages from Alien Vault OTX API

**Requirements**


Install the library from GitHub, as there is no package in PyPi:

.. code-block:: bash

   pip3 install -r intelmq/bots/collectors/alienvault_otx/REQUIREMENTS.txt

**Configuration Parameters**

* **Feed parameters** (see above)
* `api_key`: API Key
* `modified_pulses_only`: get only modified pulses instead of all, set to it to true or false, default false
* `interval`: if "modified_pulses_only" is set, define the time in hours (integer value) to get modified pulse since then, default 24 hours


.. _intelmq.bots.collectors.blueliv.collector_crimeserver:

Blueliv Crimeserver
^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.blueliv.collector_crimeserver
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect report messages from Blueliv API

For more information visit https://github.com/Blueliv/api-python-sdk

**Requirements**


Install the required library:

.. code-block:: bash

   pip3 install -r intelmq/bots/collectors/blueliv/REQUIREMENTS.txt

**Configuration Parameters**

* **Feed parameters** (see above)
* `api_key`: location of information resource, see https://map.blueliv.com/?redirect=get-started#signup
* `api_url`: The optional API endpoint, by default `https://freeapi.blueliv.com`.


.. _intelmq.bots.collectors.calidog.collector_certstream:

Calidog Certstream
^^^^^^^^^^^^^^^^^^

A Bot to collect data from the Certificate Transparency Log (CTL)
This bot works based on certstream library (https://github.com/CaliDog/certstream-python)

**Information**

* `name:` intelmq.bots.collectors.calidog.collector_certstream
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect data from Certificate Transparency Log

**Configuration Parameters**

* **Feed parameters** (see above)


.. _intelmq.bots.collectors.eset.collector:

ESET ETI
^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.eset.collector
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect data from ESET ETI TAXII server

For more information visit https://www.eset.com/int/business/services/threat-intelligence/

**Requirements**


Install the required `cabby` library:

.. code-block:: bash

   pip3 install -r intelmq/bots/collectors/eset/REQUIREMENTS.txt

**Configuration Parameters**

* **Feed parameters** (see above)
* `username`: Your username
* `password`: Your password
* `endpoint`: `eti.eset.com`
* `time_delta`: The time span to look back, in seconds. Default `3600`.
* `collection`: The collection to fetch.


.. _intelmq.bots.collectors.opendxl.collector:

McAfee openDXL
^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.opendxl.collector
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect messages via openDXL

**Configuration Parameters**

* **Feed parameters** (see above)
* `dxl_config_file`: location of the configuration file containing required information to connect $
* `dxl_topic`: the name of the DXL topic to subscribe


.. _intelmq.bots.collectors.microsoft.collector_azure:

Microsoft Azure
^^^^^^^^^^^^^^^

Iterates over all blobs in all containers in an Azure storage.
The Cache is required to memorize which files have already been processed (TTL needs to be high enough to cover the oldest files available!).

This bot significantly changed in a backwards-incompatible way in IntelMQ Version 2.2.0 to support current versions of the Microsoft Azure Python libraries.
``azure-storage-blob>=12.0.0`` is required.

**Information**

* `name`: intelmq.bots.collectors.microsoft.collector_azure
* `lookup`: yes
* `public`: no
* `cache (redis db)`: 5
* `description`: collect blobs from Microsoft Azure using their library

**Configuration Parameters**

* **Cache parameters** (see above)
* **Feed parameters** (see above)
* `connection_string`: connection string as given by Microsoft
* `container_name`: name of the container to connect to


.. _intelmq.bots.collectors.microsoft.collector_interflow:

Microsoft Interflow
^^^^^^^^^^^^^^^^^^^

Iterates over all files available by this API. Make sure to limit the files to be downloaded with the parameters, otherwise you will get a lot of data!
The cache is used to remember which files have already been downloaded. Make sure the TTL is high enough, higher than `not_older_than`.

**Information**

* `name:` intelmq.bots.collectors.microsoft.collector_interflow
* `lookup:` yes
* `public:` no
* `cache (redis db):` 5
* `description:` collect files from Microsoft Interflow using their API

**Configuration Parameters**

* **Feed parameters** (see above)
* `api_key`: API generate in their portal
* `file_match`: an optional regular expression to match file names
* `not_older_than`: an optional relative (minutes) or absolute time (UTC is assumed) expression to determine the oldest time of a file to be downloaded
* `redis_cache_*` and especially `redis_cache_ttl`: Settings for the cache where file names of downloaded files are saved. The cache's TTL must always be bigger than `not_older_than`.

**Additional functionalities**

* Files are automatically ungzipped if the filename ends with `.gz`.

.. _stomp collector bot:


.. _intelmq.bots.collectors.stomp.collector:

Stomp
^^^^^

**Information**

* `name:` intelmq.bots.collectors.stomp.collector
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` collect messages from a stomp server

**Requirements**


Install the `stomp.py` library from PyPI:

.. code-block:: bash

   pip3 install -r intelmq/bots/collectors/stomp/REQUIREMENTS.txt

**Configuration Parameters**

* **Feed parameters** (see above)
* `exchange`: exchange point
* `port`: 61614
* `server`: hostname e.g. "n6stream.cert.pl"
* `ssl_ca_certificate`: path to CA file
* `ssl_client_certificate`: path to client cert file
* `ssl_client_certificate_key`: path to client cert key file


.. _intelmq.bots.collectors.twitter.collector_twitter:

Twitter
^^^^^^^

Collects tweets from target_timelines. Up to tweet_count tweets from each user and up to timelimit back in time. The tweet text is sent separately and if allowed, links to pastebin are followed and the text sent in a separate report

**Information**

* `name:` intelmq.bots.collectors.twitter.collector_twitter
* `lookup:` yes
* `public:` yes
* `cache (redis db):` none
* `description:` Collects tweets

**Configuration Parameters**

* **Feed parameters** (see above)
* `target_timelines`: screen_names of twitter accounts to be followed
* `tweet_count`: number of tweets to be taken from each account
* `timelimit`: maximum age of the tweets collected in seconds
* `follow_urls`: list of screen_names for which URLs will be followed
* `exclude_replies`: exclude replies of the followed screen_names
* `include_rts`: whether to include retweets by given screen_name
* `consumer_key`: Twitter API login data
* `consumer_secret`: Twitter API login data
* `access_token_key`: Twitter API login data
* `access_token_secret`: Twitter API login data


.. _intelmq.bots.collectors.api.collector_api:

API collector bot
^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.collectors.api.collector_api
* `lookup:` no
* `public:` no
* `cache (redis db):` none
* `description:` Bot for collecting data using API, you need to post JSON to /intelmq/push endpoint

example usage:

.. code-block:: bash

   curl -X POST http://localhost:5000/intelmq/push -H 'Content-Type: application/json' --data '{"source.ip": "127.0.0.101", "classification.type": "system-compromise"}'

**Configuration Parameters**

* **Feed parameters** (see above)
* `port`: 5000


.. _parser bots:

***********
Parser Bots
***********

Not complete
^^^^^^^^^^^^

This list is not complete. Look at ``intelmqctl list bots`` or the list of parsers shown in the manager. But most parsers do not need configuration parameters.

TODO


.. _intelmq.bots.parsers.anubisnetworks.parser:

AnubisNetworks Cyberfeed Stream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name`: `intelmq.bots.parsers.anubisnetworks.parser`
* `lookup`: no
* `public`: yes
* `cache (redis db)`: none
* `description`: parsers data from AnubisNetworks Cyberfeed Stream

**Description**

The feed format changes over time. The parser supports at least data from 2016 and 2020.

Events with the Malware "TestSinkholingLoss" are ignored, as they are for the feed provider's internal purpose only and should not be processed at all.

**Configuration parameters**

* `use_malware_familiy_as_classification_identifier`: default: `true`. Use the `malw.family` field as `classification.type`. If `false`, check if the same as `malw.variant`. If it is the same, it is ignored. Otherwise saved as `extra.malware.family`.


.. _intelmq.bots.parsers.generic.parser_csv:

Generic CSV Parser
^^^^^^^^^^^^^^^^^^

**Information**

* `name`: `intelmq.bots.parsers.generic.parser_csv`
* `lookup`: no
* `public`: yes
* `cache (redis db)`: none
* `description`: Parses CSV data

Lines starting with `'#'` will be ignored. Headers won't be interpreted.

**Configuration parameters**

 * `"columns"`: A list of strings or a string of comma-separated values with field names. The names must match the IntelMQ Data Format field names. Empty column specifications and columns named `"__IGNORE__"` are ignored. E.g.

   .. code-block:: json

      "columns": [
           "",
           "source.fqdn",
           "extra.http_host_header",
           "__IGNORE__"
      ],

   is equivalent to:

   .. code-block:: json

      "columns": ",source.fqdn,extra.http_host_header,"

   The first and the last column are not used in this example.

   It is possible to specify multiple columns using the `|` character. E.g.

   .. code-block::

      "columns": "source.url|source.fqdn|source.ip"

   First, bot will try to parse the value as URL, if it fails, it will try to parse it as FQDN, if that fails, it will try to parse it as IP, if that fails, an error will be raised.
   Some use cases -

   - mixed data set, e.g. URL/FQDN/IP/NETMASK  `"columns": "source.url|source.fqdn|source.ip|source.network"`
   - parse a value and ignore if it fails  `"columns": "source.url|__IGNORE__"`

 * `"column_regex_search"`: Optional. A dictionary mapping field names (as given per the columns parameter) to regular expression. The field is evaluated using `re.search`. Eg. to get the ASN out of `AS1234` use: `{"source.asn": "[0-9]*"}`. Make sure to properly escape any backslashes in your regular expression (See also :issue:`#1579 <1579>`).
 * `"compose_fields"`: Optional, dictionary. Create fields from columns, e.g. with data like this:

   .. code-block:: csv

      # Host,Path
      example.com,/foo/
      example.net,/bar/

   using this compose_fields parameter:

   .. code-block:: json

      {"source.url": "http://{0}{1}"}

   You get:

   .. code-block::

      http://example.com/foo/
      http://example.net/bar/

   in the respective `source.url` fields. The value in the dictionary mapping is formatted whereas the columns are available with their index.
 * `"default_url_protocol"`: For URLs you can give a default protocol which will be pretended to the data.
 * `"delimiter"`: separation character of the CSV, e.g. `","`
 * `"skip_header"`: Boolean, skip the first line of the file, optional. Lines starting with `#` will be skipped additionally, make sure you do not skip more lines than needed!
 * `time_format`: Optional. If `"timestamp"`, `"windows_nt"` or `"epoch_millis"` the time will be converted first. With the default `null` fuzzy time parsing will be used.
 * `"type"`: set the `classification.type` statically, optional
 * `"data_type"`: sets the data of specific type, currently only `"json"` is supported value. An example

   .. code-block:: json

      {
          "columns": [ "source.ip", "source.url", "extra.tags"],
          "data_type": "{\"extra.tags\":\"json\"}"
      }

   It will ensure `extra.tags` is treated as `json`.
 * `"filter_text"`: only process the lines containing or not containing specified text, to be used in conjunction with `filter_type`
 * `"filter_type"`: value can be whitelist or blacklist. If `whitelist`, only lines containing the text in `filter_text` will be processed, if `blacklist`, only lines NOT containing the text will be processed.

   To process ipset format files use

   .. code-block:: json

      {
           "filter_text": "ipset add ",
           "filter_type": "whitelist",
           "columns": [ "__IGNORE__", "__IGNORE__", "__IGNORE__", "source.ip"]
      }

 * `"type_translation"`: If the source does have a field with information for `classification.type`, but it does not correspond to IntelMQ's types,
   you can map them to the correct ones. The `type_translation` field can hold a dictionary, or a string with a JSON dictionary which maps the feed's values to IntelMQ's.
   Example:

   .. code-block:: json

     {"malware_download": "malware-distribution"}

 * `"columns_required"`: A list of true/false for each column. By default, it is true for every column.


.. _intelmq.bots.parsers.calidog.parser_certstream:

Calidog Certstream
^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.parsers.calidog.parser_certstream
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` parsers data from Certificate Transparency Log

**Description**

For each domain in the `leaf_cert.all_domains` object one event with the domain in `source.fqdn` (and `source.ip` as fallback) is produced.
The seen-date is saved in `time.source` and the classification type is `other`.

* **Feed parameters** (see above)


.. _intelmq.bots.parsers.eset.parser:

ESET
^^^^

**Information**

* `name:` intelmq.bots.parsers.eset.parser
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Parses data from ESET ETI TAXII server

**Description**

Supported collections:

* "ei.urls (json)"
* "ei.domains v2 (json)"


.. _intelmq.bots.parsers.cymru.parser_cap_program:

Cymru CAP Program
^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.parsers.cymru.parser_cap_program
* `public:` no
* `cache (redis db):` none
* `description:` Parses data from Cymru's CAP program feed.

**Description**

There are two different feeds available:

 * `infected_$date.txt` ("old")
 * `$certname_$date.txt` ("new")

The new will replace the old at some point in time, currently you need to fetch both. The parser handles both formats.

**Old feed**

As little information on the format is available, the mappings might not be correct in all cases.
Some reports are not implemented at all as there is no data available to check if the parsing is correct at all. If you do get errors like `Report ... not implement` or similar please open an issue and report the (anonymized) example data. Thanks.

The information about the event could be better in many cases but as Cymru does not want to be associated with the report, we can't add comments to the events in the parser, because then the source would be easily identifiable for the recipient.


.. _intelmq.bots.parsers.cymru.parser_full_bogons:

Cymru Full Bogons
^^^^^^^^^^^^^^^^^

http://www.team-cymru.com/bogon-reference.html

**Information**

* `name:` intelmq.bots.parsers.cymru.parser_full_bogons
* `public:` no
* `cache (redis db):` none
* `description:` Parses data from full bogons feed.


.. _intelmq.bots.parsers.github_feed.parser:

Github Feed
^^^^^^^^^^^

**Information**


* `name:` intelmq.bots.parsers.github_feed.parser
* `description:` Parses Feeds available publicly on GitHub (should receive from `github_api` collector)


.. _intelmq.bots.parsers.hibp.parser_callback:

Have I Been Pwned Callback Parser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.parsers.hibp.parser_callback
* `public:` no
* `cache (redis db):` none
* `description:` Parses data from Have I Been Pwned feed.

**Description**

Parsers the data from a Callback of a Have I Been Pwned Enterprise Subscription.

Parses breaches and pastes and creates one event per e-mail address. The e-mail address is stored in `source.account`.
`classification.type` is `leak` and `classification.identifier` is `breach` or `paste`.


.. _intelmq.bots.parsers.html_table.parser:

HTML Table Parser
^^^^^^^^^^^^^^^^^

* `name:` intelmq.bots.parsers.html_table.parser
* `public:` yes
* `cache (redis db):` none
* `description:` Parses tables in HTML documents

**Configuration parameters**

 * `"columns"`: A list of strings or a string of comma-separated values with field names. The names must match the IntelMQ Data Format field names. Empty column specifications and columns named `"__IGNORE__"` are ignored. E.g.

   .. code-block:: json

      "columns": [
           "",
           "source.fqdn",
           "extra.http_host_header",
           "__IGNORE__"
      ],

   is equivalent to:

   .. code-block:: json

      "columns": ",source.fqdn,extra.http_host_header,"

   The first and the last column are not used in this example.
   It is possible to specify multiple columns using the `|` character. E.g.

   .. code-block:: json

      "columns": "source.url|source.fqdn|source.ip"

   First, bot will try to parse the value as URL, if it fails, it will try to parse it as FQDN, if that fails, it will try to parse it as IP, if that fails, an error will be raised.
   Some use cases -

   - mixed data set, e.g. URL/FQDN/IP/NETMASK  `"columns": "source.url|source.fqdn|source.ip|source.network"`
   - parse a value and ignore if it fails  `"columns": "source.url|__IGNORE__"`

 * `"ignore_values"`:  A list of strings or a string of comma-separated values which will not considered while assigning to the corresponding fields given in `columns`. E.g.

   .. code-block:: json

      "ignore_values": [
           "",
           "unknown",
           "Not listed",
       ],

   is equivalent to:

   .. code-block:: json

      "ignore_values": ",unknown,Not listed,"

   The following configuration will lead to assigning all values to malware.name and extra.SBL except `unknown` and `Not listed` respectively.

   .. code-block:: json

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

   Parameters **columns and ignore_values must have same length**
 * `"attribute_name"`: Filtering table with table attributes, to be used in conjunction with `attribute_value`, optional. E.g. `class`, `id`, `style`.
 * `"attribute_value"`: String.
   To filter all tables with attribute `class='details'` use

   .. code-block:: json

      "attribute_name": "class",
      "attribute_value": "details"

 * `"table_index"`: Index of the table if multiple tables present. If `attribute_name` and `attribute_value` given, index according to tables remaining after filtering with table attribute. Default: `0`.
 * `"split_column"`: Padded column to be split to get values, to be used in conjunction with `split_separator` and `split_index`, optional.
 * `"split_separator"`: Delimiter string for padded column.
 * `"split_index"`: Index of unpadded string in returned list from splitting `split_column` with `split_separator` as delimiter string. Default: `0`.
    E.g.

   .. code-block:: json

      "split_column": "source.fqdn",
      "split_separator": " ",
      "split_index": 1,

   With above configuration, column corresponding to `source.fqdn` with value `[D] lingvaworld.ru` will be assigned as `"source.fqdn": "lingvaworld.ru"`.
 * `"skip_table_head"`: Boolean, skip the first row of the table, optional. Default: `true`.
 * `"default_url_protocol"`: For URLs you can give a default protocol which will be pretended to the data. Default: `"http://"`.
 * `"time_format"`: Optional. If `"timestamp"`, `"windows_nt"` or `"epoch_millis"` the time will be converted first. With the default `null` fuzzy time parsing will be used.
 * `"type"`: set the `classification.type` statically, optional
 * `"html_parser"`: The HTML parser to use, by default "html.parser", can also be e.g. "lxml", have a look at https://www.crummy.com/software/BeautifulSoup/bs4/doc/


.. _intelmq.bots.parsers.key_value.parser:

Key-Value Parser
^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.parsers.key_value.parser
* `lookup:` no
* `public:` no
* `cache (redis db):` none
* `description:` Parses text lines in key=value format, for example FortiGate firewall logs.

**Configuration Parameters**

* `pair_separator`: String separating key=value pairs, default `" "` (space).
* `kv_separator`: String separating key and value, default `=`.
* `keys`: Array of string->string, names of keys to propagate mapped to IntelMQ event fields. Example:

  .. code-block:: json

     "keys": {
         "srcip": "source.ip",
         "dstip": "destination.ip"
     }

  The value mapped to `time.source` is parsed. If the value is numeric, it is interpreted. Otherwise, or if it fails, it is parsed fuzzy with dateutil.
  If the value cannot be parsed, a warning is logged per line.
* `strip_quotes`: Boolean, remove opening and closing quotes from values, default true.

**Parsing limitations**

The input must not have (quoted) occurrences of the separator in the values. For example, this is not parsable (with space as separator):

.. code-block::

   key="long value" key2="other value"

In firewall logs like FortiGate, this does not occur. These logs usually look like:

.. code-block::

   srcip=192.0.2.1 srcmac="00:00:5e:00:17:17"


.. _intelmq.bots.parsers.mcafee.parser_atd:

McAfee Advanced Threat Defense File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.parsers.mcafee.parser_atd
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Parse IoCs from McAfee Advanced Threat Defense reports (hash, IP, URL)

**Configuration Parameters**

* **Feed parameters** (see above)
* `verdict_severity`: min report severity to parse


.. _intelmq.bots.parsers.microsoft.parser_ctip:

Microsoft CTIP Parser
^^^^^^^^^^^^^^^^^^^^^

* `name`: `intelmq.bots.parsers.microsoft.parser_ctip`
* `public`: no
* `cache (redis db)`: none
* `description`: Parses data from the Microsoft CTIP Feed

 * `overwrite`: If an existing `feed.name` should be overwritten (only relevant for the azure data source).

**Configuration Parameters**

* ``overwrite``: Overwrite an existing field ``feed.name`` with ``DataFeed`` of the source.

**Description**

Can parse the JSON format provided by the Interflow interface (lists of dictionaries) as well as the format provided by the Azure interface (one dictionary per line).
The provided data differs between the two formats/providers.

The parser is capable of parsing both feeds:
- `ctip-c2`
- `ctip-infected-summary`
The feeds only differ by a few fields, not in the format.

The feeds contain a field called `Payload` which is nearly always a base64 encoded JSON structure.
If decoding works, the contained fields are saved as `extra.payload.*`, otherwise the field is saved as `extra.payload.text`.


.. _intelmq.bots.parsers.misp.parser:

MISP
^^^^

* `name:` intelmq.bots.parsers.misp.parser
* `public:` no
* `cache (redis db):` none
* `description:` Parses MISP events

**Description**

MISP events collected by the MISPCollectorBot are passed to this parser
for processing. Supported MISP event categories and attribute types are
defined in the `SUPPORTED_MISP_CATEGORIES` and `MISP_TYPE_MAPPING` class
constants.


.. _n6 parser bot:

.. _intelmq.bots.parsers.n6.parser_n6stomp:

n6
^^

**Information**

* `name`: `intelmq.bots.parsers.n6.parser_n6stomp`
* `public`: no
* `cache (redis db)`: none
* `description`: Convert n6 data into IntelMQ format.

**Configuration Parameters**
None

**Description**

Test messages are ignored, this is logged with debug logging level.
Also contains a mapping for the classification (results in taxonomy, type and identifier).
The `name` field is normally used as `malware.name`, if that fails due to disallowed characters, these characters are removed and the original value is saved as `event_description.text`. This can happen for names like `"further iocs: text with invalid ’ char"`.

If an n6 message contains multiple IP addresses, multiple events are generated, resulting in events only differing in the address information.


.. _intelmq.bots.parsers.twitter.parser:

Twitter
^^^^^^^

**Information**

* `name:` intelmq.bots.parsers.twitter.parser
* `public:` no
* `cache (redis db):` none
* `description:` Extracts URLs from text, fuzzy, aimed at parsing tweets

**Configuration Parameters**

* `domain_whitelist`: domains to be filtered out
* `substitutions`: semicolon delimited list of even length of pairs of substitutions (for example: '[.];.;,;.' substitutes '[.]' for '.' and ',' for '.')
* `classification_type`: string with a valid classification type as defined in data format
* `default_scheme`: Default scheme for URLs if not given. See also the next section.

**Default scheme**

The dependency `url-normalize` changed it's behavior in version 1.4.0 from using `http://` as default scheme to `https://`. Version 1.4.1 added the possibility to specify it. Thus you can only use the `default_scheme` parameter with a current version of this library >= 1.4.1, with 1.4.0 you will always get `https://` as default scheme and for older versions < 1.4.0 `http://` is used.

This does not affect URLs which already include the scheme.


.. _intelmq.bots.parsers.shadowserver.parser:
.. _intelmq.bots.parsers.shadowserver.parser_json:

Shadowserver
^^^^^^^^^^^^

There are two Shadowserver parsers, one for data in ``CSV`` format (``intelmq.bots.parsers.shadowserver.parser``) and one for data in ``JSON`` format (``intelmq.bots.parsers.shadowserver.parser_json``).
The latter was added in IntelMQ 2.3 and is meant to be used together with the Shadowserver API collector.

**Information**

* `name:` `intelmq.bots.parsers.shadowserver.parser` (for CSV data) or `intelmq.bots.parsers.shadowserver.parser_json` (for JSON data)
* `public:` yes
* `description:` Parses different reports from Shadowserver.

**Configuration Parameters**

 * `feedname`: Optional, the Name of the feed, see list below for possible values.
 * `overwrite`: If an existing `feed.name` should be overwritten.

**How this bot works?**

There are two possibilities for the bot to determine which feed the data belongs to in order to determine the correct mapping of the columns:

**Automatic feed detection**

Since IntelMQ version 2.1 the parser can detect the feed based on metadata provided by the collector.

When processing a report, this bot takes `extra.file_name` from the report and
looks in `config.py` how the report should be parsed.

If this lookup is not possible, and the feed name is not given as parameter, the feed cannot be parsed.

The field `extra.file_name` has the following structure:
`%Y-%m-%d-${report_name}[-suffix].csv` where suffix can be something like `country-geo`. For example, some possible filenames are `2019-01-01-scan_http-country-geo.csv` or `2019-01-01-scan_tftp.csv`. The important part is `${report_name}`, between the date and the suffix.
Since version 2.1.2 the date in the filename is optional, so filenames like `scan_tftp.csv` are also detected.

**Fixed feed name**

If the method above is not possible and for upgraded instances, the feed can be set with the `feedname` parameter.
Feed-names are derived from the subjects of the Shadowserver E-Mails.
A list of possible feeds can be found in the table below in the column "feed name".

.. _shadowserver-supported-reports:

**Supported reports**

These are the supported feed name and their corresponding file name for automatic detection:

  =======================================   =========================
   feed name                                 file name
  =======================================   =========================
   Accessible-ADB                            `scan_adb`
   Accessible-AFP                            `scan_afp`
   Accessible-ARD                            `scan_ard`
   Accessible-Cisco-Smart-Install            `cisco_smart_install`
   Accessible-CoAP                           `scan_coap`
   Accessible-CWMP                           `scan_cwmp`
   Accessible-MS-RDPEUDP                     `scan_msrdpeudp`
   Accessible-FTP                            `scan_ftp`
   Accessible-Hadoop                         `scan_hadoop`
   Accessible-HTTP                           `scan_http`
   Accessible-Radmin                         `scan_radmin`
   Accessible-RDP                            `scan_rdp`
   Accessible-Rsync                          `scan_rsync`
   Accessible-SMB                            `scan_smb`
   Accessible-Telnet                         `scan_telnet`
   Accessible-Ubiquiti-Discovery-Service     `scan_ubiquiti`
   Accessible-VNC                            `scan_vnc`
   Blacklisted-IP (deprecated)               `blacklist`
   Blocklist                                 `blocklist`
   Compromised-Website                       `compromised_website`
   DNS-Open-Resolvers                        `scan_dns`
   Honeypot-Amplification-DDoS-Events        `event4_honeypot_ddos_amp`
   Honeypot-Brute-Force-Events               `event4_honeypot_brute_force`
   Honeypot-Darknet                          `event4_honeypot_darknet`
   Honeypot-HTTP-Scan                        `event4_honeypot_http_scan`
   HTTP-Scanners                             `hp_http_scan`
   ICS-Scanners                              `hp_ics_scan`
   IP-Spoofer-Events                         `event4_ip_spoofer`
   Microsoft-Sinkhole-Events IPv4            `event4_microsoft_sinkhole`
   Microsoft-Sinkhole-Events-HTTP IPv4       `event4_microsoft_sinkhole_http`
   NTP-Monitor                               `scan_ntpmonitor`
   NTP-Version                               `scan_ntp`
   Open-Chargen                              `scan_chargen`
   Open-DB2-Discovery-Service                `scan_db2`
   Open-Elasticsearch                        `scan_elasticsearch`
   Open-IPMI                                 `scan_ipmi`
   Open-IPP                                  `scan_ipp`
   Open-LDAP                                 `scan_ldap`
   Open-LDAP-TCP                             `scan_ldap_tcp`
   Open-mDNS                                 `scan_mdns`
   Open-Memcached                            `scan_memcached`
   Open-MongoDB                              `scan_mongodb`
   Open-MQTT                                 `scan_mqtt`
   Open-MSSQL                                `scan_mssql`
   Open-NATPMP                               `scan_nat_pmp`
   Open-NetBIOS-Nameservice                  `scan_netbios`
   Open-Netis                                `netis_router`
   Open-Portmapper                           `scan_portmapper`
   Open-QOTD                                 `scan_qotd`
   Open-Redis                                `scan_redis`
   Open-SNMP                                 `scan_snmp`
   Open-SSDP                                 `scan_ssdp`
   Open-TFTP                                 `scan_tftp`
   Open-XDMCP                                `scan_xdmcp`
   Outdated-DNSSEC-Key                       `outdated_dnssec_key`
   Outdated-DNSSEC-Key-IPv6                  `outdated_dnssec_key_v6`
   Sandbox-URL                               `cwsandbox_url`
   Sinkhole-DNS                              `sinkhole_dns`
   Sinkhole-Events                           `event4_sinkhole`/`event6_sinkhole`
   Sinkhole-Events IPv4                      `event4_sinkhole`
   Sinkhole-Events IPv6                      `event6_sinkhole`
   Sinkhole-HTTP-Events                      `event4_sinkhole_http`/`event6_sinkhole_http`
   Sinkhole-HTTP-Events IPv4                 `event4_sinkhole_http`
   Sinkhole-HTTP-Events IPv6                 `event6_sinkhole_http`
   Sinkhole-Events-HTTP-Referer              `event4_sinkhole_http_referer`/`event6_sinkhole_http_referer`
   Sinkhole-Events-HTTP-Referer IPv4         `event4_sinkhole_http_referer`
   Sinkhole-Events-HTTP-Referer IPv6         `event6_sinkhole_http_referer`
   Spam-URL                                  `spam_url`
   SSL-FREAK-Vulnerable-Servers              `scan_ssl_freak`
   SSL-POODLE-Vulnerable-Servers             `scan_ssl_poodle`
   Vulnerable-Exchange-Server `*`            `scan_exchange`
   Vulnerable-ISAKMP                         `scan_isakmp`
   Vulnerable-HTTP                           `scan_http`
   Vulnerable-SMTP                           `scan_smtp_vulnerable`
  =======================================   =========================

`*` This report can also contain data on active webshells (column `tag` is `exchange;webshell`), and are therefore not only vulnerable but also actively infected.

In addition, the following legacy reports are supported:

  ===========================   ===================================================   ========================
   feed name                     successor feed name                                  file name
  ===========================   ===================================================   ========================
   Amplification-DDoS-Victim     Honeypot-Amplification-DDoS-Events                   ``ddos_amplification``
   CAIDA-IP-Spoofer              IP-Spoofer-Events                                    ``caida_ip_spoofer``
   Darknet                       Honeypot-Darknet                                     ``darknet``
   Drone                         Sinkhole-Events                                      ``botnet_drone``
   Drone-Brute-Force             Honeypot-Brute-Force-Events, Sinkhole-HTTP-Events    ``drone_brute_force``
   Microsoft-Sinkhole            Sinkhole-HTTP-Events                                 ``microsoft_sinkhole``
   Sinkhole-HTTP-Drone           Sinkhole-HTTP-Events                                 ``sinkhole_http_drone``
   IPv6-Sinkhole-HTTP-Drone      Sinkhole-HTTP-Events                                 ``sinkhole6_http``
  ===========================   ===================================================   ========================

More information on these legacy reports can be found in `Changes in Sinkhole and Honeypot Report Types and Formats <https://www.shadowserver.org/news/changes-in-sinkhole-and-honeypot-report-types-and-formats/>`_.

**Development**

**Structure of this Parser Bot**

The parser consists of two files:
 * ``_config.py``
 * ``parser.py`` or ``parser_json.py``

Both files are required for the parser to work properly.

**Add new Feedformats**

Add a new feed format and conversions if required to the file
``_config.py``. Don't forget to update the ``mapping`` dict.
It is required to look up the correct configuration.

Look at the documentation in the bot's ``_config.py`` file for more information.


.. _intelmq.bots.parsers.shodan.parser:

Shodan
^^^^^^

**Information**

* `name:` intelmq.bots.parsers.shodan.parser
* `public:` yes
* `description:` Parses data from Shodan (search, stream etc).

The parser is by far not complete as there are a lot of fields in a big nested structure. There is a minimal mode available which only parses the important/most useful fields and also saves everything in `extra.shodan` keeping the original structure. When not using the minimal mode if may be useful to ignore errors as many parsing errors can happen with the incomplete mapping.

**Configuration Parameters**

* `ignore_errors`: Boolean (default true)
* `minimal_mode`: Boolean (default false)


.. _intelmq.bots.parsers.zoneh.parser:

ZoneH
^^^^^

**Information**

* `name:` intelmq.bots.parsers.zoneh.parser
* `public:` yes
* `description:` Parses data from ZoneH.

**Description**
This bot is designed to consume defacement reports from zone-h.org. It expects
fields normally present in CSV files distributed by email.


.. _expert bots:

***********
Expert Bots
***********


.. _intelmq.bots.experts.abusix.expert:

Abusix
^^^^^^

**Information**

* `name:` intelmq.bots.experts.abusix.expert
* `lookup:` dns
* `public:` yes
* `cache (redis db):` 5
* `description:` RIPE abuse contacts resolving through DNS TXT queries
* `notes`: https://abusix.com/contactdb.html

**Configuration Parameters**

* **Cache parameters** (see in section :ref:`common-parameters`)

**Requirements**

This bot can optionally use the python module *querycontacts* by Abusix itself:
https://pypi.org/project/querycontacts/

.. code-block:: bash

   pip3 install querycontacts

If the package is not installed, our own routines are used.

.. _intelmq.bots.experts.aggregate.expert:

Aggregate
^^^^^^^^^

**Information**

* `name:` intelmq.bots.experts.aggregate.expert
* `lookup:` no
* `public:` yes
* `cache (redis db):` 8
* `description:` Aggregates events based upon given fields & timespan

**Configuration Parameters**

* **Cache parameters** (see in section :ref:`common-parameters`)

  * TTL is not used, using it would result in data loss.
* **fields** Given fields which are used to aggregate like `classification.type, classification.identifier`
* **threshold** If the aggregated event is lower than the given threshold after the timespan, the event will get dropped.
* **timespan** Timespan to aggregate events during the given time. I. e. `1 hour`

**Usage**

Define specific fields to filter incoming events and aggregate them.
Also set the timespan you want the events to get aggregated.
Usage i. e. `1 hour`

**Note**

The "cleanup" procedure, sends out the aggregated events or drops them based upon the given threshold value.
It is called on every incoming message and on the bot's initialization.
If you're potentially running on low traffic ( no incoming events within the given timestamp ) it is recommended to reload or restart the bot
via cronjob each 30 minutes (adapt to your configured timespan).
Otherwise you might loose information.

I. e.:

.. code-block:: bash

   crontab -e

   0,30 * * * *   intelmqctl reload my-aggregate-bot


For reloading/restarting please check the :doc:`intelmqctl` documentation.

.. _intelmq.bots.experts.asn_lookup.expert:

ASN Lookup
^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.asn_lookup.expert`
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` IP to ASN

**Configuration Parameters**

* `database`: Path to the downloaded database.

**Requirements**


Install `pyasn` module

.. code-block:: bash

   pip3 install pyasn

**Database**

Use this command to create/update the database and reload the bot:

.. code-block:: bash

   intelmq.bots.experts.asn_lookup.expert --update-database

The database is fetched from `routeviews.org <http://www.routeviews.org/routeviews/>`_ and licensed under the Creative Commons Attribution 4.0 International license (see the `routeviews FAQ <http://www.routeviews.org/routeviews/index.php/faq/#faq-6666>`_).


.. _intelmq.bots.experts.csv_converter.expert:

CSV Converter
^^^^^^^^^^^^^

**Information**

* `name`: `intelmq.bots.experts.csv_converter.expert`
* `lookup`: no
* `public`: yes
* `cache (redis db)`: none
* `description`: Converts an event to CSV format, saved in the `output` field.

**Configuration Parameters**

* `delimiter`: String, default `","`
* `fieldnames`: Comma-separated list of field names, e.g. `"time.source,classification.type,source.ip"`

**Usage**

To use the CSV-converted data in an output bot - for example in a file output,
use the configuration parameter `single_key` of the output bot and set it to `output`.


.. _intelmq.bots.experts.cymru_whois.expert:

Cymru Whois
^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.cymru_whois.expert`
* `lookup:` Cymru DNS
* `public:` yes
* `cache (redis db):` 5
* `description:` IP to geolocation, ASN, BGP prefix

Public documentation: https://www.team-cymru.com/IP-ASN-mapping.html#dns

**Configuration Parameters**

* **Cache parameters** (see in section :ref:`common-parameters`)
* ``: Overwrite existing fields. Default: `True` if not given (for backwards compatibility, will change in version 3.0.0)


.. _intelmq.bots.experts.remove_affix.expert:

RemoveAffix
^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.remove_affix.expert`
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` Cut string from string

**Configuration Parameters**

* `remove_prefix`: True - cut from start, False - cut from end
* `affix`: example 'www.'
* `field`: example field 'source.fqdn'

**Description**
Remove part of string from string, example: `www.` from domains.


.. _intelmq.bots.experts.domain_suffix.expert:

Domain Suffix
^^^^^^^^^^^^^

This bots adds the public suffix to the event, derived by a domain.
See or information on the public suffix list: https://publicsuffix.org/list/
Only rules for ICANN domains are processed. The list can (and should) contain
Unicode data, punycode conversion is done during reading.

Note that the public suffix is not the same as the top level domain (TLD). E.g.
`co.uk` is a public suffix, but the TLD is `uk`.
Privately registered suffixes (such as `blogspot.co.at`) which are part of the
public suffix list too, are ignored.

**Information**

* `name:` `intelmq.bots.experts.domain_suffix.expert`
* `lookup:` no
* `public:` yes
* `cache (redis db):` -
* `description:` extracts the domain suffix from the FQDN

**Configuration Parameters**

* `field`: either `"fqdn"` or `"reverse_dns"`
* `suffix_file`: path to the suffix file

**Rule processing**

A short summary how the rules are processed:

The simple ones:

.. code-block::

   com
   at
   gv.at

`example.com` leads to `com`, `example.gv.at` leads to `gv.at`.

Wildcards:

.. code-block::

   *.example.com

`www.example.com` leads to `www.example.com`.

And additionally the exceptions, together with the above wildcard rule:

.. code-block::

   !www.example.com

`www.example.com` does now not lead to `www.example.com`, but to `example.com`.


**Database**

Use this command to create/update the database and reload the bot:

.. code-block:: bash

   intelmq.bots.experts.domain_suffix.expert --update-database


.. _intelmq.bots.experts.domain_valid.expert:

Domain valid
^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.domain_valid.expert`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Checks if a domain is valid by performing multiple validity checks (see below).

**Configuration Parameters**

   * `domain_field`: The name of the field to be validated.
   * `tlds_domains_list`: local file with all valid TLDs, default location ``/opt/intelmq/var/lib/bots/domain_valid/tlds-alpha-by-domain.txt``

**Description**

If the field given in `domain_field` does not exist in the event, the event is dropped.
If the domain contains underscores (``_``), the event is dropped.
If the domain is not valid according to the `validators library <https://pypi.org/project/validators/>`_, the event is dropped.
If the domain's last part (the TLD) is not in the TLD-list configured by parameter ``tlds_domains_list``, the field is dropped.
Latest TLD list: https://data.iana.org/TLD/


.. _intelmq.bots.experts.deduplicator.expert:

Deduplicator
^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.deduplicator.expert`
* `lookup:` redis cache
* `public:` yes
* `cache (redis db):` 6
* `description:` Bot responsible for ignore duplicated messages. The bot can be configured to perform deduplication just looking to specific fields on the message.

**Configuration Parameters**

* **Cache parameters** (see in section :ref:`common-parameters`)
* `bypass`- true or false value to bypass the deduplicator. When set to true, messages will not be deduplicated. Default: false

**Parameters for "fine-grained" deduplication**

* `filter_type`: type of the filtering which can be "blacklist" or "whitelist". The filter type will be used to define how Deduplicator bot will interpret the parameter `filter_keys` in order to decide whether an event has already been seen or not, i.e., duplicated event or a completely new event.

  * "whitelist" configuration: only the keys listed in `filter_keys` will be considered to verify if an event is duplicated or not.
  * "blacklist" configuration: all keys except those in `filter_keys` will be considered to verify if an event is duplicated or not.
* `filter_keys`: string with multiple keys separated by comma. Please note that `time.observation` key will not be considered even if defined, because the system always ignore that key.

When using a whitelist field pattern and a small number of fields (keys), it becomes more important, that these fields exist in the events themselves.
If a field does not exist, but is part of the hashing/deduplication, this field will be ignored.
If such events should not get deduplicated, you need to filter them out before the deduplication process, e.g. using a sieve expert.
See also `this discussion thread <https://lists.cert.at/pipermail/intelmq-users/2021-July/000370.html>`_ on the mailing-list.

**Parameters Configuration Example**

*Example 1*

The bot with this configuration will detect duplication only based on `source.ip` and `destination.ip` keys.

.. code-block:: yaml

   parameters:
     redis_cache_db: 6
     redis_cache_host: "127.0.0.1"
     redis_cache_password: null
     redis_cache_port: 6379
     redis_cache_ttl: 86400
     filter_type: "whitelist"
     filter_keys: "source.ip,destination.ip"

*Example 2*

The bot with this configuration will detect duplication based on all keys, except `source.ip` and `destination.ip` keys.

.. code-block:: yaml

   parameters:
     redis_cache_db: 6
     redis_cache_host: "127.0.0.1"
     redis_cache_password: null
     redis_cache_port: 6379
     redis_cache_ttl: 86400
     filter_type: "blacklist"
     filter_keys: "source.ip,destination.ip"

**Flushing the cache**

To flush the deduplicator's cache, you can use the `redis-cli` tool. Enter the database used by the bot and submit the `flushdb` command:

.. code-block:: bash

   redis-cli -n 6
   flushdb


.. _intelmq.bots.experts.do_portal.expert:

DO Portal Expert Bot
^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.do_portal.expert`
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` The DO portal retrieves the contact information from a DO portal instance: http://github.com/certat/do-portal/

**Configuration Parameters**

* `mode` - Either `replace` or `append` the new abuse contacts in case there are existing ones.
* `portal_url` - The URL to the portal, without the API-path. The used URL is `$portal_url + '/api/1.0/ripe/contact?cidr=%s'`.
* `portal_api_key` - The API key of the user to be used. Must have sufficient privileges.


.. _intelmq.bots.experts.field_reducer.expert:

Field Reducer Bot
^^^^^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.field_reducer.expert`
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` The field reducer bot is capable of removing fields from events.

**Configuration Parameters**

* `type` - either `"whitelist"` or `"blacklist"`
* `keys` - Can be a JSON-list of field names (`["raw", "source.account"]`) or a string with a comma-separated list of field names (`"raw,source.account"`).

**Whitelist**

Only the fields in `keys` will passed along.

**Blacklist**

The fields in `keys` will be removed from events.


.. _intelmq.bots.experts.filter.expert:

Filter
^^^^^^

The filter bot is capable of filtering specific events.

**Information**

* `name:` `intelmq.bots.experts.filter.expert`
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` A simple filter for messages (drop or pass) based on a exact string comparison or regular expression

**Configuration Parameters**

*Parameters for filtering with key/value attributes*

* ``filter_key`` - key from data format
* ``filter_value`` - value for the key
* ``filter_action`` - action when a message match to the criteria (possible actions: keep/drop)
* ``filter_regex`` - attribute determines if the ``filter_value`` shall be treated as regular expression or not.
   If this attribute is not empty (can be ``true``, ``yes`` or whatever), the bot uses python's ```re.search`` <https://docs.python.org/3/library/re.html#re.search>`_ function to evaluate the filter with regular expressions.
   If this attribute is empty or evaluates to false, an exact string comparison is performed. A check on string *inequality* can be achieved with the usage of *Paths* described below.

*Parameters for time based filtering*

* `not_before` - events before this time will be dropped
* `not_after` - events after this time will be dropped

Both parameters accept string values describing absolute or relative time:

* absolute

 * basically anything parseable by datetime parser, eg. "2015-09-012T06:22:11+00:00"
 * `time.source` taken from the event will be compared to this value to decide the filter behavior

* relative

 * accepted string formatted like this "<integer> <epoch>", where epoch could be any of following strings (could optionally end with trailing 's'): hour, day, week, month, year
 * time.source taken from the event will be compared to the value (now - relative) to decide the filter behavior

*Examples of time filter definition*

* ```"not_before" : "2015-09-012T06:22:11+00:00"``` events older than the specified time will be dropped
* ```"not_after" : "6 months"``` just events older than 6 months will be passed through the pipeline

**Possible paths**

 * `_default`: default path, according to the configuration
 * `action_other`: Negation of the default path
 * `filter_match`: For all events the filter matched on
 * `filter_no_match`: For all events the filter does not match

 ======= ====== ============ ==============  ==============  =================
 action  match   `_default`  `action_other`  `filter_match`  `filter_no_match`
 ======= ====== ============ ==============  ==============  =================
 keep    ✓      ✓            ✗               ✓               ✗
 keep    ✗      ✗            ✓               ✗               ✓
 drop    ✓      ✗            ✓               ✓               ✗
 drop    ✗      ✓            ✗               ✗               ✓
 ======= ====== ============ ==============  ==============  =================

In `DEBUG` logging level, one can see that the message is sent to both matching paths, also if one of the paths is not configured. Of course the message is only delivered to the configured paths.


.. _intelmq.bots.experts.format_field.expert:

Format Field
^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.format_field.expert`
* `lookup:` none
* `cache (redis db):` none
* `description:` String method operations on column values

**Configuration Parameters**

*Parameters for stripping chars*

* `strip_columns` -  A list of strings or a string of comma-separated values with field names. The names must match the IntelMQ Data Format field names. E.g.

   .. code-block:: json

      "columns": [
           "malware.name",
           "extra.tags"
      ],

   is equivalent to:

   .. code-block:: json

      "columns": "malware.name,extra.tags"

* `strip_chars` -  a set of characters to remove as leading/trailing characters(default: space)

*Parameters for replacing chars*

* `replace_column` - key from data format
* `old_value` - the string to search for
* `new_value` - the string to replace the old value with
* `replace_count` - number specifying how many occurrences of the old value you want to replace(default: `1`)

*Parameters for splitting string to list of string*

* `split_column` - key from data format
* `split_separator` - specifies the separator to use when splitting the string(default: `,`)

Order of operation: `strip -> replace -> split`. These three methods can be combined such as first strip and then split.


.. _intelmq.bots.experts.generic_db_lookup.expert:

Generic DB Lookup
^^^^^^^^^^^^^^^^^

This bot is capable for enriching intelmq events by lookups to a database.
Currently only PostgreSQL and SQLite are supported.

If more than one result is returned, a ValueError is raised.

**Information**

* `name:` `intelmq.bots.experts.generic_db_lookup.expert`
* `lookup:` database
* `public:` yes
* `cache (redis db):` none
* `description:` This bot is capable for enriching intelmq events by lookups to a database.

**Configuration Parameters**

*Connection*

* `engine`: `postgresql` or `sqlite`
* `database`: string, defaults to "intelmq", database name or the SQLite filename
* `table`: defaults to "contacts"

*PostgreSQL specific*

* `host`: string, defaults to "localhost"
* `password`: string
* `port`: integer, defaults to 5432
* `sslmode`: string, defaults to "require"
* `user`: defaults to "intelmq"

*Lookup*

* `match_fields`: defaults to `{"source.asn": "asn"}`

The value is a key-value mapping an arbitrary number **intelmq** field names **to table** column names.
The values are compared with `=` only.

*Replace fields*

* `overwrite`: defaults to `false`. Is applied per field
* `replace_fields`: defaults to `{"contact": "source.abuse_contact"}`

`replace_fields` is again a key-value mapping an arbitrary number of **table** column names **to intelmq** field names


.. _intelmq.bots.experts.gethostbyname.expert:

Gethostbyname
^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.gethostbyname.expert`
* `lookup:` DNS
* `public:` yes
* `cache (redis db):` none
* `description:` DNS name (FQDN) to IP

**Configuration Parameters**

- `fallback_to_url` If True and no `source.fqdn` present, use `source.url` instead while producing `source.ip`
- `gaierrors_to_ignore`: Optional, list (comma-separated) of gaierror codes to ignore, e.g. `-3` for EAI_AGAIN (Temporary failure in name resolution). Only accepts the integer values, not the names.
- `overwrite`: Boolean. If true, overwrite existing IP addresses. Default: False.

**Description**

Resolves the `source/destination.fqdn` hostname using the `gethostbyname` syscall and saves the resulting IP address as `source/destination.ip`.
The following gaierror resolution errors are ignored and treated as if the hostname cannot be resolved:

- `-2`/`EAI_NONAME`: NAME or SERVICE is unknown
- `-4`/`EAI_FAIL`: Non-recoverable failure in name res.
- `-5`/`EAI_NODATA`: No address associated with NAME.
- `-8`/`EAI_SERVICE`: SERVICE not supported for `ai_socktype'.
- `-11`/`EAI_SYSTEM`: System error returned in `errno'.

Other errors result in an exception if not ignored by the parameter `gaierrors_to_ignore` (see above).
All gaierrors can be found here: http://www.castaglia.org/proftpd/doc/devel-guide/src/lib/glibc-gai_strerror.c.html


.. _intelmq.bots.experts.http.expert_status:

HTTP Status
^^^^^^^^^^^

Fetches the HTTP Status for a given URI

**Information**

* `name:` intelmq.bots.experts.http.expert_status
* `description:` The bot fetches the HTTP status for a given URL and saves it in the event.

**Configuration Parameters**

* `field:` The name of the field containing the URL to be checked (required).
* `success_status_codes:` A list of success status codes. If this parameter is omitted or the list is empty, successful status codes are the ones between 200 and 400.
* `overwrite:` Specifies if an existing 'status' value should be overwritten.


.. _intelmq.bots.experts.http.expert_content:

HTTP Content
^^^^^^^^^^^^

Fetches an HTTP resource and checks if it contains a specific string.

**Information**

* `name:` intelmq.bots.experts.http.expert_content
* `description:` The bot fetches an HTTP resource and checks if it contains a specific string.

**Configuration Parameters**

* `field:` The name of the field containing the URL to be checked (defaults to `source.url`)
* `needle:` The string that the content available on URL is checked for
* `overwrite:` A boolean value that specifies if an existing 'status' value should be overwritten.


.. _intelmq.bots.experts.idea.expert:

IDEA Converter
^^^^^^^^^^^^^^

Converts the event to IDEA format and saves it as JSON in the field `output`. All other fields are not modified.

Documentation about IDEA: https://idea.cesnet.cz/en/index

**Information**

* `name:` intelmq.bots.experts.idea.expert
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` The bot does a best effort translation of events into the IDEA format.

**Configuration Parameters**

* `test_mode`: add `Test` category to mark all outgoing IDEA events as informal (meant to simplify setting up and debugging new IDEA producers) (default: `true`)


.. _intelmq.bots.experts.jinja.expert:

Jinja2 Template Expert
^^^^^^^^^^^^^^^^^^^^^^

This bot lets you modify the content of your IntelMQ message fields using Jinja2 templates.

Documentation about Jinja2 templating language: https://jinja.palletsprojects.com/

**Information**

* `name:` intelmq.bots.experts.jinja.expert
* `description:` Modify the content of IntelMQ messages using jinja2 templates

**Configuration Parameters**

* `fields`: a dict containing as key the name of the field where the result of the Jinja2 template should be written to and as value either a Jinja2 template or a filepath to a Jinja2 template file (starting with ``file:///``). Because the experts decides if it is a filepath based on the value starting with ``file:///`` it is not possible to simply write values starting with ``file:///`` to fields.
  The object containing the existing message will be passed to the Jinja2 template with the name ``msg``.

  .. code-block:: yaml

     fields:
       output: The provider is {{ msg['feed.provider'] }}!
       feed.url: "{{ msg['feed.url'] | upper }}"
       extra.somejinjaoutput: file:///etc/intelmq/somejinjatemplate.j2


.. _intelmq.bots.experts.lookyloo.expert:

Lookyloo
^^^^^^^^

Lookyloo is a website screenshotting and analysis tool. For more information and installation instructions visit https://www.lookyloo.eu/

The bot sends a request for `source.url` to the configured Lookyloo instance and saves the retrieved website screenshot link in the field `screenshot_url`. Lookyloo only *queues* the website for screenshotting, therefore the screenshot may not be directly ready after the bot requested it.
The `pylookyloo` library is required for this bot.
The `http_user_agent` parameter is passed on, but not other HTTP-related parameter like proxies.

Events without `source.url` are ignored.

**Information**

* `name:` intelmq.bots.experts.lookyloo.expert
* `description:` LookyLoo expert bot for automated website screenshots

**Configuration Parameters**

* `instance_url`: LookyLoo instance to connect to


.. _intelmq.bots.experts.maxmind_geoip.expert:

MaxMind GeoIP
^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.experts.maxmind_geoip.expert
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` IP to geolocation

**Setup**

The bot requires the MaxMind's `geoip2` Python library, version 2.2.0 has been tested.

To download the database a free license key is required. More information can be found at https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/

**Configuration Parameters**

* `database`: Path to the local database, e.g. `"/opt/intelmq/var/lib/bots/maxmind_geoip/GeoLite2-City.mmdb"`
* `overwrite`: boolean
* `use_registered`: boolean. MaxMind has two country ISO codes: One for the physical location of the address and one for the registered location. Default is `false` (backwards-compatibility). See also https://github.com/certtools/intelmq/pull/1344 for a short explanation.
* `license_key`: License key is necessary for downloading the GeoLite2 database.

**Database**

Use this command to create/update the database and reload the bot:

.. code-block:: bash

   intelmq.bots.experts.maxmind_geoip.expert --update-database


.. _intelmq.bots.experts.misp.expert:

MISP
^^^^

Queries a MISP instance for the `source.ip` and adds the MISP Attribute UUID and MISP Event ID of the newest attribute found.

**Information**

* `name:` intelmq.bots.experts.misp.expert
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` IP address to MISP attribute and event

**Configuration Parameters**

* `misp_key`: MISP Authkey
* `misp_url`: URL of MISP server (with trailing '/')

Generic parameters used in this bot:

* `http_verify_cert`: Verify the TLS certificate of the server, boolean (default: `true`)


.. _intelmq.bots.experts.mcafee.expert_mar:

McAfee Active Response Hash lookup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.experts.mcafee.expert_mar
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Queries occurrences of hashes within local environment

**Configuration Parameters**

* **Feed parameters** (see above)
* `dxl_config_file`: location of file containing required information to connect to DXL bus
* `lookup_type`: One of:
  - `Hash`: looks up `malware.hash.md5`, `malware.hash.sha1` and `malware.hash.sha256`
  - `DestSocket`: looks up `destination.ip` and `destination.port`
  - `DestIP`: looks up `destination.ip`
  - `DestFQDN`: looks up in `destination.fqdn`


.. _intelmq.bots.experts.mcafee.expert_mar:

McAfee Active Response lookup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` intelmq.bots.experts.mcafee.expert_mar
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Queries DXL bus for hashes, IP addresses or FQDNs.

**Configuration Parameters**

* **Feed parameters** (see above)
* `dxl_config_file`: location of file containing required information to connect to DXL bus
* `lookup_type`: One of <Hash|DestSocket|DestIP|DestFQDN>


.. _intelmq.bots.experts.modify.expert:

Modify
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.modify.expert`
* `lookup:` local config
* `public:` yes
* `cache (redis db):` none
* `description:` modify expert bot allows you to change arbitrary field values of events just using a configuration file

**Configuration Parameters**

* `configuration_path`: filename
* `case_sensitive`: boolean, default: true
* `maximum_matches`: Maximum number of matches. Processing stops after the limit is reached. Default: no limit (`null`, `0`).
* `overwrite`: Overwrite any existing fields by matching rules. Default if the parameter is given: `true`, for backwards compatibility. Default will change to `false` in version 3.0.0.

**Configuration File**

The modify expert bot allows you to change arbitrary field values of events just using a configuration file. Thus it is possible to adapt certain values or adding new ones only by changing JSON-files without touching the code of many other bots.

The configuration is called `modify.conf` and looks like this:

.. code-block:: json

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

In our example above we have five groups labeled `Standard Protocols http`,
`Spamhaus Cert conficker`, `bitdefender`, `urlzone` and `default`.
All sections will be considered, in the given order (from top to bottom).

Each rule consists of *conditions* and *actions*.
Conditions and actions are dictionaries holding the field names of events
and regular expressions to match values (selection) or set values (action).
All matching rules will be applied in the given order.
The actions are only performed if all selections apply.

If the value for a condition is an empty string, the bot checks if the field does not exist.
This is useful to apply default values for empty fields.


**Actions**

You can set the value of the field to a string literal or number.

In addition you can use the `standard Python string format syntax <https://docs.python.org/3/library/string.html#format-string-syntax>`_
to access the values from the processed event as `msg` and the match groups
of the conditions as `matches`, see the bitdefender example above.
Group 0 (`[0]`) contains the full matching string. See also the documentation on `re.Match.group <https://docs.python.org/3/library/re.html?highlight=re%20search#re.Match.group>`_.

Note that `matches` will also contain the match groups
from the default conditions if there were any.

**Examples**

We have an event with `feed.name = Spamhaus Cert` and `malware.name = confickerab`. The expert loops over all sections in the file and eventually enters section `Spamhaus Cert`. First, the default condition is checked, it matches! OK, going on. Otherwise the expert would have selected a different section that has not yet been considered. Now, go through the rules, until we hit the rule `conficker`. We combine the conditions of this rule with the default conditions, and both rules match! So we can apply the action: `classification.identifier` is set to `conficker`, the trivial name.

Assume we have an event with `feed.name = Spamhaus Cert` and `malware.name = feodo`. The default condition matches, but no others. So the default action is applied. The value for `classification.identifier` will be set to `feodo` by `{msg[malware.name]}`.

**Types**

If the rule is a string, a regular expression search is performed, also for numeric values (`str()` is called on them). If the rule is numeric for numeric values, a simple comparison is done. If other types are mixed, a warning will be thrown.

For boolean values, the comparison value needs to be `true` or `false` as in JSON they are written all-lowercase.


.. _intelmq.bots.experts.national_cert_contact_certat.expert:

National CERT contact lookup by CERT.AT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.national_cert_contact_certat.expert`
* `lookup:` https
* `public:` yes
* `cache (redis db):` none
* `description:` https://contacts.cert.at offers an IP address to national CERT contact (and cc) mapping. See https://contacts.cert.at for more info.

**Configuration Parameters**

* `filter`: (true/false) act as a filter for AT.
* `overwrite_cc`: set to true if you want to overwrite any potentially existing cc fields in the event.


.. _intelmq.bots.experts.rdap.expert:

RDAP
^^^^

**Information**

* `name:` `intelmq.bots.experts.rdap.expert`
* `lookup:` http/https
* `public:` yes/no
* `cache (redis db):` 5
* `description:` Asks rdap servers for a given domain.

**Configuration Parameters**

* ``rdap_order``: a list of strings, default ``['abuse', 'technical']``. Search order of contacts with these roles.
* ``rdap_bootstrapped_servers``: Customized RDAP servers. Do not forget the trailing slash. For example:

.. code-block:: bash

   {
      "at": {
         "url": "rdap.server.at/v1/,
         "auth": {
            "type": "jwt",
            "token": "ey..."
         }
      },
      "de": "rdap.service:1337/v1/"
   }


.. _intelmq.bots.experts.recordedfuture_iprisk.expert:

RecordedFuture IP risk
^^^^^^^^^^^^^^^^^^^^^^

This Bot tags events with score found in recorded futures large IP risklist.

**Information**

* `name:` `intelmq.bots.experts.recordedfuture_iprisk.expert`
* `lookup:` local database
* `public:` no
* `cache (redis db):` none
* `description:` Record risk score associated to source and destination IP if they are present. Assigns 0 to IP addresses not in the RF list.

**Configuration Parameters**

* `database`: Location of csv file obtained from recorded future API (a script is provided to download the large IP set)
* `overwrite`: set to true if you want to overwrite any potentially existing risk score fields in the event.
* `api_token`: This needs to contain valid API token to download the latest database data.

**Description**

For both `source.ip` and `destination.ip` the corresponding risk score is fetched from a local database created from Recorded Future's API. The score is recorded in `extra.rf_iprisk.source` and `extra.rf_iprisk.destination`. If a lookup for an IP fails a score of 0 is recorded.

See https://www.recordedfuture.com/products/api/ and speak with your recorded future representative for more information.


The list is obtained from recorded future API and needs a valid API TOKEN
The large list contains all IP's with a risk score of 25 or more.
If IP's are not present in the database a risk score of 0 is given

A script is supplied that may be run as intelmq to update the database.

**Database**

Use this command to create/update the database and reload the bot:

.. code-block:: bash

   intelmq.bots.experts.recordedfuture_iprisk.expert --update-database


.. _intelmq.bots.experts.reverse_dns.expert:

Reverse DNS
^^^^^^^^^^^

For both `source.ip` and `destination.ip` the PTR record is fetched and the first valid result is used for `source.reverse_dns`/`destination.reverse_dns`.

**Information**

* `name:` `intelmq.bots.experts.reverse_dns.expert`
* `lookup:` DNS
* `public:` yes
* `cache (redis db):` 8
* `description:` IP to domain

**Configuration Parameters**

* **Cache parameters** (see in section :ref:`common-parameters`)
* `cache_ttl_invalid_response`: The TTL for cached invalid responses.
* `overwrite`: Overwrite existing fields. Default: `True` if not given (for backwards compatibility, will change in version 3.0.0)


.. _intelmq.bots.experts.rfc1918.expert:

RFC1918
^^^^^^^

Several RFCs define ASNs, IP Addresses and Hostnames (and TLDs) reserved for *documentation*.
Events or fields of events can be dropped if they match the criteria of either being reserved for documentation (e.g. AS 64496, Domain `example.com`)
or belonging to a local area network (e.g. `192.168.0.0/24`). These checks can applied to URLs, IP Addresses, FQDNs and ASNs.

It is configurable if the whole event should be dropped ("policies") or just the field removed, as well as which fields should be checked.

Sources:

* :rfc:`1918`
* :rfc:`2606`
* :rfc:`3849`
* :rfc:`4291`
* :rfc:`5737`
* https://en.wikipedia.org/wiki/IPv4
* https://en.wikipedia.org/wiki/Autonomous\_system\_(Internet)

**Information**

* `name:` `intelmq.bots.experts.rfc1918.expert`
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` removes events or single fields with invalid data

**Configuration Parameters**

* `fields`: string, comma-separated list of fields e.g. `destination.ip,source.asn,source.url`. Supported fields are:

  * `destination.asn` & `source.asn`
  * `destination.fqdn` & `source.fqdn`
  * `destination.ip` & `source.ip`
  * `destination.url` & `source.url`
* `policy`: string, comma-separated list of policies, e.g. `del,drop,drop`. `drop` will cause that the the entire event to be removed if the field is , `del` causes the field to be removed.

With the example parameter values given above, this means that:

* If a `destination.ip` value is part of a reserved network block, the field will be removed (policy "del").
* If a `source.asn` value is in the range of reserved AS numbers, the event will be removed altogether (policy "drop).
* If a `source.url` value contains a host with either an IP address part of a reserved network block, or a reserved domain name (or with a reserved TLD), the event will be dropped (policy "drop")


.. _intelmq.bots.experts.ripe.expert:

RIPE
^^^^

Online RIPE Abuse Contact and Geolocation Finder for IP addresses and Autonomous Systems.

**Information**

* `name:` `intelmq.bots.experts.ripe.expert`
* `lookup:` HTTPS API
* `public:` yes
* `cache (redis db):` 10
* `description:` IP to abuse contact

**Configuration Parameters**

* **Cache parameters** (see section :ref:`common-parameters`)
* `mode`: either `append` (default) or `replace`
* `query_ripe_db_asn`: Query for IPs at `http://rest.db.ripe.net/abuse-contact/%s.json`, default `true`
* `query_ripe_db_ip`: Query for ASNs at `http://rest.db.ripe.net/abuse-contact/as%s.json`, default `true`
* `query_ripe_stat_asn`: Query for ASNs at `https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=%s`, default `true`
* `query_ripe_stat_ip`: Query for IPs at `https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=%s`, default `true`
* `query_ripe_stat_geolocation`: Query for IPs at `https://stat.ripe.net/data/maxmind-geo-lite/data.json?resource=%s`, default `true`


.. _intelmq.bots.experts.sieve.expert:

Sieve
^^^^^

**Information**

* `name:` `intelmq.bots.experts.sieve.expert`
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` Filtering with a sieve-based configuration language

**Configuration Parameters**

* `file`: Path to sieve file. Syntax can be validated with `intelmq_sieve_expert_validator`.


**Description**

The sieve bot is used to filter and/or modify events based on a set of rules. The
rules are specified in an external configuration file and with a syntax *similar*
to the `Sieve language <http://sieve.info>`_ used for mail filtering.

Each rule defines a set of matching conditions on received events. Events can be
matched based on keys and values in the event. Conditions can be combined using
parenthesis and the boolean operators ``&&`` and ``||``. If the processed event
matches a rule's conditions, the corresponding actions are performed. Actions
can specify whether the event should be kept or dropped in the pipeline
(filtering actions) or if keys and values should be changed (modification
actions).

**Requirements**

To use this bot, you need to install the required dependencies:

.. code-block:: bash

   pip3 install -r intelmq/bots/experts/sieve/REQUIREMENTS.txt

**Examples**

The following excerpts illustrate some of the basic features of the sieve file
format:

.. code-block::

   if :exists source.fqdn {
     keep  // aborts processing of subsequent rules and forwards the event.
   }


   if :notexists source.abuse_contact || source.abuse_contact =~ '.*@example.com' {
     drop  // aborts processing of subsequent rules and drops the event.
   }

   if source.ip << '192.0.0.0/24' {
       add! comment = 'bogon' // sets the field comment to this value and overwrites existing values
       path 'other-path' // the message is sent to the given path
   }

   if classification.type == ['phishing', 'malware-distribution'] && source.fqdn =~ '.*\.(ch|li)$' {
     add! comment = 'domainabuse'
     keep
   } elif classification.type == 'scanner' {
     add! comment = 'ignore'
     drop
   } else {
     remove comment
   }


**Reference**

*Sieve File Structure*

The sieve file contains an arbitrary number of rules of the form:

.. code-block::

   if EXPRESSION {
       ACTIONS
   } elif EXPRESSION {
       ACTIONS
   } else {
       ACTIONS
   }


Nested if-statements and mixed if statements and rules in the same scope are possible.

*Expressions*

Each rule specifies on or more expressions to match an event based on its keys
and values. Event keys are specified as strings without quotes. String values
must be enclosed in single quotes. Numeric values can be specified as integers
or floats and are unquoted. IP addresses and network ranges (IPv4 and IPv6) are
specified with quotes. List values for use with list/set operators are specified
as string, float, int, bool and string literals separated by commas and enclosed
in square brackets.
Expression statements can be combined and chained using
parentheses and the boolean operators ``&&`` and ``||``.
The following operators may be used to match events:

 * `:exists` and `:notexists` match if a given key exists, for example:

    ``if :exists source.fqdn { ... }``

 * `==` and `!=` match for equality of strings, numbers, and booleans, for example:

   ``if feed.name != 'acme-security' || feed.accuracy == 100 || extra.false_positive == false { ... }``

 * `:contains` matches on substrings.

 * `=~` matches strings based on the given regular expression. `!~` is the inverse regular expression match.

 * Numerical comparisons are evaluated with `<`, `<=`, `>`, `>=`.

 * `<<` matches if an IP address is contained in the specified network range:

   ``if source.ip << '10.0.0.0/8' { ... }``

 * String values to match against can also be specified as lists of strings, which have separate operators. For example:

   ``if source.ip :in ['8.8.8.8', '8.8.4.4'] { ... }``

  In this case, the event will match if it contains a key `source.ip` with
  either value `8.8.8.8` or `8.8.4.4`.

  There are also `:containsany` to match at least one of a list of substrings, and `:regexin` to match at least one of
  a list of regular expressions, similar to the `:contains` and `=~` operators.

 * Lists of numeric values support `:in` to check for inclusion in a list of numbers:

   ``if source.port :in [80, 443] { ... }``

 * `:equals` tests for equality between lists, including order. Example for checking a hostname-port pair:
   ``if extra.host_tuple :equals ['dns.google', 53] { ... }``
 * `:setequals` tests for set-based equality (ignoring duplicates and value order) between a list of given values. Example for checking for the first nameserver of two domains, regardless of the order they are given in the list:
   ``if extra.hostnames :setequals ['ns1.example.com', 'ns1.example.mx'] { ... }``

 * `:overlaps` tests if there is at least one element in common between the list specified by a key and a list of values. Example for checking if at least one of the ICS, database or vulnerable tags is given:
   ``if extra.tags :overlaps ['ics', 'database', 'vulnerable'] { ... } ``

 * `:subsetof` tests if the list of values from the given key only contains values from a set of values specified as the argument. Example for checking for a host that has only ns1.example.com and/or ns2.[...] as its apparent hostname:
   ``if extra.hostnames :subsetof ['ns1.example.com', 'ns2.example.com'] { ... }``

 * `:supersetof` tests if the list of values from the given key is a superset of the values specified as the argument. Example for matching hosts with at least the IoT and vulnerable tags:
   ``if extra.tags :supersetof ['iot', 'vulnerable'] { ... }``

 * Boolean values can be matched with `==` or `!=` followed by `true` or `false`. Example:
   ``if extra.has_known_vulns == true { ... }``

 * The combination of multiple expressions can be done using parenthesis and boolean operators:

  ``if (source.ip == '127.0.0.1') && (comment == 'add field' || classification.taxonomy == 'vulnerable') { ... }``

 * Any single expression or a parenthesised group of expressions can be negated using `!`:

 ``if ! source.ip :contains '127.0.0.' || ! ( source.ip == '172.16.0.5' && source.port == 25 ) { ... }``

  * Note: Since 3.0.0, list-based operators are used on list values, such as `foo :in [1, 2, 3]` instead of `foo == [1, 2, 3]`
    and `foo :regexin ['.mx', '.zz']` rather than `foo =~ ['.mx', '.zz']`, and similarly for `:containsany` vs `:contains`.
    Besides that, ``:notcontains` has been removed, with e.g `foo :notcontains ['.mx', '.zz']` now being represented using negation
    as `! foo :contains ['.mx', '.zz']`.

*Actions*

If part of a rule matches the given conditions, the actions enclosed in `{` and
`}` are applied. By default, all events that are matched or not matched by rules
in the sieve file will be forwarded to the next bot in the pipeline, unless the
`drop` action is applied.

 * `add` adds a key value pair to the event. It can be a string, number, or boolean. This action only applies if the key is not yet defined in the event. If the key is already defined, the action is ignored. Example:

   ``add comment = 'hello, world'``

   Some basic mathematical expressions are possible, but currently support only relative time specifications objects are supported.
   For example:
   ```add time.observation += '1 hour'```
   ```add time.observation -= '10 hours'```

 * `add!` same as above, but will force overwrite the key in the event.

 * `update` modifies an existing value for a key. Only applies if the key is already defined. If the key is not defined in the event, this action is ignored. This supports mathematical expressions like above. Example:

   ``update feed.accuracy = 50``

   Some basic mathematical expressions are possible, but currently support only relative time specifications objects are supported.
   For example:
   ```update time.observation += '1 hour'```
   ```update time.observation -= '10 hours'```

 * `remove` removes a key/value from the event. Action is ignored if the key is not defined in the event. Example:

    ``remove extra.comments``

 * `keep` sends the message to the next bot in the pipeline (same as the default behaviour), and stops sieve file processing.

   ``keep``

 * `path` sets the path (named queue) the message should be sent to (implicitly
   or with the command `keep`. The named queue needs to configured in the
   pipeline, see the User Guide for more information.

   ``path 'named-queue'``

   You can as well set multiple destination paths with the same syntax as for value lists:

   ``path ['one', 'two']``

   This will result in two identical message, one sent to the path `one` and the other sent to the path `two`.

   If the path is not configured, the error looks like:

   ```
     File "/path/to/intelmq/intelmq/lib/pipeline.py", line 353, in send
       for destination_queue in self.destination_queues[path]:
   KeyError: 'one'
   ```

 * `drop` marks the event to be dropped. The event will not be forwarded to the next bot in the pipeline. The sieve file processing is interrupted upon
   reaching this action. No other actions may be specified besides the `drop` action within `{` and `}`.


*Comments*

Comments may be used in the sieve file: all characters after `//` and until the end of the line will be ignored.


*Validating a sieve file*

Use the following command to validate your sieve files:

.. code-block:: bash

   $ intelmq.bots.experts.sieve.validator
   usage: intelmq.bots.experts.sieve.validator [-h] sievefile

   Validates the syntax of sievebot files.

   positional arguments:
     sievefile   Sieve file

   optional arguments:
     -h, --help  show this help message and exit


.. _intelmq.bots.experts.splunk_saved_search.expert:

Splunk saved search
^^^^^^^^^^^^^^^^^^^

**Information**

* `name`: `intelmq.bots.experts.splunk_saved_search.expert`
* `lookup`: splunk database
* `public`: no
* `cache (redis db)`: none
* `description`: Enrich an event from Splunk search results.

**Configuration Parameters**

* **HTTP parameters** (see above)
* `auth_token`: String, Splunk API authentication token
* `url`: String, base URL of the Splunk REST API
* `retry_interval`: Integer, optional, default 5, number of seconds to wait between polling for search results to be available
* `saved_search`: String, name of Splunk saved search to run
* `search_parameters`: Array of string->string, optional, default ``{}``, IntelMQ event fields containing the data to search for, mapped to parameters of the Splunk saved search. Example:

  .. code-block:: json

     "search_parameters": {
         "source.ip": "ip"
     }

* `result_fields`: Array of string->string, optional, default ``{}``, Splunk search result fields mapped to IntelMQ event fields to store the results in. Example:

  .. code-block:: json

     "result_fields": {
         "username": "source.account"
     }

* `not_found`: List of strings, default ``[ "warn", "send" ]``, what to do if the search returns zero results. All specified actions are performed. Valid values are:

  * `warn`: log a warning message
  * `send`: send the event on unmodified
  * `drop`: drop the message

    * `send` and `drop` are mutually exclusive

* `multiple_result_handling`: List of strings, default ``[ "warn", "use_first", "send" ]``, what to do if the search returns more than one result. All specified actions are performed. Valid values are:

  * `limit`: limit the search so that duplicates are impossible
  * `warn`: log a warning message
  * `use_first`: use the first search result
  * `ignore`: do not modify the event
  * `send`: send the event on
  * `drop`: drop the message

    * `limit` cannot be combined with any other value
    * `send` and `drop` are mutually exclusive
    * `ignore` and `use_first` are mutually exclusive

* `overwrite`: Boolean or null, optional, default null, whether search results overwrite values already in the message or not. If null, attempting to add a field that already exists throws an exception.

**Description**

Runs a saved search in Splunk using fields in an event, adding fields from the search result into the event.

Splunk documentation on saved searches: https://docs.splunk.com/Documentation/Splunk/latest/Report/Createandeditreports

The saved search should take parameters according to the `search_parameters` configuration and deliver results according to `result_fields`. The examples above match a saved search of this format:

::

   index="dhcp" ipv4address="$ip$" | ... | fields _time username ether

The time window used is the one saved with the search.

Waits for Splunk to return an answer for each message, so slow searches will delay the entire botnet. If you anticipate a load of more than one search every few seconds, consider running multiple load-balanced copies of this bot.


.. _intelmq.bots.experts.taxonomy.expert:

Taxonomy
^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.taxonomy.expert`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Adds the `classification.taxonomy` field according to the RSIT taxonomy.

Please note that there is a :issue:`slight mismatch of IntelMQ's taxonomy to the upstream taxonomy <1409>`, but it should not matter here much.

**Configuration Parameters**

None.

**Description**

Information on the "Reference Security Incident Taxonomy" can be found here: https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force

For brevity, "type" means `classification.type` and "taxonomy" means `classification.taxonomy`.

- If taxonomy is missing, and type is given, the according taxonomy is set.
- If neither taxonomy, not type is given, taxonomy is set to "other" and type to "unknown".
- If taxonomy is given, but type is not, type is set to "unknown".


.. _intelmq.bots.experts.threshold.expert:

Threshold
^^^^^^^^^

**Information**


* **Cache parameters** (see section :ref:`common-parameters`)
* `name`: `intelmq.bots.experts.threshold.expert`
* `lookup`: redis cache
* `public`: no
* `cache (redis db)`: 11
* `description`: Check if the number of similar messages during a specified time interval exceeds a set value.

**Configuration Parameters**

* `filter_keys`: String, comma-separated list of field names to consider or ignore when determining which messages are similar.
* `filter_type`: String, `whitelist` (consider only the fields in `filter_keys`) or `blacklist` (consider everything but the fields in `filter_keys`).
* `timeout`: Integer, number of seconds before threshold counter is reset.
* `threshold`: Integer, number of messages required before propagating one. In forwarded messages, the threshold is saved in the message as `extra.count`.
* `add_keys`: Array of string->string, optional, fields and values to add (or update) to propagated messages. Example:

  .. code-block:: json

     "add_keys": {
         "classification.type": "spam",
         "comment": "Started more than 10 SMTP connections"
     }

**Limitations**

This bot has certain limitations and is not a true threshold filter (yet). It works like this:

1. Every incoming message is hashed according to the `filter_*` parameters.
2. The hash is looked up in the cache and the count is incremented by 1, and the TTL of the key is (re-)set to the timeout.
3. If the new count matches the threshold exactly, the message is forwarded. Otherwise it is dropped.

Please note: Even if a message is sent, any further identical messages are dropped, if the time difference to the last message is less than the timeout! The counter is not reset if the threshold is reached.


.. _intelmq.bots.experts.tor_nodes.expert:

Tor Nodes
^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.tor_nodes.expert`
* `lookup:` local database
* `public:` yes
* `cache (redis db):` none
* `description:` check if IP is tor node

**Configuration Parameters**

* `database`: Path to the database

**Database**

Use this command to create/update the database and reload the bot:

.. code-block:: bash

   intelmq.bots.experts.tor_nodes.expert --update-database

.. _intelmq.bots.experts.trusted_introducer_lookup.expert:

Trusted Introducer Lookup Expert
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.trusted_introducer_lookup.expert`
* `lookup:` internet
* `public:` yes
* `cache (redis db):` none
* `description:` Lookups data from trusted introducer public teams list.

**Configuration Parameters**

* **order**: Possible values are 'domain', 'asn'. You can set multiple values, so first match wins.
* If 'domain' is set, it will lookup the `source.fqdn` field. It will go from high-order to low-order, i.e. 1337.super.example.com -> super.example.com -> example.com -> `.com`
* If 'asn' is set, it will lookup `source.asn`.

After a match, the abuse contact will be fetched from the trusted introducer teams list and will be stored in the event as `source.abuse_contact`.
If there is no match, the event will not be enriched and will be sent to the next configured step.


.. _intelmq.bots.experts.tuency.expert:

Tuency
^^^^^^

**Information**

* `name:` `intelmq.bots.experts.tuency.expert`
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Queries the `IntelMQ API <https://gitlab.com/intevation/tuency/tuency/-/blob/master/backend/docs/IntelMQ-API.md>`_ of a `Tuency Contact Database <https://gitlab.com/intevation/tuency/tuency/>`_ instance.

**Configuration Parameters**

- `url`: Tuency instance URL. Without the API path.
- `authentication_token`: The Bearer authentication token. Without the ``Bearer`` prefix.
- `overwrite`: Boolean, if existing data in ``source.abuse_contact`` should be overwritten. Default: true

**Description**

*tuency* is a contact management database addressing the needs of CERTs.
Users of *tuency* can configure contact addresses and delivery settings for IP objects (addresses, netblocks), Autonomous Systems, and (sub-)domains.
This expert queries the information for ``source.ip`` and ``source.fqdn`` using the following other fields:

- ``classification.taxonomy``
- ``classification.type``
- ``feed.provider``
- ``feed.name``

These fields therefore need to exist, otherwise the message is skipped.

The API parameter "feed_status" is currently set to "production" constantly, until IntelMQ supports this field.

The API answer is processed as following. For the notification interval:

- If *suppress* is true, then ``extra.notify`` is set to false.
- Otherwise:

  - If the interval is *immediate*, then ``extra.ttl`` is set to 0.
  - Otherwise the interval is converted into seconds and saved in ``extra.ttl``.

For the contact lookup:
For both fields *ip* and *domain*, the *destinations* objects are iterated and its *email* fields concatenated to a comma-separated list in ``source.abuse_contact``.

The IntelMQ fields used by this bot may change in the next IntelMQ release, as soon as better suited fields are available.


.. _intelmq.bots.experts.truncate_by_delimiter.expert:

Truncate By Delimiter
^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.experts.truncate_by_delimiter.expert`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Cut string if length is bigger than maximum length

**Configuration Parameters**

* `delimiter`: The delimiter to be used for truncating, for example ``.`` or ``;``
* `max_length`: The maximum string length.
* `field`: The field to be truncated, e.g. ``source.fqdn``

The given field is truncated step-by-step using the delimiter from the beginning, until the field is shorter than `max_length`.

Example: Cut through a long domain with a dot. The string is truncated until the domain does not exceed the configured maximum length.

- input domain (e.g. ``source.fqdn``): ``www.subdomain.web.secondsubomain.test.domain.com``
- delimiter: ``.``
- ``max_length``: 20
- Resulting value ``test.domain.com`` (length: 15 characters)


.. _intelmq.bots.experts.url2fqdn.expert:

Url2FQDN
^^^^^^^^

This bot extracts the Host from the `source.url` and `destination.url` fields and
writes it to `source.fqdn` or `destination.fqdn` if it is a hostname, or
`source.ip` or `destination.ip` if it is an IP address.

**Information**

* `name:` `intelmq.bots.experts.url2fqdn.expert`
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` writes domain name from URL to FQDN or IP address

**Configuration Parameters**

* `overwrite`: boolean, replace existing FQDN / IP address?


.. _intelmq.bots.experts.uwhoisd.expert:

uWhoisd
^^^^^^^

`uWhoisd <https://github.com/Lookyloo/uwhoisd>`_ is a universal Whois server that supports
caching and stores whois entries for historical purposes.

The bot sends a request for `source.url`, `source.fqdn`, `source.ip` or `source.asn`
to the configured uWhoisd instance and saves the retrieved whois entry:

* If both `source.url` and `source.fqdn` are present, it will only do a request for `source.fqdn`,
  as the hostname of `source.url` should be the same as `source.fqdn`.
  The whois entry will be saved in `extra.whois.fqdn`.
* If `source.ip` is present, the whois entry will be saved in `extra.whois.ip`
* If `source.asn` is present, he whois entry will be saved in `extra.whois.asn`

Events without `source.url`, `source.fqdn`, `source.ip`, or `source.asn`, are ignored.

**Note**: requesting a whois entry for a fully qualified domain name (FQDN) only works if the request
only contains the domain. uWhoisd will automatically strip the subdomain part if it is present in the request.

Example: `https://www.theguardian.co.uk`

* TLD: `co.uk` (uWhoisd uses the `Mozilla public suffix list <https://publicsuffix.org/list/>`_ as a reference)
* Domain: `theguardian.co.uk`
* Subdomain: `www`

The whois request will be for `theguardian.co.uk`

**Information**

* `name:` intelmq.bots.experts.uwhoisd.expert
* `description:` uWhoisd is a universal Whois server

**Configuration Parameters**

* `server`: IP or hostname to connect to  (default: localhost)
* `port`: Port to connect to (default: 4243)


.. _intelmq.bots.experts.wait.expert:

Wait
^^^^

**Information**

* `name:` `intelmq.bots.experts.wait.expert`
* `lookup:` none
* `public:` yes
* `cache (redis db):` none
* `description:` Waits for a some time or until a queue size is lower than a given number.

**Configuration Parameters**

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

.. _output bots:

***********
Output Bots
***********


.. _intelmq.bots.outputs.amqptopic.output:

AMQP Topic
^^^^^^^^^^

Sends data to an AMQP Server
See https://www.rabbitmq.com/tutorials/amqp-concepts.html for more details on amqp topic exchange.

Requires the `pika python library <https://pypi.org/project/pika/>`_.

**Information**

* `name`: `intelmq.bots.outputs.amqptopic.output`
* `lookup`: to the amqp server
* `public`: yes
* `cache`: no
* `description`: Sends the event to a specified topic of an AMQP server

**Configuration parameters**

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

**Examples of usage**

* Useful to send events to a RabbitMQ exchange topic to be further processed in other platforms.

**Confirmation**

If routing key or exchange name are invalid or non existent, the message is
accepted by the server but we receive no confirmation.
If parameter require_confirmation is True and no confirmation is received, an
error is raised.

**Common errors**

*Unroutable messages / Undefined destination queue*

The destination exchange and queue need to exist beforehand,
with your preferred settings (e.g. durable, `lazy queue <https://www.rabbitmq.com/lazy-queues.html>`_.
If the error message says that the message is "unroutable", the queue doesn't exist.


.. _intelmq.bots.outputs.blackhole.output:

Blackhole
^^^^^^^^^

This output bot discards all incoming messages.

**Information**

* `name`: `intelmq.bots.outputs.blackhole.output`
* `lookup`: no
* `public`: yes
* `cache`: no
* `description`: discards messages


.. _intelmq.bots.outputs.bro_file.output:

Bro file
^^^^^^^^^

**Information**

* `name`: `intelmq.bots.outputs.bro_file.output`
* `lookup`: no
* `public`: yes
* `cache`: no
* `description`: BRO (zeek) file output

**Description**
File example:
```
#fields    indicator    indicator_type    meta.desc    meta.cif_confidence    meta.source
xxx.xxx.xxx.xxx    Intel::ADDR    phishing    100    MISP XXX
www.testdomain.com    Intel::DOMAIN    apt    85    CERT
```

.. _intelmq.bots.outputs.elasticsearch.output:

Elasticsearch Output Bot
^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name`: `intelmq.bots.outputs.elasticsearch.output`
* `lookup`: yes
* `public`: yes
* `cache`: no
* `description`: Output Bot that sends events to Elasticsearch

Only ElasticSearch version 7 supported.

It is also possible to feed data into ElasticSearch using ELK-Stack via Redis and Logstash, see :doc:`ELK-Stack` for more information. This methods supports various different versions of ElasticSearch.

**Configuration parameters**

* `elastic_host`: Name/IP for the Elasticsearch server, defaults to 127.0.0.1
* `elastic_port`: Port for the Elasticsearch server, defaults to 9200
* `elastic_index`: Index for the Elasticsearch output, defaults to intelmq
* `rotate_index`: If set, will index events using the date information associated with the event.

  Options: 'never', 'daily', 'weekly', 'monthly', 'yearly'. Using 'intelmq' as the elastic_index, the following are examples of the generated index names:

  .. code-block::

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

See `contrib/elasticsearch/elasticmapper` for a utility for creating Elasticsearch mappings and templates.

If using `rotate_index`, the resulting index name will be of the form [elastic_index]-[event date].
To query all intelmq indices at once, use an alias (https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html), or a multi-index query.

The data in ES can be retrieved with the HTTP-Interface:

.. code-block:: bash

   > curl -XGET 'http://localhost:9200/intelmq/events/_search?pretty=True'


.. _intelmq.bots.outputs.file.output:

File
^^^^

**Information**

* `name:` `intelmq.bots.outputs.file.output`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` output messages (reports or events) to file

Multihreading is disabled for this bot, as this would lead to corrupted files.

**Configuration Parameters**

* `encoding_errors_mode`: By default `'strict'`, see for more details and options: https://docs.python.org/3/library/functions.html#open For example with `'backslashreplace'` all characters which cannot be properly encoded will be written escaped with backslashes.
* `file`: file path of output file. Missing directories will be created if possible with the mode 755.
* `format_filename`: Boolean if the filename should be formatted (default: `false`).
* `hierarchical_output`: If true, the resulting dictionary will be hierarchical (field names split by dot).
* `single_key`: if `none`, the whole event is saved (default); otherwise the bot saves only contents of the specified key. In case of `raw` the data is base64 decoded.

**Filename formatting**

The filename can be formatted using pythons string formatting functions if `format_filename` is set. See https://docs.python.org/3/library/string.html#formatstrings

For example:
 * The filename `.../{event[source.abuse_contact]}.txt` will be (for example) `.../abuse@example.com.txt`.
 * `.../{event[time.source]:%Y-%m-%d}` results in the date of the event used as filename.

If the field used in the format string is not defined, `None` will be used as fallback.


.. _intelmq.bots.outputs.files.output:

Files
^^^^^

**Information**

* `name:` `intelmq.bots.outputs.files.output`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` saving of messages as separate files

**Configuration Parameters**

* `dir`: output directory (default `/opt/intelmq/var/lib/bots/files-output/incoming`)
* `tmp`: temporary directory (must reside on the same filesystem as `dir`) (default: `/opt/intelmq/var/lib/bots/files-output/tmp`)
* `suffix`: extension of created files (default `.json`)
* `hierarchical_output`: if `true`, use nested dictionaries; if `false`, use flat structure with dot separated keys (default)
* `single_key`: if `none`, the whole event is saved (default); otherwise the bot saves only contents of the specified key


.. _intelmq.bots.outputs.mcafee.output_esm_ip:

McAfee Enterprise Security Manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.outputs.mcafee.output_esm_ip`
* `lookup:` yes
* `public:` no
* `cache (redis db):` none
* `description:` Writes information out to McAfee ESM watchlist

**Configuration Parameters**

* **Feed parameters** (see above)
* `esm_ip`: IP address of ESM instance
* `esm_user`: username of user entitled to write to watchlist
* `esm_pw`: password of user
* `esm_watchlist`: name of the watchlist to write to
* `field`: name of the IntelMQ field to be written to ESM


.. _intelmq.bots.outputs.misp.output_feed:

MISP Feed
^^^^^^^^^

**Information**

* `name:` `intelmq.bots.outputs.misp.output_feed`
* `lookup:` no
* `public:` no
* `cache (redis db):` none
* `description:` Create a directory layout in the MISP Feed format

The PyMISP library >= 2.4.119.1 is required, see `REQUIREMENTS.txt <https://github.com/certtools/intelmq/blob/master/intelmq/bots/outputs/misp/REQUIREMENTS.txt>`_.

**Configuration Parameters**

* **Feed parameters** (see above)
* `misp_org_name`: Org name which creates the event, string
* `misp_org_uuid`: Org UUID which creates the event, string
* `output_dir`: Output directory path, e.g. `/opt/intelmq/var/lib/bots/mispfeed-output`. Will be created if it does not exist and possible.
* `interval_event`: The output bot creates one event per each interval, all data in this time frame is part of this event. Default "1 hour", string.

**Usage in MISP**

Configure the destination directory of this feed as feed in MISP, either as local location, or served via a web server. See `the MISP documentation on Feeds <https://www.circl.lu/doc/misp/managing-feeds>`_ for more information


.. _intelmq.bots.outputs.misp.output_api:

MISP API
^^^^^^^^

**Information**

* `name:` `intelmq.bots.outputs.misp.output_api`
* `lookup:` no
* `public:` no
* `cache (redis db):` none
* `description:` Connect to a MISP instance and add event as MISPObject if not there already.

The PyMISP library >= 2.4.120 is required, see
`REQUIREMENTS.txt <https://github.com/certtools/intelmq/blob/master/intelmq/bots/outputs/misp/REQUIREMENTS.txt>`_.

**Configuration Parameters**

* **Feed parameters** (see above)
* `add_feed_provider_as_tag`: boolean (use `true` when in doubt)
* `add_feed_name_as_tag`: boolean (use `true` when in doubt)
* `misp_additional_correlation_fields`: list of fields for which the correlation flags will be enabled (in addition to those which are in significant_fields)
* `misp_additional_tags`: list of tags to set not be searched for when looking for duplicates
* `misp_key`: string, API key for accessing MISP
* `misp_publish`: boolean, if a new MISP event should be set to "publish".

  Expert setting as MISP may really make it "public"!
  (Use `false` when in doubt.)
* `misp_tag_for_bot`: string, used to mark MISP events
* `misp_to_ids_fields`: list of fields for which the `to_ids` flags will be set
* `misp_url`: string, URL of the MISP server
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

(More details can be found in the docstring of `output_api.py <https://github.com/certtools/intelmq/blob/master/intelmq/bots/outputs/misp/output_api.py>`_.


.. _intelmq.bots.outputs.mongodb.output:

MongoDB
^^^^^^^

Saves events in a MongoDB either as hierarchical structure or flat with full key names. `time.observation` and `time.source` are saved as datetime objects, not as ISO formatted string.

**Information**

* `name:` `intelmq.bots.outputs.mongodb.output`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` MongoDB is the bot responsible to send events to a MongoDB database

**Configuration Parameters**

* `collection`: MongoDB collection
* `database`: MongoDB database
* `db_user` : Database user that should be used if you enabled authentication
* `db_pass` : Password associated to `db_user`
* `host`: MongoDB host (FQDN or IP)
* `port`: MongoDB port, default: 27017
* `hierarchical_output`: Boolean (default true) as MongoDB does not allow saving keys with dots, we split the dictionary in sub-dictionaries.
* `replacement_char`: String (default `'_'`) used as replacement character for the dots in key names if hierarchical output is not used.

**Installation Requirements**

.. code-block:: bash

   pip3 install pymongo>=2.7.1

The bot has been tested with pymongo versions 2.7.1, 3.4 and 3.10.1 (server versions 2.6.10 and 3.6.8).


.. _intelmq.bots.outputs.redis.output:

Redis
^^^^^

**Information**

* `name:` `intelmq.bots.outputs.redis.output`
* `lookup:` to the Redis server
* `public:` yes
* `cache (redis db):` none
* `description:` Output Bot that sends events to a remote Redis server/queue.

**Configuration Parameters**

* `redis_db`: remote server database, e.g.: 2
* `redis_password`: remote server password
* `redis_queue`: remote server list (queue), e.g.: "remote-server-queue"
* `redis_server_ip`: remote server IP address, e.g.: 127.0.0.1
* `redis_server_port`: remote server Port, e.g.: 6379
* `redis_timeout`: Connection timeout, in milliseconds, e.g.: 50000
* `hierarchical_output`: whether output should be sent in hierarchical JSON format (default: false)
* `with_type`: Send the `__type` field (default: true)

**Examples of usage**

* Can be used to send events to be processed in another system. E.g.: send events to Logstash.
* In a multi tenant installation can be used to send events to external/remote IntelMQ instance. Any expert bot queue can receive the events.
* In a complex configuration can be used to create logical sets in IntelMQ-Manager.


.. _intelmq.bots.outputs.rt.output:

Request Tracker
^^^^^^^^^^^^^^^

**Information**

* `name:` `intelmq.bots.outputs.rt.output`
* `lookup:` to the Request Tracker instance
* `public:` yes
* `cache (redis db):` none
* `description:` Output Bot that creates Request Tracker tickets from events.

**Description**

The bot creates tickets in Request Tracker and uses event fields for the ticket body text. The bot follows the workflow of the RTIR:

- create ticket in Incidents queue (or any other queue)

  - all event fields are included in the ticket body,
  - event attributes are assigned to tickets' CFs according to the attribute mapping,
  - ticket taxonomy can be assigned according to the CF mapping. If you use taxonomy different from `ENISA RSIT <https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force>`_, consider using some extra attribute field and do value mapping with modify or sieve bot,

- create linked ticket in Investigations queue, if these conditions are met

  - if first ticket destination was Incidents queue,
  - if there is source.abuse_contact is specified,
  - if description text is specified in the field appointed by configuration,

- RT/RTIR supposed to do relevant notifications by scrip working on condition "On Create",
- configuration option investigation_fields specifies which event fields has to be included in the investigation,
- Resolve Incident ticket, according to configuration (Investigation ticket status should depend on RT scrip configuration),

Take extra caution not to flood your ticketing system with enormous amount of tickets. Add extra filtering for that to pass only critical events to the RT, and/or deduplicating events.

**Configuration Parameters**

- `rt_uri`, `rt_user`, `rt_password`, `verify_cert`: RT API endpoint connection details, string.
- `queue`: ticket destination queue. If set to 'Incidents', 'Investigations' ticket will be created if create_investigation is set to true, string.
- `CF_mapping`: mapping attributes to ticket CFs, dictionary. E.g `{"event_description.text":"Description","source.ip":"IP","extra.classification.type":"Incident Type","classification.taxonomy":"Classification"}`
- `final_status`: the final status for the created ticket, string. E.g. `resolved` if you want to resolve the created ticket. The linked Investigation ticket will be resolved automatically by RTIR scripts.
- `create_investigation`: if an Investigation ticket should be created (in case of RTIR workflow). `true` or `false`, boolean.
- `investigation_fields`: attributes to include into investigation ticket, comma-separated string. E.g. `time.source,source.ip,source.port,source.fqdn,source.url,classification.taxonomy,classification.type,classification.identifier,event_description.url,event_description.text,malware.name,protocol.application,protocol.transport`.
- `description_attr`: which event attribute contains text message being sent to the recipient, string. If it is not specified or not found in the event, the Investigation ticket is not going to be created. Example: `extra.message.text`.


.. _intelmq.bots.outputs.restapi.output:

REST API
^^^^^^^^

**Information**

* `name:` `intelmq.bots.outputs.restapi.output`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` REST API is the bot responsible to send events to a REST API listener through POST

**Configuration Parameters**

* `auth_token`: the user name / HTTP header key
* `auth_token_name`: the password / HTTP header value
* `auth_type`: one of: `"http_basic_auth"`, `"http_header"`
* `hierarchical_output`: boolean
* `host`: destination URL
* `use_json`: boolean


.. _intelmq.bots.outputs.rpz_file.output:

RPZ
^^^^^^^^

The DNS RPZ functionality is "DNS firewall". Bot generate a blocklist.

**Information**

* `name:` `intelmq.bots.outputs.rpz_file.output`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Generate RPZ file

**Configuration Parameters**

* `cname`: example rpz.yourdomain.eu
* `organization_name`: Your organisation name
* `rpz_domain`: Information website about RPZ
* `hostmaster_rpz_domain`: Technical website
* `rpz_email`: Contact email
* `ttl`: Time to live
* `ncachttl`: DNS negative cache
* `serial`: Time stamp or another numbering
* `refresh`: Refresh time
* `retry`: Retry time
* `expire`: Expiration time
* `test_domain`: For test domain, it's added in first rpz file (after header)

File example:
```
$TTL 3600
@ SOA rpz.yourdomain.eu. hostmaster.rpz.yourdomain.eu. 2105260601 60 60 432000 60
NS localhost.
;
; yourdomain.eu. CERT.XX Response Policy Zones (RPZ)
; Last updated: 2021-05-26 06:01:41 (UTC)
;
; Terms Of Use: https://rpz.yourdomain.eu
; For questions please contact rpz [at] yourdomain.eu
;
*.maliciousdomain.com CNAME rpz.yourdomain.eu.
*.secondmaliciousdomain.com CNAME rpz.yourdomain.eu.
```

**Description**

The prime motivation for creating this feature was to protect users from badness on the Internet related to known-malicious global identifiers such as host names, domain names, IP addresses, or nameservers.
More information: https://dnsrpz.info


.. _intelmq.bots.outputs.smtp.output:

SMTP Output Bot
^^^^^^^^^^^^^^^

Sends a MIME Multipart message containing the text and the event as CSV for every single event.

**Information**

* `name:` `intelmq.bots.outputs.smtp.output`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Sends events via SMTP

**Configuration Parameters**

* `fieldnames`: a list of field names to be included in the email, comma separated string or list of strings. If empty, no attachment is sent - this can be useful if the actual data is already in the body (parameter ``text``) or the ``subject``.
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

For several strings you can use values from the string using the `standard Python string format syntax <https://docs.python.org/3/library/string.html#format-string-syntax>`_.
Access the event's values with `{ev[source.ip]}` and similar. Any not existing fields will result in `None`.
For example, to set the recipient(s) to the value given in the event's `source.abuse_contact` field, use this as `mail_to` parameter: `{ev[source.abuse_contact]}`

Authentication is optional. If both username and password are given, these
mechanism are tried: CRAM-MD5, PLAIN, and LOGIN.

Client certificates are not supported. If `http_verify_cert` is true, TLS certificates are checked.


.. _intelmq.bots.outputs.sql.output:

SQL
^^^

**Information**

* `name:` `intelmq.bots.outputs.sql.output`
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` SQL is the bot responsible to send events to a PostgreSQL or SQLite Database, e.g. the IntelMQ :doc:`eventdb`
* `notes`: When activating autocommit, transactions are not used: http://initd.org/psycopg/docs/connection.html#connection.autocommit

**Configuration Parameters**

The parameters marked with 'PostgreSQL' will be sent to libpq via psycopg2. Check the `libpq parameter documentation <https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS>`_ for the versions you are using.

* `autocommit`: `psycopg's autocommit mode <http://initd.org/psycopg/docs/connection.html?#connection.autocommit>`_, optional, default True
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

**PostgreSQL**

You have two basic choices to run PostgreSQL:

1. on the same machine as intelmq, then you could use Unix sockets if available on your platform
2. on a different machine. In which case you would need to use a TCP connection and make sure you give the right connection parameters to each psql or client call.

Make sure to consult your PostgreSQL documentation
about how to allow network connections and authentication in case 2.

**PostgreSQL Version**

Any supported version of PostgreSQL should work (v>=9.2 as of Oct 2016) `[1] <https://www.postgresql.org/support/versioning/>`_.

If you use PostgreSQL server v >= 9.4, it gives you the possibility
to use the time-zone `formatting string <https://www.postgresql.org/docs/9.4/static/functions-formatting.html>`_ "OF" for date-times
and the `GiST index for the CIDR type <https://www.postgresql.org/docs/9.4/static/release-9-4.html#AEN120769>`_. This may be useful depending on how
you plan to use the events that this bot writes into the database.

**How to install**

Use `intelmq_psql_initdb` to create initial SQL statements
from `harmonization.conf`. The script will create the required table layout
and save it as `/tmp/initdb.sql`

You need a PostgreSQL database-user to own the result database.
The recommendation is to use the name `intelmq`.
There may already be such a user for the PostgreSQL database-cluster
to be used by other bots. (For example from setting up
the expert/certbund_contact bot.)

Therefore if still necessary: create the database-user
as postgresql superuser, which usually is done via the system user `postgres`:

.. code-block:: bash

   createuser --no-superuser --no-createrole --no-createdb --encrypted --pwprompt intelmq

Create the new database:

.. code-block:: bash

   createdb --encoding='utf-8' --owner=intelmq intelmq-events

(The encoding parameter should ensure the right encoding on platform
where this is not the default.)

Now initialize it as database-user `intelmq` (in this example
a network connection to localhost is used, so you would get to test
if the user `intelmq` can authenticate):

.. code-block:: bash

   psql -h localhost intelmq-events intelmq </tmp/initdb.sql

**SQLite**

Similarly to PostgreSQL, you can use `intelmq_psql_initdb` to create initial SQL statements
from `harmonization.conf`. The script will create the required table layout
and save it as `/tmp/initdb.sql`.

Create the new database (you can ignore all errors since SQLite doesn't know all SQL features generated for PostgreSQL):

.. code-block:: bash

   sqlite3 your-db.db
   sqlite> .read /tmp/initdb.sql

Then, set the `database` parameter to the `your-db.db` file path.

.. _stomp output bot:

.. _intelmq.bots.outputs.stomp.output:

STOMP
^^^^^

**Information**

* `name`: intelmq.bots.outputs.stomp.output
* `lookup`: yes
* `public`: yes
* `cache (redis db)`: none
* `description`: This collector will push data to any STOMP stream. STOMP stands for Streaming Text Oriented Messaging Protocol. See: https://en.wikipedia.org/wiki/Streaming_Text_Oriented_Messaging_Protocol

**Requirements**
:

Install the stomp.py library, e.g. `apt install python3-stomp.py` or `pip install stomp.py`.

You need a CA certificate, client certificate and key file from the organization / server you are connecting to.
Also you will need a so called "exchange point".

**Configuration Parameters**

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


.. _intelmq.bots.outputs.tcp.output:

TCP
^^^

**Information**

* `name:` intelmq.bots.outputs.tcp.output
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` TCP is the bot responsible to send events to a TCP port (Splunk, another IntelMQ, etc..).

Multihreading is disabled for this bot.

**Configuration Parameters**

* `counterpart_is_intelmq`: Boolean. If you are sending to an IntelMQ TCP collector, set this to True, otherwise e.g. with filebeat, set it to false.
* `ip`: IP of destination server
* `hierarchical_output`: true for a nested JSON, false for a flat JSON (when sending to a TCP collector).
* `port`: port of destination server
* `separator`: separator of messages, e.g. "\n", optional. When sending to a TCP collector, parameter shouldn't be present.
  In that case, the output waits every message is acknowledged by "Ok" message the TCP collector bot implements.

**Sending to an IntelMQ TCP collector**

If you intend to link two IntelMQ instance via TCP, set the parameter `counterpart_is_intelmq` to true. The bot then awaits an "Ok" message to be received after each message is sent.
The TCP collector just sends "Ok" after every message it gets.


.. _intelmq.bots.outputs.templated_smtp.output:

Templated SMTP
^^^^^^^^^^^^^^

Sends a MIME Multipart message built from an event and static text using Jinja2 templates.

**Information**

* `name:` intelmq.bots.outputs.templated_smtp.output
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Sends events via SMTP

**Requirements**

Install the required `jinja2` library:

.. code-block:: bash

   pip3 install -r intelmq/bots/collectors/templated_smtp/REQUIREMENTS.txt

**Configuration Parameters**

Parameters:

* `attachments`: list of objects with structure::

   - content-type: string, templated, content-type to use.
     text: string, templated, attachment text.
     name: string, templated, filename of attachment.

* `body`: string, optional, templated, body text. The default body template prints every field in the event except 'raw', in undefined order, one field per line, as "field: value".

* `mail_from`: string, templated, sender address.

* `mail_to`: string, templated, recipient addresses, comma-separated.

* `smtp_host`: string, optional, default "localhost", hostname of SMTP server.

* `smtp_password`: string, default null, password (if any) for authenticated SMTP.

* `smtp_port`: integer, default 25, TCP port to connect to.

* `smtp_username`: string, default null, username (if any) for authenticated SMTP.

* `tls`: boolean, default false, whether to use use SMTPS. If true, also set smtp_port to the SMTPS port.

* `starttls`: boolean, default true, whether to use opportunistic STARTTLS over SMTP.

* `subject`: string, optional, default "IntelMQ event", templated, e-mail subject line.

* `verify_cert`: boolean, default true, whether to verify the server certificate in STARTTLS or SMTPS.

Authentication is attempted only if both username and password are specified.

Templates are in Jinja2 format with the event provided in the variable "event". E.g.::

   mail_to: "{{ event['source.abuse_contact'] }}"

See the Jinja2 documentation at https://jinja.palletsprojects.com/ .

Attachments are template strings, especially useful for sending
structured data. E.g. to send a JSON document including "malware.name"
and all other fields starting with "source."::

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

You are responsible for making sure that the text produced by the
template is valid according to the content-type.

If you are migrating from the SMTP output bot that produced CSV format
attachments, use the following configuration to produce a matching
format::

   attachments:
     - content-type: text/csv
       text: |
         {%- set fields = ["classification.taxonomy", "classification.type", "classification.identifier", "source.ip", "source.asn", "source.port"] %}
         {%- set sep = joiner(";") %}
         {%- for field in fields %}{{ sep() }}{{ field }}{%- endfor %}
         {% set sep = joiner(";") %}
         {%- for field in fields %}{{ sep() }}{{ event[field] }}{%- endfor %}
       name: event.csv


.. _intelmq.bots.outputs.touch.output:

Touch
^^^^^

**Information**

* `name:` intelmq.bots.outputs.touch.output
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Touches a file for every event received.

**Configuration Parameters**

* `path`: Path to the file to touch.


.. _intelmq.bots.outputs.udp.output:

UDP
^^^

**Information**

* `name:` intelmq.bots.outputs.udp.output
* `lookup:` no
* `public:` yes
* `cache (redis db):` none
* `description:` Output Bot that sends events to a remote UDP server.

Multihreading is disabled for this bot.

**Configuration Parameters**

* `field_delimiter`: If the format is 'delimited' this will be added between fields. String, default: `"|"`
* `format`: Can be `'json'` or `'delimited'`. The JSON format outputs the event 'as-is'. Delimited will deconstruct the event and print each field:value separated by the field delimit. See examples below.
* `header`: Header text to be sent in the UDP datagram, string.
* `keep_raw_field`: boolean, default: false
* `udp_host`: Destination's server's Host name or IP address
* `udp_port`: Destination port

**Examples of usage**

Consider the following event:

.. code-block:: json

   {"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware-distribution"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}

With the following Parameters:

* field_delimiter   : |
* format            : json
* Header            : header example
* keep_raw_field    : true
* ip                : 127.0.0.1
* port              : 514

Resulting line in syslog:

.. code-block::

   Apr 29 11:01:29 header example {"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware-distribution"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}

With the following Parameters:

* field_delimiter   : |
* format            : delimited
* Header            : IntelMQ-event
* keep_raw_field    : false
* ip                : 127.0.0.1
* port              : 514

Resulting line in syslog:

.. code-block::

   Apr 29 11:17:47 localhost IntelMQ-event|source.ip: 85.25.160.114|time.source:2016-04-25T11:39:00+00:00|feed.url:http://www.malwaredomainlist.com/updatescsv.php|time.observation:2016-04-29T11:17:44+00:00|source.reverse_dns:static-ip-85-25-160-114.inaddr.ip-pool.com|feed.name:Malware Domain List|event_description.text:Angler EK|source.url:http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/|source.asn:8972|classification.type:malware-distribution|feed.accuracy:100.0
