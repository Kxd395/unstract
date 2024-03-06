#!/usr/bin/env bash

cmd=$1
if [ "$cmd" = "migrate" ]; then
    echo "Migration initiated"
    .venv/bin/python manage.py migrate
fi

# NOTE: Leaving below for reference incase required in the future
# python manage.py runserver 0.0.0.0:8000 --insecure
# NOTE updated socket threads
.venv/bin/gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 4 \
    --log-level debug \
    --timeout 600 \
    --access-logfile - \
    --reload \
    backend.wsgi:application
