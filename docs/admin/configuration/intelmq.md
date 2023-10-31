<!-- comment
   SPDX-FileCopyrightText: 2015 Aaron Kaplan <aaron@lo-res.org>, 2015-2021 Sebastian Wagner, 2020-2021 Birger Schacht, 2023 Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Configuring IntelMQ

## Directories

### LSB

If you installed the packages, standard Linux paths (LSB paths) are used:

- `/etc/intelmq/` (configurations)
- `/var/log/intelmq/` (logs)
- `/var/lib/intelmq/` (local states)
- `/var/run/intelmq/` (PID files)
  
Otherwise, the configuration directory is `/opt/intelmq/etc/`. Using the environment variable `INTELMQ_ROOT_DIR` allows setting any arbitrary root directory.

You can switch this by setting the environment variables `INTELMQ_PATHS_NO_OPT` and `INTELMQ_PATHS_OPT`, respectively.

- When installing the Python packages, you can set `INTELMQ_PATHS_NO_OPT` to something non-empty to use LSB-paths.
- When installing the deb/rpm packages, you can set `INTELMQ_PATHS_OPT` to something non-empty to use `/opt/intelmq/` paths, or a path set with `INTELMQ_ROOT_DIR`.

The environment variable `ROOT_DIR` is meant to set an alternative root directory instead of `/`. This is primarily meant for package build environments an analogous to setuptool's `--root` parameter. Thus it is only used in LSB-mode.

## Environment Variables

| Name | Type | Description |
| ---- | ---- | ------------|
| `INTELMQ_PATHS_OPT` | |
| `INTELMQ_PATHS_NO_OPT` | |
| `INTELMQ_ROOT_DIR` | |
| `ROOT_DIR` | |

## Configuration Files

### `runtime.yaml`

This is the main configuration file. It uses YAML format since IntelMQ 3.0. It consists of two parts:

* Global Configuration
* Individual Bot Configuration 

!!! warning
    Comments in YAML are currently not preserved by IntelMQ (known bug [#2003](https://github.com/certtools/intelmq/issues/2003)).

Example `runtime.yaml` configuration file is installed by the tool `intelmqsetup`. If this is not the case, make sure the program was run. It is shipped preconfigured with 4 collectors and parsers, 6 common experts and one output bot. The default collector and the parser handle data from malware domain list, the file output bot writes all data to one of these files (based on your installation):

- `/opt/intelmq/var/lib/bots/file-output/events.txt`

- `/var/lib/intelmq/bots/file-output/events.txt`

The `runtime.yaml` configuration is divided into two sections:

- Global configuration which is applied to each bot.
- Individual bot configuration which overloads the global configuration and contains bot specific options.

Example configuration snippet:

```yaml
global: # global configuration section
  # ...
  http_timeout_max_tries: 3
  http_timeout_sec: 30
  http_user_agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36
  http_verify_cert: true

blocklistde-apache-collector: # individual bot configuration section
  group: Collector
  name: Blocklist.de Apache List
  module: intelmq.bots.collectors.http.collector_http
  description: Blocklist.de Apache Collector fetches all IP addresses which have been reported within the last 48 hours as having run attacks on the service Apache, Apache-DDOS, RFI-Attacks.
  parameters:
    http_url: https://lists.blocklist.de/lists/apache.txt
    name: Blocklist.de Apache
    rate_limit: 3600
    http_verify_cert: false # overriding the global configuration for this particular bot
```

#### Global Configuration

The global configuration parameters apply to all bots, however they can be overridden in the individual bot configuration.

##### Logging

The logging can be configured with the following parameters:

**`logging_handler`**

(required, string) Allowed values are `file` or `syslog`.

**`logging_level`**

(required, string) Allowed values are `CRITICAL`, `ERROR`, `WARNING`, `INFO` or `DEBUG`. Defines the system-wide log level that will be use by all bots and the intelmqctl tool. We recommend `logging_level` `WARNING` for production environments and
`INFO` if you want more details. In any case, watch your free disk space!

**`logging_path`**

(required, string) When the `logging_handler` is `file` this parameter is used to set the logging directory for all the bots as well as the `intelmqctl` tool. Defaults to `/opt/intelmq/var/log/` or `/var/log/intelmq/` respectively.

**`logging_syslog`**

(required, string) When the `logging_handler` is `syslog`. Either a list with hostname and UDP port of syslog service, e.g. `["localhost", 514]` or a device name/path. Defaults to `/var/log`.

##### Log Rotation

To rotate the logs, you can use the standard Linux-tool logrotate. An example logrotate configuration is given
in `contrib/logrotate/` and delivered with all deb/rpm-packages. When not using logrotate, IntelMQ can rotate the logs
itself, which is not enabled by default! You need to set both values.

**`logging_max_size`**

(optional, integer) Maximum number of bytes to be stored in one logfile before the file is rotated. Defaults to 0 (log rotation disabled).

**`logging_max_copies`**

(optional, integer) Maximum number of logfiles to keep. Compression is not supported. Default is unset.

Some information can as well be found in Python's documentation on the used
[RotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler).

##### Error Handling

**`error_log_message`**

(required, boolean) Whether to write the message (Event/Report) to the log file in case of an error.

**`error_log_exception`**

(required, boolean) Whether to write an error exception to the log file in case of an error.

**`error_procedure`**

(required, string) Allowed values are `stop` or `pass`. In case of an error, this option defines the procedure that the bot will adopt. Use the following values:

  - `stop` - stop bot after retrying X times (as defined in `error_max_retries`) with a delay between retries (as defined in `error_retry_delay`). If the bot reaches the `error_max_retries` value, it will remove the message from the pipeline and stop. If the option `error_dump_message` is also enable, the bot will dump the removed message to its dump file (to be found in var/log).

  - `pass` - will skip this message and will process the next message after retrying X times, removing the current message from pipeline. If the option `error_dump_message` is also enable, then the bot will dump the removed message to its dump file. After max retries are reached, the rate limit is applied (e.g. a collector bot fetch an unavailable resource does not try forever).

**`error_max_retries`**

(required, integer) In case of an error, the bot will try to re-start processing the current message X times as
  defined by this option.

**`error_retry_delay`**

(required, integer) Defines the number of seconds to wait between subsequent re-tries in case of an error.

**`error_dump_message`**

(required, boolean) Specifies if the bot will write queued up messages to its dump file (use intelmqdump to
  re-insert the message). 

If the path `_on_error` exists for a bot, the message is also sent to this queue, instead of (only) dumping the file if
configured to do so.

##### Miscellaneous

**`load_balance`**

(required, boolean) this option allows you to choose the behavior of the queue. Use the following values:

  - **true** - splits the messages into several queues without duplication
  - **false** - duplicates the messages into each queue - When using AMQP as message broker, take a look at the `multithreading`{.interpreted-text role="ref"} section and the `instances_threads` parameter.

**`rate_limit`**

(required, integer) time interval (in seconds) between messages processing. int value.

**`ssl_ca_certificate`**

(optional, string) trusted CA certificate for IMAP connections (supported by some bots).

**`source_pipeline_broker`**

(optional, string) Allowed values are `redis` and `amqp`. Selects the message broker IntelMQ should use. As this parameter can be overridden by each bot, this allows usage of different broker systems and hosts, as well as switching between them on the same IntelMQ instance. Defaults to `redis`.

  - **redis** - Please note that persistence has to be [manually activated](http://redis.io/topics/persistence). 
  - **amqp** - [Using the AMQP broker]() is currently beta but there are no known issues. A popular AMQP broker is [RabbitMQ](https://www.rabbitmq.com/).

**`destination_pipeline_broker`**

(required, string) See `source_pipeline_broker`.

**`source_pipeline_host`**

(required, string) Hostname or path to Unix socket that the bot will use to connect and receive messages.

**`source_pipeline_port`**

(optional, integer) Broker port that the bot will use to connect and receive messages. Can be empty for Unix socket.

**`source_pipeline_password`**

(optional, string) Broker password that the bot will use to connect and receive messages. Can be null for unprotected broker.

**`source_pipeline_db`**

(required, integer) broker database that the bot will use to connect and receive messages (requirement from
  redis broker).

**`destination_pipeline_host`**

(optional, string) broker IP, FQDN or Unix socket that the bot will use to connect and send messages.

**`destination_pipeline_port`**

(optional, integer) broker port that the bot will use to connect and send messages. Can be empty for
  Unix socket.

**`destination_pipeline_password`**

(optional, string) broker password that the bot will use to connect and send messages. Can be null
  for unprotected broker.

**`destination_pipeline_db`**

(required, integer) broker database that the bot will use to connect and send messages (requirement from
  redis broker).

**`http_proxy`**

(optional, string) Proxy to use for HTTP.

**`https_proxy`**

(optional, string) Proxy to use for HTTPS.

**`http_user_agent`**

(optional, string) User-Agent to be used for HTTP requests.

**`http_verify_cert`**

(optional, boolean) Verify the TLS certificate of the server. Defaults to true.

#### Individual Bot Configuration

!!! info
    For the individual bot configuration please see the [Bots](../../user/bots.md) document in the User Guide.

##### Run Mode

This sections provides more detailed explanation of the two run modes of the bots.

###### Continuous

Most of the cases, bots will need to be configured as `continuous` run mode (the default) in order to have them always
running and processing events. Usually, the types of bots that will require the continuous mode will be Parsers, Experts
and Outputs. To do this, set `run_mode` to
`continuous` in the `runtime.yaml` for the bot. Check the following example:

```yaml
blocklistde-apache-parser:
  name: Blocklist.de Parser
  group: Parser
  module: intelmq.bots.parsers.blocklistde.parser
  description: Blocklist.DE Parser is the bot responsible to parse the report and sanitize the information.
  enabled: false
  run_mode: continuous
  parameters: ...
```

You can now start the bot using the following command:

```bash
intelmqctl start blocklistde-apache-parser
```

Bots configured as `continuous` will never exit except if there is an error and the error handling configuration
requires the bot to exit. See the Error Handling section for more details.

###### Scheduled

In many cases, it is useful to schedule a bot at a specific time (i.e. via cron(1)), for example to collect information
from a website every day at midnight. To do this, set `run_mode` to `scheduled` in the
`runtime.yaml` for the bot. Check out the following example:

```yaml
blocklistde-apache-collector:
  name: Generic URL Fetcher
  group: Collector
  module: intelmq.bots.collectors.http.collector_http
  description: All IP addresses which have been reported within the last 48 hours as having run attacks on the service Apache, Apache-DDOS, RFI-Attacks.
  enabled: false
  run_mode: scheduled
  parameters:
    feed: Blocklist.de Apache
    provider: Blocklist.de
    http_url: https://lists.blocklist.de/lists/apache.txt
    ssl_client_certificate: null
```

You can schedule the bot with a crontab-entry like this:

```
0 0 * * * intelmqctl start blocklistde-apache-collector
```

Bots configured as `scheduled` will exit after the first successful run. Setting `enabled` to `false` will cause the bot
to not start with
`intelmqctl start`, but only with an explicit start, in this example
`intelmqctl start blocklistde-apache-collector`.

##### Additional Runtime Parameters

Some of the parameters are deliberately skipped from the User Guide because they are configured via graphical user interface provided by the IntelMQ Manager. These parameters have to do with configuring the pipeline: defining how the data is exchanged between the bots. Using the IntelMQ Manager for this have many benefits as it guarantees that the configuration is correct upon saving.

However as an administrator you should be also familiar with the manual (and somewhat tedious) configuration. For each bot there are two parameters that need to be set:

**`source_queue`**

(optional, string) The name of the source queue from which the bot is going to processing data. Each bot has maximum one source queue (collector bots don't have any source queue as they fetch data from elsewhere). Defaults to the bot id appended with the string `-queue`.

Example: a bot with id `example-bot` will have a default source queue named `example-bot-queue`.


**`destination_queues`**

(optional, object) Bots can have multiple destination queues. Destination queues can also be grouped into **named paths**. There are two special path names `_default` and `_on_error`.  The path `_default` is used if the path is not is specified by the bot itself (which is the most common case). In case of an error during the processing, the message will be sent to the `_on_error` path if specified (optional). 

Only few of the bots (mostly expert bots with filtering capabilities) can take advantage of arbitrarily named paths. Some expert bots are capable of sending messages to paths, this feature is explained in their documentation, e.g. the [Filter](../../user/bots.md#intelmq.bots.experts.filter.expert) expert and the [Sieve](../../user/bots.md#intelmq.bots.experts.sieve.expert) expert.

Example:

```yaml
blocklistde-apache-collector:
  # ...
  parameters:
    # ...
    destination_queues:
      _default:
        - <first destination pipeline name>
        - <second destination pipeline name>
      _on_error:
        - <optional first destination pipeline name in case of errors>
        - <optional second destination pipeline name in case of errors>
      other-path:
        - <second destination pipeline name>
        - <third destination pipeline name>
```

### `harmonization.conf`

This configuration is used to specify the fields for all message types. The harmonization library will load this configuration to check, during the message processing, if the values are compliant to the configured harmonization format.
Usually, this configuration doesn't need any change. It is mostly maintained by the IntelMQ maintainers.

**Template:**

```json
{
  "<message type>": {
    "<field 1>": {
      "description": "<field 1 description>",
      "type": "<field value type>"
    },
    "<field 2>": {
      "description": "<field 2 description>",
      "type": "<field value type>"
    }
  }
}
```

**Example:**

```json
{
  "event": {
    "destination.asn": {
      "description": "The autonomous system number from which originated the connection.",
      "type": "Integer"
    },
    "destination.geolocation.cc": {
      "description": "Country-Code according to ISO3166-1 alpha-2 for the destination IP.",
      "regex": "^[a-zA-Z0-9]{2}$",
      "type": "String"
    }
  }
}
```








