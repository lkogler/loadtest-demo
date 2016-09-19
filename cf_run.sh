#!/usr/bin/env bash

gunicorn --bind 0.0.0.0:$PORT wsgi --graceful-timeout=$GUNICORN_TIMEOUT --timeout=$GUNICORN_TIMEOUT --workers=$WORKER_PROCESSES
