* Download database from http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
* Unzip
* Create geoip folder '/opt/intelmq/var/lib/bots/geoip'
* Copy database to '/opt/intelmq/var/lib/bots/geoip'
* Update the correspondent section in '/opt/intelmq/etc/runtime.conf':

```
    "database": "/opt/intelmq/var/lib/bots/geoip/GeoLite2-City.mmdb"
```
* Update the corresponding 'bot_id' section in '/opt/intelmq/etc/pipeline.conf'.
