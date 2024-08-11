#!/bin/bash
# https://stackoverflow.com/questions/33615683/how-to-access-the-pid-from-an-lsof
# kill -9 $(lsof -i :8600)
lsof -t -i:8600 | xargs kill -9