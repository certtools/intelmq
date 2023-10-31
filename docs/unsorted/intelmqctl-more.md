<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

## Command-line interface: intelmqctl

**Syntax** see `intelmqctl -h`

- Starting a bot: `intelmqctl start bot-id`
- Stopping a bot: `intelmqctl stop bot-id`
- Reloading a bot: `intelmqctl reload bot-id`
- Restarting a bot: `intelmqctl restart bot-id`
- Get status of a bot: `intelmqctl status bot-id`
- Run a bot directly for debugging purpose and temporarily leverage the logging level to DEBUG: `intelmqctl run bot-id`
- Get a pdb (or ipdb if installed) live console.
  `intelmqctl run bot-id console`
- See the message that waits in the input queue.
  `intelmqctl run bot-id message get`
- See additional help for further explanation.
  `intelmqctl run bot-id --help`
- Starting the botnet (all bots): `intelmqctl start`
- Starting a group of bots: `intelmqctl start --group experts`
- Get a list of all configured bots: `intelmqctl list bots`
- Get a list of all queues: `intelmqctl list queues` If -q is given, only queues with more than one item are listed.
- Get a list of all queues and status of the bots:
  `intelmqctl list queues-and-status`
- Clear a queue: `intelmqctl clear queue-id`
- Get logs of a bot: `intelmqctl log bot-id number-of-lines log-level`
  Reads the last lines from bot log. Log level should be one of DEBUG, INFO, ERROR or CRITICAL. Default is INFO. Number
  of lines defaults to 10, -1 gives all. Result can be longer due to our logging format!
- Upgrade from a previous version: `intelmqctl upgrade-config` Make a backup of your configuration first, also including
  bot's configuration files.

#### Reloading

Whilst restart is a mere stop & start, performing
`intelmqctl reload <bot_id>` will not stop the bot, permitting it to keep the state: the same common behavior as for (
Linux) daemons. It will initialize again (including reading all configuration again) after the current action is
finished. Also, the rate limit/sleep is continued
(with the *new* time) and not interrupted like with the restart command. So if you have a collector with a rate limit of
24 h, the reload does not trigger a new fetching of the source at the time of the reload, but just 24 h after the last
run -- with the new configuration. Which state the bots are keeping depends on the bots of course.

#### Forcing reset pipeline and cache (be careful)

If you are using the default broker (Redis), in some test situations you may need to quickly clear all pipelines and
caches. Use the following procedure:

```bash
redis-cli FLUSHDB
redis-cli FLUSHALL
```

## Management

IntelMQ has a modular structure consisting of bots. There are four types of bots:

- `collector bots` retrieve data from internal or external sources, the output are *
  reports* consisting of many individual data sets / log lines.
- `parser bots` parse the (report) data by splitting it into individual *events* (log lines) and giving them a defined
  structure, see also `/dev/data-format` for the list of fields an event may be split up into.
- `expert bots` enrich the existing events by e.g. lookup up information such as DNS reverse records, geographic
  location information (country code) or abuse contacts for an IP address or domain name.
- `output bots` write events to files, databases, (REST)-APIs or any other data sink that you might want to write to.

Each bot has one source queue (except collectors) and can have multiple destination queues (except outputs). But
multiple bots can write to the same pipeline (queue), resulting in multiple inputs for the next bot.

Every bot runs in a separate process. A bot is identifiable by a *bot id*.

Currently only one instance (i.e. *with the same bot id*) of a bot can run at the same time. Concepts for
multiprocessing are being discussed, see this issue:
`Multiprocessing per queue is not supported #186 <186>`. Currently you can run multiple processes of the same bot (
with *different bot ids*) in parallel.

Example: multiple gethostbyname bots (with different bot ids) may run in parallel, with the same input queue and sending
to the same output queue. Note that the bot providing the input queue **must** have the
`load_balance` option set to `true`.
