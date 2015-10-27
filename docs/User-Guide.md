**Table of Contents**

1. [Requirements](#requirements)
2. [Installation](#installation)
    1. [Install Dependencies](#install-dependencies)
        1. [Python 3.4 (recommended)](#dependencies-python34)
        2. [Python 2.7](#dependencies-python27)
    2. [Install](#install)
        1. [Python 3.4 (recommended)](#install-python34)
        2. [Python 2.7](#install-python27)
3. [Management](#management)
4. [Configuration](#configuration)
    1. [system.conf](#conf-system)
    2. [startup.conf](#conf-startup)
    3. [pipeline.conf](#conf-pipeline)
    4. [default.conf](#conf-defaults)
        1. [Error Handling](#conf-defaults-error)
        2. [Miscellaneous](#conf-defaults-miscellaneous)
    5. [runtime.conf](#conf-runtime)
    6. [harmonization.conf](#conf-harmonization)
5. [Upgrade](#upgrade)
6. [Uninstall](#uninstall)
7. [Frequently Asked Questions](#faq)


<a name="requirements"></a>
# Requirements

The following instructions assume the following requirements:

* **Operating System:** Ubuntu 14.04 LTS or Debian 8 or CentOS 7

<a name="installation"></a>
# Installation

<a name="install-dependencies"></a>
## Install Dependencies

<a name="dependencies-python34"></a>
#### Python 3.4 (recommended)

##### Ubuntu 14.04 / Debian 8

```bash
apt-get install python3 python3-pip
apt-get install git build-essential libcurl4-gnutls-dev libffi-dev
apt-get install redis-server
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

<a name="dependencies-python27"></a>
#### Python 2.7

##### Ubuntu 14.04 / Debian 8

```bash
apt-get install python
apt-get install git build-essential libcurl4-gnutls-dev libffi-dev
apt-get install python-dev python-pip python-zmq python-pycurl python-openssl python-pyasn1
apt-get install redis-server
```

##### CentOS 7

```bash
yum install git libcurl-devel gcc gcc-c++
yum install python python-devel 
yum install redis
```

Enable redis on startup:
```bash
systemctl enable redis
systemctl start redis
```

<a name="install"></a>
## Install

The `REQUIREMENTS` files define a list python packages and versions, which are necessary to run *all components* of intelmq. The defined versions are recommendations.

<a name="install-python34"></a>
#### Python 3.4 (recommended)

```bash
git clone https://github.com/certtools/intelmq.git /tmp/intelmq
cd /tmp/intelmq

sudo -s

pip3 install -r REQUIREMENTS
python3.4 setup.py install

useradd -d /opt/intelmq -U -s /bin/bash intelmq
echo 'export PATH="$PATH:$HOME/bin"' > /opt/intelmq/.profile
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
echo 'export INTELMQ_PYTHON=/usr/bin/python3.4' >> /opt/intelmq/.profile
```

<a name="install-python27"></a>
#### Python 2.7

```bash
sudo su -

git clone https://github.com/certtools/intelmq.git /tmp/intelmq
cd /tmp/intelmq

pip2 install -r REQUIREMENTS2
python2.7 setup.py install

useradd -d /opt/intelmq -U -s /bin/bash intelmq
echo 'export PATH="$PATH:$HOME/bin"' > /opt/intelmq/.profile
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

<a name="management"></a>
# Management

## How it Works
Intelmq has a modular structure consisting of bots. There are four types of bots:

* *CollectorBots* retrieve data from internal or external sources, the output
are *reports* consisting of many individual data sets.
* *ParserBots* parse the data by splitting it into individual *events* and
giving them a defined structure, see also [Data-Harmonization](Data-Harmonization.md).
* *ExpertBots* enrich the existing events by e.g. reverse records, geographic location
information or abuse contacts.
* *OutputBots* write events to files, databases, (REST)-APIs, etc.

Each bot has one source queue (except collectors) and can have multiple
destination queues (except outputs). But multiple bots can write to the same
pipeline, resulting in multiple inputs for the next bot.

Every bot runs in a separate process, they are uniquely identifiable by a *bot id*.

Currently only one instance of one bot can be run. Concepts for Multiprocessing are
being discussed, see this issue:
[Multiprocessing per queue is not supported #186](https://github.com/certtools/intelmq/issues/186).


## Web interface: intelmq-manager

IntelMQ has a tool called IntelMQ Manager that gives to user a easy way to 
configure all pipeline with bots that your CERT needs. It is recommended to
use the Manager to become acquainted with the functionalities and concepts.
The intelmq-manager has all possibilities of intelmqctl and has a graphical
interface for startup and pipeline configuration.

See [github.com/certtools/intelmq-manager](https://github.com/certtools/intelmq-manager).

## Command-line interface

**Syntax:**

```bash
# su - intelmq

$ intelmqctl --h
usage: 
        intelmqctl --bot [start|stop|restart|status] --id=cymru-expert
        intelmqctl --botnet [start|stop|restart|status]
        intelmqctl --list [bots|queues]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --id BOT_ID, -i BOT_ID
                        bot ID
  --type {text,json}, -t {text,json}
                        choose if it should return regular text or other forms
                        of output
  --log [log-level]:[number-of-lines], -l [log-level]:[number-of-lines]
                        Reads the last lines from bot log, or from system log
                        if no bot ID was given. Log level should be one of
                        DEBUG, INFO, ERROR or CRTICAL. Default is INFO. Number
                        of lines defaults to 10, -1 gives all. Reading from
                        system log is not implemented yet.
  --bot [start|stop|restart|status], -b [start|stop|restart|status]
  --botnet [start|stop|restart|status], -n [start|stop|restart|status]
  --list [bots|queues], -s [bots|queues]
  --clear queue, -c queue
                        Clears the given queue in broker

description: intelmqctl is the tool to control intelmq system. Outputs are
logged to /opt/intelmq/var/log/intelmqctl
```

### Botnet

The botnet represents all currently configured bots. To get an overview which
bots are running, use `intelmqctl -n status`.

### Start bots with non-default Python

The python version/path can be specified by the `INTELMQ_PYTHON` environment variable. By default it's the default python binary. This can be used to start the bots with current Python (version 3), while the default Python version for the operating system is still Legacy Python (version 2).

    $ export INTELMQ_PYTHON=/usr/bin/python3.4
	$ intelmqctl -n start

## Utilities

### Inspecting dumped messages

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


### Monitoring Logs

All bots and `intelmqctl` log to `/opt/intelmq/var/log/`. In case of failures,
messages are dumped to the same directory with file ending `.dump`.

```bash
tail -f /opt/intelmq/var/log/*.log
```

### Reset Pipeline and Cache (be careful)

```bash
redis-cli FLUSHDB
redis-cli FLUSHALL
```

<a name="configuration"></a>
# Configuration

By default, one collector, one parser and one output are started. The default
collector an parser handle data from malware domain list, the file output bot
writes all data to `/opt/intelmq/var/lib/bots/file-output/events.txt`.

The configuration directory is `/opt/intelmq/etc/`, all files are JSON.

* `defaults.conf`: Some default values for bots and their behavior, e.g.
error handling, log options and pipeline configuration. Will be removed in
[future](https://github.com/certtools/intelmq/issues/267).
* `system.conf`: System configuration for e.g. the logger and the pipeline.
* `startup.conf`: Maps the bot ids to python modules.
* `runtime.conf`: Configuration for the individual bots.
* `pipeline.conf`: Defines source and destination queues per bot.
* `BOTS`: Includes configuration hints for all bots. E.g. feed URLs or
database connection parameters. Use this as a template for `startup.conf`
and `runtime.conf`. Also read by the intelmq-manager.

To configure a new BOT, you need to define it first in `startup.conf`.
Then do the configuration in `runtime.conf` using the bot if.
Configure source and destination queues in `pipeline.conf`.
Use the intelmq-manager mentioned above to generate the configuration files if unsure.

1. [system.conf](#conf-system)
2. [startup.conf](#conf-startup)
3. [pipeline.conf](#conf-pipeline)
4. [defaults.conf](#conf-defaults)
    1. [Error Handling](#conf-defaults-error)
    2. [Miscellaneous](#conf-defaults-miscellaneous)
5. [runtime.conf](#conf-runtime)
6. [harmonization.conf](#conf-harmonization)


<a name="conf-system"></a>
## system.conf

FIXME

<a name="conf-startup"></a>
## startup.conf

FIXME

<a name="conf-pipeline"></a>
## pipeline.conf

FIXME

<a name="conf-defaults"></a>
## defaults.conf

All bots inherits this configuration parameters and they can overwrite them using the same parameters in configuration.

<a name="conf-defaults-error"></a>
#### Error Handling

* **`error_log_message`** - in case of an error, this option will allows bot to write the message (report or event) in log file. Use the following values:
    * **`true/false`** - write or not write message in log file

* **`error_log_exception`** - in case of an error, this option will allows bot to write the error exception in log file. Use the following values:
    * **`true/false`** - write or not write exception in log file

* **`error_procedure`** - in case of an error, this option defines the procedure that bot will adopt. Use the following values:

    * **`stop`** - stop bot after retry X times, defined in `error_max_retries` option with a delay between retries defined at `error_retry_delay` option. If bot reach `error_max_retries` value, bot will remove the message from pipeline and stop. If the option `error_dump_message` is enable, the bot will dump the removed message to the dump log.
    
    * **`pass`** - will pass to the next message after retry X times, removing from pipeline the current message. If the option `error_dump_message` is enable, the bot will dump the removed message to the dump log.

* **`error_max_retries`** - in case of an error and the value of the `error_procedure` option is `retry`, bot will try to start processing the current message X times defined at `error_max_retries` option. The value must be an `integer value`.

* **`error_retry_delay`** - in case of an error, this option will allows you to define the number of seconds which bot will wait until next retry. The value must be an `integer value`.

* **`error_dump_message`** - in case of an error, this option will allows bot to write the message (report or event) in the dump file (use intelmqdump to re-insert the message).
    * **`true/false`** - write or not write message in dump file

<a name="conf-defaults-miscellaneous"></a>
#### Miscellaneous

* **`load_balance`** - this option allows to choose the behavior of the queue. Use the following values:
    * **`true`** - splits the messages into several queues wihtout duplication
    * **`false`** - duplicates the messages into each queue

* **`broker`** - select which broker intelmq can use. Use the following values:
    * **`redis`** - Redis allows some persistence but is not so fast as ZeroMQ.
    * **`zeromq`** - (under development) ZeroMQ is fast but doest allow persistence.

* **`rate_limit`** - time interval (in seconds) between messages processing. The value must be an `integer value`.

* **`source_pipeline_host`** - broker IP or FQDN that bot will use to connect and receive messages.

* **`source_pipeline_port`** - broker port that bot will use to connect and receive messages.

* **`source_pipeline_db`** - broker database that bot will use to connect and receive messages (requirement from redis broker).

* **`destination_pipeline_host`** - broker IP or FQDN that bot will use to connect and send messages.

* **`destination_pipeline_port`** - broker port that bot will use to connect and send messages.

* **`destination_pipeline_db`** - broker database that bot will use to connect and send messages (requirement from redis broker).

* **`http_proxy`** - proxy HTTP that bot will use when perform HTTP requests (e.g. bots/collectors/collector_http.py). The value must follow RFC1738.

* **`https_proxy`** - proxy HTTPS that bot will use when perform secure HTTPS requests (e.g. bots/collectors/collector_http.py).

* **`http_user_agent`** - user-agent that bot will use when perform HTTP/HTTPS requests (e.g. bots/collectors/collector_http.py).

* **`http_verify_cert`** - defines if bot will verify SSL certificates when perform HTTPS requests (e.g. bots/collectors/collector_http.py).
    * **`true/false`** - verify or not verify SSL certificates

<a name="conf-runtime"></a>
## runtime.conf

<a name="conf-harmonization"></a>
## harmonization.conf




## Additional Information

### Perfomance Tests

Somes tests have been made with a virtual machine with 
the following specifications:

* CPU: 1 core dedicated from i7 processor
* Memory: 4GB
* HDD: 10GB

The entire solution didnt have any problem handling 2.000.000 
queued events in memory with bots digesting the messages.


<a name="upgrade"></a>
# Upgrade

## Stop IntelMQ and Backup

* Make sure that your IntelMQ system is completely stopped.
* Create a backup of IntelMQ Home directory, which includes all configurations.

```bash
sudo su -

cp -R /opt/intelmq /opt/intelmq-backup
```

## Upgrade

```bash
cd intelmq/
git pull
python setup.py install
```

## Restore Configurations

* Apply your configurations backup.

```bash
rm -rf /opt/intelmq/*
cp -R /opt/intelmq-backup/* /opt/intelmq/
```


# Uninstall

<a name="uninstall"></a>
```bash
pip uninstall intelmq
```

<a name="faq"></a>
# Frequently Asked Questions

Consult the [FAQ.md](FAQ) if you encountered any problem.
