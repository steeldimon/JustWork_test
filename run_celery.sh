#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

cd pages_app
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m pages_app -c "celery -A pages_app worker -l info --concurrency=1"
