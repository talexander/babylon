#!/bin/sh

export UWSGI_SOCKET=127.0.0.1:9090
export UWSGI_MODULE=wsgi
export UWSGI_MASTER=1
export UWSGI_PROCESSES=4
export UWSGI_MEMORY_REPORT=1
export UWSGI_HARAKIRI=30
export UWSGI_CHDIR=/opt/venv/storeenv/store/store/
export UWSGI_VIRTUALENV=/opt/venv/storeenv/
export UWSGI_PYTHONPATH=/opt/venv/storeenv/store/
export UWSGI_TOUCH_RELOAD=/opt/venv/storeenv/store/uwsgi.sh
export UWSGI_DAEMONIZE=/opt/venv/storeenv/store/store/logs/uwsgi.log

exec /usr/bin/uwsgi
