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
