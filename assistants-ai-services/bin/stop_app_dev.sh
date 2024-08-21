#!/bin/bash
# https://stackoverflow.com/questions/33615683/how-to-access-the-pid-from-an-lsof
# kill -9 $(lsof -i :5432)
lsof -t -i:5432 | xargs kill -9