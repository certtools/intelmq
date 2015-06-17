* Install python module:
```
# pip install pyasn --pre
```

* Download database and convert:
```
# cd /tmp/
# pyasn_util_download.py --latest
# pyasn_util_convert.py --single <downloaded_filename>.bz2 ipasn.dat
```

* Copy database to IntelMQ:
```
# mkdir /opt/intelmq/var/lib/bots/asnlookup
# mv /tmp/ipasn.dat /opt/intelmq/var/lib/bots/asnlookup/
# chown -R intelmq.intelmq /opt/intelmq/var/lib/bots/asnlookup
```

* Make sure that ASNLookup bot at runtime.conf has the value '/opt/intelmq/var/lib/bots/asnlookup/ipasn.dat' in 'database' field.
