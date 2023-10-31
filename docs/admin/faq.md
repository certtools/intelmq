<!-- comment
   SPDX-FileCopyrightText: 2014 Tomás Lima <synchroack@gmail.com>, 2016-2021 Sebastian Wagner <wagner@cert.at>, 2023 Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Frequently asked questions

## How can I improve the speed?

In most cases the bottlenecks are look-up experts. In these cases you
can easily use the integrated load balancing features.

### Multithreading

When using the AMQP broker, you can make use of Multi-threading. See the
`multithreading` section.

### "Classic" load-balancing (Multiprocessing)

Before Multithreading was available in IntelMQ, and in case you use
Redis as broker, the only way to do load balancing involves more work.
Create multiple instances of the same bot and connect them all to the
same source and destination bots. Then set the parameter `load_balance`
to `true` for the bot which sends the messages to the duplicated bot.
Then, the bot sends messages to only one of the destination queues and
not to all of them.

True Multi*processing* is not available in IntelMQ. See also this
`discussion on a possible enhanced load balancing <186>`.

### Other options

For any bottleneck based on (online) lookups, optimize the lookup itself
and if possible use local databases.

It is also possible to use multiple servers to spread the workload. To
get the messages from one system to the other you can either directly
connect to the other's pipeline or use a fast exchange mechanism such
as the TCP Collector/Output (make sure to secure the network by other
means).

### Removing raw data for higher performance and less space usage <div id="faq-remove-raw" />

If you do not need the raw data, you can safely remove it. For events
(after parsers), it keeps the original data, eg. a line of a CSV file.
In reports it keeps the actual data to be parsed, so don't delete the
raw field in Reports - between collectors and parsers.

The raw data consumes about 50% - 30% of the messages' size. The size
of course depends on how many additional data you add to it and how much
data the report includes. Dropping it, will improve the speed as less
data needs to be transferred and processed at each step.

**In a bot**

You can do this for example by using the *Field Reducer Expert*. The
configuration could be:

- `type`: `blacklist`
- `keys`: `raw`

Other solutions are the *Modify* bot and the *Sieve* bot. The last one
is a good choice if you already use it and you only need to add the
command:

```
remove raw
```

**In the database**

In case you store data in the database and you want to keep its size
small, you can (periodically) delete the raw data there.

To remove the raw data for a events table of a PostgreSQL database, you
can use something like:

```sql
UPDATE events SET raw = NULL WHERE "time.source" < '2018-07-01';
```

If the database is big, make sure only update small parts of the
database by using an appropriate `WHERE` clause. If you do not see any
negative performance impact, you can increase the size of the chunks,
otherwise the events in the output bot may queue up. The `id` column can
also be used instead of the source's time.

Another way of reducing the `raw`-data from the database is described in
the EventDB documentation: `eventdb_raws_table`.

### How to Uninstall

If you installed intelmq with native packages: Use the package management tool to remove the package `intelmq`. These
tools do not remove configuration by default.

If you installed manually via pip (note that this also deletes all configuration and possibly data):

```bash
pip3 uninstall intelmq
rm -r /opt/intelmq
```

