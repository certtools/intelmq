1. Download database from http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
2. Unzip
3. Copy database to 'bots/experts/geoip/'
4. Update the correspondent 'bot_id' section in 'conf/bots.conf':

```
    [geoip]
    database = /opt/intelmq/src/bots/experts/geoip/GeoLite2-City.mmdb
```
