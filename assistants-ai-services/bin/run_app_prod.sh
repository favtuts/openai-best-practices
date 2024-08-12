#!/bin/bash
# start the werkzeug
FLASK_ENV=production pipenv run uwsgi --ini app.ini --need-app
