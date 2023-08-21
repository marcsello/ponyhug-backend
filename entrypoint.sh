#!/bin/sh

echo "Starting PonyHug 2023 server..."

python3 init.py # <- single-threaded init stuff

# run the app in a multi-worker multi-thread env
exec gunicorn -b 0.0.0.0:8000 --workers 4 --threads 2 'application:create_app()'