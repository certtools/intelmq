* Install the REQUIREMENTS.TXT
* Download database from https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
* Unzip
* Create geoip folder '/opt/intelmq/var/lib/bots/maxmind_geoip'
* Copy database to '/opt/intelmq/var/lib/bots/maxmind_geoip'
* Update the correspondent section in '/opt/intelmq/etc/runtime.conf':

```
    "database": "/opt/intelmq/var/lib/bots/maxmind_geoip/GeoLite2-City.mmdb"
```

This product includes GeoLite2 data created by MaxMind, available from
<a href="http://www.maxmind.com">http://www.maxmind.com</a>.
