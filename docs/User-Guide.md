# User Guide

For installation instructions, see [INSTALL.md](INSTALL.md).
For upgrade instructions, see [UPGRADING.md](UPGRADING.md).

**Table of Contents:**
- [Where to get help?](#where-to-get-help)
- [Configure services](#configure-services)
- [Configuration](#configuration)
- [System Configuration (defaults)](#system-configuration-defaults)
    - [Error Handling](#error-handling)
    - [Miscellaneous](#miscellaneous)
- [Pipeline Configuration](#pipeline-configuration)
- [Runtime Configuration](#runtime-configuration)
- [Harmonization Configuration](#harmonization-configuration)
- [Utilities](#utilities)
- [Management](#management)
  - [Web interface: IntelMQ Manager](#web-interface-intelmq-manager)
  - [Command-line interface: intelmqctl](#command-line-interface-intelmqctl)
    - [Botnet Concept](#botnet-concept)
    - [Scheduled Run Mode](#scheduled-run-mode)
    - [Continuous Run Mode](#continuous-run-mode)
    - [Reloading](#reloading)
    - [Forcing reset pipeline and cache (be careful)](#forcing-reset-pipeline-and-cache-be-careful)
- [Error Handling](#error-handling)
  - [Tool: intelmqdump](#tool-intelmqdump)
- [Monitoring Logs](#monitoring-logs)
- [Uninstall](#uninstall)
- [Integration with ticket systems, etc.](#integration-with-ticket-systems-etc)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Additional Information](#additional-information)
- [Bash Completion](#bash-completion)
- [Performance Tests](#performance-tests)

# Where to get help?

In case you are lost or something is not discussed in this guide, you might want to subscribe to the [intelmq users mailinglist](https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-users) and ask your questions there.

With that clarified, let's dig into the details...


# Configure services
You need to enable and start Redis if not already done. Using systemd it can be done with:
```bash
systemctl enable redis.service
systemctl start redis.service
```

# Configuration

Note: If you installed the packages, LSB paths are used instead of `/opt/intelmq`.
Otherwise, the configuration directory is `/opt/intelmq/etc/`. All files are JSON. By
default, the installation method puts its distributed configuration files into
`etc/examples`, so it does not overwrite your local configuration. Prior to the
first run, copy them to `etc`:

```bash
cd /opt/intelmq/etc
cp -a examples/* .
```

* `defaults.conf`: default values for all bots and their behavior, e.g.
error handling, log options and pipeline configuration. Will be removed in the [future](https://github.com/certtools/intelmq/issues/267).
* `runtime.conf`: Configuration for the individual bots. See [Bots](Bots.md) for more details.
* `pipeline.conf`: Defines source and destination queues per bot (i.e. where does a bot get its data from, where does it send it to?).
* `BOTS`: Includes configuration hints for all bots. E.g. feed URLs or
database connection parameters. Use this as a template for `runtime.conf`. This is also read by the intelmq-manager.

To configure a new bot, you need to define and configure it in `runtime.conf` using the template from BOTS.
Configure source and destination queues in `pipeline.conf`.
Use the IntelMQ Manager mentioned above to generate the configuration files if unsure.

In the shipped examples 4 collectors and parsers, 6 common experts and one output are configured. The default collector and the parser handle data from malware domain list, the file output bot writes all data to `/opt/intelmq/var/lib/bots/file-output/events.txt`.

## System Configuration (defaults)

All bots inherit this configuration parameters and they can overwrite them using the same parameters in their respective configuration in the ''runtime.conf'' file.

Example:

* `logging_handler`: Can be one of `"file"` or `"syslog"`.
* `logging_level`: Defines the system-wide log level that will be use by all bots and the intelmqctl tool. Possible values are: `"CRITICAL"`, `"ERROR"`, `"WARNING"`, `"INFO"` and `"DEBUG"`.
* `logging_path`: If `logging_handler` is `file`. Defines the system-wide log-folder that will be use by all bots and the intelmqctl tool. Default value: `/opt/intelmq/var/log/`
* `logging_syslog`: If `logging_handler` is `syslog`. Either a list with hostname and UDP port of syslog service, e.g. `["localhost", 514]` or a device name/path, e.g. the default `"/var/log"`.

We recommend `logging_level` `WARNING` for production environments and `INFO` if you want more details. In any case, watch your free disk space.

You can set these parameters per bot as well. The settings will take effect after the runtime configuration has been (re-)read (which is after loading the defaults configuration. See the intelmqctl documentation).

#### Error Handling

* **`error_log_message`** - in case of an error, this option will allow the bot to write the message (report or event) to the log file. Use the following values:
    * **`true/false`** - write or not write message to the log file

* **`error_log_exception`** - in case of an error, this option will allow the bot to write the error exception to the log file. Use the following values:
    * **`true/false`** - write or not write exception to the log file

* **`error_procedure`** - in case of an error, this option defines the procedure that the bot will adopt. Use the following values:

    * **`stop`** - stop bot after retrying X times (as defined in `error_max_retries`)  with a delay between retries (as defined in `error_retry_delay`). If the bot reaches the `error_max_retries` value, it will remove the message from the pipeline and stop. If the option `error_dump_message` is also enable, the bot will dump the removed message to its dump file (to be found in var/log).
    
    * **`pass`** - will skip this message and will process the next message after retrying X times, removing the current message from pipeline. If the option `error_dump_message` is also enable, then the bot will dump the removed message to its dump file.

* **`error_max_retries`** - in case of an error, the bot will try to re-start processing the current message X times as defined by this option. int value.

* **`error_retry_delay`** - defines the number of seconds to wait between subsequent re-tries in case of an error. int value.

* **`error_dump_message`** - specifies if the bot will write queued up messages to its dump file (use intelmqdump to re-insert the message).
    * **`true/false`** - write or not write message to the dump file

#### Miscellaneous

* **`load_balance`** - this option allows you to choose the behavior of the queue. Use the following values:
    * **`true`** - splits the messages into several queues without duplication
    * **`false`** - duplicates the messages into each queue

* **`broker`** - select which broker intelmq can use. Use the following values:
    * **`redis`** - Redis allows some persistence but is not so fast as ZeroMQ (in development). But note that persistence has to be manually activated. See http://redis.io/topics/persistence

* **`rate_limit`** - time interval (in seconds) between messages processing.  int value.

* **`source_pipeline_host`** - broker IP, FQDN or Unix socket that the bot will use to connect and receive messages.

* **`source_pipeline_port`** - broker port that the bot will use to connect and receive messages. Can be empty for Unix socket.

* **`source_pipeline_password`** - broker password that the bot will use to connect and receive messages. Can be null for unprotected broker.

* **`source_pipeline_db`** - broker database that the bot will use to connect and receive messages (requirement from redis broker).

* **`destination_pipeline_host`** - broker IP, FQDN or Unix socket that the bot will use to connect and send messages. 

* **`destination_pipeline_port`** - broker port that the bot will use to connect and send messages. Can be empty for Unix socket.

* **`destination_pipeline_password`** - broker password that the bot will use to connect and send messages. Can be null for unprotected broker.

* **`destination_pipeline_db`** - broker database that the bot will use to connect and send messages (requirement from redis broker).

* **`http_proxy`** - HTTP proxy the that bot will use when performing HTTP requests (e.g. bots/collectors/collector_http.py). The value must follow [RFC1738](https://www.ietf.org/rfc/rfc1738.txt).

* **`https_proxy`** -  HTTPS proxy that the bot will use when performing secure HTTPS requests (e.g. bots/collectors/collector_http.py).

* **`http_user_agent`** - user-agent string that the bot will use when performing HTTP/HTTPS requests (e.g. bots/collectors/collector_http.py).

* **`http_verify_cert`** - defines if the bot will verify SSL certificates when performing HTTPS requests (e.g. bots/collectors/collector_http.py).
    * **`true/false`** - verify or not verify SSL certificates

## Pipeline Configuration

This configuration is used by each bot to load the source pipeline and destination pipelines associated to each of them. IntelMQ Manager generates this configuration.

**Template:**
```
{
	...
    "<bot ID>": {
        "source-queue": "<source pipeline name>",
        "destination-queues": [
            "<first destination pipeline name>",
            "<second destination pipeline name>",
            ...
        ]
    },
	...
}
```

Note that `destination-queues` contains one of the following values:
* None
* string
* list of strings (as in the template above)
* dict of either strings or lists for complex expert bots:

```
"destination-queues": {
    "_default": "<first destination pipeline name>",
    "_on_error": "<optional destination pipeline name in case of errors>",
    "other-path": [
        "<second destination pipeline name>",
        "<third destination pipeline name>",
        ...
        ],
    ...
    }

```
In that case, bot will be able to send the message to one of defined paths. The path `"_default"` is used if none is not specified.
In case of errors during processing, and the optional path `"_on_error"` is specified, the message will be sent to the pipelines given given as on-error.
Other destination queues can be explicitly addressed by the bots, e.g. bots with filtering capabilities.

**Example:**
```
{
	...
    "malware-domain-list-parser": {
        "source-queue": "malware-domain-list-parser-queue",
        "destination-queues": [
            "file-output-queue"
        ]
    },
	...
}
```
Note that a bot must only have one (input) source queue but may have multiple destination queues.

More examples can be found at `intelmq/etc/pipeline.conf` directory in IntelMQ repository.

## Runtime Configuration

This configuration is used by each bot to load its specific (runtime) parameters. Usually, the `BOTS` file is used to generate `runtime.conf`. Also, the IntelMQ Manager generates this configuration. You may edit it manually as well. Be sure to re-load the bot (see the intelmqctl documentation).

**Template:**
```
{
    "<bot ID>": {
        "group": "<bot type (Collector, Parser, Expert, Output)>",
        "name": "<human-readable bot name>",
        "module": "<bot code (python module)>",
        "description": "<generic description of the bot>",
        "parameters": {
            "<parameter 1>": "<value 1>",
            "<parameter 2>": "<value 2>",
            "<parameter 3>": "<value 3>"
        }
    }
}
```

**Example:**
```
{
    "malware-domain-list-collector": {
        "group": "Collector",
        "name": "Malware Domain List",
        "module": "intelmq.bots.collectors.http.collector_http",
        "description": "Malware Domain List Collector is the bot responsible to get the report from source of information.",
        "parameters": {
            "http_url": "http://www.malwaredomainlist.com/updatescsv.php",
            "feed": "Malware Domain List",
            "rate_limit": 3600
        }
    }
}
```

More examples can be found in the `intelmq/etc/runtime.conf` directory. See [Bots](Bots.md) for more details.

By default, all of the bots are started when you start the whole botnet, however there is a possibility to *disable* a bot. This means that the bot will not start every time you start the botnet, but you can start and stop the bot if you specify the bot explicitly. To disable a bot, add the following to your runtime.conf: `"enabled": false`. For example: 

```
{
    "malware-domain-list-collector": {
        "group": "Collector",
        "name": "Malware Domain List",
        "module": "intelmq.bots.collectors.http.collector_http",
        "description": "Malware Domain List Collector is the bot responsible to get the report from source of information.",
        "enabled": false,
        "parameters": {
            "http_url": "http://www.malwaredomainlist.com/updatescsv.php",
            "feed": "Malware Domain List",
            "rate_limit": 3600
        }
    }
}
```

## Harmonization Configuration

This configuration is used to specify the fields for all message types. The harmonization library will load this configuration to check, during the message processing, if the values are compliant to the "harmonization" format. Usually, this configuration doesn't need any change. It is mostly maintained by the intelmq maintainers.

**Template:**
```
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
    },
}
```

**Example:**
```
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
        },
    },
}
```

More examples can be found in the `intelmq/etc/harmonization.conf` directory.



# Utilities

## Management

IntelMQ has a modular structure consisting of bots. There are four types of bots:

* [CollectorBots](Bots.md#collectors) retrieve data from internal or external sources, the output
are *reports* consisting of many individual data sets / log lines.
* [ParserBots](Bots.md#parsers) parse the (report) data by splitting it into individual *events* (log lines) and
giving them a defined structure, see also [Data Harmonization](Data-Harmonization.md) for the list of fields an event may be split up into.
* [ExpertBots](Bots.md#experts) enrich the existing events by e.g. lookup up information such as DNS reverse records, geographic location information (country code) or abuse contacts for an IP address or domain name.
* [OutputBots](Bots.md#outputs) write events to files, databases, (REST)-APIs or any other data sink that you might want to write to.

Each bot has one source queue (except collectors) and can have multiple
destination queues (except outputs). But multiple bots can write to the same pipeline (queue), resulting in multiple inputs for the next bot.

Every bot runs in a separate process. A bot is identifiable by a *bot id*.

Currently only one instance (i.e. *with the same bot id*) of a bot can run at the same time. Concepts for multiprocessing are being discussed, see this issue: [Multiprocessing per queue is not supported #186](https://github.com/certtools/intelmq/issues/186).
Currently you can run multiple processes of the same bot (with *different bot ids*) in parallel.

Example: multiple gethostbyname bots (with different bot ids) may run in parallel, with the same input queue and sending to the same output queue. Note that the bot providing the input queue **must** have the ``load_balance`` option set to ``true``.

### Web interface: IntelMQ Manager

IntelMQ has a tool called IntelMQ Manager that gives users an easy way to configure all pipelines with bots that your team needs. For beginners, it's recommended to use the IntelMQ Manager to become acquainted with the functionalities and concepts. The IntelMQ Manager offers some of the possibilities of the intelmqctl tool and has a graphical interface for runtime and pipeline configurations.

See the [IntelMQ Manager repository](https://github.com/certtools/intelmq-manager).

### Command-line interface: intelmqctl

**Syntax:**

```bash
# su - intelmq
$ intelmqctl -h
usage: intelmqctl [-h] [-v] [--type {text,json}] [--quiet]
                  {list,check,clear,log,run,help,start,stop,restart,reload,status,enable,disable}
                  ...

        description: intelmqctl is the tool to control intelmq system.

        Outputs are logged to /opt/intelmq/var/log/intelmqctl

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --type {text,json}, -t {text,json}
                        choose if it should return regular text or other
                        machine-readable
  --quiet, -q           Quiet mode, useful for reloads initiated scripts like
                        logrotate

subcommands:
  {list,check,clear,log,run,help,start,stop,restart,reload,status,enable,disable}
    list                Listing bots or queues
    check               Check installation and configuration
    clear               Clear a queue
    log                 Get last log lines of a bot
    run                 Run a bot interactively
    check               Check installation and configuration
    help                Show the help
    start               Start a bot or botnet
    stop                Stop a bot or botnet
    restart             Restart a bot or botnet
    reload              Reload a bot or botnet
    status              Status of a bot or botnet
    enable              Enable a bot
    disable             Disable a bot

        intelmqctl [start|stop|restart|status|reload] --group [collectors|parsers|experts|outputs]
        intelmqctl [start|stop|restart|status|reload] bot-id
        intelmqctl [start|stop|restart|status|reload]
        intelmqctl list [bots|queues|queues-and-status]
        intelmqctl log bot-id [number-of-lines [log-level]]
        intelmqctl run bot-id message [get|pop|send]
        intelmqctl run bot-id process [--msg|--dryrun]
        intelmqctl run bot-id console
        intelmqctl clear queue-id
        intelmqctl check

Starting a bot:
    intelmqctl start bot-id
Stopping a bot:
    intelmqctl stop bot-id
Reloading a bot:
    intelmqctl reload bot-id
Restarting a bot:
    intelmqctl restart bot-id
Get status of a bot:
    intelmqctl status bot-id

Run a bot directly for debugging purpose and temporarily leverage the logging level to DEBUG:
    intelmqctl run bot-id
Get a pdb (or ipdb if installed) live console.
    intelmqctl run bot-id console
See the message that waits in the input queue.
    intelmqctl run bot-id message get
See additional help for further explanation.
    intelmqctl run bot-id --help

Starting the botnet (all bots):
    intelmqctl start
    etc.

Starting a group of bots:
    intelmqctl start --group experts
    etc.

Get a list of all configured bots:
    intelmqctl list bots

Get a list of all queues:
    intelmqctl list queues
If -q is given, only queues with more than one item are listed.

Get a list of all queues and status of the bots:
    intelmqctl list queues-and-status

Clear a queue:
    intelmqctl clear queue-id

Get logs of a bot:
    intelmqctl log bot-id number-of-lines log-level
Reads the last lines from bot log.
Log level should be one of DEBUG, INFO, ERROR or CRITICAL.
Default is INFO. Number of lines defaults to 10, -1 gives all. Result
can be longer due to our logging format!

Outputs are additionally logged to /opt/intelmq/var/log/intelmqctl
```

#### Botnet Concept

The "botnet" represents all currently configured bots which are explicitly enabled. It is, in essence, the graph (pipeline.conf) of the bots which are connected together via their input source queues and destination queues. 

To get an overview which bots are running, use `intelmqctl status` or use the IntelMQ Manager. Set `"enabled": true` in the runtime configuration to add a bot to the botnet. By default, bots will be configured as `"enabled": true`. See [Bots](Bots.md) for more details on configuration.

Disabled bots can still be started explicitly using `intelmqctl start <bot_id>`, but will remain in the state `disabled` if stopped (and not be implicitly enabled by the `start` command). They are not started by `intelmqctl start` in analogy to the behavior of widely used initialization systems.


#### Scheduled Run Mode

In many cases, it is useful to schedule a bot at a specific time (i.e. via cron(1)), for example to collect information from a website every day at midnight. To do this, set `run_mode` to `scheduled` in the `runtime.conf` for the bot. Check out the following example:

```json
"blocklistde-apache-collector": {
    "name": "Generic URL Fetcher",
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "description": "All IP addresses which have been reported within the last 48 hours as having run attacks on the service Apache, Apache-DDOS, RFI-Attacks.",
    "enabled": false,
    "run_mode": "scheduled",
    "parameters": {
        "feed": "Blocklist.de Apache",
        "provider": "Blocklist.de",
        "http_url": "https://lists.blocklist.de/lists/apache.txt",
        "ssl_client_certificate": null
    },
},
```

You can schedule the bot with a crontab-entry like this:
```
0 0 * * * intelmqctl start blocklistde-apache-collector
```

Bots configured as `scheduled` will exit after the first successful run.


#### Continuous Run Mode

Most of the cases, bots will need to be configured as `continuous` run mode (the default) in order to have them always running and processing events. Usually, the types of bots that will require the continuous mode will be Parsers, Experts and Outputs. To do this, set `run_mode` to `continuous` in the `runtime.conf` for the bot. Check the following example:

```json
"blocklistde-apache-parser": {
    "name": "Blocklist.de Parser",
    "group": "Parser",
    "module": "intelmq.bots.parsers.blocklistde.parser",
    "description": "Blocklist.DE Parser is the bot responsible to parse the report and sanitize the information.",
    "enabled": false,
    "run_mode": "continuous",
    "parameters": {
    },
},
```

You can now start the bot using the following command:
```
intelmqctl start blocklistde-apache-parser
```

Bots configured as `continuous` will never exit except if there is an error and the error handling configuration requires the bot to exit. See the Error Handling section for more details.


#### Reloading

Whilst restart is a mere stop & start, performing `intelmqctl reload <bot_id>` will not stop the bot, permitting it to keep the state: the same common behavior as for (Linux) daemons. It will initialize again (including reading all configuration again) after the current action is finished. Also, the rate limit/sleep is continued (with the *new* time) and not interrupted like with the restart command. So if you have a collector with a rate limit of 24 h, the reload does not trigger a new fetching of the source at the time of the reload, but just 24 h after the last run – with the new configuration. 
Which state the bots are keeping depends on the bots of course.

#### Forcing reset pipeline and cache (be careful)

If you are using the default broker (Redis), in some test situations you may need to quickly clear all pipelines and caches. Use the following procedure:
```bash
redis-cli FLUSHDB
redis-cli FLUSHALL
```

## Error Handling

### Tool: intelmqdump

When bots are failing due to bad input data or programming errors, they can dump the problematic message to a file along with a traceback, if configured accordingly. These dumps are saved at `/opt/intelmq/var/log/[botid].dump` as JSON files. IntelMQ comes with an inspection and reinjection tool, called `intelmqdump`. It is an interactive tool to show all dumped files and the number of dumps per file. Choose a file by bot-id or listed numeric id. You can then choose to delete single entries from the file with `e 1,3,4`, show a message in more readable format with `s 1` (prints the raw-message, can be long!), recover some messages and put them back in the pipeline for the bot by `a` or `r 0,4,5`. Or delete the file with all dumped messages using `d`.

```bash
 $ intelmqdump -h
usage:
    intelmqdump [botid]
    intelmqdump [-h|--help]

intelmqdump can inspect dumped messages, show, delete or reinject them into
the pipeline. It's an interactive tool, directly start it to get a list of
available dumps or call it with a known bot id as parameter.

positional arguments:
  botid       botid to inspect dumps of

optional arguments:
  -h, --help  show this help message and exit

Interactive actions after a file has been selected:
- r, Recover by IDs
  > r id{,id} [queue name]
  > r 3,4,6
  > r 3,7,90 modify-expert-queue
  The messages identified by a consecutive numbering will be stored in the
  original queue or the given one and removed from the file.
- a, Recover all
  > a [queue name]
  > a
  > a modify-expert-queue
  All messages in the opened file will be recovered to the stored or given
  queue and removed from the file.
- e, Delete entries by IDs
  > e id{,id}
  > e 3,5
  The entries will be deleted from the dump file.
- d, Delete file
  > d
  Delete the opened file as a whole.
- s, Show by IDs
  > s id{,id}
  > s 0,4,5
  Show the selected IP in a readable format. It's still a raw format from
  repr, but with newlines for message and traceback.
- q, Quit
  > q

$ intelmqdump
 id: name (bot id)                    content
  0: alienvault-otx-parser            1 dumps
  1: cymru-whois-expert               8 dumps
  2: deduplicator-expert              2 dumps
  3: dragon-research-group-ssh-parser 2 dumps
  4: file-output2                     1 dumps
  5: fraunhofer-dga-parser            1 dumps
  6: spamhaus-cert-parser             4 dumps
  7: test-bot                         2 dumps
Which dump file to process (id or name)? 3
Processing dragon-research-group-ssh-parser: 2 dumps
  0: 2015-09-03T13:13:22.159014 InvalidValue: invalid value u'NA' (<type 'unicode'>) for key u'source.asn'
  1: 2015-09-01T14:40:20.973743 InvalidValue: invalid value u'NA' (<type 'unicode'>) for key u'source.asn'
recover (a)ll, delete (e)ntries, (d)elete file, (q)uit, (s)how by ids, (r)ecover by ids? d
Deleted file /opt/intelmq/var/log/dragon-research-group-ssh-parser.dump
```

## Monitoring Logs

All bots and `intelmqctl` log to `/opt/intelmq/var/log/`. In case of failures, messages are dumped to the same directory with the file ending `.dump`.

```bash
tail -f /opt/intelmq/var/log/*.log
```

# Uninstall

```bash
pip uninstall intelmq
rm -rf /opt/intelmq
```

# Integration with ticket systems, etc.
First of all, IntelMQ is a message (event) processing system: it collects feeds, processes them, enriches them, filters them and then stores them somewhere or sends them to another system. It does this in a composable, data flow oriented fashion, based on single events. There are no aggregation or grouping features. Now, if you want to integrate IntelMQ with your ticket system or some other system, you need to send its output to somewhere where your ticket system or other services can pick up IntelMQ's data. This could be a database, splunk, or you could send your events directly via email to a ticket system.

Different users came up with different solutions for this, each of them fitting their own organisation. Hence these solutions are not part of the core IntelMQ repository. 
  * CERT.at uses a postgresql DB (postgres output bot) and has a small tool `intelmqcli` which fetches the events in the postgresql DB which are marked as "new" and will group them and send them out via the RT ticket system.
  * Others, including BSI, use a tool called `intelmq-mailgen`. It sends E-Mails to the recipients, optionally PGP-signed with defined text-templates, CSV formatted attachments with grouped events and generated ticket numbers.

The following lists external github repositories which you might consult for examples on how to integrate IntelMQ into your workflow:

  * [certat repository](https://github.com/certat/intelmq)
  * [Intevation's Mailgen](https://github.com/Intevation/intelmq-mailgen)
  
If you came up with another solution for integration, we'd like to hear from you! Please reach out to us on the [intelmq-users list](https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-users).

# Frequently Asked Questions

Consult the [FAQ](FAQ.md) if you encountered any problems.


# Additional Information

## Bash Completion

To enable bash completion on `intelmqctl` and `intelmqdump` in order to help you run the commands in an easy manner, follow the installation process [here](../contrib/bash-completion/README.md).

## Performance Tests

Some tests have been made with a virtual machine with 
the following specifications:

* CPU: 1 core dedicated from i7 processor
* Memory: 4GB
* HDD: 10GB

The entire solution didn't have any problem handling 2.000.000 
queued events in memory with bots digesting the messages.
