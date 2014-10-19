* Download database from http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
* Unzip
* Create geoip folder '/var/lib/intelmq/geoip'
* Copy database to '/var/lib/intelmq/geoip'
* Update the correspondent section in '/etc/intelmq/BOTS':

```
    "database": "/var/lib/intelmq/geoip/GeoLite2-City.mmdb"
```
* Update the corresponding 'bot_id' section in '/etc/intelmq/pipeline.conf'.
