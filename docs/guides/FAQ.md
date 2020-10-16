# Frequently asked questions

**Table of Contents:**

- [Send IntelMQ events to Splunk](#send-intelmq-events-to-splunk)
- [Permission denied when using redis unix socket](#permission-denied-when-using-redis-unix-socket)
- [Why is the time invalid?](#why-is-the-time-invalid)
- [How can I improve the speed?](#how-can-i-improve-the-speed)
- [My bot(s) died on startup with no errors logged](#my-bots-died-on-startup-with-no-errors-logged)
- [Orphaned Queues](#orphaned-queues)
- [Multithreading is not available for this bot](#multithreading-is-not-available-for-this-bot)

## Send IntelMQ events to Splunk

1. Go to Splunk and configure in order to be able to receive logs(intelmq events) to a tcp port
2. Use tcp output bot and configure accordingly to the Splunk configuration that you applied.

## Permission denied when using redis unix socket

If you get an error like this:

```
intelmq.lib.exceptions.PipelineError: pipeline failed - ConnectionError('Error 13 connecting to unix socket: /var/run/redis/redis.sock. Permission denied.',)
```

make sure the permissions for the socket are set accordingly in `/etc/redis/redis.conf` (or wherever your config is), e.g.:

    unixsocketperm 777

## Why is the time invalid?

If you wonder why you are getting errors like this:
```python
intelmq.lib.exceptions.InvalidValue: invalid value '2017-03-06T07:36:29' () for key 'time.source'
```
IntelMQ requires time zone information for all timestamps. Without a time zone, the time is ambiguous and therefore rejected.

## How can I improve the speed?

In most cases the bottlenecks are look-up experts. In these cases you can easily use the integrated load balancing features.

### Multithreading

When using the AMQP broker, you can make use of Multi-threading. See the [Uer-Guide, section Multithreading](User-Guide.html#multithreading-beta).

### "Classic" load-balancing (Multiprocessing)

Before Multithreading was available in IntelMQ, and in case you use Redis as broker, the only way to do load balancing involves more work.
Create multiple instances of the same bot and connect them all to the same source and destination bots. Then set the parameter `load_balance` to `true` for the bot which sends the messages to the duplicated bot. Then, the bot sends messages to only one of the destination queues and not to all of them.

True Multi*processing* is not available in IntelMQ. See also this discussion on a possible enhanced load balancing: https://github.com/certtools/intelmq/issues/186

### Other options

For any bottleneck based on (online) lookups, optimize the lookup itself and if possible use local databases.

It is also possible to use multiple servers to spread the workload. To get the messages from one system to the other you can either directly connect to the other's pipeline or use a fast exchange mechanism such as the TCP Collector/Output (make sure to secure the network by other means).

### Removing raw data for higher performance and less space usage

If you do not need the raw data, you can safely remove it. For events (after parsers), it keeps the original data, eg. a line of a CSV file. In reports it keeps the actual data to be parsed, so don't delete the raw field in Reports - between collectors and parsers.

The raw data consumes about 50% - 30% of the messages' size. The size of course depends on how many additional data you add to it and how much data the report includes. Dropping it, will improve the speed as less data needs to be transferred and processed at each step.


#### In a bot

You can do this for example by using the *Field Reducer Expert*. The configuration could be:

 * `type`: `blacklist`
 * `keys`: `raw`

Other solutions are the *Modify* bot and the *Sieve* bot. The last one is a good choice if you already use it and you only need to add the command:

```
remove raw
```

#### In the database

In case you store data in the database and you want to keep its size small, you can (periodically) delete the raw data there.

To remove the raw data for a events table of a PostgreSQL database, you can use something like:

```
UPDATE events SET raw = NULL WHERE "time.source" < '2018-07-01';
```

If the database is big, make sure only update small parts of the database by using an appropriate `WHERE` clause. If you do not see any negative performance impact, you can increase the size of the chunks, otherwise the events in the output bot may queue up. The `id` column can also be used instead of the source's time.

## My bot(s) died on startup with no errors logged

Rather than starting your bot(s) with `intelmqctl start`, try `intelmqctl run [bot]`. This will provide valuable debug output you might not otherwise see, pointing to issues like system configuration errors.

## Orphaned Queues

This section has been moved to the [intelmqctl documentation](intelmctl.html#orphaned-queues)

## Multithreading is not available for this bot

Multithreading is not available for some bots and AMQP broker is necessary. Possible reasons why a certain bot or a setup does not support Multithreading include:

 * Multithreading is only available when using the AMQP broker.
 * For most collectors, Multithreading is disabled. Otherwise this would lead to duplicated data, as the data retrieval is not atomic.
 * Some bots use libraries which are not thread safe. Look a the bot's documentation for more information.
 * Some bots' operations are not thread safe. Look a the bot's documentation for more information.

If you think this mapping is wrong, please report a bug.
