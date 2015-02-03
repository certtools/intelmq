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
# mkdir /var/lib/intelmq/asnlookup
# mv /tmp/ipasn.dat /var/lib/intelmq/asnlookup/
# chown -R intelmq.intelmq /var/lib/intelmq/asnlookup
```

* Make sure that ASNLookup bot at runtime.conf has the value '/var/lib/intelmq/asnlookup/ipasn.dat' in 'database' field.