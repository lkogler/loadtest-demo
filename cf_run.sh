#!/usr/bin/env bash

gunicorn --bind 0.0.0.0:$PORT wsgi --graceful-timeout=60 --workers=$WORKER_PROCESSES
