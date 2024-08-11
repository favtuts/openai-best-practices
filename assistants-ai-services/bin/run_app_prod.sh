#!/bin/bash
# start the werkzeug
pipenv run uwsgi --ini app.ini --need-app
