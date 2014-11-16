* This module uses pyasn DB (pip install pyasn or  https://github.com/hadiasghari/pyasn)


* use pyasn_util_download.py --latest to download
* use pyasn_util_convert.py --single <downloadedfilename>.bz2 ipasn.dat
* Create data folder '/var/lib/intelmq/asnlookup'
* Copy database to '/var/lib/intelmq/asnlookup'
* Update the correspondent section in '/etc/intelmq/BOTS':

```
    "database": "/var/lib/intelmq/asnlookup/ipasn.dat"


