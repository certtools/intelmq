# intelmqctl documentation

**Table of Contents:**
- [Introduction](#introduction)
- [Output type](#output-type)
- [Manage individual bots](#manage-individual-bots)
  - [start](#start)
  - [stop](#stop)
  - [status](#status)
  - [restart](#restart)
  - [reload](#reload)
  - [run](#run)
    - [console](#console)
    - [message](#message)
    - [process](#process)
  - [disable](#disable)
  - [enable](#enable)
- [Manage the botnet](#manage-the-botnet)
  - [start](#start)
  - [stop](#stop)
  - [status](#status)
  - [restart](#restart)
  - [reload](#reload)
  - [enable / disable](#enable-disable)
- [List bots](#list-bots)
- [List queues](#list-queues)
- [Log](#log)
- [Check](#check)
- [Exit code](#exit-code)
- [Known issues](#known-issues)

## Introduction

intelmqctl is the main tool to handle a intelmq installation.
It handles the bots themselves and has some tools to handle the installation.

## Output type

intelmqctl can be used as command line tool, as library and as tool by other programs.
If called directly, it will print all output to the console (stderr).
If used as python library, the python types themselves are returned.
The third option is to use machine-readable JSON as output (used by other managing tools).

## Manage individual bots

As all init systems, intelmqctl has the methods start, stop, restart, reload and status.

### start

This will start the bot with the ID `file-output`. A file with it's PID will be created in `/opt/intelmq/var/run/[bot-id].pid`.

```bash
> intelmqctl start file-output
intelmqctl: Starting file-output...
intelmqctl: file-output is running.
```

If the bot is already running, it won't be started again:
```bash
> intelmqctl start file-output
intelmqctl: file-output is running.
```

### stop

If the PID file does exist, a SIGINT will be sent to the process. After 0.25s we check if the process is running. If not, the PID file will be removed.

```bash
> intelmqctl stop file-output
intelmqctl: Stopping file-output...
intelmqctl: file-output is stopped.
```

If there's no running bot, there's nothing to do.
```bash
> intelmqctl stop file-output
intelmqctl: file-output was NOT RUNNING.
```

If the bot did not stop in 0.25s, intelmqctl will say it's still running:

```bash
> intelmqctl stop file-output
intelmqctl: file-output is still running
```

### status

Checks for the PID file and if the process with the given PID is alive. If the PID file exists, but the process does not exist, it will be removed.

```bash
> intelmqctl status file-output
intelmqctl: file-output is stopped.
> intelmqctl start file-output
intelmqctl: Starting file-output...
intelmqctl: file-output is running.
> intelmqctl status file-output
intelmqctl: file-output is running.
```

### restart

The same as stop and start consecutively.

```bash
> intelmqctl restart file-output
intelmqctl: Stopping file-output...
intelmqctl: file-output is stopped.
intelmqctl: Starting file-output...
intelmqctl: file-output is running.
```

### reload

Sends a SIGHUP to the bot, which will then reload the configuration.

```bash
> intelmqctl reload file-output
intelmqctl: Reloading file-output ...
intelmqctl: file-output is running.
```
If the bot is not running, we can't reload it:
```bash
> intelmqctl reload file-output
intelmqctl: file-output was NOT RUNNING.
```

### run

Run a bot directly for debugging purpose.

If launched with no arguments, the bot will call its init method and start processing messages as usual – but you see everything happens.

```bash
> intelmqctl run file-output
file-output: RestAPIOutputBot initialized with id file-output and version 3.5.2 as process 12345.
file-output: Bot is starting.
file-output: Loading source pipeline and queue 'file-output-queue'.
file-output: Connected to source queue.
file-output: No destination queues to load.
file-output: Pipeline ready.
file-output: Waiting for incoming message.
```

Should you get lost any time, just use the **--help** after any argument for further explanation.

```bash
> intelmqctl run file-output --help
```

Note that if another instance of the bot is running, only warning will be displayed.

```bash
> intelmqctl run file-output
intelmqctl: Main instance of the bot is running in the background. You may want to launch: intelmqctl stop file-output
```

You can set the log level with the `-l` flag, e.g. `-l DEBUG`. For the 'console' subcommand, 'DEBUG' is the default.

#### console

If launched with **console** argument, you get a ```pdb``` live console; or ```ipdb``` or ```pudb``` consoles if they were previously installed (I.E. ```pip3 install ipdb --user```).

```bash
> intelmqctl run file-output console
*** Using console ipdb. Please use 'self' to access to the bot instance properties. ***
ipdb> self. ...
```

You may specify the desired console in the next argument.

```bash
> intelmqctl run file-output console pudb
```

#### message

Operate directly with the input / output pipelines.

If **get** is the parameter, you see the message that waits in the input (source or internal) queue. If the argument is **pop**, the message gets popped as well.

```bash
> intelmqctl run file-output message get
file-output: Waiting for a message to get...
{
    "classification.type": "c&c",
    "feed.url": "https://example.com",
    "raw": "1233",
    "source.ip": "1.2.3.4",
    "time.observation": "2017-05-17T22:00:33+00:00",
    "time.source": "2017-05-17T22:00:32+00:00"
}
```

To send directly to the bot's ouput queue, just as it was sent by ```self.send_message()``` in bot's ```process()``` method, use the **send** argument.
In our case of ```file-output```, it has no destionation queue so that nothing happens.

```bash
> intelmqctl run file-output message send '{"time.observation": "2017-05-17T22:00:33+00:00", "time.source": "2017-05-17T22:00:32+00:00"}'
file-output: Bot has no destination queues.
```

Note, if you would like to know possible parameters of the message, put a wrong one – you will be prompted if you want to list all the current bot harmonization.

#### process

With no other arguments, bot\'s ```process()``` method will be run one time.

```bash
> intelmqctl run file-output process
file-output: Bot is starting.
file-output: Pipeline ready.
file-output: Processing...
file-output: Waiting for incoming message.
file-output: Received message {'raw': '1234'}.
```

If run with **--dryrun|-d** flag, the message gets never really popped out from the source or internal pipeline, nor sent to the output pipeline.
Plus, you receive a note about the exact moment the message would get sent, or acknowledged. If the message would be sent to a non-default path, the name of this path is printed on the console.

```bash
> intelmqctl run file-output process -d
file-output:  * Dryrun only, no message will be really sent through.
...
file-output: DRYRUN: Message would be acknowledged now!
```

You may trick the bot to process a JSON instead of the Message in its pipeline with **--msg|-m** flag.

```bash
> intelmqctl run file-output process -m '{"source.ip":"1.2.3.4"}'
file-output:  * Message from cli will be used when processing.
...
```

If you wish to display the processed message as well, you the **--show-sent|-s** flag. Then, if sent through (either with `--dryrun` or without), the message gets displayed as well.


### disable

Sets the `enabled` flag in runtime.conf to `false`.
Assume the bot is now enabled (default for all bots).

```bash
> intelmqctl status file-output
intelmqctl: file-output is stopped.
> intelmqctl disable file-output
> intelmqctl status file-output
intelmqctl: file-output is disabled.
```

### enable

Ensures that the `enabled` flag in runtime.conf is not set to `false`.
Assume that the bot is now dibbled.

```bash
> intelmqctl status file-output
intelmqctl: file-output is disabled.
> intelmqctl enable file-output
> intelmqctl status file-output
intelmqctl: file-output is stopped.
```


## Manage the botnet

In IntelMQ, the botnet is the set of all currently configured and enabled bots.
All configured bots have their configuration in runtime.conf and their queues in pipeline.conf.
By default, all bots are enabled. To disable a bot set `enabled` to `false`.
Also see [Bots.md](Bots) and [User-Guide.md#runtime-configuration](User Guide: Runtime Configuration).

If not bot id is given, the command applies to all bots / the botnet.
All commands except the start action are applied to all bots.
But only enabled bots are started.

In the examples below, a very minimal botnet is used.

### start

The start action applies to all bots which are enabled.

```bash
> intelmqctl start
intelmqctl: Starting abusech-domain-parser...
intelmqctl: abusech-domain-parser is running.
intelmqctl: Starting abusech-feodo-domains-collector...
intelmqctl: abusech-feodo-domains-collector is running.
intelmqctl: Starting deduplicator-expert...
intelmqctl: deduplicator-expert is running.
intelmqctl: file-output is disabled.
intelmqctl: Botnet is running.
```

As we can > intelmqctl stop
intelmqctl: Stopping Botnet...
intelmqctl: Stopping abusech-domain-parser...
intelmqctl: abusech-domain-parser is stopped.
intelmqctl: Stopping abusech-feodo-domains-collector...
intelmqctl: abusech-feodo-domains-collector is stopped.
intelmqctl: Stopping deduplicator-expert...
intelmqctl: deduplicator-expert is stopped.
intelmqctl: Stopping file-output...
intelmqctl: file-output is stopped.
intelmqctl: Botnet is stopped.
see, file-output is disabled and thus has not been started. You can always explicitly start disabled bots.

### stop
The stop action applies to all bots. Assume that all bots have been running:

```bash
> intelmqctl stop
intelmqctl: Stopping Botnet...
intelmqctl: Stopping abusech-domain-parser...
intelmqctl: abusech-domain-parser is stopped.
intelmqctl: Stopping abusech-feodo-domains-collector...
intelmqctl: abusech-feodo-domains-collector is stopped.
intelmqctl: Stopping deduplicator-expert...
intelmqctl: deduplicator-expert is stopped.
intelmqctl: Stopping file-output...
intelmqctl: file-output is stopped.
intelmqctl: Botnet is stopped.
```

### status

With this command we can see the status of all configured bots. Here, the botnet was started beforehand:
```bash
> intelmqctl status
intelmqctl: abusech-domain-parser is running.
intelmqctl: abusech-feodo-domains-collector is running.
intelmqctl: deduplicator-expert is running.
intelmqctl: file-output is disabled.
```
And if the disabled bot has also been started:
```bash
> intelmqctl status
intelmqctl: abusech-domain-parser is running.
intelmqctl: abusech-feodo-domains-collector is running.
intelmqctl: deduplicator-expert is running.
intelmqctl: file-output is running.
```

If the botnet is stopped, the output looks like this:
```bash
> intelmqctl status
intelmqctl: abusech-domain-parser is stopped.
intelmqctl: abusech-feodo-domains-collector is stopped.
intelmqctl: deduplicator-expert is stopped.
intelmqctl: file-output is disabled.
```

### restart
The same as start and stop consecutively.

### reload
The same as reload of every bot.

### enable / disable
The sub commands `enable` and `disable` set the corresponding flags in runtime.conf.

```bash
> intelmqctl status
intelmqctl: file-output is stopped.
intelmqctl: malware-domain-list-collector is stopped.
intelmqctl: malware-domain-list-parser is stopped.
> intelmqctl disable file-output
> intelmqctl status
intelmqctl: file-output is disabled.
intelmqctl: malware-domain-list-collector is stopped.
intelmqctl: malware-domain-list-parser is stopped.
> intelmqctl enable file-output
> intelmqctl status
intelmqctl: file-output is stopped.
intelmqctl: malware-domain-list-collector is stopped.
intelmqctl: malware-domain-list-parser is stopped.
```

## List bots
`intelmqctl list bots` does list all configured bots and their description.

## List queues
`intelmqctl list queues` shows all queues which are currently in use according to the configuration and how much events are in it:

```bash
> intelmqctl list queues
intelmqctl: abusech-domain-parser-queue - 0
intelmqctl: abusech-domain-parser-queue-internal - 0
intelmqctl: deduplicator-expert-queue - 0
intelmqctl: deduplicator-expert-queue-internal - 0
intelmqctl: file-output-queue - 234
intelmqctl: file-output-queue-internal - 0
```

Use the `-q` or `--quiet` flag to only show non-empty queues:

```bash
> intelmqctl list queues -q
intelmqctl: file-output-queue - 234
```

## Log

intelmqctl can show the last log lines for a bot, filtered by the log level.

See the help page for more information.

## Check
This command will do various sanity checks on the installation and especially the configuration.

## Exit code
In case of errors, unsuccessful operations, the exit code is higher than 0.
For example, when running `intelmqctl start` and one enabled bot is not running, the exit code is 1.
The same is valid for e.g. `intelmqctl status`, which can be used for monitoring, and all other operations.

## Known issues

The currently implemented process managing using PID files is very erroneous.
