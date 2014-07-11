* Download database from http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
* Unzip
* Copy database to 'bots/experts/geoip/'
* Update the correspondent 'bot_id' section in 'conf/bots.conf':

```
    [geoip]
    database = /opt/intelmq/src/bots/experts/geoip/GeoLite2-City.mmdb
```
* Update 'conf/pipeline.conf' with 'bot_id'
