..
   SPDX-FileCopyrightText: 2017 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

========================
intelmqctl documentation
========================

.. contents::

------------
Introduction
------------

intelmqctl is the main tool to handle a intelmq installation.
It handles the bots themselves and has some tools to handle the installation.

-----------
Output type
-----------

intelmqctl can be used as command line tool, as library and as tool by other programs.
If called directly, it will print all output to the console (stderr).
If used as python library, the python types themselves are returned.
The third option is to use machine-readable JSON as output (used by other managing tools).

----------------------
Manage individual bots
----------------------

As all init systems, intelmqctl has the methods start, stop, restart, reload and status.

start
=====

This will start the bot with the ID `file-output`. A file with it's PID will be created in `/opt/intelmq/var/run/[bot-id].pid`.

.. code-block:: bash

   > intelmqctl start file-output
   Starting file-output...
   file-output is running.

If the bot is already running, it won't be started again:

.. code-block:: bash

   > intelmqctl start file-output
   file-output is running.

stop
====

If the PID file does exist, a SIGINT will be sent to the process. After 0.25s we check if the process is running. If not, the PID file will be removed.

.. code-block:: bash

   > intelmqctl stop file-output
   Stopping file-output...
   file-output is stopped.

If there's no running bot, there's nothing to do.

.. code-block:: bash

   > intelmqctl stop file-output
   file-output was NOT RUNNING.

If the bot did not stop in 0.25s, intelmqctl will say it's still running:

.. code-block:: bash

   > intelmqctl stop file-output
   file-output is still running

status
======

Checks for the PID file and if the process with the given PID is alive. If the PID file exists, but the process does not exist, it will be removed.

.. code-block:: bash

   > intelmqctl status file-output
   file-output is stopped.
   > intelmqctl start file-output
   Starting file-output...
   file-output is running.
   > intelmqctl status file-output
   file-output is running.

restart
=======

The same as stop and start consecutively.

.. code-block:: bash

   > intelmqctl restart file-output
   Stopping file-output...
   file-output is stopped.
   Starting file-output...
   file-output is running.

reload
======

Sends a SIGHUP to the bot, which will then reload the configuration.

.. code-block:: bash

   > intelmqctl reload file-output
   Reloading file-output ...
   file-output is running.

If the bot is not running, we can't reload it:

.. code-block:: bash

   > intelmqctl reload file-output
   file-output was NOT RUNNING.

run
===

Run a bot directly for debugging purpose.

If launched with no arguments, the bot will call its init method and start processing messages as usual – but you see everything happens.

.. code-block:: bash

   > intelmqctl run file-output
   file-output: RestAPIOutputBot initialized with id file-output and version 3.5.2 as process 12345.
   file-output: Bot is starting.
   file-output: Loading source pipeline and queue 'file-output-queue'.
   file-output: Connected to source queue.
   file-output: No destination queues to load.
   file-output: Bot initialization completed.
   file-output: Waiting for incoming message.

Should you get lost any time, just use the **--help** after any argument for further explanation.

.. code-block:: bash

   > intelmqctl run file-output --help

Note that if another instance of the bot is running, only warning will be displayed.

.. code-block:: bash

   > intelmqctl run file-output
   Main instance of the bot is running in the background. You may want to launch: intelmqctl stop file-output

You can set the log level with the `-l` flag, e.g. `-l DEBUG`. For the 'console' subcommand, 'DEBUG' is the default.

console
-------

If launched with **console** argument, you get a ```pdb``` live console; or ```ipdb``` or ```pudb``` consoles if they were previously installed (I.E. ```pip3 install ipdb --user```).

.. code-block:: bash

   > intelmqctl run file-output console
   *** Using console ipdb. Please use 'self' to access to the bot instance properties. ***
   ipdb> self. ...

You may specify the desired console in the next argument.

.. code-block:: bash

   > intelmqctl run file-output console pudb

message
-------

Operate directly with the input / output pipelines.

If **get** is the parameter, you see the message that waits in the input (source or internal) queue. If the argument is **pop**, the message gets popped as well.

.. code-block:: bash

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

To send directly to the bot's output queue, just as it was sent by ```self.send_message()``` in bot's ```process()``` method, use the **send** argument.
In our case of ```file-output```, it has no destination queue so that nothing happens.

.. code-block:: bash

   > intelmqctl run file-output message send '{"time.observation": "2017-05-17T22:00:33+00:00", "time.source": "2017-05-17T22:00:32+00:00"}'
   file-output: Bot has no destination queues.

Note, if you would like to know possible parameters of the message, put a wrong one – you will be prompted if you want to list all the current bot harmonization.

process
-------

With no other arguments, bot\'s ```process()``` method will be run one time.

.. code-block:: bash

   > intelmqctl run file-output process
   file-output: Bot is starting.
   file-output: Bot initialization completed.
   file-output: Processing...
   file-output: Waiting for incoming message.
   file-output: Received message {'raw': '1234'}.

If run with **--dryrun|-d** flag, the message gets never really popped out from the source or internal pipeline, nor sent to the output pipeline.
Plus, you receive a note about the exact moment the message would get sent, or acknowledged. If the message would be sent to a non-default path, the name of this path is printed on the console.

.. code-block:: bash

   > intelmqctl run file-output process -d
   file-output:  * Dryrun only, no message will be really sent through.
   ...
   file-output: DRYRUN: Message would be acknowledged now!

You may trick the bot to process a JSON instead of the Message in its pipeline with **--msg|-m** flag.

.. code-block:: bash

   > intelmqctl run file-output process -m '{"source.ip":"1.2.3.4"}'
   file-output:  * Message from cli will be used when processing.
   ...

If you wish to display the processed message as well, you the **--show-sent|-s** flag. Then, if sent through (either with `--dryrun` or without), the message gets displayed as well.


disable
=======

Sets the `enabled` flag in the runtime configuration of the bot to `false`.
By default, all bots are enabled.

Example output:

.. code-block:: bash

   > intelmqctl status file-output
   file-output is stopped.
   > intelmqctl disable file-output
   > intelmqctl status file-output
   file-output is disabled.

enable
======

Sets the `enabled` flag in the runtime configuration of the bot to `true`.

Example output:

.. code-block:: bash

   > intelmqctl status file-output
   file-output is disabled.
   > intelmqctl enable file-output
   > intelmqctl status file-output
   file-output is stopped.

-----------------
Manage the botnet
-----------------

In IntelMQ, the botnet is the set of all currently configured and enabled bots.
All configured bots have their configuration in runtime.conf.
By default, all bots are enabled. To disable a bot set `enabled` to `false`.
Also see :doc:`bots` and :ref:`runtime-configuration`.

If not bot id is given, the command applies to all bots / the botnet.
All commands except the start action are applied to all bots.
But only enabled bots are started.

In the examples below, a very minimal botnet is used.

start
=====

The start action applies to all bots which are enabled.

.. code-block:: bash

   > intelmqctl start
   Starting abusech-domain-parser...
   abusech-domain-parser is running.
   Starting abusech-feodo-domains-collector...
   abusech-feodo-domains-collector is running.
   Starting deduplicator-expert...
   deduplicator-expert is running.
   file-output is disabled.
   Botnet is running.

As we can file-output is disabled and thus has not been started. You can always explicitly start disabled bots.

stop
====

The stop action applies to all bots. Assume that all bots have been running:

.. code-block:: bash

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

status
======

With this command we can see the status of all configured bots. Here, the botnet was started beforehand:

.. code-block:: bash

   > intelmqctl status
   abusech-domain-parser is running.
   abusech-feodo-domains-collector is running.
   deduplicator-expert is running.
   file-output is disabled.

And if the disabled bot has also been started:

.. code-block:: bash

   > intelmqctl status
   abusech-domain-parser is running.
   abusech-feodo-domains-collector is running.
   deduplicator-expert is running.
   file-output is running.

If the botnet is stopped, the output looks like this:

.. code-block:: bash

   > intelmqctl status
   abusech-domain-parser is stopped.
   abusech-feodo-domains-collector is stopped.
   deduplicator-expert is stopped.
   file-output is disabled.

restart
=======

The same as start and stop consecutively.

reload
======

The same as reload of every bot.

enable / disable
================

The sub commands `enable` and `disable` set the corresponding flags in runtime.conf.

.. code-block:: bash

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

---------
List bots
---------

`intelmqctl list bots` does list all configured bots and their description.

-----------
List queues
-----------

`intelmqctl list queues` shows all queues which are currently in use according to the configuration and how much events are in it:

.. code-block:: bash

   > intelmqctl list queues
   abusech-domain-parser-queue - 0
   abusech-domain-parser-queue-internal - 0
   deduplicator-expert-queue - 0
   deduplicator-expert-queue-internal - 0
   file-output-queue - 234
   file-output-queue-internal - 0

Use the `-q` or `--quiet` flag to only show non-empty queues:

.. code-block:: bash

   > intelmqctl list queues -q
   file-output-queue - 234

The `--sum` or `--count` flag will show the sum of events on all queues:

.. code-block:: bash

   > intelmqctl list queues --sum
   42

---
Log
---

intelmqctl can show the last log lines for a bot, filtered by the log level.

See the help page for more information.

-----
Check
-----

This command will do various sanity checks on the installation and especially the configuration.


.. _orphan-queues:

Orphaned Queues
===============

The `intelmqctl check` tool can search for orphaned queues. "Orphaned queues" are queues that have been used in the past and are no longer in use. For example you had a bot which you removed or renamed afterwards, but there were still messages in it's source queue. The source queue won't be renamed automatically and is now disconnected. As this queue is no longer configured, it won't show up in the list of IntelMQ's queues too. In case you are using redis as message broker, you can use the `redis-cli` tool to examine or remove these queues:

.. code-block:: bash

   redis-cli -n 2
   keys * # lists all existing non-empty queues
   llen [queue-name] # shows the length of the queue [queue-name]
   lindex [queue-name] [index] # show the [index]'s message of the queue [queue-name]
   del [queue-name] # remove the queue [queue-name]

To ignore certain queues in this check, you can set the parameter `intelmqctl_check_orphaned_queues_ignore` in the *defaults* configuration file. For example:

.. code-block:: json

   "intelmqctl_check_orphaned_queues_ignore": ["Taichung-Parser"],

---------------------
Configuration upgrade
---------------------

The `intelmqctl upgrade-config` function upgrade, upgrade the configuration from previous versions to the current one.
It keeps track of previously installed versions and the result of all "upgrade functions" in the "state file", locate in the `$var_state_path/state.json` (`/opt/intelmq/var/lib/state.json` or `/var/lib/intelmq/state.json`).

This function has been introduced in version 2.0.1.

It makes backups itself for all changed files before every run. Backups are overridden if they already exists. So make sure to always have a backup of your configuration just in case.

---------
Exit code
---------

In case of errors, unsuccessful operations, the exit code is higher than 0.
For example, when running `intelmqctl start` and one enabled bot is not running, the exit code is 1.
The same is valid for e.g. `intelmqctl status`, which can be used for monitoring, and all other operations.

------------
Known issues
------------

The currently implemented process managing using PID files is very erroneous.
