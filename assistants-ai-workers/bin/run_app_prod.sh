#!/bin/bash

if [[ ! -e /tmp/l2_app.py.pid ]]; then   # Check if the file already exists
    #python test.py &                   #+and if so do not run another process.
    WORKDIR=/emteller/assistant-worker
    cd ${WORKDIR}
    ls
    /home/nsd/.local/bin/pipenv run python l2_app.py &
    echo $! > /tmp/l2_app.py.pid
else
    echo -n "ERROR: The process is already running with pid "
    cat /tmp/l2_app.py.pid
    echo
fi
