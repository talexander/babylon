#!/bin/sh

killall uwsgi
exec /opt/venv/storeenv/bin/uwsgi --ini uwsgi.ini
