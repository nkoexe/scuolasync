#!/bin/bash

killall python
sleep 5
python -m gunicorn -k gevent -w 1 -b 0.0.0.0:80 sostituzioni.app:app