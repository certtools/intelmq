redis-cli FLUSHALL
rm -rf /opt/intelmq/var/lib/bots/file-output/events.txt 
rm -rf /opt/intelmq/var/log/*
killall -s 9 python
