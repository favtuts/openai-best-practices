#!/bin/bash

if [[ -e /tmp/l2_app.py.pid ]]; then   # If the file do not exists, then the
    kill `cat /tmp/l2_app.py.pid`      #+the process is not running. Useless
    rm /tmp/l2_app.py.pid              #+trying to kill it.
else
    echo "l2_app.py is not running"
fi
