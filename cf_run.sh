#!/usr/bin/env bash

ENVIRONMENT_VARIABLES_FILE=.env


if [ -f ${ENVIRONMENT_VARIABLES_FILE} ]
  then
    source ${ENVIRONMENT_VARIABLES_FILE}
    source env/bin/activate
fi

gunicorn --bind 0.0.0.0:$PORT wsgi --graceful-timeout=$GUNICORN_TIMEOUT --timeout=$GUNICORN_TIMEOUT --workers=$WORKER_PROCESSES
