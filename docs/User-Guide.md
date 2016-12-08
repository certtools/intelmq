# User Guide

  * [Requirements](#requirements)
  * [Install](#install)
    * [Install Dependencies](#install-dependencies)
        * [Ubuntu 14.04 / Debian 8](#ubuntu-1404--debian-8)
        * [CentOS 7](#centos-7)
    * [Install](#install-1)
      * [Python 3.4 (recommended)](#python-34-recommended-1)
  * [Configuration](#configuration)
    * [System Configuration](#system-configuration)
    * [Pipeline Configuration](#pipeline-configuration)
    * [Defaults Configuration](#defaults-configuration)
        * [Error Handling](#error-handling)
        * [Miscellaneous](#miscellaneous)
    * [Runtime Configuration](#runtime-configuration)
    * [Harmonization Configuration](#harmonization-configuration)
  * [Utilities](#utilities)
    * [Management](#management)
      * [Web interface: IntelMQ Manager](#web-interface-intelmq-manager)
      * [Command-line interface: intelmqctl](#command-line-interface-intelmqctl)
        * [Botnet Concept](#botnet-concept)
        * [Forcing reset pipeline and cache (be careful)](#forcing-reset-pipeline-and-cache-be-careful)
    * [Error Handling](#error-handling-1)
      * [Tool: intelmqdump](#tool-intelmqdump)
    * [Monitoring Logs](#monitoring-logs)
  * [Upgrade](#upgrade)
    * [Stop IntelMQ and Backup](#stop-intelmq-and-backup)
    * [Upgrade](#upgrade-1)
    * [Restore Configurations](#restore-configurations)
  * [Uninstall](#uninstall)
  * [Frequently Asked Questions](#frequently-asked-questions)
  * [Additional Information](#additional-information)
    * [Performance Tests](#performance-tests)


# Requirements

The following instructions assume the following requirements:

* **Operating System:** Ubuntu 14.04 LTS or Debian 8 or CentOS 7

Please report any errors you encounter at https://github.com/certtools/intelmq/issues

# Install

## Install Dependencies

#### Ubuntu 14.04 / Debian 8

```bash
apt-get install python3 python3-pip
apt-get install git build-essential libcurl4-gnutls-dev libffi-dev
apt-get install python3-dev
apt-get install redis-server
```
**Special note for Debian 8**: 
if you are using Debian 8, you need to install this package extra: ``apt-get install libgnutls28-dev``.
In addition, Debian 8 has an old version of pip3. Please get a current one via:
```bash
curl "https://bootstrap.pypa.io/get-pip.py" -o "/tmp/get-pip.py"
python3.4 /tmp/get-pip.py
```

##### CentOS 7

```bash
yum install epel-release
yum install python34 python34-devel
yum install git libcurl-devel gcc gcc-c++
yum install redis
```

Install the last pip version:
```bash
curl "https://bootstrap.pypa.io/get-pip.py" -o "/tmp/get-pip.py"
python3.4 /tmp/get-pip.py
```

Enable redis on startup:
```bash
systemctl enable redis
systemctl start redis
```

## Install

The `REQUIREMENTS` files define a list python packages and versions, which are necessary to run *all components* of IntelMQ. The defined versions are recommendations.

If you do not do any modifications on the code, use `pip install intelmq` instead of `pip install .`!

```bash
git clone https://github.com/certtools/intelmq.git /tmp/intelmq
cd /tmp/intelmq

sudo -s

pip3 install -r REQUIREMENTS
pip3 install .

useradd -d /opt/intelmq -U -s /bin/bash intelmq
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

# Configuration

By default, one collector, one parser and one output are started. The default collector and the parser handle data from malware domain list, the file output bot writes all data to `/opt/intelmq/var/lib/bots/file-output/events.txt`.

The configuration directory is `/opt/intelmq/etc/`, all files are JSON. By
default, the installation method puts it's distributed configuration files into
`etc/examples`, so it does not overwrite your local configuration. Prior to the
first run, copy them to `etc`:

```bash
cd /opt/intelmq/etc
cp -a examples/* .
```

* `defaults.conf`: default values for bots and their behavior, e.g.
error handling, log options and pipeline configuration. Will be removed in the [future](https://github.com/certtools/intelmq/issues/267).
* `runtime.conf`: Configuration for the individual bots.
* `pipeline.conf`: Defines source and destination queues per bot.
* `BOTS`: Includes configuration hints for all bots. E.g. feed URLs or
database connection parameters. Use this as a template for `runtime.conf`. Also read by the intelmq-manager.

To configure a new bot, you need to define and configure it in `runtime.conf`
using the template from BOTS.
Configure source and destination queues in `pipeline.conf`.
Use the IntelMQ Manager mentioned above to generate the configuration files if unsure.


## System Configuration (defaults)

All bots inherit this configuration parameters and they can overwrite them using the same parameters in configuration.

Small extract:

* `logging_handler`: Can be one of `"file"` or `"syslog"`.
* `logging_level`: Defines for all system the level of logging that will be use by all bots and intelmqctl tool. Possible values are: `"CRITICAL"`, `"ERROR"`, `"WARNING"`, `"INFO"` and `"DEBUG"`.
* `logging_path`: If `logging_handler` is `file`. Defines for all system the logs folder that will be use by all bots and intelmqctl tool. Default value is: `/opt/intelmq/var/log/`
* `logging_syslog`: If `logging_handler` is `syslog`. Either a list with hostname and UDP port of syslog service, e.g. `["localhost", 514]` or a device name, e.g. the default `"/var/log"`.

We recommend logging_level WARNING for production environments and INFO if you want more details. In any case, monitor your free disk space.

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

More examples can be found at `intelmq/etc/pipeline.conf` directory in IntelMQ repository.

#### Error Handling

* **`error_log_message`** - in case of an error, this option will allow the bot to write the message (report or event) in the log file. Use the following values:
    * **`true/false`** - write or not write message in log file

* **`error_log_exception`** - in case of an error, this option will allow the bot to write the error exception in the log file. Use the following values:
    * **`true/false`** - write or not write exception in log file

* **`error_procedure`** - in case of an error, this option defines the procedure that the bot will adopt. Use the following values:

    * **`stop`** - stop bot after retry X times, defined in `error_max_retries` option with a delay between retries defined at `error_retry_delay` option. If bot reach `error_max_retries` value, it will remove the message from pipeline and stop. If the option `error_dump_message` is enable, the bot will dump the removed message to the dump log.
    
    * **`pass`** - will pass to the next message after retry X times, removing from pipeline the current message. If the option `error_dump_message` is enable, the bot will dump the removed message to the dump log.

* **`error_max_retries`** - in case of an error and the value of the `error_procedure` option is `retry`, bot will try to start processing the current message X times defined at `error_max_retries` option. The value must be an `integer value`.

* **`error_retry_delay`** - in case of an error, this option will allows you to define the number of seconds which bot will wait until next retry. The value must be an `integer value`.

* **`error_dump_message`** - in case of an error, this option will allows the bot to write the message (report or event) in the dump file (use intelmqdump to re-insert the message).
    * **`true/false`** - write or not write message in dump file

#### Miscellaneous

* **`load_balance`** - this option allows you to choose the behavior of the queue. Use the following values:
    * **`true`** - splits the messages into several queues wihtout duplication
    * **`false`** - duplicates the messages into each queue

* **`broker`** - select which broker intelmq can use. Use the following values:
    * **`redis`** - Redis allows some persistence but is not so fast as ZeroMQ (in development). But note that persistence has to be manually activated. See http://redis.io/topics/persistence

* **`rate_limit`** - time interval (in seconds) between messages processing. The value must be an `integer value`.

* **`source_pipeline_host`** - broker IP, FQDN or Unix socket that the bot will use to connect and receive messages.

* **`source_pipeline_port`** - broker port that the bot will use to connect and receive messages. Can be empty for Unix socket.

* **`source_pipeline_password`** - broker password that the bot will use to connect and receive messages. Can be null for unprotected broker.

* **`source_pipeline_db`** - broker database that the bot will use to connect and receive messages (requirement from redis broker).

* **`destination_pipeline_host`** - broker IP, FQDN or Unix socket that the bot will use to connect and send messages. 

* **`destination_pipeline_port`** - broker port that the bot will use to connect and send messages. Can be empty for Unix socket.

* **`destination_pipeline_password`** - broker password that the bot will use to connect and send messages. Can be null for unprotected broker.

* **`destination_pipeline_db`** - broker database that the bot will use to connect and send messages (requirement from redis broker).

* **`http_proxy`** - proxy HTTP the that bot will use when performing HTTP requests (e.g. bots/collectors/collector_http.py). The value must follow RFC1738.

* **`https_proxy`** - proxy HTTPS that the bot will use when performing secure HTTPS requests (e.g. bots/collectors/collector_http.py).

* **`http_user_agent`** - user-agent that the bot will use when performing HTTP/HTTPS requests (e.g. bots/collectors/collector_http.py).

* **`http_verify_cert`** - defines if the bot will verify SSL certificates when performing HTTPS requests (e.g. bots/collectors/collector_http.py).
    * **`true/false`** - verify or not verify SSL certificates

## Runtime Configuration

This configuration is used by each bot to load the specific parameters associated to each of them. Usually, BOTS file is used to generate runtime.conf. IntelMQ Manager generates this configuration.

**Template:**
```
    },

	...
}
```

**Example:**
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

More examples can be found at `intelmq/etc/runtime.conf` directory in IntelMQ repository.


## Harmonization Configuration

This configuration is used to specify the fields for all message types. The harmonization library will load this configuration to check, during the message processing, the values are compliant to harmonization. Usually, this configuration doesn't need any change.

**Template:**
```
{
	...
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
	...
}
```

**Example:**
```
{
	...
    "event": {
        "destination.asn": {
            "description": "The autonomous system number from which originated the connection.",
            "type": "Integer"
        },
        "destination.geolocation.cc": {
            "description": "Country-Code accoriding to ISO3166-1 alpha-2 for the destination IP.",
            "regex": "^[a-zA-Z0-9]{2}$",
            "type": "String"
        },
    	...
    },
	...
}
```

More examples can be found at `intelmq/etc/harmonization.conf` directory in IntelMQ repository.



# Utilities

## Management

IntelMQ has a modular structure consisting of bots. There are four types of bots:

* [CollectorBots](Bots.md#collectors) retrieve data from internal or external sources, the output
are *reports* consisting of many individual data sets.
* [ParserBots](Bots.md#parsers) parse the data by splitting it into individual *events* and
giving them a defined structure, see also [Data Harmonization](Data-Harmonization.md).
* [ExpertBots](Bots.md#experts) enrich the existing events by e.g. reverse records, geographic location information or abuse contacts.
* [OutputBots](Bots.md#outputs) write events to files, databases, (REST)-APIs, etc.

Each bot has one source queue (except collectors) and can have multiple
destination queues (except outputs). But multiple bots can write to the same pipeline, resulting in multiple inputs for the next bot.

Every bot runs in a separate process, they are uniquely identifiable by a *bot id*.

Currently only one instance of one bot can be run. Concepts for multiprocessing are being discussed, see this issue: [Multiprocessing per queue is not supported #186](https://github.com/certtools/intelmq/issues/186).

### Web interface: IntelMQ Manager

IntelMQ has a tool called IntelMQ Manager that gives to user a easy way to 
configure all pipeline with bots that your team needs. It is recommended to
use the IntelMQ Manager to become acquainted with the functionalities and concepts.
The IntelMQ Manager has all possibilities of intelmqctl tool and has a graphical interface for runtime and pipeline configuration.

See [IntelMQ Manager repository](https://github.com/certtools/intelmq-manager).

### Command-line interface: intelmqctl

**Syntax:**

```bash
# su - intelmq

$ intelmqctl -h
usage: 
        intelmqctl [start|stop|restart|status|run] bot-id
        intelmqctl [start|stop|restart|status]
        intelmqctl list [bots|queues]
        intelmqctl log bot-id [number-of-lines [log-level]]
        intelmqctl clear queue-id

Starting a bot:
    intelmqctl start bot-id
Stopping a bot:
    intelmqctl stop bot-id
Restarting a bot:
    intelmqctl restart bot-id
Get status of a bot:
    intelmqctl status bot-id

Run a bot directly (blocking) for debugging purpose:
    intelmqctl run bot-id

Starting the botnet (all bots):
    intelmqctl start
    etc.

Get a list of all configured bots:
    intelmqctl list bots

Get a list of all queues:
    intelmqctl list queues

Clear a queue:
    intelmqctl clear queue-id

Get logs of a bot:
    intelmqctl log bot-id [number-of-lines [log-level]]
    Reads the last lines from bot log, or from system log if no bot ID was
    given. Log level should be one of DEBUG, INFO, ERROR or CRITICAL.
    Default is INFO. Number of lines defaults to 10, -1 gives all. Result
    can be longer due to our logging format!

positional arguments:
  [start|stop|restart|status|run|list|clear|log]
  parameter

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --type {text,json}, -t {text,json}
                        choose if it should return regular text or other
                        machine-readable
  --quiet, -q           Quiet mode, useful for reloads initiatedscripts like
                        logrotate

description: intelmqctl is the tool to control intelmq system. Outputs are
logged to /opt/intelmq/var/log/intelmqctl
```

#### Botnet Concept

The botnet represents all currently configured bots. To get an overview which bots are running, use `intelmqctl status`or use IntelMQ Manager.

#### Forcing reset pipeline and cache (be careful)

If you are using the default broker (Redis), in some test situations you may need to quickly clear all pipelines and caches. Use the following procedure:
```bash
redis-cli FLUSHDB
redis-cli FLUSHALL
```

## Error Handling

### Tool: intelmqdump

When bots are failing due to bad input data or programming errors, they can dump the problematic message to a file along with a traceback, if configured accordingly. These dumps are saved at `/opt/intelmq/var/log/[botid].dump` as JSON files. There is an inspection and reinjection tool included in intelmq, called `intelmqdump`. It is an interactive tool able to show all dumped files, the number of dumps per file. Choose a file by bot-id or listed numeric id. You can then choose to delete single entries from the file with `e 1,3,4`, show a message in more readable format with `s 1` (prints the raw-message, can be long!), recover some messages and put them back in the pipeline for the bot by `a` or `r 0,4,5`. Or delete the file with all dumped messages using `d`.

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

All bots and `intelmqctl` log to `/opt/intelmq/var/log/`. In case of failures, messages are dumped to the same directory with file ending `.dump`.

```bash
tail -f /opt/intelmq/var/log/*.log
```

# Upgrade

## Stop IntelMQ and Backup

* Make sure that your IntelMQ system is completely stopped.
* Create a backup of IntelMQ Home directory, which includes all configurations. They are not overwritten, but backups are always nice to have!

```bash
sudo su -

cp -R /opt/intelmq /opt/intelmq-backup
```

## Upgrade

```bash
cd intelmq/
git pull
pip install -U intelmq  # or pip install -U . if you have a local repository
```

## Restore Configurations

* Apply your configurations backup.

```bash
rm -rf /opt/intelmq/etc/*
cp -R /opt/intelmq-backup/etc/* /opt/intelmq/etc/
```

## Redefine permissions

```bash
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

# Uninstall

```bash
pip uninstall intelmq
rm -rf /opt/intelmq
```

# Frequently Asked Questions

Consult the [FAQ](FAQ.md) if you encountered any problem.


# Additional Information

## Performance Tests

Somes tests have been made with a virtual machine with 
the following specifications:

* CPU: 1 core dedicated from i7 processor
* Memory: 4GB
* HDD: 10GB

The entire solution didnt have any problem handling 2.000.000 
queued events in memory with bots digesting the messages.
