## Send IntelMQ events to Splunk

1. Go to Splunk and configure in order to be able to receive logs(intelmq events) to a tcp port
2. Use tcp output bot and configure accordingly to the Splunk configuration that you applied.


## Imbox Module Error

**Error:**
```
Pipeline connection failed (error("UID command error: BAD ['Error in IMAP command UID STORE: Flags list contains non-atoms.']",))
```

**Solution:**
```
root@server:~# python
Python 2.7.3 (default, Feb 27 2014, 20:00:17) 
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import imbox
>>> print imbox.__path__
['/usr/local/lib/python2.7/dist-packages/imbox']
```

Replace the following line in the file '/usr/local/lib/python2.7/dist-packages/imbox':

```
self.connection.uid('STORE', uid, '+FLAGS', '\\Seen')
```

To:

```
self.connection.uid('STORE', uid, '+FLAGS', '(\\Seen)')
```


## Timezone - Naive Datetime

**Error:**
```
Pipeline connection failed (ValueError('astimezone() cannot be applied to a naive datetime',))
```

**Solution:**

Every timestamp ('source_time' or 'observation_time') must have a timezone.

Bad Example:
```
2014-06-25 00:00:00
```

Good Example:
```
2014-06-25 00:00:00 UTC
```

Consult this example how ShadowServer SNMP Bot solve the problem.

## Git information

https://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html
