#!/usr/bin/env sh

# start webserver with gunicorn
source .env/bin/activate
gunicorn -w 4 wrapper:app
