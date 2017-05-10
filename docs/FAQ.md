## Send IntelMQ events to Splunk

1. Go to Splunk and configure in order to be able to receive logs(intelmq events) to a tcp port
2. Use tcp output bot and configure accordingly to the Splunk configuration that you applied.

## Git information

https://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html

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
IntelMQ is requires time zone information for all timestamps. Without a time zone, the time is not usable and therefore will be rejected.
