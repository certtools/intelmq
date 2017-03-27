#!/bin/bash

d=`date +%F`
mkdir $d
cd $d
for db in ripe.db.organisation.gz ripe.db.role.gz ripe.db.aut-num.gz ripe.db.inet6num.gz ripe.db.inetnum.gz
 do
 echo "Downloading: " $db
 curl -O "http://ftp.ripe.net/ripe/dbase/split/$db"
 done

echo "Downloading: Delegated list."
curl -O ftp://ftp.ripe.net/ripe/stats/delegated-ripencc-latest

exit 0
