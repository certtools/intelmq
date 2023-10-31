<!-- comment
   SPDX-FileCopyrightText: 2015 Aaron Kaplan <aaron@lo-res.org>, 2015-2021 Sebastian Wagner, 2020-2021 Birger Schacht, 2023 Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Managing IntelMQ

## Required services

You need to enable and start Redis if not already done. Using systemd it
can be done with:

```bash
systemctl enable redis.service
systemctl start redis.service
```

## Introduction

`intelmqctl` is the main tool to handle a intelmq installation. It handles
the bots themselves and has some tools to handle the installation.

Should you get lost any time, just use the **--help** after any
argument for further explanation.

```bash
> intelmqctl run file-output --help
```

## Manage the botnet

In IntelMQ, the botnet is the set of all currently configured and
enabled bots. All configured bots have their configuration in
`runtime.yaml`. By default, all bots are enabled.

If no bot id is given, the command applies to all bots / the botnet.
All commands except the start action are applied to all bots. But only
enabled bots are started.

In the examples below, a very minimal botnet is used.

### start

The start action applies to all bots which are enabled.

```bash
> intelmqctl start
Starting abusech-domain-parser...
abusech-domain-parser is running.
Starting abusech-feodo-domains-collector...
abusech-feodo-domains-collector is running.
Starting deduplicator-expert...
deduplicator-expert is running.
file-output is disabled.
Botnet is running.
```

As we can file-output is disabled and thus has not been started. You can
always explicitly start disabled bots.

### stop

The stop action applies to all bots. Assume that all bots have been
running:

```bash
> intelmqctl stop
Stopping Botnet...
Stopping abusech-domain-parser...
abusech-domain-parser is stopped.
Stopping abusech-feodo-domains-collector...
abusech-feodo-domains-collector is stopped.
Stopping deduplicator-expert...
deduplicator-expert is stopped.
Stopping file-output...
file-output is stopped.
Botnet is stopped.
```

### status

With this command we can see the status of all configured bots. Here,
the botnet was started beforehand:

```bash
> intelmqctl status
abusech-domain-parser is running.
abusech-feodo-domains-collector is running.
deduplicator-expert is running.
file-output is disabled.
```

And if the disabled bot has also been started:

```bash
> intelmqctl status
abusech-domain-parser is running.
abusech-feodo-domains-collector is running.
deduplicator-expert is running.
file-output is running.
```

If the botnet is stopped, the output looks like this:

```bash
> intelmqctl status
abusech-domain-parser is stopped.
abusech-feodo-domains-collector is stopped.
deduplicator-expert is stopped.
file-output is disabled.
```

### restart

The same as start and stop consecutively.

### reload

The same as reload of every bot.

### enable / disable

The sub commands `enable` and `disable` set the corresponding flags in `runtime.yaml`.

```bash
> intelmqctl status
file-output is stopped.
malware-domain-list-collector is stopped.
malware-domain-list-parser is stopped.
> intelmqctl disable file-output
> intelmqctl status
file-output is disabled.
malware-domain-list-collector is stopped.
malware-domain-list-parser is stopped.
> intelmqctl enable file-output
> intelmqctl status
file-output is stopped.
malware-domain-list-collector is stopped.
malware-domain-list-parser is stopped.
```

## Manage individual bots

As all init systems, intelmqctl has the methods start, stop, restart,
reload and status.

### start

This will start the bot with the ID `file-output`. A file
with it's PID will be created in `/opt/intelmq/var/run/[bot-id].pid`.

```bash
> intelmqctl start file-output
Starting file-output...
file-output is running.
```

If the bot is already running, it won't be started again:

```bash
> intelmqctl start file-output
file-output is running.
```

### stop

If the PID file does exist, a SIGINT will be sent to the process. After
0.25s we check if the process is running. If not, the PID file will be
removed.

```bash
> intelmqctl stop file-output
Stopping file-output...
file-output is stopped.
```

If there's no running bot, there's nothing to do.

```bash
> intelmqctl stop file-output
file-output was NOT RUNNING.
```

If the bot did not stop in 0.25s, intelmqctl will say it's still
running:

```bash
> intelmqctl stop file-output
file-output is still running
```

### status

Checks for the PID file and if the process with the given PID is alive.
If the PID file exists, but the process does not exist, it will be
removed.

```bash
> intelmqctl status file-output
file-output is stopped.
> intelmqctl start file-output
Starting file-output...
file-output is running.
> intelmqctl status file-output
file-output is running.
```

### restart

The same as stop and start consecutively.

```bash
> intelmqctl restart file-output
Stopping file-output...
file-output is stopped.
Starting file-output...
file-output is running.
```

### reload

Sends a SIGHUP to the bot, which will then reload the configuration.

```bash
> intelmqctl reload file-output
Reloading file-output ...
file-output is running.
```

If the bot is not running, we can't reload it:

```bash
> intelmqctl reload file-output
file-output was NOT RUNNING.
```

### run

This command is used for **debugging** purposes.

If launched with no arguments, the bot will call its init method and
start processing messages as usual -- but you see everything happens.

```bash
> intelmqctl run file-output
file-output: RestAPIOutputBot initialized with id file-output and version 3.5.2 as process 12345.
file-output: Bot is starting.
file-output: Loading source pipeline and queue 'file-output-queue'.
file-output: Connected to source queue.
file-output: No destination queues to load.
file-output: Bot initialization completed.
file-output: Waiting for incoming message.
```

Note that if another instance of the bot is running, only warning will
be displayed.

```bash
> intelmqctl run file-output
Main instance of the bot is running in the background. You may want to launch: intelmqctl stop file-output
```

You can set the log level with the `-l` flag, e.g. `-l DEBUG`. For the 'console' subcommand, 'DEBUG' is the default.

#### console

This command is used for **debugging** purposes.

If launched with **console** argument, you get a `pdb` live
console; or `ipdb` or `pudb` consoles if they were previously installed (I.E.
`pip3 install ipdb --user`).

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

If **get** is the parameter, you see the message that waits in the input
(source or internal) queue. If the argument is **pop**, the message gets
popped as well.

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

To send directly to the bot's output queue, just as it was sent by `self.send_message()` in bot's `process()` method, use the **send** argument. In our case of `file-output`, it has no destination queue so that nothing happens.

```bash
> intelmqctl run file-output message send '{"time.observation": "2017-05-17T22:00:33+00:00", "time.source": "2017-05-17T22:00:32+00:00"}'
file-output: Bot has no destination queues.
```

Note, if you would like to know possible parameters of the message, put
a wrong one -- you will be prompted if you want to list all the current
bot harmonization.

#### process

With no other arguments, bot's `process()` method will be run one time.

```bash
> intelmqctl run file-output process
file-output: Bot is starting.
file-output: Bot initialization completed.
file-output: Processing...
file-output: Waiting for incoming message.
file-output: Received message {'raw': '1234'}.
```

If run with **--dryrun|-d** flag, the message gets never really popped
out from the source or internal pipeline, nor sent to the output
pipeline. Plus, you receive a note about the exact moment the message
would get sent, or acknowledged. If the message would be sent to a
non-default path, the name of this path is printed on the console.

```bash
> intelmqctl run file-output process -d
file-output:  * Dryrun only, no message will be really sent through.
...
file-output: DRYRUN: Message would be acknowledged now!
```

You may trick the bot to process a JSON instead of the Message in its
pipeline with **--msg|-m** flag.

```bash
> intelmqctl run file-output process -m '{"source.ip":"1.2.3.4"}'
file-output:  * Message from cli will be used when processing.
...
```

If you wish to display the processed message as well, you the
**--show-sent|-s** flag. Then, if sent through (either with
`--dryrun` or without), the message gets displayed as well.

### disable

Sets the `enabled` flag in the runtime configuration of the
bot to `false`. By default, all bots are enabled.

Example output:

```bash
> intelmqctl status file-output
file-output is stopped.
> intelmqctl disable file-output
> intelmqctl status file-output
file-output is disabled.
```

### enable

Sets the `enabled` flag in the runtime configuration of the
bot to `true`.

Example output:

```bash
> intelmqctl status file-output
file-output is disabled.
> intelmqctl enable file-output
> intelmqctl status file-output
file-output is stopped.
```

## List bots

`intelmqctl list bots` does list all configured bots and
their description.

## List queues

`intelmqctl list queues` shows all queues which are
currently in use according to the configuration and how much events are
in it:

```bash
> intelmqctl list queues
abusech-domain-parser-queue - 0
abusech-domain-parser-queue-internal - 0
deduplicator-expert-queue - 0
deduplicator-expert-queue-internal - 0
file-output-queue - 234
file-output-queue-internal - 0
```

Use the `-q` or `--quiet` flag to only show
non-empty queues:

```bash
> intelmqctl list queues -q
file-output-queue - 234
```

The `--sum` or `--count` flag will show the
sum of events on all queues:

```bash
> intelmqctl list queues --sum
42
```

## Logging

intelmqctl can show the last log lines for a bot, filtered by the log
level.

Logs are stored in `/opt/intelmq/var/log/` or `/var/log/intelmq/` directory. In case of failures, messages are dumped to the same directory with the file extension `.dump`.

See the help page for more information.

## Check

This command will do various sanity checks on the installation and
especially the configuration.

### Orphaned Queues

The `intelmqctl check` tool can search for orphaned queues.
"Orphaned queues" are queues that have been used in the past and are
no longer in use. For example you had a bot which you removed or renamed
afterwards, but there were still messages in it's source queue. The
source queue won't be renamed automatically and is now disconnected. As
this queue is no longer configured, it won't show up in the list of
IntelMQ's queues too. In case you are using redis as message broker,
you can use the `redis-cli` tool to examine or remove these
queues:

```bash
redis-cli -n 2
keys * # lists all existing non-empty queues
llen [queue-name] # shows the length of the queue [queue-name]
lindex [queue-name] [index] # show the [index]'s message of the queue [queue-name]
del [queue-name] # remove the queue [queue-name]
```

To ignore certain queues in this check, you can set the parameter
`intelmqctl_check_orphaned_queues_ignore` in the
*defaults* configuration file. For example:

```yaml
"intelmqctl_check_orphaned_queues_ignore": ["Taichung-Parser"]
```

## Configuration upgrade

The `intelmqctl upgrade-config` function upgrade, upgrade
the configuration from previous versions to the current one. It keeps
track of previously installed versions and the result of all "upgrade
functions" in the "state file", locate in the `$var_state_path/state.json`
`/opt/intelmq/var/lib/state.json` or `/var/lib/intelmq/state.json`).

This function has been introduced in version 2.0.1.

It makes backups itself for all changed files before every run. Backups
are overridden if they already exists. So make sure to always have a
backup of your configuration just in case.

## Output type

intelmqctl can be used as command line tool, as library and as tool by
other programs. If called directly, it will print all output to the
console (stderr). If used as python library, the python types themselves
are returned. The third option is to use machine-readable JSON as output
(used by other managing tools).

## Exit code

In case of errors, unsuccessful operations, the exit code is higher than
0. For example, when running `intelmqctl start` and one
enabled bot is not running, the exit code is 1. The same is valid for
e.g. `intelmqctl status`, which can be used for monitoring,
and all other operations.
   
## Error Handling

When bots are failing due to bad input data or programming errors, they can dump the problematic message to a file along
with a traceback, if configured accordingly. These dumps are saved at in the logging directory as `[botid].dump` as JSON
files. IntelMQ comes with an inspection and reinjection tool, called `intelmqdump`. It is an interactive tool to show
all dumped files and the number of dumps per file. Choose a file by bot-id or listed numeric id. You can then choose to
delete single entries from the file with `e 1,3,4`, show a message in more readable format with `s 1` (prints the
raw-message, can be long!), recover some messages and put them back in the pipeline for the bot by `a` or `r 0,4,5`. Or delete the file with all dumped messages using `d`.

```bash
intelmqdump -h
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
  --truncate TRUNCATE, -t TRUNCATE
                        Truncate raw-data with more characters than given. 0 for no truncating. Default: 1000.

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
- d, Delete entries by IDs
  > d id{,id}
  > d 3,5
  The entries will be deleted from the dump file.
- d, Delete file
  > d
  Delete the opened file as a whole.
- s, Show by IDs
  > s id{,id}
  > s 0,4,5
  Show the selected IP in a readable format. It's still a raw format from
  repr, but with newlines for message and traceback.
- e, Edit by ID
  > e id
  > e 0
  > e 1,2
  Opens an editor (by calling `sensible-editor`) on the message. The modified message is then saved in the dump.
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
(r)ecover by ids, recover (a)ll, delete (e)ntries, (d)elete file, (s)how by ids, (q)uit, edit id (v)? d
Deleted file /opt/intelmq/var/log/dragon-research-group-ssh-parser.dump
```

Bots and the intelmqdump tool use file locks to prevent writing to already opened files. Bots are trying to lock the
file for up to 60 seconds if the dump file is locked already by another process
(intelmqdump) and then give up. Intelmqdump does not wait and instead only shows an error message.

By default, the `show` command truncates the `raw` field of messages at 1000 characters to change this limit or disable
truncating at all (value 0), use the `--truncate` parameter.

## Known issues

The currently implemented process managing using PID files is very
erroneous.
