# intelmqctl documentation

  * [Introduction](#introduction)
  * [Output type](#output-type)
  * [Manage individual bots](#manage-individual-bots)
   * [start](#start)
   * [stop](#stop)
   * [status](#status)
   * [restart](#restart)
   * [reload](#reload)
   * [disable](#disable)
   * [enable](#enable)
  * [Manage the botnet](#manage-the-botnet)
   * [start](#start-1)
   * [stop](#stop-1)
   * [status](#status-1)
   * [restart](#restart-1)
   * [reload](#reload-1)
  * [List bots](#list-bots)
  * [List queues](#list-queues)
  * [Log](#log)
  * [Check](#check)
  * [Known issues](#known-issues)

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

## Known issues

The currently implemented process managing using PID files is very erroneous.
If a PID is saved, the process dies and a new program gets the same PID, another program receives the SIGINT signal.
