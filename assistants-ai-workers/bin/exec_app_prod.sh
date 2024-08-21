#!/bin/bash

# this script use for running under systemctl service
# no need to maintain pid in temp file

WORKDIR=/emteller/assistant-worker
cd ${WORKDIR}
/home/nsd/.local/bin/pipenv run python l2_app.py &