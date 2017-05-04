* Install python module:
```
# pip install pyasn 
```

* Download database and convert:
```
# cd /tmp/
# pyasn_util_download.py --latest
# pyasn_util_convert.py --single <downloaded_filename.bz2>  ipasn.dat
```

Note: the '<' '>' characters only are syntactic markings, no shell redirection is necessary.

* Copy database to IntelMQ:
```
# mkdir /opt/intelmq/var/lib/bots/asn_lookup
# mv /tmp/ipasn.dat /opt/intelmq/var/lib/bots/asn_lookup/
# chown -R intelmq.intelmq /opt/intelmq/var/lib/bots/asn_lookup
```

* Make sure that ASNLookup bot at runtime.conf has the value '/opt/intelmq/var/lib/bots/asn_lookup/ipasn.dat' in 'database' field.
