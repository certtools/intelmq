flush:
	redis-cli FLUSHDB
	redis-cli FLUSHALL

flushqu:
	killall python
	rabbitmqctl stop_app ; rabbitmqctl reset ; rabbitmqctl start_app
