#!/bin/bash
# start the flask application
FLASK_ENV=development pipenv run flask run --debug --port 5432
