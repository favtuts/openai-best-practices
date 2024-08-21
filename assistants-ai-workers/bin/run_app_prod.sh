#!/bin/bash

WORKDIR=/emteller/assistant_worker

cd ${WORKDIR}

/home/nsd/.local/bin/pipenv run l2_app.py
