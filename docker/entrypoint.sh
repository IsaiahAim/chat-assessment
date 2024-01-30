#!/bin/sh

python manage.py migrate --no-input
rm celerybeat.pid
python manage.py loaddata */fixtures/*.json

exec "$@"