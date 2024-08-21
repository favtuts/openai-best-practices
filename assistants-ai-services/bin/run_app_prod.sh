#!/bin/bash
# start the werkzeug
FLASK_ENV=production /home/nsd/.local/bin/pipenv run uwsgi --ini app.ini --need-app
