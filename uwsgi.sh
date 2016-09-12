#!/bin/sh
echo 'BEFORE UWSGI'
uwsgi --ini $HOME/uwsgi.ini
echo 'AFER UWSGI'
