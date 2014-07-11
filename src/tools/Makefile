clean-cache:
	redis-cli FLUSHDB
	redis-cli FLUSHALL

clean-mq:
	rabbitmqctl stop_app ; rabbitmqctl reset ; rabbitmqctl start_app

clean-bots:
	kill -9 $(ps aux | grep -v grep | grep "python -m bots" | awk '{print $2}')
