# Frequently asked questions

**Table of Contents:**

- [Send IntelMQ events to Splunk](#send-intelmq-events-to-splunk)
- [Git information](#git-information)
- [Permission denied when using redis unix socket](#permission-denied-when-using-redis-unix-socket)
- [Why is the time invalid?](#why-is-the-time-invalid)
- [How can I improve the speed?](#how-can-i-improve-the-speed)
- [My bot(s) died on startup with no errors logged](#my-bots-died-on-startup-with-no-errors-logged)
- [Orphaned Queues](#orphaned-queues)

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

In most cases the bottlenecks are look-up experts. In these cases you can easily use the integrated load balancing features. Create multiple instances of the same bot and connect them all to the same source and destination bots. Then set the parameter `load_balance` to `true` for the bot which sends the messages to the duplicated bot. Then, the bot sends messages to only one of the destination queues and not to all of them.

See also this discussion on a possible enhanced load balancing: https://github.com/certtools/intelmq/issues/186

### Removing raw data for higher performance and less space usage

If you do not need the raw data, you can safely remove it. For events (after parsers), it keeps the original data, eg. a line of a CSV file. In reports it keeps the actual data to be parsed, so don't delete the raw field in Reports - between collectors and parsers.

The raw data consumes about 50% - 30% of the messages' size (Depending of course on how many additional data you add to it and how much data the report includes). Dropping it, will improve the speed as less data needs to be transferred and processed at each step.


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

Rather than starting your bot(s) with `intelmqctl start`, try `intelmqctl run [bot]`. This will provide valuable debug output you might not otherwise see, pointing to issues like configuration errors.

## Orphaned Queues

The `intelmqctl check` tool can search for orphaned queues. "Orphaned queues" are queues that have been used in the past and are no longer in use. For example you had a bot which you removed or renamed afterwards, but there were still messages in it's source queue. The source queue won't be renamed automatically and is now disconnected. As this queue is no longer configured, it won't show up in the list of IntelMQ's queues too. In case you are using redis as message broker, you can use the `redis-cli` tool to examine or remove these queues:

```bash
redis-cli -n 2
keys * # lists all existing non-empty queues
llen [queue-name] # shows the length of the queue [queue-name]
lindex [queue-name] [index] # show the [index]'s message of the queue [queue-name]
del [queue-name] # remove the queue [queue-name]
```
